import open3d as o3d
import numpy as np
def compare_pointclouds():
    # Visualize the original and noisy point clouds side by side
    opcd = o3d.io.read_point_cloud("Results/CorruptedPointClouds/missing_points_1/sphere_missing_points_severity_1.pcd")
    cpcd = o3d.io.read_point_cloud("Results/CorruptedPointClouds/missing_points_5/sphere_missing_points_severity_5.pcd")

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

def save_image_of_pointcloud(pcd, filename="Results/point_cloud_image.png"):
        vis = o3d.visualization.Visualizer()
        vis.create_window(visible=False)  # Create a window without displaying it

        # Add the point cloud to the visualizer
        vis.add_geometry(pcd)

        # Set a view control to zoom in/out, rotate, etc. (optional, for a better angle)
        view_control = vis.get_view_control()
        view_control.set_front([0.0, 0.0, -1.0])  # Adjust camera view (optional)
        view_control.set_lookat([0.0, 0.0, 0.0])
        view_control.set_up([0.0, -1.0, 0.0])
        view_control.set_zoom(0.8)  # Zoom in/out

        # Capture the screen as an image
        vis.poll_events()  # Process visualization events
        vis.update_renderer()  # Update the renderer to display the current view

        # Save the screenshot to a file
        vis.capture_screen_image(filename)

        # Close the visualizer
        vis.destroy_window()

        print(f"Point cloud image saved as {filename}")



if __name__ =="__main__":
    #compare_pointclouds()

    pcd = o3d.io.read_point_cloud("Results/CorruptedPointClouds/missing_points_5/sphere_missing_points_severity_5.pcd")
    save_image_of_pointcloud(pcd, "Results/Images/Missing5.png")