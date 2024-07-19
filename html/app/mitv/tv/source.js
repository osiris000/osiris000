

loadIfApp("firefox",{css:"default.css"})
loadIfApp("chrome",{css:"default.css"})



/* Estructura Principal  */

const MAIN = { TAG:"main",
className:"pantalla",
innerHTML:" <!--MAIN Panel --> "  }


const NAV = { TAG:"nav",
className:"navbar",
innerHTML:`
<img style="float:left;height:100%;" src="uf.png">
<!--div style="color:#dd2211;float:right;font-weight:bold;font-family:'gill sans';letter-spacing:2.3px;padding:10px;font-size:28px;font-style:oblique;">
ultrafast.tv
</div-->` }


const CENTER_SCREEN = { TAG:"div",
className:"center_screen",innerHTML:" <!-- CENTER_SCREEN --> "
}


const SCROLL_PANEL = { TAG:"div",
className:"scroll_panel",innerHTML:""
}

const VIDEO_PANEL = { TAG:"section",
innerHTML:"",
className:"video_panel"}


const VIDEO_PLAYER_TOP = { TAG:"div",
className:"video_player_top"
}

const PLAYER_PANEL = { TAG:"figure",
className:"player_panel"}


const VIDEO_PLAYER = { TAG:"video",
className:"video_player",
poster:"https://compostela21.com/img/connecting-loading.gif", 
style:"text-align:center;display:block;"
}

const VIDEO_PLAYER_CONTROLS = { TAG:"div",
className:"video_player_controls",
innerHTML: `

<button onclick="Player.play()">Play</button>
<button onclick="Player.pause()">STOP</button>
Video Player Controls

` , 
style:"text-align:center;display:none"
}

const VIDEO_FEED = { 
TAG:"section",
className:"feed", 
innerHTML:"", 
click:`alert("EVENT CLICK TEXT");` , 
style:"cursor:pointer"}






const SUGGESTIONS_PANEL = { TAG: "section",
className:"suggestions" ,
 innerHTML: `
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-3185107427297382"
     data-ad-slot="1119731952"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>

<!--
Pruebas:<br>

<a href="javascript:void(0)" onclick="
ajax('url=https://vtwitt.com/tv/cinetv.m3u8','','/tv/ivideo3.php','GET')
">Cambio de Canal m3u8</a>

<br>

<a href="javascript:void(0)" onclick="
ajax('url=https://www.youtube.com/watch?v=UI_jSsHm6TE','','/tv/ivideo3.php','GET')
">Cambio a Vídeo Youtube</a>


<br>

<a href="javascript:void(0)" onclick="
ajax('url=https://youtube.com/?v=SBCpGpw46as','','/tv/ivideo3.php','GET')
">Youtube Short</a>

<br>

<a href="javascript:void(0)" onclick="
ajax('x=tunel&url=https://youtu.be/gKtPmFcGD-Q','','/tv/ivideo3.php','GET')
">Cambio a Vídeo Youtube [Pipe 403]</a>
-->` }


const FOOTER_PANEL = { TAG: "footer",
className:"footer" , innerHTML: "" }



/* Otros Elementos  */


const SHARE_THIS_SCRIPT = { TAG: "script",

type:"text/javascript",
src:"https://platform-api.sharethis.com/js/sharethis.js#property=6168f3274564d200122a7e54&product=inline-share-buttons"

}


const SHARE_THIS_DIV = { TAG: "div",
innerHTML: "Share This Div" , style:"float:right",
className:"sharethis-inline-share-buttons"
}


var script = document.createElement("script");
script.src = "paneles.js"
script.type = "text/javascript"
document.head.append(script) 

