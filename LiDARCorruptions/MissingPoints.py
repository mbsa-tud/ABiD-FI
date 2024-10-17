import open3d as o3d
import numpy as np

# Function to remove points from the point cloud (simulate missing points)
def remove_points(pcd, severity=1):
    # Get points as a numpy array
    points = np.asarray(pcd.points)

    # Ensure severity is between 1 and 5
    severity = max(1, min(5, severity))

    # Calculate the percentage of points to remove based on severity
    removal_percentage = severity * 0.15  # 15% for severity 1, up to 75% for severity 5
    num_points_to_remove = int(len(points) * removal_percentage)

    # Randomly select indices of points to remove
    remaining_indices = np.random.choice(len(points), len(points) - num_points_to_remove, replace=False)

    # Create a new point cloud with the remaining points
    remaining_points = points[remaining_indices]

    # Create a new point cloud with the remaining points
    reduced_pcd = o3d.geometry.PointCloud()
    reduced_pcd.points = o3d.utility.Vector3dVector(remaining_points)

    # Copy the colors and normals from the original point cloud if available, for remaining points
    if pcd.has_colors():
        colors = np.asarray(pcd.colors)[remaining_indices]
        reduced_pcd.colors = o3d.utility.Vector3dVector(colors)

    if pcd.has_normals():
        normals = np.asarray(pcd.normals)[remaining_indices]
        reduced_pcd.normals = o3d.utility.Vector3dVector(normals)

    return reduced_pcd


