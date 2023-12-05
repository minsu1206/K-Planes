#!/bin/bash

# training
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=sear_steak
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=flame_salmon_1
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=flame_steak

# render
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=sear_steak --render-only
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=flame_salmon_1 --render-only
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=flame_steak --render-only

# validate-only
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=sear_steak --validate-only
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=flame_salmon_1 --validate-only
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=flame_steak --validate-only

# spacetime-only
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=sear_steak --spacetime-only
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=flame_salmon_1 --spacetime-only
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=flame_steak --spacetime-only


