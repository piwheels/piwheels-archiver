from pathlib import Path

files_file = Path("files.txt")
output_file = Path("update_files.sql")

# Get filenames only (basename)
filenames = [Path(fp).name for fp in files_file.read_text().splitlines() if fp.strip()]

# Split into chunks if the list is very large
chunk_size = 1000
total_chunks = (len(filenames) + chunk_size - 1) // chunk_size  # ceiling division

with output_file.open("w") as f:
    for i in range(0, len(filenames), chunk_size):
        chunk_index = (i // chunk_size) + 1
        chunk = filenames[i:i + chunk_size]
        f.write(f"-- Doing chunk {chunk_index}/{total_chunks}\n")
        sql = (
            "UPDATE files\n"
            "SET location = '/simple'\n"
            "WHERE filename IN (\n    "
            + ",\n    ".join(f"'{name}'" for name in chunk)
            + "\n);\n\n"
        )
        f.write(sql)

print(f"Written queries to {output_file}")
