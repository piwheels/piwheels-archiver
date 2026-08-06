: > audit.txt

audit_package() {
    local pkg="$1"
    echo "Auditing ${pkg}"
    local output
    output=$(piw-audit-packages "$pkg" --delete-extras --ensure-project-symlinks --archive-dir /home/piwheels/archive/www 2>&1)
    if [[ -n "$output" ]]; then
        echo "$pkg" >> audit.txt
        echo "$output"
    fi
}
export -f audit_package

xargs -P 8 -I{} bash -c 'audit_package "$@"' _ {} < packages.txt
