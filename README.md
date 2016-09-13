# Gate Transformer QGIS plugin
### Modify geometry of pedestrian movement gates in space syntax

## About
Gate Transformer is a plugin to modify the geometry of gates used in space syntax movement observations.
Gates are usually drawn perpendicular to the axial line, with varying lengths. For presentation of movement observations the typical output is a map showing lines along the axial lines to indicate the movement direction. The gates should all be rotated 90degrees and have the same length.

## Installation
Currently the plugin is not available through the QGIS plugins repository. To install you need to download the latest GateTransformer_private_0.0.1B.zip file from the releases page (https://github.com/OpenDigitalWorks/GateTransformer/releases). 
Unzip and copy the entire folder into the QGIS plugins directory.

This directory can be found here:
* MS Windows: C:\Users\[your user name]\.qgis2\python\plugins\
* Mac OSX: Users/[your user name]/.qgis2/python/plugins/
* Linux: home/[your user name]/.qgis2/python/plugins/

This directory is usually hidden and you must make hidden files visible.
Under Mac OSX you can open the folder in Finder by selecting 'Go > Go To Folder...' and typing '~/.qgis2/python/plugins/'. If you haven’t installed any QGIS plugins so far, you need to create the ‘plugins’ directory in
the ‘.qgis2/python/’ directory. After copying the plugin, it will be available in the plugin manager window once you (re)start
QGIS. Check the box next to the plugin to load it.

## Software Requirements
QGIS (2.0 or above) - http://www.qgis.org/en/site/

## How to
* Gates layer Choose the line-based gate layer from the drop-down menu that you want to transform
* Rotate Line (degree) Define the angle in degrees for rotating the selected gates.
* Resize Line (metre) Define the length in metres for resizing the selected gates.
* Rescale Line (multiple) Define the multiple in ratio for rescaling the selected gates.
* Transform Pressing the transform button will activate the analysis for the selected transformation
* Close Pressing close will close and terminate the Gate Transformer
