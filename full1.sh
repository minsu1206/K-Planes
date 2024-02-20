#!/bin/bash

PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/cookspinach_hybrid.py data_downsample=4 pose_npy_suffix=colmap expname=cookspinach_rightview_colmap selection=[[0,2,6,8],[4]]
PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/cookspinach_hybrid.py data_downsample=4 pose_npy_suffix=sparf expname=cookspinach_rightview__sparf selection=[[0,2,6,8],[4]]

PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/coffeemartini_hybrid.py data_downsample=4 pose_npy_suffix=colmap expname=coffeemartini_colmap selection=[[2,3,5,6],[4]]
PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/coffeemartini_hybrid.py data_downsample=4 pose_npy_suffix=sparf expname=coffeemartini_sparf selection=[[2,3,5,6],[4]]

PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/flamesteak_hybrid.py data_downsample=4 pose_npy_suffix=colmap expname=flamesteak_colmap selection=[[1,3,7,9],[5]]
PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/flamesteak_hybrid.py data_downsample=4 pose_npy_suffix=sparf expname=flamesteak_sparf selection=[[1,3,7,9],[5]]

PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/flamesalmon_hybrid.py data_downsample=4 pose_npy_suffix=colmap expname=flamesalmon_colmap selection=[[4,5,7,8],[6]]
PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/flamesalmon_hybrid.py data_downsample=4 pose_npy_suffix=sparf expname=flamesalmon_sparf selection=[[4,5,7,8],[6]]

PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/walking_hybrid.py data_downsample=4 pose_npy_suffix=colmap expname=walking_colmap selection=[[2,5,11,14],[8]]
PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/walking_hybrid.py data_downsample=4 pose_npy_suffix=sparf expname=walking_sparf selection=[[2,5,11,14],[8]]

