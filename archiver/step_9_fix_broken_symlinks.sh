#!/usr/bin/bash

BASE="/home/piwheels/archive/www/simple"

missing_armv7="missing_armv7.txt"
failed_armv6="failed_armv6.txt"

# empty output files first
: > "$missing_armv7"
: > "$failed_armv6"

while read -r f; do
    armv7="$BASE/$f"
    armv6="${armv7/armv7l/armv6l}"

    if [[ ! -e "$armv7" ]]; then
        echo "$f" >> "$missing_armv7"
        continue
    fi

    if [[ ! -e "$armv6" && ! -L "$armv6" ]]; then
        if ! ln -s "$(basename "$armv7")" "$armv6"; then
            echo "${f/armv7l/armv6l}" >> "$failed_armv6"
        fi
    fi

done < armv7.txt
