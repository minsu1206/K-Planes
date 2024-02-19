# K-Planes: Explicit Radiance Fields in Space, Time, and Appearance

Where we develop an extensible (to arbitrary-dimensional scenes) and explicit radiance field model which can be used for static, dynamic, and variable appearance datasets.

Code release for:

> __K-Planes: Explicit Radiance Fields in Space, Time, and Appearance__
>
> [Sara Fridovich-Keil*](https://people.eecs.berkeley.edu/~sfk/), [Giacomo Meanti*](https://www.iit.it/web/iit-mit-usa/people-details/-/people/giacomo-meanti), [Frederik Rahbæk Warburg](https://frederikwarburg.github.io/), [Benjamin Recht](https://people.eecs.berkeley.edu/~brecht/), [Angjoo Kanazawa](https://people.eecs.berkeley.edu/~kanazawa/)

:rocket: [Project page](https://sarafridov.github.io/K-Planes)

:newspaper: [Paper](https://arxiv.org/abs/2301.10241)

:file_folder: [Raw output videos and pretrained models](https://drive.google.com/drive/folders/1zs_folzaCdv88y065wc6365uSRfsqITH)

<img src="https://github.com/sarafridov/K-Planes/blob/gh-pages/assets/nerfacc.png" alt="nerfacc" width="50"/>[Integration with NerfAcc library for even faster training](https://www.nerfacc.com/en/stable/examples/dynamic/kplanes.html)

<img src="https://github.com/sarafridov/K-Planes/blob/gh-pages/assets/dozer.png" alt="nerfacc" width="50"/>[Integration with NerfStudio for easier visualization and development](https://github.com/Giodiro/kplanes_nerfstudio)


## Setup 

We recommend setup with a conda environment using PyTorch for GPU (a high-memory GPU is not required). Training and evaluation data can be downloaded from the respective websites (NeRF, LLFF, DyNeRF, D-NeRF, Phototourism). 

## Training

Our config files are provided in the `configs` directory, organized by dataset and explicit vs. hybrid model version. These config files may be updated with the location of the downloaded data and your desired scene name and experiment name. To train a model, run
```
PYTHONPATH='.' python plenoxels/main.py --config-path path/to/config.py
```

Note that for DyNeRF scenes it is recommended to first run for a single iteration at 4x downsampling to pre-compute and store the ray importance weights, and then run as usual at 2x downsampling. This is not required for other datasets.

## Visualization/Evaluation

The `main.py` script also supports rendering a novel camera trajectory, evaluating quality metrics, and rendering a space-time decomposition video from a saved model. These options are accessed via flags `--render-only`, `--validate-only`, and `--spacetime-only`, and a saved model can be specified via `--log-dir`.


## License and Citation

```
@inproceedings{kplanes_2023,
      title={K-Planes: Explicit Radiance Fields in Space, Time, and Appearance},
      author={{Sara Fridovich-Keil and Giacomo Meanti} and Frederik Rahbæk Warburg and Benjamin Recht and Angjoo Kanazawa},
      year={2023},
      booktitle={CVPR}
}
```
Note: Joint first-authorship is not fully supported in BibTex; you may need to modify the above depending on your format.

This work is made available under the BSD 3-clause license. Click [here](LICENSE) to view a copy of the license.

---

# CUSTOMIZED

### Setup 
1. `docker pull ciplab/minsu_torch:kplanes`
   
   be sure that gpu is 2080Ti / 3090 / A5000 / A6000 / A100 (Titan RTX not 
   tested for TinyCUDANN)

2. git clone repository
   `git clone https://github.com/minsu1206/K-Planes.git`


2. dataset prepare

   : `cp -r /media/NAS2/CIPLAB/nerf_team/room1_processed dataset/samsung2024`

3. overview ...

   ```
   dataset
   - room1
      - frames{downsample_factor}
         -cam00
         -cam01
         ...
         -cam15
         poses_bounds_${tag1}.npy
         intrinsic_${tag1}.npy
   - room2
      - frames{downsample_factor}
         -cam00
         -cam01
         ...
   K-planes
      plenoxels
      logs
      full_example.sh
      full1.sh
      full2.sh
      ...
   ```

### Train

See `full_example.sh.`

This includes
- train
- evaluate
- render (spiral / arc)
- visualization of spacetime

How to do ablation study ?

K-planes code support configuration overriding. <br>
Add $hyperparams=$value at last. <br>
Note that this value is basically string type.
Another notes:
1. To utilize customized poses_bounds.npy, name this file as "poses_bounds_{$tag}.npy"
   then, override pose_npy_suffix=$tag when you run training code.
   if pose_npy_suffix='', it uses "poses_bounds.npy" automatically.

2. To utilize intrinsic_pose, use_intrinsic=True
   please note that if pose_npy_suffix != '', it uses "intrinsic_{$pose_suffix_npy}.npy" for training


### Render_arc

see `render_arc.sh`

This script is the example of how to render images along arc path. <br>
Be sure that the path of trained model is correct. <br>
Checkpoint path is `os.path.join(args.log_dir, "model.pth")`

### Some utilities
1. cropping result video into 3 videos. 
   
   : python cropvideo.py $PATH or bash cropvideo.sh $PATH

2. ...