import open3d as o3d
import numpy as np


# Function to simulate horizontal occlusion/shadowing (along the X-axis) by removing points based on severity
def horizontal_occlusion(pcd, severity=1):
    points = np.asarray(pcd.points)

    # Ensure severity is between 1 and 5
    severity = max(1, min(5, severity))

    # Define how much of the point cloud to occlude based on severity
    min_x = np.min(points[:, 0])
    max_x = np.max(points[:, 0])
    cloud_range_x = max_x - min_x

    # Occlusion width grows with severity, starting from a small stripe
    occlusion_width = severity * 0.05 * cloud_range_x  # At severity 5, up to 25% of points are removed

    # Randomly select a center for the occlusion region within the point cloud
    occlusion_center = np.random.uniform(min_x, max_x)

    # Define the range of X values to be removed based on occlusion width
    occlusion_min = occlusion_center - occlusion_width / 2
    occlusion_max = occlusion_center + occlusion_width / 2

    # Keep only the points outside the occlusion range (along the X-axis)
    remaining_points = points[(points[:, 0] < occlusion_min) | (points[:, 0] > occlusion_max)]

    # Create a new point cloud with the remaining points
    occluded_pcd = o3d.geometry.PointCloud()
    occluded_pcd.points = o3d.utility.Vector3dVector(remaining_points)

    # Copy the colors and normals if available
    if pcd.has_colors():
        colors = np.asarray(pcd.colors)[(points[:, 0] < occlusion_min) | (points[:, 0] > occlusion_max)]
        occluded_pcd.colors = o3d.utility.Vector3dVector(colors)

    if pcd.has_normals():
        normals = np.asarray(pcd.normals)[(points[:, 0] < occlusion_min) | (points[:, 0] > occlusion_max)]
        occluded_pcd.normals = o3d.utility.Vector3dVector(normals)

    return occluded_pcd

# Function to simulate vertical occlusion/shadowing (along the Y-axis) by removing points based on severity
def vertical_occlusion(pcd, severity=1):
    points = np.asarray(pcd.points)

    # Ensure severity is between 1 and 5
    severity = max(1, min(5, severity))

    # Define how much of the point cloud to occlude based on severity
    min_y = np.min(points[:, 1])
    max_y = np.max(points[:, 1])
    cloud_range_y = max_y - min_y

    # Occlusion width grows with severity, starting from a small stripe
    occlusion_width = severity * 0.05 * cloud_range_y  # At severity 5, up to 25% of points are removed

    # Randomly select a center for the occlusion region within the point cloud
    occlusion_center = np.random.uniform(min_y, max_y)

    # Define the range of Y values to be removed based on occlusion width
    occlusion_min = occlusion_center - occlusion_width / 2
    occlusion_max = occlusion_center + occlusion_width / 2

    # Keep only the points outside the occlusion range (along the Y-axis)
    remaining_points = points[(points[:, 1] < occlusion_min) | (points[:, 1] > occlusion_max)]

    # Create a new point cloud with the remaining points
    occluded_pcd = o3d.geometry.PointCloud()
    occluded_pcd.points = o3d.utility.Vector3dVector(remaining_points)

    # Copy the colors and normals if available
    if pcd.has_colors():
        colors = np.asarray(pcd.colors)[(points[:, 1] < occlusion_min) | (points[:, 1] > occlusion_max)]
        occluded_pcd.colors = o3d.utility.Vector3dVector(colors)

    if pcd.has_normals():
        normals = np.asarray(pcd.normals)[(points[:, 1] < occlusion_min) | (points[:, 1] > occlusion_max)]
        occluded_pcd.normals = o3d.utility.Vector3dVector(normals)

    return occluded_pcd