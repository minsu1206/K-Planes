#!/bin/bash

# training
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=sear_steak
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=flame_salmon_1
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py expname=flame_steak

# render
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py --render-only expname=sear_steak log-dir=logs/baseline/sear_steak
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py --render-only expname=flame_salmon_1 log-dir=logs/baseline/flame_salmon_1
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py --render-only expname=flame_steak log-dir=logs/baseline/flame_steak

# validate-only
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py --validate-only expname=sear_steak log-dir=logs/baseline/sear_steak
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py --validate-only expname=flame_salmon_1 log-dir=logs/baseline/flame_salmon_1
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py --validate-only expname=flame_steak log-dir=logs/baseline/flame_steak

# spacetime-only
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py --spacetime-only expname=sear_steak log-dir=logs/baseline/sear_steak
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py --spacetime-only expname=flame_salmon_1 log-dir=logs/baseline/flame_salmon_1
PYTHONPATH='.' python plenoxels/main.py --device 1 --config-path plenoxels/configs/final/DyNeRF/dynerf_hybrid.py --spacetime-only expname=flame_steak log-dir=logs/baseline/flame_steak
