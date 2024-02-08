#!/bin/bash

# training
PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/n3dv_hybrid.py data_downsample=4 pose_npy_suffix=align_k expname=cut_roasted_beef_align_k
PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/n3dv_hybrid.py data_downsample=4 pose_npy_suffix=align expname=cut_roasted_beef_align