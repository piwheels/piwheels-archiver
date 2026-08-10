xargs -P 4 -I{} cp -avP /home/piwheels/archive/www/simple/{} /home/piwheels/www/simple/{} < files.txt
sed 's/$/.metadata/' files.txt | xargs -P 4 -I{} cp -avP /home/piwheels/archive/www/simple/{} /home/piwheels/www/simple/{}

# cp -P preserves symlink targets verbatim; archive's own symlinks are
# absolute, so relativise anything that copied over as an absolute link
{ cat files.txt; sed 's/$/.metadata/' files.txt; } | while read -r f; do
    path="/home/piwheels/www/simple/$f"
    [ -L "$path" ] || continue
    target=$(readlink "$path")
    [[ "$target" == /* ]] || continue
    ln -sfn "$(basename "$target")" "$path"
done
