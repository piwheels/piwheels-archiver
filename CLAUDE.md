# piwheels archiver

This directory contains a set of files which are used as a process to move any files with few to no
downloads from the "piwheels master" server to the "piwheels archive server".

- The piwheels master is a Raspberry Pi 4
- The piwheels archive is a VM
- The piwheels master serves a pip-compatible simple index
- The archive server follows the same directory structure and archived files are linked from
the master's index html files
- The archive server's www directory is mounted on the master with SSHFS so files can be
copied/moved between servers or deleted from the master
- Some files are actually symlinks - most files tagged "armv6l" are just symlinks to the "armv7l"
versions. Not always the case. When archiving armv6/v7 files, these must be kept together.

## Steps

1. Make a list of files which match the criteria. Freeze this so upcoming tasks are processing
a known set of files. Query the database for such files and make a list of files and a list of
affected packages.

2. Ensure all package directories exist on the archive server before moving files over

3. Copy files from master to archive, then run step 8's broken symlink check. Stops with an
error if any are found, so they can be fixed (step 9) before anything goes live in step 4

4. Write an update query to be run on the database to update locations of files moved (then run the
query)

5. Rewrite the simple index pages for all affected packages, using `piw-rebuild`

6. Delete the moved files from the master

7. Run `piw-audit` for each affected package to ensure no files are missing or broken

8. Identify any broken symlinks

9. Fix any broken symlinks
