/*  

funciones para tratar con el objeto xhr-ajax

*/


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






/* otras funciones a depurar*/


function getId(thid){return encodeURIComponent(document.getElementById(thid).value);}
function EUwysiwyg(thid){return encodeURIComponent(document.getElementById(thid).contentDocument.body.innerHTML);}
function gId(thid){return document.getElementById(thid);}
function GId(thid){return document.getElementById(thid).value;}

function xEval(obj,mode) {
if (!mode) return eval(obj)
else return Function('"use strict";return (' + obj + ')')();
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
