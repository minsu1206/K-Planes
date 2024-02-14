#!/bin/bash

# training
CUDA_VISIBLE_DEVICES=1 PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/synthetic_hybrid.py data_downsample=2 pose_npy_suffix=made use_intrinsic=True expname=robot_synthetic_ndc_made
CUDA_VISIBLE_DEVICES=1 PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/synthetic_hybrid2.py data_downsample=2 pose_npy_suffix=made use_intrinsic=True expname=robot_synthetic_contract_made