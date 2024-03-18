


#instalamos aplicaciones necesarias

python3.9-venv         	apt install python3-pip python3.9-venv
python3.9 		apt install python3.9 python3.9-venv
pip3			apt install python3.9-pip
apache2 		apt install apache2 libapache2-mod-fcgid 
php			apt install php php-fpm libapache2-mod-php php-mysqli
mariadb 		apt install mariadb 
ffmpeg			apt install ffmpeg 
transmission-cli	apt install transmission-cli 
docker			apt install docker docker.io
tcptrack		apt install tcptrack

port-audio              apt install portaudio19-dev


Osiris-python3.9-venv 			eval python3.9 -m venv bin/com/osiris_env 
Osiris-venv-activate 			eval source bin/com/osiris_env/bin/activate

Osiris-venv-export 			eval export PYTHONPATH=".:$VIRTUAL_ENV/lib/python3.9/site-packages"

yt-dlp 				pip3 install yt-dlp
Osiris-install-bardapi 		pip install bardapi==0.1.23a
Osiris-force-reinstall-bardapi 	pip install bardapi --force-reinstall 
Osiris-upgrade-bardapi		 	pip install bardapi --upgrade 

#; source tutorial-env/bin/activate


#etc.. si no se chekea desde install.sh, se ignora

#NUEVA-app	apt install NUEVA-app

pip   pip install python-bitcoinlib Flask


