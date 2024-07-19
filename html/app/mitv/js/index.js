/* index js */



moveTag(MainPanel,Body)



moveTag(IntroApp,MainPanel)




moveTag(Splash, MainPanel)







moveTag(SplashContainer,MainPanel)





moveTag(SplashContent,SplashContainer)


moveTag(CloseSplash, SplashContent)




onload = function(){



IntroApp.innerHTML += `
<iframe id='iftvx2' class="rumble" layout="responsive" style="width:95vw;height:80vh;display:flex" src="tv/player2.php?chn=../channels/main/live-ts/master_ultrafast.m3u8" frameborder="0" allowfullscreen></iframe>
`


/*

final de carga

*/


}
