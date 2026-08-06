BASE="/home/piwheels/www/simple"

while read -r f; do
    path="$BASE/$f"
    [ -L "$path" ] && ! [ -e "$path" ] && echo "$f"
    [ -L "$path.metadata" ] && ! [ -e "$path.metadata" ] && echo "$f.metadata"
done < files.txt > broken.txt

# Produce armv7.txt for step 9: convert broken armv6l symlink paths to their armv7l equivalents
grep 'armv6l' broken.txt | sed 's/armv6l/armv7l/g' > armv7.txt
echo "Found $(wc -l < broken.txt) broken symlinks, $(wc -l < armv7.txt) armv6l needing fix"
