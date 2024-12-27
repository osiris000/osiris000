/* index js */



moveTag(MainPanel,Body)



moveTag(IntroApp,MainPanel)




moveTag(Splash, MainPanel)







moveTag(SplashContainer,MainPanel)





moveTag(SplashContent,SplashContainer)


moveTag(CloseSplash, SplashContent)




onload = function(){

  function makeResizable(elementId) {
    const container = document.getElementById(elementId + "-container");
    const content = document.getElementById(elementId);

    // Estilos iniciales
    container.style.width = "70vw";
    container.style.position = "absolute";
    container.style.padding = "10px";
    container.style.boxSizing = "border-box";
    container.style.visibility = "hidden"; 
    container.style.height = "460px";
    container.style.fontSize = "18px";
    container.style.fontWeight = "bold";
    container.style.overflow = "hidden"; // Evita que el contenido sobresalga
    container.style.resize = "both"; 
    container.style.background = "rgba(125,125,125,.35)"


	content.style.resize = "both";
    content.style.width = "100%";
    content.style.height = "calc(100% - 20px)"; 
    content.style.fontSize = "22px";
    content.style.color = "#feedde";
    content.style.background = "rgba(122, 2, 255, 0.7)";
    content.style.padding = "10px";
    content.style.boxSizing = "border-box";



  }




randnick  = Math.floor(Math.random() * 9000000) + 1000000;


IntroApp.innerHTML = `
<div id="webirc-container">
  <b style="background:rgba(120,180,195,.4);padding:2px;"> IRC - CHAT </b>   <a href="javascript:void(0);" onclick="document.getElementById('webirc-container').style.visibility='hidden';" style="float:right;cursor:pointer;color:#c4edea;font-weight:bold;"> [ocultar] </a>  <!-- <a href="javascript:void(0);" onclick="document.getElementById('webirc-container').style.display='none';" style="cursor:pointer"> [X] </a> --> <br>
<div id='webirc'>  <iframe 
  loading="lazy"  frameborder="0" scrolling="no" 
  src="https://chathispano.com/webchat/?theme=embebed&style=orange&title=Osiris-Irc-Chat&logo=https://cdn.chathispano.com/news/esquina.jpg&autojoin=true&autoload=false&tema=CLI&nick=osiris_`+randnick+`&chan=#OsirisWeb"
 style="width: 100%;height:100%;"
  ></iframe></div></div>

`

makeResizable("webirc");

IntroApp.innerHTML += `
<iframe id='iftvx2' class="rumble" layout="responsive" style="width:95vw;height:90vh;display:flex" src="tv/player2.php?chn=../channels/main/live-ts/master_ultrafast.m3u8" frameborder="0" allowfullscreen></iframe>
`






/*

final de carga

*/


}
