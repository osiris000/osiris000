/* index js */



moveTag(MainPanel,Body)



moveTag(IntroApp,MainPanel)




moveTag(Splash, MainPanel)







moveTag(SplashContainer,MainPanel)





moveTag(SplashContent,SplashContainer)


moveTag(CloseSplash, SplashContent)




onload = function(){



IntroApp.innerHTML += `

<br>
<iframe class="rumble" layout="responsive" style="width:60vw;height:60vh;" src="tv/player2.php?chn=../channels/main/live-ts/master_ultrafast.m3u8" frameborder="0" allowfullscreen></iframe>
<br><br>
`


/*

final de carga

*/


}
