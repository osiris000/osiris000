


#instalamos aplicaciones necesarias

python3 	apt install python3
apache2 	apt install apache2 libapache2-mod-fcgid 
php apt 	install php php-fpm libapache2-mod-php
mariadb	apt install mariadb 
ffmpeg		apt install ffmpeg 
pip		apt install pip 


#etc.. si no se chekea desde install.sh, se ignora

NUEVA  apt install NUEVA



