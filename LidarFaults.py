import open3d as o3d

# Load the PCD file
pcd = o3d.io.read_point_cloud("your_pointcloud.pcd")

# Print some basic information about the point cloud
print(pcd)
print("Number of points:", len(pcd.points))

# Visualize the point cloud
o3d.visualization.draw_geometries([pcd], window_name="PCD Point Cloud", width=800, height=600)