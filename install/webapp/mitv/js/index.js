/* index js */


moveTag(MainPanel,Body)

moveTag(IntroApp,MainPanel)

moveTag(Splash, MainPanel)

moveTag(SplashContainer,MainPanel)

moveTag(SplashContent,SplashContainer)

moveTag(CloseSplash, SplashContent)



/* final de carga */

onload = function(){

IntroApp.innerHTML += `

APP: `+app+` <br>

API: `+wfcore+`<br>

</h5>Mitv fin de carga<h5><b>Click para cerrar</b>`

}
