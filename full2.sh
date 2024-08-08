#!/bin/bash

# training
# CUDA_VISIBLE_DEVICES=1 PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/synthetic_hybrid.py data_downsample=2 pose_npy_suffix=made use_intrinsic=True expname=robot_synthetic_ndc_made
# CUDA_VISIBLE_DEVICES=1 PYTHONPATH='.' python plenoxels/main.py --device 0 --config-path plenoxels/configs/final/samsung2024/synthetic_hybrid2.py data_downsample=2 pose_npy_suffix=made use_intrinsic=True expname=robot_synthetic_contract_made

# sparse
# bash full_example2.sh cook_spinach
# bash full_example2.sh flame_steak
# bash full_example2.sh sear_steak

bash full_example_beef.sh cut_roasted_beef
bash full_example_coffee_salmon.sh coffee_martini
bash full_example_coffee_salmon.sh flame_salmon_1
