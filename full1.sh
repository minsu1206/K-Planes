#!/bin/bash

# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=cut_roasted_beef num_steps=1 data_downsample=4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=cook_spinach num_steps=1 data_downsample=4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=coffee_martini num_steps=1 data_downsample=4

PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/room1_hybrid.py data_downsample=2 pose_npy_suffix=sparf use_intrinsic=True expname=room1_sparf_ndcnear0.4far4.0 selection=[[1,3,7,9],[5]] ndc_near=0.4 ndc_far=4.0
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/room2_hybrid.py data_downsample=2 pose_npy_suffix=sparf use_intrinsic=True expname=room2_sparf_ndcnear0.4 selection=[[0,1,3,4],[2]] ndc_near=0.4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/room2_hybrid.py data_downsample=2 pose_npy_suffix=sparf use_intrinsic=True expname=room2_sparf_bboxmult1.2 selection=[[0,1,3,4],[2]] ndc_near=0.4 bbox_mult=[1.2,1.2,1.2]
