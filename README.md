![osiris gif](https://vtwitt.com/jsa/osiris.gif)



<h3>Aplicaciones que instala el instalador osiris</h3> 

El instalador puede no estar ajustado a los requerimientos de todos los sistemas
debido a la fase de implementación en que se encuentra. véase install.com e install.sh  
De momento no se le ha dado la opción de saltar instalador al inciar la aplicación.
Si tiene python3 instalado puede entrar en la consola pulsando enter el resto de preguntas en caso contrario instálelo desde el instalador o la consola.

Es importante para cada inicio de sesión si no está habilitado el entorno virtual habilitarlo desde el instalador.


	Cuando pida instalar:	

		Osiris-python3-venv 	
		Osiris-venv-activate 	
		Osiris-venv-export	

pulsar Y de Yes y luego C de Continuar

Cuando estén instalados sólo será necesario hacerlo	Osiris-venv-activate y Osiris-venv-export en el primer inicio de sesión para activar el directorio virtual. Sin embargo está en el futuro se hará de forma automática. 


Para instalar Bard hay que instalar la bardapi se deduce que ya tenemos pip en el sistema además está incluida en este repositorio.  

El instalador pregunta tres veces por bard api para instalar , forzar la reinstalación y actualizarla. Para esto es nacesario tener activado el directorio virtual. El directorio virtual hay que montarlo siempre ya se acceda a la aplicación en local o en remoto en cada inicio de sesión. Esto garantiza estar usando siempre una misma versión del software.


Una vez activado y montado el directorio virtual este permanece activo mientras no se cierre la consola o modifique el PYTHONPATH  


El programa está preparado para instalar en un sistema GNU/debian-Linux instala las aplicaciones necesarias para convertir el entorno
en un sistema cliente-servidor integrado con el sistema 
y de fácil administración.





python3 python3-venv  
pip  
rustc   
Apache2 http server fcgid   
php-fpm   
mariadb   
ffmpeg   
yt-dlp   
transmission-cli   
docker docker.io   
git    

Entorno virtual para python3-venv osiris_env  
La ruta al venv es bin/com/osiris_env    

Apis:   

bardapi  IA de google   


Integra bard desde la consola osiris 

![osiris-bard](https://vtwitt.com/jsa/media/image/osiris/ksnip_20230928-070413-[ksnip_20230928-070413].png)


Comandos para bard

bard [ Entra en bard.py y monta la api si no fue montada y abre sesión nueva ]   
bard --clear-log [ Borra el log de la conversación actual ]   
bard texto [ Envía mensaje a Google-Bard e imprime la respuesta en la consola ]  
bard --reset  [ Desmonta la api al volver a usar bard se monta automáticamente ]    
bard --help  [ Muestra la ayuda del comando bard presente en bin/help/bard.hlp ] 


--help y --reset es un modificador común a todos los comandos.


....

Ejecutar ./osiris.sh


1-comprueba que se es root, en caso contrario pide la contraseña root  
  si correcta cambia a root y continúa el programa  
  
2-Comprueba que estén instaladas las aplicaciones necesarias en el sistema  
  si no lo están da la opción de instalarlas    

chekeo de aplicaciones se hace desde install.sh añadiendo líneas  check_command_installed   
	
	Ejemplo:

		check_command_installed /usr/bin/python3 --version


comandos de instalación en install.com  

	Ejemplo:
		
		python3		apt install python3   


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


\>\>\>create [nombre del comando] --create  


Al hacerlo se crea el archivo [nombre del comando.py] en el directorio bin/com, con una función main que recibe los argumentos de ese comando nuevo.  



def main(args):  
&nbsp;&nbsp;&nbsp;&nbsp;print('Args dentro de nuevo_com', args)  


si la función main no existe o está mal formada, el programa lo avisa  
ya que es esa función la que recoje los argumentos pasados por la consola  
para saltar esa formalidad y ejecutar el script igualmente, sería  

\>\>\> nuevo_com --force (por implementar)

para ver la ayuda del comando se typea  

\>\>\> nuevo_com --help  

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

¿Cómo funciona?

Las aplicaciones en desarrollo se encuentran bajo el directorio install/webapp  
dentro hay un directorio "especial" llamado default, que es a partir del cual se  
crean las aplicaciones base.  

al tipear, por ejemplo, en consola:  

install webapp mitv  

indicará que es necesario pasarle un argumento dash (--argumento)  
de momento son dos:  

--create-default  
--update  

al hacer por ejemplo:  

install webapp mitv --create-default  

se crea en la carpeta de instalación de aplicaciones web la app "mitv"  
usando como base "default"  

Una vez esté hecho se puede copiar/actualizar al directorio web público html/app  
usando --update:  

install webapp mitv --update  

la cual estaría accesible desde http://127.0.0.1/app/mitv, pudiendo seguir su  
desarrollo en http://127.0.0.2/webapp/mitv  , actualizando los cambios usando el comando anterior.  



webApps.- en desarrollo


MiTv - una app para crear y gestionar canales de televisión en streaming en formato hls (web)  




![mitv jpg](https://pbs.twimg.com/media/F2pmVzQW8AAPm1K?format=jpg&name=small)  

Esta aplicación usa un api javascript en desarrollo llamada wfcore  

Su lógica se basa en que en HTML los tags se pueden tratar de maneras diferentes, tanto
como tags como paneles, haciendo esa división para mejorar la lógica de la aplicación
de forma que consideraremos paneles a los tags html que estructuran la aplicación.  

wfcore es una api en desarrollo para manejar la lógica estructural de los documentos html para construir aplicaciones web, si bien no dejan de ser tags html también se les consideran paneles cuando se trata de elementos posicionales y objetos necesarios para la aplicación.  

![wfcore jpg](https://pbs.twimg.com/media/F2sUK4qXwAA4eBX?format=png&name=small)  





















