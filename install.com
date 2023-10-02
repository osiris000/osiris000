


#instalamos aplicaciones necesarias


python3.9 		apt install python3.9 python3-venv
apache2 		apt install apache2 libapache2-mod-fcgid 
php				apt install php php-fpm libapache2-mod-php
mariadb 		apt install mariadb 
ffmpeg			apt install ffmpeg 
pip3			apt install python3-pip
transmission-cli	apt install transmission-cli 
docker			apt install docker docker.io




Osiris-python3-venv 			python3 -m venv bin/com/osiris_env 
Osiris-venv-activate 			source bin/com/osiris_env/bin/activate
Osiris-venv-export 			eval export PYTHONPATH="$VIRTUAL_ENV/lib/python3.9/site-packages"
Osiris-install-bardapi 		pip install bardapi 
Osiris-force-reinstall-bardapi 	pip install bardapi --force-reinstall 
Osiris-upgrade-bardapi		 	pip install bardapi --upgrade 

#; source tutorial-env/bin/activate


#etc.. si no se chekea desde install.sh, se ignora

NUEVA-app	apt install NUEVA-app




