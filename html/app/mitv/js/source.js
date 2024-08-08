
MAINPANEL = {

TAG:"main",
className:"panel_principal",

}


INTRO_APP = {

TAG:"div",
innerHTML:``

}


SPLASH = {


TAG:"button",
innerHTML:"Menú",
click:`document.getElementById('splash-container').style.display = 'flex';`,



}


SPLASH_CONTAINER = {

TAG:"div",


}


SPLASH_CONTENT = {

TAG:"div",

innerHTML:`
<button type="button" onclick="document.getElementById('iftvx2').src='tv/app.php'">Channels Ultrafast</button>
<button type="button" onclick="document.getElementById('iftvx2').src='tv/player2.php?chn=../channels/main/live-ts/master_ultrafast.m3u8'">Reload Channel</button>
`,
style:"display:block;"


}


CLOSE_SPLASH = {

TAG:"button",
innerHTML: "Cerrar",
click:`document.getElementById('splash-container').style.display = 'none';`

}