
# Fault Injection Tool
This tool allows the user to inject (1) Internal Faults, e.g. BitFlips or Zeros, and (2) External Faults, including the most common image corruptions in Computer Vision. Furthermore, this tool will also allow for the injection of LiDAR faults (tbd).

## Description of Program 

- **Configuration.json**
This document contains the required information and variables for the program. The user can set certain parameters, as well as paths here. This file will later be updated by the GUI to manage the user input.


- **ExternalFaults.py**
This is the primary document for the injection of image corruptions. It grabs the selected faults from the config file, loads and copies the specified images into the *Results/CorruptedImages* folder and executes the fault injection. By copying the images, it can be guaranteed, that the different faults do not overlap on the images, as for each fault type a seperate folder is created. 


- **ImageCorruptions**
This folder contains the codes for the image corruptions, that are not included in the ImageCorruption library, such as dirt and rain. If you want to add a specific type of image corruption, please add the file to this folder.


- **InternalFaults.py**
This file manages the injection of internal faults into a loaded neural network. It utilizes a modified TensorFI2 Version ( see *TensorFI2* folder). Based on the specified parameters of the config file, it injects a number of faults (BitFlips, Zeros, Random Value) statically into saved weights and biases or dynamically into the output layers during inference. It also allows for running experiments with various numbers of bitflips in different layers (needs to be specified in the config file).


- **FaultInjection.py**
This document manages the injection of both types of faults. In order to do this, the first step is to corrupt the images and use the new images as the testing input for a corrupted network. The procedure is as follows: 

(1) Corrupt images and save to separate folder

(2) Update the labels for the newly generated images

(3) Add internal faults to selected model

(4) Test and evaluate the performance of the corrupted network with the corrupted images.




