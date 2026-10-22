import sys
from itertools import groupby
from pathlib import Path

from piwheels.master.db import Database


UNITS = ["B", "KB", "MB", "GB", "TB"]


def human_size(n):
    for unit in UNITS:
        if n < 1024 or unit == "TB":
            return f"{n:,.1f} {unit}"
        n /= 1024


def parse_size(s):
    # Accepts e.g. 500M, 50G, 1.5T, 50GB or a plain number of bytes
    s = s.strip().upper().removesuffix("B")
    for power, unit in enumerate(UNITS[1:], start=1):
        if s.endswith(unit[0]):
            return int(float(s[:-1]) * 1024 ** power)
    return int(s)


def measure(path):
    # cp -P copies symlinks as links, so only regular files take up space
    if path.is_symlink():
        return 0, 0, 1, 0
    if path.is_file():
        return path.stat().st_size, 1, 0, 0
    return 0, 0, 0, 1


db = Database("postgresql:///piwheels")
simple = Path("/home/piwheels/archive/www/simple")
files_file = "files.txt"
packages_file = "packages.txt"
limit = parse_size(sys.argv[1]) if len(sys.argv) > 1 else None

with db._conn.begin():
    rows = db._conn.execute(
        """
		with downloads_per_build as (
			select
				b.build_id,
				count(d.accessed_at) as download_count
			from builds b
			join files f using (build_id)
			left join downloads d
			  on d.filename = f.filename
			 and d.accessed_at > current_timestamp - interval '1 month'
			where f.location = 'https://archive1.piwheels.org/simple'
			group by b.build_id
		)
		select
			b.build_id,
			b.package,
			f.filename,
            dpb.download_count
		from files f
		join builds b using (build_id)
		join downloads_per_build dpb using (build_id)
		where dpb.download_count > 25
		order by dpb.download_count desc, b.package, b.build_id, f.filename;
    """
    ).all()

candidate_packages = {row[1] for row in rows}
print(
    f"Found {len(rows):,} files from {len(candidate_packages):,} packages "
    f"eligible to unarchive"
)

# Take whole builds (keeping armv6l symlinks with their armv7l targets),
# most downloaded first, until the next build would exceed the limit
selected = []
total_bytes = real_files = symlinks = missing = 0
for build_id, build_rows in groupby(rows, key=lambda row: row[0]):
    build_rows = list(build_rows)
    build_stats = [0, 0, 0, 0]
    for _, package, filename, _ in build_rows:
        for path in (simple / package / filename, simple / package / f"{filename}.metadata"):
            build_stats = [a + b for a, b in zip(build_stats, measure(path))]
    if limit is not None and total_bytes + build_stats[0] > limit:
        break
    selected.extend(build_rows)
    total_bytes += build_stats[0]
    real_files += build_stats[1]
    symlinks += build_stats[2]
    missing += build_stats[3]

packages = {row[1] for row in selected}
if limit is not None:
    print(
        f"Limited to {human_size(limit)}: selected {len(selected):,} files "
        f"from {len(packages):,} packages "
        f"({len(rows) - len(selected):,} files left for a later run)"
    )
    if rows and not selected:
        print(
            f"Warning: the first build ({rows[0][1]}, "
            f"{human_size(build_stats[0])}) is bigger than the limit, so "
            f"nothing was selected - raise the limit to make progress"
        )

with open(packages_file, "w") as f:
    f.writelines(f"{pkg}\n" for pkg in sorted(packages))

with open(files_file, "w") as f:
    f.writelines(
        f"{package}/{filename}\n"
        for package, filename in sorted((row[1], row[2]) for row in selected)
    )

print(
    f"{human_size(total_bytes)} to transfer in {real_files:,} files "
    f"(plus {symlinks:,} symlinks, {missing:,} missing)"
)
