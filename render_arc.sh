#!/bin/bash
CUDA_VISIBLE_DEVICES=3 PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/n3dv_hybrid.py --render-only-arc --log-dir logs/use_align_nouse_k/cut_roasted_beef_align_bd data_downsample=4 logdir=logs/use_align_nouse_k pose_npy_suffix=align_bd use_intrinsic=True expname=cut_roasted_beef_align_bd
