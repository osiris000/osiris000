
MAINPANEL = {

TAG:"main",
className:"panel_principal",
style:"cursor:pointer"

}


INTRO_APP = {

TAG:"div",
click:` this.style.display='none' `,
innerHTML:`<p>MiTv WebApp</p>`

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
innerHTML:"<h1>SPLASH CONTENT</h1>"


}


CLOSE_SPLASH = {

TAG:"button",
innerHTML: "Cerrar",
click:`document.getElementById('splash-container').style.display = 'none';`


}