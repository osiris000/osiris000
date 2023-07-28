<?php
session_start();
$_SESSION["ADM"] = false;
if($_REQUEST["x"]=="123454321") $_SESSION["ADM"] =1;
if(!$_SESSION["ADM"]) {print("
<center>
<h1><form action='index.php' method='post'>
<input name='x' type='password' value='Insert Password' width='160'
onclick=\"x.value=''\">
<input type='submit' value='enviar'>
</form>
Login de Acceso
</h1>
</center>
");phpinfo();exit();}

?>
<link rel="stylesheet" type="text/css" href="styles.css">
<script src="https://vtwitt.com/hls.js/dist/hls.js"></script>
<script src="/lib/ajax/hxr.js"></script>
<style>
.comt,.com{
width:100%;
}
.comt{
height:240px;
}
#companel{

background:white;

}
</style>


<a href="javascript:void(0);"
onclick="open('admin.php','_blank','width=420,height=360')">
Abrir en ventana sin pestaña
</a>

<div id='companel'>
<textarea id="com1" class='comt'>
<?=trim(file_Get_contents('php/datas/default com.com'));?>
</textarea><br>
<input type="button" onclick='if(confirm("CLEAR TEXTAREA??")){
gId("com1").value = ""
gId("namecom").value = ""
}
' value='Nuevo'><input type='button' onclick='
ajaxReturn("save=1&rewrite=1&com="+getId("com1")+"&name="+getId("namecom"),"avisos","php/saver.php","POST","flush")
clickId("#hrefId_listacom")'
 value='Guardar'><input type="text" value='default com' id='namecom' paceholder='guardar comando como'>
<span id='listacom'><input type="button" onclick="
jxp('action=listacom','listacom');
" id='hrefId_listacom' 
value="lista comandos">


</span>

<br>


<input type="button" value="KILL" onclick="alert('matar proceso');return false">
<input type="button" value="UnBucle" onclick="unbucle=1">

<input type="button" value="EXEC" onclick="scom('>'+getId('com1'))">LOOP<input type="text" id="nwhiles" placeholder="relays" style="width:30px;" value="1">
BUFFER<input type="text" value="64" id="buffer" style="width:60px;">
TimeCtrlPs<input type="text" value="10000" id="TimeInterval" onchange="TimeInterval = this.value"  style="width:60px;">


<!--input type="button" value="EXIT_AJAX" onclick='EXIT_AJAX=true'-->

<br>
<input type="button" value="Browser" onclick='r=display("browserfile");this.value="Browser "+r'>
<input type="button" value="Sub-Editor" onclick='r=display("comdata");this.value="comdata "+r'>
<input type="button" value="avisos" onclick='r=display("avisos");this.value="avisos "+r'>
<input type="button" value="idx" onclick='r=display("idx");this.value="idx "+r'>
<input type="button" value="VideoPlayer" onclick='r=display("mg");

 this.value="VideoPlayer "+r'>

</div>
<iframe id='browserfile' src="readlist.php" style="display:none;width:100%;height:320px;" frameborder=0></iframe>
<hr>
<div id="procs_div" style="overflow-y:scroll;overflow-x:hidden;position:fixed;max-height:30%;height:flex;width:100%;bottom:0;"></div>
<div id="comdata"></div>
<div id="avisos"></div>
<code id='idx' style=''>RETURN PJXML EXEC JS</code>
<div id='mg' style="display:none;">
<input type="button" value="Abrir" onclick='if(src=prompt("AD VIDEO URL","mitv/live/play.m3u8")){addVideo2("MASTER",src);}'>
<button type="button" onclick="MASTER.stop()">Stop</button>
<figure>
<video id="MASTER" controls autoplay ></video>
</figure>
</div>

<script>

unbucle=0

function progres1(data){
document.getElementById('idx').innerHTML = data
console.log(data)
}

document.getElementById('idx').style.maxHeight = "160px"
document.getElementById('idx').style.overflow = "auto"
document.getElementById('idx').style.display = "block"



