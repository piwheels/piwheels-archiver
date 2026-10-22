xargs -P 4 -I{} cp -avP /home/piwheels/www/simple/{} /home/piwheels/archive/www/simple/{} < files.txt
sed 's/$/.metadata/' files.txt | xargs -P 4 -I{} cp -avP /home/piwheels/www/simple/{} /home/piwheels/archive/www/simple/{}

# cp -P preserves symlink targets verbatim; master's own symlinks are
# absolute, so relativise anything that copied over as an absolute link
{ cat files.txt; sed 's/$/.metadata/' files.txt; } | while read -r f; do
    path="/home/piwheels/archive/www/simple/$f"
    [ -L "$path" ] || continue
    target=$(readlink "$path")
    [[ "$target" == /* ]] || continue
    ln -sfn "$(basename "$target")" "$path"
done

# Check for broken symlinks now, while nothing is live and the master
# still has every file
bash "$(dirname "$0")/step_8_find_broken_symlinks.sh"
if [ -s broken.txt ]; then
    echo "Broken symlinks listed in broken.txt - run step 9, then re-run step 8"
    echo "and check broken.txt is empty before moving on to step 4"
    exit 1
fi
