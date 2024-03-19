


#instalamos aplicaciones necesarias

python3.9-venv  	apt install python3-pip python3.9-venv
python3.9 			apt install python3.9 python3.9-venv
pip3				apt install python3.9-pip
php					apt install php php-fpm php-mysqli
apache2 			apt install apache2 libapache2-mod-php libapache2-mod-fcgid 

mariadb 			apt install mariadb 
ffmpeg				apt install ffmpeg 
transmission-cli	apt install transmission-cli 
docker				apt install docker docker.io
tcptrack			apt install tcptrack
nodejs   			apt install nodejs
certbot 			apt install certbot
tor 				apt install tor

port-audio          apt install portaudio19-dev


Osiris-python3.9-venv 			eval python3.9 -m venv bin/com/osiris_env 
Osiris-venv-activate 			eval source bin/com/osiris_env/bin/activate

Osiris-venv-export 			eval export PYTHONPATH=".:$VIRTUAL_ENV/lib/python3.9/site-packages"

yt-dlp 				pip install yt-dlp


#; source tutorial-env/bin/activate


#etc.. si no se chekea desde install.sh, se ignora

#NUEVA-app	apt install NUEVA-app

depend pip install python-bitcoinlib Flask
depend /usr/sbin/a2enmod ssl rewrite


