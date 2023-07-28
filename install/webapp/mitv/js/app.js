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

    document.addEventListener('DOMContentLoaded', function() {
      // Call the function to load scripts after the document is loaded



      loadScriptsSequentially(scriptsToLoad);


    });
