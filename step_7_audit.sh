while read -r pkg; do
    echo "Auditing ${pkg}"
    output=$(piw-audit-packages "$pkg" --delete-extras --ensure-project-symlinks --archive-dir /home/piwheels/archive/www 2>&1)
    if [[ -n "$output" ]]; then
        echo "$pkg" >> audit.txt
        echo "$output"
    fi
done < packages.txt
