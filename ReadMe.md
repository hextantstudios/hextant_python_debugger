# Blender Add-on: Python Debugger

Allows debugging of Blender Python add-ons using Visual Studio Code or Visual Studio 2019 v16.6 or later.

Debugging Blender add-ons can be a bit painful without a proper debugger. This add-on (inspired by the [Blender Debugger for VS Code](https://github.com/AlansCodeLog/blender-debugger-for-vscode) add-on) uses the [debugpy](https://github.com/microsoft/debugpy) package to start a debug server inside Blender on a specific port. VS Code or Visual Studio can then be used to attach to it to set breakpoints, inspect local variables, or evaluate custom expressions.

## Installation

* Download the latest release from [here](https://github.com/hextantstudios/hextant_python_debugger/releases/latest/download/hextant_python_debugger.zip) or clone it using Git to your custom Blender `...\scripts\addons\` folder.
* From Blender's Main Menu:
  * *Edit / Preferences*
  * Click the *Install* button and select the downloaded zip file.
  * Check the check-box next to the add-on to activate it.
  * In the add-on's Preferences section
    * Click *Install debugpy* to install the `debugpy` package.
      * If this fails, open Blender's console from *Window/Toggle System Console* and see if there are additional error messages.
      * Note: Before uninstalling the add-on you may wish to click *Uninstall debugpy*.
    * *Server Port:* The default port (`5678`) should be fine, but it can be changed if needed as long as the same value is used when connecting from Visual Studio.

## Setup a Custom *Scripts* Folder for Your Add-on

While it is not essential to do so, it is a bit easier to develop a new add-on in you own custom scripts folder. This can be configured in Blender:

* *Edit / Preferences / File Paths / Scripts* - Set to a folder on your drive. 
  * ex: `C:\blender-scripts\`

* Create a sub-folder underneath this named `addons\`. (Required by Blender.)
* Finally, create a folder for your add-on in the `addons\` folder (or place your Python file here if using only only a single file).
  * ex: `C:\blender-scripts\addons\my_blender_addon\...`

* Your add-on should now show up in Blender's preferences. The drop-down there can be set to *User* to show all add-ons in this folder.

## Debug a Blender Add-on from Visual Studio Code

To debug your Blender add-on using Visual Studio Code, a few things need to be done initially. In Visual Studio Code:

* Enable the Python extension for Visual Studio Code:

  * Click *File / Preferences / Extensions*
    * Search for Python and install the extension by Microsoft.
    * Note: While you may get a warning about Python not being installed. This can be ignored as it is not required for remote debugging. If you wish, you can install it from the *Download* link provided, [python.org](https://www.python.org/downloads/), your OS's package manager, or the [Microsoft Store](https://apps.microsoft.com/store/search/python?hl=en-us&gl=US).

* Click *File / Open Folder* and open the folder containing your add-on.

* Click *Run / Add Configuration*

  * Select a debug configuration: *Remote Attach*

  * Host name: `localhost`

  * Port number: `5678` - Or use the value set in the Blender add-on's preferences.

  * This will create and open a `.vscode/launch.json` file in your add-on projects folder.

    * Copy and paste the `localRoot` value to the `remoteRoot` and save and close the file:
      ```json
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "${workspaceFolder}"
      ```

You should now be able to debug your add-on as needed by doing the following:

* From Blender's main menu, click: *{Blender Icon} / System / Start Debug Server*
  * Note that this only needs to be done once per Blender execution. If the menu appears disabled, the `debugpy` package needs to be installed from the add-on's preferences.
* From Visual Studio Code:
  * If not already open, click *File / Open Folder* and open the folder containing your add-on.
  * Press `F5` to connect to Blender
    * An error showing `connect ECONNREFUSED 127.0.0.1:5678` usually means the debug server has not been started.
  * To set a breakpoint in an add-on file, click to the left of the desired line (or use the `F9` hotkey). When Blender executes that line, Visual Studio Code should highlight it and populate the *Call Stack* and *Variables* window. The *Watch* window can be used to view custom expressions.
    * The debug toolbar can be used to control stepping or `F10` steps over a line and `F11` steps into one. `F5` continues execution.
  * After making a change and saving the file, the add-on will need to be reloaded in Blender. See my [Reload Add-on](https://github.com/hextantstudios/hextant_reload_addon) add-on for more information about how to do this quickly and properly.
  * Note: To exclude the auto-generated `__pycache__` folder (that is created when Blender compiles the add-on) from the *Explorer* file view and find-in-file searches in Visual Studio Code:
    * Click *File / Preferences / Settings*
      * Click  *User / Text Editor / Files / Exclude* (or search for "Files/Exclude")
      * Add: `**/__pycache__`

## Debug a Blender Add-on from Visual Studio 2019 or 2022

To debug your Blender Add-on from Visual Studio 2019 v16.6 or later, you will need to intially:

* Open the *Visual Studio Installer* application and install the *Python development* workload.
  * Note that *only* the *Python language support* option is needed for remote debugging and others Python options can be un-checked.

You should now be able to debug your add-on as needed by doing the following:

* From Blender's main menu, click: *{Blender Icon} / System / Start Debug Server*
  * Note that this only needs to be done once per Blender execution. If the menu appears disabled, the `debugpy` package needs to be installed from the add-on's preferences.
* From Visual Studio:
  * Click *File / Open / Folder* and open the folder containing your add-on.
  * Click *Debug / Attach to Process* (`Ctrl + Alt + P`)
    * Connection type: *Python remote (debugpy)*
    * Connection target: `localhost:5678` (*press enter*)
    * It should now show in the Processes list, click *Attach*.
  * To set a breakpoint in an add-on file, click to the left of the desired line (or use the `F9` hotkey). When Blender executes that line, Visual Studio should highlight it and populate the *Call Stack* and *Locals* window. The *Watch* window can be used to view custom expressions.
    * The debug toolbar can be used to control stepping or `F10` steps over a line and `F11` steps into one. `F5` continues execution.
  * After making a change and saving the file, the add-on will need to be reloaded in Blender. See my [Reload Add-on](https://github.com/hextantstudios/hextant_reload_addon) add-on for more information about how to do this quickly and properly.
  * Note: To exclude the auto-generated `__pycache__` folder (that is created when Blender compiles the add-on) from the *Solution Explorer* and searches in Visual Studio perform *one* of the following:
    * Click the *Show All Files* button in the *Solution Explorer* and open `VSWorkspaceSettings.json` 
      * Add  `__pycache__` to the `"ExcludedItems"` array.
    * *or* add `__pycache__` to your `.gitignore` file if using Git.

## Known Issues

* *None currently.*

## License

This work is licensed under [GNU General Public License Version 3](https://download.blender.org/release/GPL3-license.txt).