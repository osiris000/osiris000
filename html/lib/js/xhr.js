
function sEval(obj) {
return eval(obj)
//    return Function('"use strict";return (' + obj + ')')();
}


$ajax = new Array()


function ajax(datas,ih,loc,method="GET",js,mode="=",masajax=$ajax.length){

mode = mode

$ajax[masajax] =  new XMLHttpRequest()


if(method.toUpperCase()=="GET"){
loc = loc+"?"+datas;    
}

$ajax[masajax].open(method,loc)


$ajax[masajax].onreadystatechange = function(){





if($ajax[masajax].readyState===4){

if(ih){

sEval(`document.getElementById('`+ih+`').innerHTML` + eval(`mode`) + `$ajax[`+masajax+`].responseText`)


} if(js) sEval(js) ; $ajax[masajax] = "END 4:"+masajax } else {

	if($ajax[masajax].readyState==3){
	if(!ih) sEval($ajax[masajax].responseText)
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










var cargandoGif = document.createElement("img");
cargandoGif.src = "/img/cargando.gif";
cargandoGif.width=25;
cargandoGif.height=25;
cargandoGif.alt="cargando...";
function ConstructorXMLHttpRequest(){
if(window.XMLHttpRequest){
return new XMLHttpRequest();
} else if(window.ActiveXObject) {
var vO = new Array('Msxml2.XMLHTTP.5.0','Msxml2.XMLHTTP.4.0','Msxml2.XMLHTTP.3.0','Msxml2.XMLHTTP','Microsoft.XMLHTTP');
for(var i = 0; i < vO.length; i++){
try {return new ActiveXObject(vO[i]);} 
catch (errorControlado) {}}}
throw new Error("No se pudo crear el objeto XMLHttpRequest");
}
function ajaxi(){
return ConstructorXMLHttpRequest();
}
function carga(ajax,resultado){
var cargando = "estado";
document.getElementById(resultado).innerHTML= "<div id='"+cargando+"'></div>";
ajax.onreadystatechange = function(){
    
if(ajax.readyState<4){
document.getElementById(cargando).appendChild(cargandoGif); //"<img src='"+cargandoGif.src+"'>";
		} else{
document.getElementById(cargando).innerHTML="Completado";
document.getElementById(resultado).innerHTML=ajax.responseText;                    
  
                    
                }
	};
}
function getId(thid){return encodeURIComponent(document.getElementById(thid).value);}
function EUwysiwyg(thid){return encodeURIComponent(document.getElementById(thid).contentDocument.body.innerHTML);}
function gId(thid){return document.getElementById(thid);}
function GId(thid){return document.getElementById(thid).value;}


function ajaxPost(datas,muestra,archivo,metodo="POST"){

return ajax(datas,muestra,archivo,metodo="POST",reval="")

ajax = new ConstructorXMLHttpRequest();
carga(ajax,muestra);
ajax.open(metodo,archivo,true);
ajax.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
ajax.send(datas);
}

thread = 0;
TREAD = new Array()
DEBUG = 'idx'
function ajaxReturn(datas,muestra,archivo,metodo="POST",reval=""){

return ajax(datas,muestra,archivo,metodo="POST",reval="")

EXIT_AJAX = 0;
if(!muestra && DEBUG) muestra = DEBUG
thread++
if(metodo==="GET"){
archivo = archivo+"?"+datas;    
}
TREAD[thread] = new ConstructorXMLHttpRequest();
TREAD[thread].open(metodo,archivo,true);
TREAD[thread].onreadystatechange = function(){
if(TREAD[thread].readyState>2){
valor = TREAD[thread].responseText;
if(EXIT_AJAX===true) {/*return*/}
if(reval == 'function') eval(valor);
else if(reval==='flush'){ 
document.getElementById(muestra).style.display="block";
} else if(reval) eval(""+reval+"(escape(valor.trim()))");
if(reval!="function") document.getElementById(muestra).innerHTML=valor;
}}
TREAD[thread].setRequestHeader('Content-Type','application/x-www-form-urlencoded');
if(metodo==="POST"){
    TREAD[thread].send(datas);
} else if(metodo==="GET"){
    TREAD[thread].send();
}
}

function dmenu(divid,classname){
    var dcls=document.getElementsByClassName(classname);
    for(i=0;i<dcls.length;i++){
    if(dcls[i].id!==divid){
    dcls[i].style.visibility="hidden";
    dcls[i].style.display="none";
    }else{
    dcls[i].style.visibility="visible";
    dcls[i].style.display="block";
     }
   }
 }
 


function display(id){
if(!id) return "Undefined";
id = document.getElementById(id)
dsplay = id.style.display
if(dsplay=='block') id.style.display = "none"
else id.style.display = "block"
return id.style.display
}



function clearHTML(id){
if(!id) return "Undefined";
id = document.getElementById(id)
id.innerHTML = "";
}


 function emulaClick(emulado){
var y = document.querySelector(emulado);
y.click();
return;
}


 function clickId(emulado){
var y = document.querySelector(emulado);
y.click();
return;
}



function xplayer(v,src,type){

  var video = document.getElementById(v);
  var videoSrc = src;
  //
  // First check for native browser HLS support
  //
  if (video.canPlayType(type)) {
    video.src = videoSrc;
    video.play = true
    //
    // If no native HLS support, check if HLS.js is supported
    //
  } else if (Hls.isSupported()) {
    var hls = new Hls();
    hls.loadSource(videoSrc);
    hls.attachMedia(video);
  }


document.getElementById("mg").innerHTML += "<br>"+v+"<br>"+src+"<br>"+type+"<br>"



}
