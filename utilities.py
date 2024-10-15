import open3d as o3d
import numpy as np
def compare_pointclouds():
    # Visualize the original and noisy point clouds side by side
    opcd = o3d.io.read_point_cloud("Results/CorruptedPointClouds/noise/sphere.pcd")
    cpcd = o3d.io.read_point_cloud("Results/CorruptedPointClouds/noise/sphere_corrupted.pcd")

    print("Original Point Cloud:")
    o3d.visualization.draw_geometries([opcd], window_name="Original Point Cloud", width=800, height=600)

    print("Noisy Point Cloud:")
    o3d.visualization.draw_geometries([cpcd], window_name="Noisy Point Cloud", width=800, height=600)

def create_sphere_point_cloud(radius=1.0, num_points=1000):
        # Generate points using spherical coordinates
        points = []

        for _ in range(num_points):
            # Random angles
            phi = np.random.uniform(0, np.pi)  # polar angle
            theta = np.random.uniform(0, 2 * np.pi)  # azimuthal angle

            # Convert spherical coordinates to Cartesian coordinates
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.sin(phi) * np.sin(theta)
            z = radius * np.cos(phi)

            points.append([x, y, z])

        # Convert to a numpy array
        points = np.array(points)

        # Create an Open3D PointCloud object
        sphere_pcd = o3d.geometry.PointCloud()
        sphere_pcd.points = o3d.utility.Vector3dVector(points)

        return sphere_pcd


if __name__ =="__main__":
    compare_pointclouds()