#!/bin/bash

# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=cut_roasted_beef num_steps=1 data_downsample=4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=cook_spinach num_steps=1 data_downsample=4
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=coffee_martini num_steps=1 data_downsample=4

# training
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/n3dv_hybrid.py data_downsample=4 use_intrinsic=True
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/walking_hybrid.py data_downsample=2 use_intrinsic=True
PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/taekwondo_hybrid.py data_downsample=2 use_intrinsic=True