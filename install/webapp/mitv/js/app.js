

 const scriptsToLoad = ["js/config.js", "js/load.js"];

 

    function loadScriptsSequentially(scripts, index = 0) {
      if (index >= scripts.length) {
        // All scripts are loaded
        console.log("All scripts loaded!");
        return;
      }

      const script = document.createElement("script");
      script.src = scripts[index];
     


      script.onload = function () {
        // Load the next script after this one is loaded
        loadScriptsSequentially(scripts, index + 1);
      };


      document.head.append(script);
 
    }

    //document.addEventListener('DOMContentLoaded', function() {
      // Call the function to load scripts after the document is loaded

     loadScriptsSequentially(scriptsToLoad);

  //  });




const loadIfApp = function(object) {
  const userAgent = navigator.userAgent.toLowerCase();
  const defaultConfig = object['default'];
  const loadedFiles = {
    css: [],
    js: []
  };

  const loadFiles = function(files) {
    for (const [key, values] of Object.entries(files)) {
      if (!values) {
        console.log(`Error de carga no existe ruta para ${key}`);
        continue;
      }

      values.forEach(value => {
        switch (key) {
          case 'css':
            const cssLink = document.createElement('link');
            cssLink.rel = 'stylesheet';
            cssLink.type = 'text/css'
            cssLink.href = value;
            document.head.append(cssLink);
            loadedFiles.css.push(cssLink);
            break;
          case 'js':
            const jsScript = document.createElement('script');
            jsScript.src = value;
            jsScript.type = 'text/javascript';
            document.head.append(jsScript);
            loadedFiles.js.push(jsScript);
            break;
        }
      });
    }
  };

  for (const [browserCode, files] of Object.entries(object)) {
    const reg = new RegExp(browserCode, 'i');
    if (reg.test(userAgent)) {
      loadFiles(files);
      return loadedFiles;
    }
  }

  // Si no se encontró un navegador específico, cargar los archivos por defecto
  loadFiles(defaultConfig);
  return loadedFiles;
};



