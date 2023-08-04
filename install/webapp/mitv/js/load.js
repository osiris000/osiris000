/* load2 */


  document.title = title

  const scriptsToLoad2 = [wfcore,xhr,source,paneles,indexFile];

  loadScriptsSequentially(scriptsToLoad2);

  const loadedFiles = loadIfApp(loadIfNavigator);

