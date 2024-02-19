#!/bin/bash

# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=cut_roasted_beef num_steps=1 data_downsample=4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=cook_spinach num_steps=1 data_downsample=4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=coffee_martini num_steps=1 data_downsample=4

# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/room4_hybrid.py data_downsample=2 pose_npy_suffix=sparf use_intrinsic=True expname=room4_colmap_nfscale0.7 selection=[[4,6,10,12],[8]] near_scaling=0.7
PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/room4_hybrid.py data_downsample=2 pose_npy_suffix=sparf use_intrinsic=True expname=room4_colmap_ndcnear0.4 selection=[[4,6,10,12],[8]] ndc_near=0.4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/room4_hybrid.py data_downsample=2 pose_npy_suffix=sparf use_intrinsic=True expname=room4_sparf_camscale0.25 selection=[[4,6,10,12],[8]]
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/room4_hybrid.py data_downsample=2 pose_npy_suffix=sparf use_intrinsic=True expname=room4_sparf_camscale0.5 selection=[[4,6,10,12],[8]]
