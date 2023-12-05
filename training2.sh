#!/bin/bash

# importance sampling (initial)
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=sear_steak
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=flame_salmon_1
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=flame_steak --device 1
