# PlantGL-Recipes

## Troubleshoot (Windows)

#### Do you have Microsoft Visual Studio 2015 Update 3 installed ?

If not, please install it. You can have multiple versions installed, so you won't have to uninstall your favorite Visual Studio version.

#### Do you have the Windows 10 SDK installed ?

Within the Visual Studio 2015 installer, please install the following package :

`Windows and Web Development -> Universal Windows App Development Tools -> Tools (1.4.1) and Windows 10 SDK (10.0.14393)`

Otherwise, `rc.exe` will be missing and libQGLViewer won't build.

#### Do you have the latest version of Miniconda 3 installed ?

Python 3.7 (or greater) is required.

You can download it [here](https://docs.conda.io/en/latest/miniconda.html).

#### Do you have any Visual Studio-related variable in your environment ?

Please remove them to avoid any conflict.

#### Do you have any Visual Studio-related path in your PATH environment variable ?

Please remove them to avoid any conflict.
