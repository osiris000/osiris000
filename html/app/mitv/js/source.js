
MAINPANEL = {

TAG:"main",
className:"panel_principal",

}





INTRO_APP = {

TAG:"div",
innerHTML:`LOADING....`,
style:`display:flex;resize:both`

}



SPLASH = {


TAG:"button",
innerHTML:"Menú",
click:`document.getElementById('splash-container').style.display = 'flex';`,



}


SPLASH_CONTAINER = {

TAG:"div"


}


SPLASH_CONTENT = {

TAG:"div",

innerHTML:`
<button type="button" class='mbuton' onclick="document.getElementById('iftvx2').src='tv/player2.php?chn=../channels/main/live-ts/master_ultrafast.m3u8'">Osiris TV</button>
<button type="button" class='mbuton' onclick="document.getElementById('iftvx2').src='tv/app.php'">Canales Tv</button>
<button type="button" class='mbuton' onclick="document.getElementById('iftvx2').src='../freedirectory/video/peliculas/cartelera.php'">Cartelera</button>
<button type="button" class='mbuton' onclick="document.getElementById('webirc-container').style.display='block';document.getElementById('webirc-container').style.visibility='visible';"> IRC - Chat </button>
`,
style:"width:auto;display:block;"


}


CLOSE_SPLASH = {

TAG:"button",
innerHTML: "Cerrar",
click:`document.getElementById('splash-container').style.display = 'none';`,
className:`mbuton`
}
