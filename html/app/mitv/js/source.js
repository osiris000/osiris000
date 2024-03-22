
MAINPANEL = {

TAG:"main",
className:"panel_principal",
style:"cursor:pointer"

}


INTRO_APP = {

TAG:"div",
click:` this.style.display='none' `,
innerHTML:``

}


SPLASH = {


TAG:"button",
innerHTML:"Menú",
click:`document.getElementById('splash-container').style.display = 'flex';`



}


SPLASH_CONTAINER = {

TAG:"div",


}


SPLASH_CONTENT = {

TAG:"div",

innerHTML:`<p><iframe src="https://vtwitt.com/tv" width="840px" height="520px">



</iframe></p>`


}


CLOSE_SPLASH = {

TAG:"button",
innerHTML: "Cerrar",
click:`document.getElementById('splash-container').style.display = 'none';`


}