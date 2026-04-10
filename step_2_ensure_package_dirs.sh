while IFS= read -r package; do
    dir="/home/piwheels/archive/www/simple/${package}"
    echo $dir
    mkdir -p "$dir"
done < packages.txt
