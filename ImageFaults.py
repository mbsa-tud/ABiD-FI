from imagecorruptions import get_corruption_names
from imagecorruptions import corrupt
from ImageCorruptions.ChromaticAberration import chromatic_aberration
from ImageCorruptions.Dirt import add_dirt
from ImageCorruptions.Rain import add_rain
from ImageCorruptions.CoarseDropout import coarse_dropout
from ImageCorruptions.Fisheye import add_fisheye
import cv2
import json
import os
import random
import shutil
from tqdm import tqdm
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


def get_corruptions(config):
    """This function gets the names of each fault that was selected and returns them in a list"""

    if config["ExternalFaults"]["compare_all"]:
        FaultList = [key for key, value in config["ExternalFaults"]["Faults"].items()]
    else:
        FaultList = [fault_name for fault_name, fault_data in config['ExternalFaults']['Faults'].items() if
                     fault_data['active'] == 1]
    return FaultList


def define_images(config, verbose, fault_data, corruption, severity = ""):
    """This function randomly selects images from the source directory. It copies all source images to a new (
    corrupted) folder and return the list of selected images as well as the folder name, where the corrupted images
    will be saved. """
    all_images = os.listdir(config["ExternalFaults"]["image_dir"])
    #all_labels = pd.read_csv(config["ExternalFaults"]["image_csv"],
                          #names=["image_id", "filename", "class_id", "label"])
    selected_images = random.sample(all_images, round(fault_data["probability"] * len(all_images)))

    if verbose:
        print(
            f"Applying level {severity} {corruption} to {round(fault_data['probability'] * len(all_images))} out of {len(all_images)} images.")

    # creates a new folder, copies all images and then injects selected faults in a certain amount of them
    if config["ExternalFaults"]["mixed"]:
        folder_corrupted_images = f"Results/CorruptedImages/Mixed"
    else:
        folder_corrupted_images = f"{config['ExternalFaults']['result_dir']}/{corruption}_severity_{severity}"

    if not os.path.exists(folder_corrupted_images):
        os.makedirs(f"{folder_corrupted_images}/images")
        for image_name in all_images:  # copies all images
            source = f"{config['ExternalFaults']['image_dir']}/{image_name}"
            destination = f"{folder_corrupted_images}/images/{image_name}"
            shutil.copy(source, destination)
    return selected_images, folder_corrupted_images, #all_labels


def inject_external_faults(config, verbose):
    FaultList = get_corruptions(config)

    # Iterate through all selected corruptions
    for corruption in FaultList:
        # loading data and specs about this specific corruption
        fault_data = config["ExternalFaults"]["Faults"][f"{corruption}"]

        # In order to allow the iteration through all severities (defines a list of severities to iterate through)
        if config["ExternalFaults"]["all_severities"]:
            severities = [1, 2, 3, 4, 5]
        else:
            severities = [fault_data["severity"]]

        for severity in severities:
            selected_images, folder_corrupted_images = define_images(config, verbose, fault_data, corruption, severity) #all_labels infront of =
            corrupted_filenames = []

            # selecting one image and injecting the faults
            for image_name in tqdm(selected_images):
                image = cv2.imread(f"{folder_corrupted_images}/images/{image_name}")

                # Actual corruption image has to be numpy array and functions should return a numpy array
                if corruption == "chromatic_aberration":
                    corrupted = chromatic_aberration(image, severity)
                elif corruption == "coarse_dropout":
                    corrupted = coarse_dropout(image, severity)
                elif corruption == "fisheye":
                    corrupted = add_fisheye(image, severity)
                elif corruption == "rain":
                    corrupted = add_rain(image, severity)
                elif corruption == "dirt":
                    corrupted = add_dirt(image, severity)
                else:
                    corrupted = corrupt(image, corruption_name=corruption, severity=severity)

                # Tracking which images were corrupted and saving them in a txt file
                if config["ExternalFaults"]["keep_originals"]:
                    # Create Label for the newly created corrupted images
                    #corrupted_label = all_labels.loc[all_labels["filename"] == image_name, :] # creates a new DataFrame, that contains the properties of the original image

                    image_name = f"{image_name.split('.')[0]}_{severity}.jpg"  # to get rid of .jpg at the end
                    cv2.imwrite(f"{folder_corrupted_images}/images/{image_name}", corrupted)

                    # Modify the properties of the entry and add to DataFrame
                    #corrupted_label["filename"] = image_name
                    #all_labels = pd.concat([all_labels, corrupted_label])
                else:
                    cv2.imwrite(f"{folder_corrupted_images}/images/{image_name}", corrupted)

                corrupted_filenames.append((image_name, corruption))

        # creates a txt file, documenting which images were selected and corrupted
        with open(f"{folder_corrupted_images}/CorruptedImages.txt", 'a') as file:
            for data in corrupted_filenames:
                file.write(str(data) + '\n')
        #all_labels.to_csv(f"{folder_corrupted_images}/labels.csv", header=False, index=False)

