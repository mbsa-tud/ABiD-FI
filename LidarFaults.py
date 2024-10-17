import os
import random
import numpy as np
import open3d as o3d  # Make sure you have Open3D installed via pip
import shutil
from tqdm import tqdm

from LiDARCorruptions.Noise import add_noise
from LiDARCorruptions.Outliers import add_outliers
from LiDARCorruptions.MissingPoints import remove_points

def get_lidar_corruptions(config):
    """This function gets the names of each fault that was selected and returns them in a list."""
    if config["LiDARFaults"]["compare_all"]:
        FaultList = [key for key, value in config["LiDARFaults"]["Faults"].items()]
    else:
        FaultList = [fault_name for fault_name, fault_data in config['LiDARFaults']['Faults'].items() if
                     fault_data['active'] == 1]
    return FaultList


def define_lidar_pointclouds(config, verbose, fault_data, corruption, severity):
    """Selects point clouds from the source directory, creates a new folder, and copies all source point clouds."""
    all_pointclouds = os.listdir(config["LiDARFaults"]["pointcloud_dir"])
    selected_pointclouds = random.sample(all_pointclouds, round(fault_data["probability"] * len(all_pointclouds)))

    if verbose:
        print(
            f"Applying {corruption} with a severity of {severity} to {round(fault_data['probability'] * len(all_pointclouds))} out of {len(all_pointclouds)} point clouds.")

    folder_corrupted_pointclouds = f"{config['LiDARFaults']['result_dir']}/{corruption}_{severity}"

    if not os.path.exists(folder_corrupted_pointclouds):
        os.makedirs(folder_corrupted_pointclouds)
        for pointcloud_name in all_pointclouds:  # Copies all point clouds
            source = f"{config['LiDARFaults']['pointcloud_dir']}/{pointcloud_name}"
            destination = f"{folder_corrupted_pointclouds}/{pointcloud_name}"
            shutil.copy(source, destination)

    return selected_pointclouds, folder_corrupted_pointclouds


def inject_lidar_faults(config, verbose):
    FaultList = get_lidar_corruptions(config)

    # Iterate through all selected corruptions
    for corruption in FaultList:
        # Loading data and specs about this specific corruption
        fault_data = config["LiDARFaults"]["Faults"][corruption]

        # In order to allow the iteration through all severities
        if config["LiDARFaults"]["all_severities"]:
            severities = [1, 2, 3, 4, 5]
        else:
            severities = [fault_data["severity"]]

        for severity in severities:
            # Adjust the fault severity level based on the current severity in iteration

            selected_pointclouds, folder_corrupted_pointclouds = define_lidar_pointclouds(config, verbose, fault_data,
                                                                                          corruption, severity)
            corrupted_filenames = []

            # Selecting point cloud and injecting the faults
            for pointcloud_name in tqdm(selected_pointclouds):
                pcd = o3d.io.read_point_cloud(f"{folder_corrupted_pointclouds}/{pointcloud_name}")

                # Inject faults based on corruption type
                if corruption == "noise":
                    corrupted_pcd = add_noise(pcd, severity)  # Apply noise with the current severity level

                elif corruption == "outliers":
                    corrupted_pcd = add_outliers(pcd, severity)  # Apply outliers with the current severity level

                elif corruption == "missing_points":
                    corrupted_pcd = remove_points(pcd, severity)
                else:
                    print(f"Unknown corruption type: {corruption}")
                    continue

                # Save the corrupted point cloud, include severity in the filename
                corrupted_filename = f"{pointcloud_name.split('.')[0]}_{corruption}_severity_{severity}.pcd"
                o3d.io.write_point_cloud(f"{folder_corrupted_pointclouds}/{corrupted_filename}", corrupted_pcd,
                                         write_ascii=True)

                # Track which point clouds were corrupted
                corrupted_filenames.append((corrupted_filename, corruption))

            # Create a text file documenting which point clouds were selected and corrupted
            with open(f"{folder_corrupted_pointclouds}/CorruptedPointClouds.txt", 'a') as file:
                for data in corrupted_filenames:
                    file.write(str(data) + '\n')
