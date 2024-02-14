#!/bin/bash

# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=cut_roasted_beef num_steps=1 data_downsample=4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=cook_spinach num_steps=1 data_downsample=4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=coffee_martini num_steps=1 data_downsample=4

# for weights
CUDA_VISIBLE_DEVICES=2 PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/synthetic_hybrid.py data_downsample=2 pose_npy_suffix=colmap use_intrinsic=True expname=robot_synthetic_ndc_colmappose num_steps=1

# training
CUDA_VISIBLE_DEVICES=2 PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/synthetic_hybrid.py data_downsample=2 pose_npy_suffix=colmap use_intrinsic=True expname=robot_synthetic_ndc_colmappose
CUDA_VISIBLE_DEVICES=2 PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/synthetic_hybrid2.py data_downsample=2 pose_npy_suffix=colmap use_intrinsic=True expname=robot_synthetic_contract_colmappose
CUDA_VISIBLE_DEVICES=2 PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/synthetic_hybrid.py data_downsample=2 pose_npy_suffix=made use_intrinsic=True expname=robot_synthetic_ndc_made
CUDA_VISIBLE_DEVICES=2 PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/synthetic_hybrid2.py data_downsample=2 pose_npy_suffix=made use_intrinsic=True expname=robot_synthetic_contract_made