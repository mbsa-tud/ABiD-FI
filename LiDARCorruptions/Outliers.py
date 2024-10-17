import open3d as o3d
import numpy as np

# Function to induce outliers into the point cloud
def add_outliers(pcd, severity=1):
    # Ensure severity is in the range [1, 5]
    severity = max(1, min(5, severity))

    # Get points as a numpy array
    points = np.asarray(pcd.points)
    num_points = len(points)

    # Define the proportion of points to turn into outliers based on severity
    proportion_of_outliers = severity * 0.05  # Severity 1: 5% outliers, Severity 5: 25% outliers
    num_outliers = int(proportion_of_outliers * num_points)

    # Select random indices of points to become outliers
    outlier_indices = np.random.choice(num_points, num_outliers, replace=False)

    # Create a new point cloud to store outlier-modified points
    modified_points = points.copy()

    # Introduce outliers by adding random offsets to the selected points
    # The magnitude of deviation is larger with higher severity
    outlier_deviation = severity * 0.01  # Severity 1: small deviation, Severity 5: large deviation
    random_offsets = np.random.uniform(-outlier_deviation, outlier_deviation, (num_outliers, 3))

    # Apply the offsets to the selected points
    modified_points[outlier_indices] += random_offsets * 10  # Increase deviation scale

    # Create a new point cloud with modified points (including outliers)
    outlier_pcd = o3d.geometry.PointCloud()
    outlier_pcd.points = o3d.utility.Vector3dVector(modified_points)

    # Copy the colors from the original point cloud if available
    if pcd.has_colors():
        outlier_pcd.colors = pcd.colors
    if pcd.has_normals():
        outlier_pcd.normals = pcd.normals

    return outlier_pcd