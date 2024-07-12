#!/bin/bash

config_root=plenoxels/configs/final
config_py_path=DyNeRF/dynerf_hybrid.py
config_path=${config_root}/${config_py_path}
expname=$1
# NOTE
# get isg / ist weight
# can skip this line when video resolution is smaller than half-size of N3DV resolution\
PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path ${config_path} expname=$expname num_steps=1 data_downsample=4

# # train
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path ${config_path} expname=$expname data_downsample=2
# # train with another hyperparams (example)
# # training with poses_bounds_sparf.npy / near=0.4 / far=2.6 / expand bbox by multiplying 1.2 into x,y,z axis
# # PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path ${config_path} expname=$expname num_steps=1 data_downsample=2 pose_npy_suffix=sparf ndc_near=0.4 ndc_far=4.0 bbox_mult=[1.2,1.2,1.2]

# # eval
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path ${config_path} --validate-only --log-dir logs/baseline/$expname expname=$expname num_steps=1 data_downsample=2
# # spiral path render
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path ${config_path} --render-only --log-dir logs/baseline/$expname expname=$expname num_steps=1 data_downsample=2
# # arc path render
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path ${config_path} --render-only-arc --log-dir logs/baseline/$expname expname=$expname num_steps=1 data_downsample=2
# # visualize spacetime planes
# PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path ${config_path} --spacetime-only --log-dir logs/baseline/$expname expname=$expname num_steps=1 data_downsample=2