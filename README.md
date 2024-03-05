<h1>Osiris Dynamic Shell</h1>

ODS es una shell dinámica sobre la shell del sistema escrita en Bash y Python principalmente.   

Se conoce como dinámica porque se pueden montar y desmontar los comandos-programa en memoria y alternar entre ellos, pasándoles argumentos, sin afectarse mutuamente.   


Para ejecutarlo basta con situarse sobre el directorio raiz y ejecutar <b>. osiris</b>  


Lo primero que pide es instalar, si no están instalados, python3.9 , venv (entorno de dependencias para osiris) y su activación, si ya están instalados se saltan o el sistema avisará que ya están instalados  .

El entorno virtual hay que activarlo cada vez que se inicie el programa tecleando la opción “y”  

Al entrar en la ODS el programa pide una contraseña, por defecto es <b>osiris</b>, para cambiarla una vez dentro, se usa la orden <b>Reset_Password</b>   


Para acceder directamente a osiris saltando el instalador se ejecuta <b>. osiris -p</b>    


Al acceder, el programa pedirá siempre la contraseña root y después la propia de osiris.    



El propósito de osiris es facilitar un entorno orientado a web2, web3, multimedia y blockchain, entre otras aplicaciones, para GNU/Linux/debian. Una red alternativa P2P.      

	
La instalación de aplicaciones se habilitan descomentando sus líneas en <b>install.sh</b>   


Por defecto python3 está descomentada "#" por lo cual al iniciar el programa comprueba si está instalado porque e necesario de inicio   

		check_command_installed /usr/bin/python3 --version


Pero, por ejemplo,

		#check_command_installed /usr/bin/apache2 --version

Está deshabilitada por el símbolo de comentario en bash "#" lo cual al descomentarla, guardar los cambios y volver a ejecutar el programa, pedirá permiso para instalarlo después de comprobar si está instalado ya.         



Osiris se implementa y modifica desde su propia consola, en el ejemplo siguiente es subiendo estos archivos a github, listados en bin/gitup.txt que se ejecuta desde la consola desde el comando >>> shell>  
Haciendo >>>shell> ./gitup  
     

![osiris png](https://vtwitt.com/jsa/media/./osiris/gitup.png)   


Se puede ver como al final se cambia el comando a ffmpeg2 con la orden "use"  


En la siguente captura se hace uso de ffmpeg2 en desarrollo con el comando fdev (clon desarrollo) en pruebas  


![osiris png](https://vtwitt.com/jsa/media/./osiris/ffmpeg2.png)   


La direfencia entre "orden" y "comando", es que las órdenes son propias del core de osiris, mientras que los
comandos son implementaciones de programas escritos en python a los cuales se les pasa argumentos desde la consola
a su función interna "main"  


Para usar los comandos sin intercambiarlos haga >>> xom> use, esto volverá el promp a >>> entonoces a partir de ahí puede hacer:
  
	>>> shell ls    
	>>> fdev yt intro     
	>>> shell ./gitup      
	>>> mount xcom   
	>>> xcom> args...   
	...etc   



Para editar/modificar el código fuente un comando se usa el modificador --edit   



Se instala desde este git, para mayor seguridad hacerlo en el directorio /var/www/osiris000   


Para iniciarlo /var/www/osiris000~#. osiris   


<b>Actualmente podría dar algún problema al clonarlo para evitarlo elimine el directorio bin/com/osiris_env para instalar las nuevas dependencias habilitándo la instalación en install.sh descomentando las lineas check_command_installed</b>   


![osiris gif](https://vtwitt.com/jsa/osiris.gif)







<h4>La documentación a continuación está incompleta y desactualizada si bien ayuda a entender el funcionamiento interno del programa. Este programa está en desarrollo y podría existir alguna configuración incorrecta para algún comando específico </h4>

<h3>Aplicaciones que instala el instalador osiris</h3> 

El instalador puede no estar ajustado a los requerimientos de todos los sistemas
debido a la fase de implementación en que se encuentra. véase install.com e install.sh  
De momento no se le ha dado la opción de saltar instalador al inciar la aplicación.
Si tiene python3 instalado puede entrar en la consola pulsando enter el resto de preguntas en caso contrario instálelo desde el instalador o la consola.

Es importante para cada inicio de sesión si no está habilitado el entorno virtual habilitarlo desde el instalador.

	Cuando pida instalar estas dos opciones:	

		Osiris-venv-activate 	
		Osiris-venv-export	

pulsar Y de Yes y luego C de Continuar

Cuando estén instalados sólo será necesario hacerlo	

Osiris-venv-activate y Osiris-venv-export en el primer inicio de sesión para activar el directorio virtual. 
Sin embargo está en el futuro se hará de forma automática. 


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

\>\>\> nuevo_com --reset  

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



Comandos y modificadores.  

se dividen en dos. Los comandos del sistema que son:  

  use [command]  
  [command] --reset  
  [command] --help  


El prompt osiris es >>>  

Para usar un comando se puede poner su nombre y argumentos o si se va a usar activamente, montarlo para no tener que escribirlo cada vez.para ello 
se usa el comando de 0siris “use” de la siguiente manera, por ejemplo para montar el comando "bard"  

\>>> use bard  

A continuación el prompt pasa a:  

\>>> bard>  

para desmontarlo solo hay que typear "use", así:  

\>>> bard> use  

Lo que resulta en el prompt principal :  

\>>>  


Comandos:  

	shell [command line]


	create	[nombre de comando nuevo] --create

		

	install  webapp [ nombre ]
					--create-default
					--update  



	bard	[texto se comunica con bard] (hace consulta - texto)   


		--edit (edita un archivo en modo lectura/escritura) en bin/com/data/bard predeterminadamente    
		--load-header (carga un archivo como cabecera de consulta)
		--load-footer (carga un archivo como pie de consulta)
		--show-header (muestra la cabecera cargada en memoria)
		--show-footer (muestra el pie cargado en memoria)
		--clear-header (borra la cabecera de la memoria)
		--clear-footer (borra el pie de la memoria)

		Esto permite dividir el mensaje hasta en tres partes.
		De esta forma modelamos la respuesta de bard usando hasta dos filtros
		uno de entrada y otro de salida (header y footer)

		la prioridad de envío es
		sólo pregunta, combinado o  ambos.

		[HEADER]
		....texto mensaje
		[FOOTER]

		... Respuesta del modelo (bard)


	sniff	[ interface name ]  
					--interfaces (muestra interfaces)

	

	scanip  



Contacto para más información y otros asuntos: osiris.osscom@gmail.com    




<b>AMM 2024</b> [LICENCIA](LICENSE.md)  

