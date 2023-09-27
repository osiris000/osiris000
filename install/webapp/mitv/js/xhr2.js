/********************

	Para depurar y ampliar

*********************/

/*  

funciones para tratar con el objeto xhr-ajax

*/


// variable $ajax , almacena (puntero al) cada objeto
// xhr abierto por la función ajax()

$ajax = new Array()


// funcion ajax()

// parámetro 1
// 'datas' son las variables a enviar por url
// al servidor en espera de respuesta
// formato var=valor&var=valor

// parámetro2 
// 'ih' el nombre de un div si quiere imprimir html
// sino en blanco o false

// 3
// 'loc' es la url destino by example location.php

// 4
// 'method', puede ser GET o POST , si false por defecto será GET

// 5 
// 'js' indica cuando el retorno es javascript para ejecutar
// normalmente para este caso se usa con 'ih' a false



function ajax(datas,ih,loc,method="GET",js,mode="=",masajax=$ajax.length){

mode = mode

$ajax[masajax] =  new XMLHttpRequest()


if(!method) method =="GET"

if(method.toUpperCase()=="GET"){
loc = loc+"?"+datas;    
}

$ajax[masajax].open(method,loc)


$ajax[masajax].onreadystatechange = function(){





if($ajax[masajax].readyState===4){

if(ih){

xEval(`document.getElementById('`+ih+`').innerHTML` + xEval(`mode`) + `$ajax[`+masajax+`].responseText`,1)


} if(js) xEval(js,1) ; $ajax[masajax] = "END 4:"+masajax } else {

	if($ajax[masajax].readyState==3){
	if(!ih) xEval($ajax[masajax].responseText,1)
		}
        //readyState < 4
	}
//end function
}



if(method.toUpperCase()=="POST"){
	
	$ajax[masajax].setRequestHeader('Content-Type','application/x-www-form-urlencoded');
	$ajax[masajax].send(datas)
	
} else if(method.toUpperCase()==="GET"){
	$ajax[masajax].send()
}

}



function xEval(obj,mode) {
if (!mode) return eval(obj)
else return Function('"use strict";return (' + obj + ')')();
}





