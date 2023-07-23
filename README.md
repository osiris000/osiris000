![osiris gif](https://vtwitt.com/jsa/osiris.gif)


<h3>Requisitos mínimos (sistema completo)</h3>

Gnu-Linux/debian 

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
php			apt install apt install php php-fpm libapache2-mod-php  
transmission-cli	apt install transmission-cli  


Esto permite instalar los paquetes de las versiones adecuadas  
con los paquetes necesarios para las distintas aplicaciones  


  
Una vez se dan los requisitos, el instalador redirige a la aplicación  
residente en bin/osiris.py  

La primera vez que se entra en bin/osiris.py pide crear una contraseña nueva  
para la aplicación de administración y gestión de la consola osiris.  
desde esta consola se podrán instalar y administrar, apps, módulos,  
extensiones, web, blockchain, contenedores y microsevicios.  


Una vez dentro aparece el prompt >>>  

Hay distintos comandos, los primeros son:  

será comandos válidos los presentes en valid_commands = ["agenda", "install"]  
próximamente se extraerán de un archivo de configuración.  


Al añadir un comando nuevo, éste se puede crear para implementarlo,  
si por ejemplo, añadimos "nuevo_com",  

valid_commands = ["agenda", "install","nuevo_com"]  

cuando lo tecleamos nos dirá que no existe ruta al comando nuevo  
pero podemos crear el ejecutable al comando (python) escribiendo  

\>\>\>nuevo_com create  

Al hacerlo se crea el archivo nuevo_com.py en el directorio bin/com, con una función main que recibe  
los argumentos.  

def main(args):  
&nbsp;&nbsp;&nbsp;&nbsp;print('Args dentro de nuevo_com', args)  


si la función main no existe o está mal formada, el programa lo avisa  
ya que es esa función la que recoje los argumentos pasados por la consola  
para saltar esa formalidad y ejecutar el script igualmente, sería  

\>\>\> nuevo_com force

para ver la ayuda del comando se typea  

\>\>\> nuevo_com help  

Si no existe archivo de ayuda, se crea automáticamente uno  
en el directorio bin/help con el nombre nuevo_com.hlp  


Es decir, se pueden usar los comandos que llevará el sistema por defecto  
así como implementar nuevos desde la consola o archivos, de esta manera se podrán  
instalar/desinstalar/deshabilitar, crear, personalizar y compartir comandos  
a modo de utilidades para osiris  


Una vez se usa un comando se importa el archivo (módulo) para su  
uso, sin embargo se ese archivo cambia por una modificación de la  
implementación, para ver los cambios habría que volver a cargarlo  
dinámicamente, para ello se haría:  

\>\>\> nuevo_com reset  

de ese modo al volver a ejecutarlo recargaría nuevamente el módulo  
con los cambios realizados, evitando así tener que reiniciar el programa  
para utilizar el comando con los cambios nuevos.  


al ejecutar \>\>\>nuevo_com argumento1 argumento2 ...  

se ejecuta el codigo de la función main presente en com/nuevo_com.py  

def main(args):  
&nbsp;&nbsp;&nbsp;&nbsp;print(args)  

lo que arrojaría ["argumento1","argumento2","..."]  
a partir de ahí se pueden implementar cada comando en particular  
el código de fuera de las funciones (print,..) lo ejecuta sólo la primera vez  
que se llama al comando ya que las sucesivas ya tiene el módulo cargado,  
si se hacen cambios en el código del archivo comando y se quiere recargar sin salir  
de la aplicación, puede hacerse usando el argumento reset, >>>nuevo_com reset  



Comando install por defecto  


install auto-install: Este comando inicia la auto-instalación, que probablemente se encargue de instalar o configurar varias aplicaciones de forma automática. El usuario puede ejecutarlo sin argumentos o con argumentos adicionales según sea necesario.  

install webapp: Este comando permite instalar una aplicación web específica. El usuario puede proporcionar el nombre de la aplicación (app_name) como un argumento adicional para indicar cuál aplicación web desea instalar.  

Por ejemplo, el usuario podría ejecutar el siguiente comando para instalar la aplicación web "mitv":  


install webapp mitv  












