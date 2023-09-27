

/* requiere de wfcore2 y xhr2 ó wfcore3   */


/*VideoContainer = addPanel({TAG:"div"})
VideoContainer.id = "video-container"
*/


function XPlayer() {
  
  this.set = {
    id: "",
    inner: "",
    css: "default.css"
  };

  
  this.settings = function(options) {
    this.set.id = options.id || this.set.id;
    this.set.inner = options.inner || this.set.inner;
    this.set.css = options.css || this.set.css;
  };

  this.updateId = function(newId) {
    this.set.id = newId;
  };

  return this;
}



var player = new XPlayer();

player.settings({
  id: "player1",
  innerId: "player-inner",
  css: "custom.css"
});

console.log(player.set.id);  // Salida: "player1"

player.set.id = "tal";

console.log(player.set.id);  // Salida: "tal"

/*




_PLAYER = {}
_player = {}


_PLAYER["playerPanel"] = {TAG:"div"}

_player["playerPanel"] = addPanel(_PLAYER["playerPanel"])



_PLAYER["videoPlayerPanel"] = {TAG:"div"}

_player["videoPlayerPanel"] = addPanel(_PLAYER["videoPlayerPanel"])
_player["videoPlayerPanel"].id = "videoPlayerPanel"


_PLAYER["videoPlayer"] = {TAG:"video"}

_player["videoPlayer"] = addPanel(_PLAYER["videoPlayer"])
_player["videoPlayer"].id = "videoPlayer"


_PLAYER["loadingText"] = {TAG:"div"}

_player["loadingText"] = addPanel(_PLAYER["loadingText"])
_player["loadingText"].id = "loadingText"



Splay = addPanel({TAG:"div"})
Splay.id = "splay"

Pantalla = addPanel({TAG:"div",className:"pantalla"})
Fondo = addPanel({TAG:"div",className:"fondo"})


BotonPlay = addPanel({TAG:"div",className:"boton-play"})



*/





//moveTag(Player,MainPanel)