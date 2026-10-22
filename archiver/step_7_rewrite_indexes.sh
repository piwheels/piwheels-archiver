while read -r pkg; do
    echo "Rebuilding index for $pkg..."
    piw-rebuild index "$pkg"
done < packages.txt
