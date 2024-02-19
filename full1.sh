#!/bin/bash

# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=cut_roasted_beef num_steps=1 data_downsample=4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=cook_spinach num_steps=1 data_downsample=4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=coffee_martini num_steps=1 data_downsample=4

# for weights
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/room1_hybrid.py data_downsample=2 pose_npy_suffix=sparf use_intrinsic=True expname=room1_sparf_camscale0.25 selection=[[1,3,7,9],[5]] cam_scale=0.25
PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/room1_hybrid.py data_downsample=2 pose_npy_suffix=sparf use_intrinsic=True expname=room1_sparf_camscale0.5 selection=[[1,3,7,9],[5]] cam_scale=0.5
PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/room1_hybrid.py data_downsample=2 pose_npy_suffix=sparf use_intrinsic=True expname=room1_sparf_camscale0.75 selection=[[1,3,7,9],[5]] cam_scale=0.75

# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/room2_hybrid.py data_downsample=2 pose_npy_suffix=colmap use_intrinsic=True expname=room2_colmap selection=[[0,1,3,4],[2]]
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/room2_hybrid.py data_downsample=2 pose_npy_suffix=sparf use_intrinsic=True expname=room2_colmap selection=[[0,1,3,4],[2]]
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/room2_hybrid.py data_downsample=2 pose_npy_suffix=gt use_intrinsic=True expname=room2_colmap selection=[[0,1,3,4],[2]]
