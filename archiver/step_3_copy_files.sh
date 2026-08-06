xargs -P 4 -I{} cp -avP /home/piwheels/www/simple/{} /home/piwheels/archive/www/simple/{} < files.txt
sed 's/$/.metadata/' files.txt | xargs -P 4 -I{} cp -avP /home/piwheels/www/simple/{} /home/piwheels/archive/www/simple/{}
