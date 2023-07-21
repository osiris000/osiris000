![osiris gif](https://vtwitt.com/jsa/osiris.gif)


<h3>Requisitos mínimos (sistema completo)</h3>

Linux/debian

python3

rustc

Apache2 http server fcgid

php7.4 fpm

mariadb

ffmpeg

youtube-dl

transmission-cli

docker

pip3

git 

....

Ejecutar ./osiris.sh


1-comprueba que se es root, en caso contrario pide la contraseña root  
  si correcta cambia a root y continúa el programa  
  
2-Comprueba que estén instaladas las aplicaciones necesarias en el sistema  
  si no lo están da la opción de instalarlas    

chekeo de aplicaciones se hace desde install.sh añadiendo líneas  

check_command_installed /usr/bin/python3 --version   
check_command_installed /usr/sbin/apache2 -v   
check_command_installed /usr/bin/php --version   
check_command_installed /usr/bin/transmission-cli --version   


comandos de instalación en install.com  

python3		apt install python3   
apache2		apt install apache2 libapache2-mod-fcgid  
php			apt install php7-fpm  
transmission-cli	apt install transmission-cli  


Esto permite instalar los paquetes de las versiones adecuadas  
con los paquetes necesarios para distintas aplicaciones  