document.getElementById('idx').innerHTML = ""



flushdata="";

function addVideo(s,src='in.mp4',mimetype="application/x-mpegURL"){

//video = document.createElement("video")
//video.id = s
//video.style="width:100%;height:280px;"+
//"border:solid 3px #239476;"
//video.controls = true;
document.getElementById('mg').innerHTML = "<video id='"+s+"' controls></video>"
//document.getElementById('mg').appendChild(video)
//alert(src+"\n"+document.getElementById('mg').innerHTML)
xplayer(s,src,mimetype)
}

/*
Proceso = new Array();
procs = new Array();
procs_info = new Array()
prs = new Array()
ps = 1

function scom(a,ps=procs.length){


ps++


Proceso[ps] = "START PROCESS"


procs[ps] = document.createElement("div")
procs[ps].id = "Proc_"+ps
procs_info[ps] = document.createElement("div")
procs_info[ps].id = "Proc_"+ps+"_info"
procs_info[ps].innerHTML = "Abierta Petición a Proceso :ajaxPid: "+ps
procs_div.prepend(procs[ps])
procs_div.prepend(procs_info[ps])
filejhp = 'php/execajax-while.php'

buffer = document.getElementById('buffer').value 

prs[ps] = 
ajax("VAR="+a+"&ps="+ps+"&divresp="+procs[ps].id+"&buffer="+buffer+"&relay="+GId('nwhiles'),'',filejhp,'GET');
}


*/




Proceso = new Array();
procs = new Array();
procs_info = new Array()
procs_ping = new Array()
prs = new Array()




psctrl = new Array();
time_interval = new Array()

TimeInterval = 10000

function scom(a,ps=procs.length){

if(ps==0) ps = 1

if(isNaN(TimeInterval) || TimeInterval < 5000) TimeInterval = 12000

time_interval[ps] = TimeInterval


Proceso[ps] = "START PROCESS"
procs[ps] = document.createElement("div")
procs[ps].id = "Proc_"+ps
procs_info[ps] = document.createElement("span")
procs_info[ps].id = "Proc_"+ps+"_info"
procs_info[ps].innerHTML = "Abierta Petición a Proceso :ajaxPid: "+ps
procs_ping[ps] = document.createElement("span")
procs_ping[ps].id = "Proc_"+ps+"_ping"
procs_ping[ps].innerHTML = "Ping: "+ps

procs_div.prepend(procs[ps])
procs_div.prepend(procs_info[ps])
procs_div.append(procs_ping[ps])

filejhp = 'php/execajax-while.php'

buffer = document.getElementById('buffer').value 


psctrl[ps] = setInterval(`

thctrl(`+ps+`)

`,time_interval[ps])





prs[ps] = 
ajax("VAR="+a+"&ajaxpid="+psctrl[ps]+"&ps="+ps+"&divresp="+procs[ps].id+"&buffer="+buffer+"&relay="+GId('nwhiles'),'',filejhp,'GET');


}


thc = new Array()
rthc = new Array()
function thctrl(param){

//alert(param,psctrl[param])
//s = document.getElementById(procs_ping[param])
//s.innerHTML = psctrl[param]+".:."+param

thc[param] = ajax("psid="+param,'avisos',"php/pctrl.php","GET")
}


function PCTL(param,divid){

ajax("XX="+param,false,"php/pctrl.php","GET")

}



function jxp(action,put){
ajaxReturn(action,put,'php/jxp.php','GET')
}




    
    function addVideo2(s,src){
    
  var video = document.getElementById(s);
  var videoSrc = src;
  //
  // First check for native browser HLS support
  //
  if (video.canPlayType('application/x-mpegURL')) {
    video.src = videoSrc;
    video.controls = true
    video.play = true;
    //
    // If no native HLS support, check if HLS.js is supported
    //
  } else if (Hls.isSupported()) {
    var hls = new Hls();
    hls.loadSource(videoSrc);
    hls.attachMedia(video);
  }
  
}
</script>


