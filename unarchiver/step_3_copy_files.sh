xargs -P 4 -I{} cp -avP /home/piwheels/archive/www/simple/{} /home/piwheels/www/simple/{} < files.txt
sed 's/$/.metadata/' files.txt | xargs -P 4 -I{} cp -avP /home/piwheels/archive/www/simple/{} /home/piwheels/www/simple/{}
