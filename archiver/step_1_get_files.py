from piwheels.master.db import Database


db = Database("postgresql:///piwheels")
files_file = "files.txt"
packages_file = "packages.txt"

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
			where f.location = '/simple'
			group by b.build_id
		)
		select
			b.package,
			f.filename,
            dpb.download_count
		from files f
		join builds b using (build_id)
		join downloads_per_build dpb using (build_id)
		where dpb.download_count < 10
		order by b.package, f.filename;
    """
    ).all()


packages = {row[0] for row in rows}
print(f"Found {len(rows):,} files from {len(packages):,} packages to archive")

with open(packages_file, "w") as f:
    f.writelines(f"{pkg}\n" for pkg in sorted(packages))

with open(files_file, "w") as f:
    f.writelines(
        f"{package}/{filename}\n"
        for package, filename, c in sorted(rows)
    )
