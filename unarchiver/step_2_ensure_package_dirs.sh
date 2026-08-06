while IFS= read -r package; do
    dir="/home/piwheels/www/simple/${package}"
    echo $dir
    mkdir -p "$dir"
done < packages.txt
