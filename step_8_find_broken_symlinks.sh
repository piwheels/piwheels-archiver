BASE="/home/piwheels/archive/www/simple"

while read -r f; do
    path="$BASE/$f"
    [ -L "$path" ] && ! [ -e "$path" ] && echo "$f"
done < files.txt > broken.txt
