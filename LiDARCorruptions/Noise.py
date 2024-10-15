import open3d as o3d
import numpy as np


# Function to add noise to the point cloud
def add_noise(pcd, noise_level=1):
    # Get points as a numpy array
    points = np.asarray(pcd.points)

    noise_level=noise_level/100
    # Generate random noise
    noise = np.random.normal(0, noise_level, points.shape)

    # Add noise to the points
    noisy_points = points + noise

    # Create a new point cloud with noisy points
    noisy_pcd = o3d.geometry.PointCloud()
    noisy_pcd.points = o3d.utility.Vector3dVector(noisy_points)

    # Copy the colors from the original point cloud if available
    if pcd.has_colors():
        noisy_pcd.colors = pcd.colors
    if pcd.has_normals():
        noisy_pcd.normals = pcd.normals

    return noisy_pcd