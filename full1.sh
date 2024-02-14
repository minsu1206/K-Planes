#!/bin/bash

# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=cut_roasted_beef num_steps=1 data_downsample=4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=cook_spinach num_steps=1 data_downsample=4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=coffee_martini num_steps=1 data_downsample=4

# training
CUDA_VISIBLE_DEVICES=2 PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/n3dv_hybrid.py data_downsample=4 pose_npy_suffix=align_bd_k use_intrinsic=True expname=cut_roasted_beef_align_bd_k
CUDA_VISIBLE_DEVICES=2 PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/n3dv_hybrid.py data_downsample=4 pose_npy_suffix=align_bd use_intrinsic=True expname=cut_roasted_beef_align_bd
