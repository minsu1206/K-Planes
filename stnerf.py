import os
import open3d as o3d
import numpy as np
import torch

def campose_to_extrinsic(camposes):
    if camposes.shape[1]!=12:
        raise Exception(" wrong campose data structure!")
    
    res = np.zeros((camposes.shape[0],4,4))
    
    res[:,0,:] = camposes[:,0:4]
    res[:,1,:] = camposes[:,4:8]
    res[:,2,:] = camposes[:,8:12]
    res[:,3,3] = 1.0
    
    return res

root_path = "/workspace/lustre/datasets/nerf_team/taekwondo"
scale = 0.1

camposes = np.loadtxt(os.path.join(root_path,'pose/RT_c2w.txt'))

Ts = torch.Tensor(campose_to_extrinsic(camposes))
Ts[:, 0:3, 3] *= scale

inv_Ts = torch.inverse(Ts).unsqueeze(1)

pointcloud = o3d.io.read_point_cloud(os.path.join(root_path, 'background/0.ply'))
xyz = np.asarray(pointcloud.points)
xyz = torch.Tensor(xyz)
pointcloud = xyz * scale

vs = pointcloud.clone().unsqueeze(-1)
vs = torch.cat([vs, torch.ones(vs.size(0), 1, vs.size(2))], dim=1)

pts = torch.matmul(inv_Ts, vs)
pts_max = torch.max(pts, dim=1)[0].squeeze() #(M,4)
pts_min = torch.min(pts, dim=1)[0].squeeze() #(M,4)

pts_max = pts_max[:,2]   #(M)
pts_min = pts_min[:,2]   #(M)
near = pts_min
# self.near[self.near<(pts_max*0.1)] = pts_max[self.near<(pts_max*0.1)]*0.1
far = pts_max

print("near = ", near, "far = ", far)
print(near.min(), far.max())

