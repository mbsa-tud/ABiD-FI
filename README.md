
# Fault Injection Tool
This tool allows the user to inject (1) Image Faults, including the most common image corruptions in Computer Vision, and (2) LIDAR Faults.

## Description of Program 

- **Configuration.json**
This document contains the required information and variables for the program. The user can set certain parameters, as well as paths here. This file will later be updated by the GUI to manage the user input.


- **ExternalFaults.py**
This is the primary document for the injection of image corruptions. It grabs the selected faults from the config file, loads and copies the specified images into the *Results/CorruptedImages* folder and executes the fault injection. By copying the images, it can be guaranteed, that the different faults do not overlap on the images, as for each fault type a seperate folder is created. 


- **ImageCorruptions**
This folder contains the codes for the image corruptions, that are not included in the ImageCorruption library, such as dirt and rain. If you want to add a specific type of image corruption, please add the file to this folder.





