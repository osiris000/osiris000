/* config app */

app = "mitv"

/* title */

title = "MiTv App"

/* wfcore version  */

wfcore = "js/wfcore2.js"

/* xhr version */

xhr = "js/xhr2.js"

/* js indexfile */

indexFile = "js/index.js"

/* paneles */

paneles = "js/paneles.js"

/* source */

source = "js/source.js"


/* hls.js lib */


hlsJs = "https://cdn.jsdelivr.net/npm/hls.js@latest"


/* Player */


player = "js/player.js"


/* load scripts order */

const scriptsToLoad2 = [wfcore,xhr,source,paneles,indexFile,hlsJs,player];



/* load if navigator */

const loadIfNavigator = {
 
firefox : {
 	css: ['css/firefox.css', 'css/player.css']
 },

 chrome : {
 	css: ['css/chrome.css','css/player.css'] 
 },
  
 default: {
    css: ['css/chrome.css', 'css/player.css']
  }
};




