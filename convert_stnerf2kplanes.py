"""
Codes for converting ST-NeRF data structure into K-Planes
"""
import os
import cv2
import glob
import numpy as np

downsample = 4

root = "/workspace/lustre/datasets/nerf_team/walking"

frames = glob.glob(f"{root}/frame1/images/*.png")

for frame_path in frames:

    cam_idx = int(os.path.basename(frame_path).replace(".png", ""))

    # print(cam_idx)
    os.makedirs(f"{root}/images_{downsample}/cam{cam_idx:02d}", exist_ok=True)

    # os.subprocess(f"cp {}")

timestamps = sorted(glob.glob(f"{root}/frame*"))

for time in timestamps:
    
    frames = glob.glob(f"{time}/images/*.png")

    time_stamp = int(os.path.basename(time).replace("frame", ""))

    print(time_stamp, time)

    for frame_path in frames:

        cam_idx = int(os.path.basename(frame_path).replace(".png", ""))

        img = cv2.imread(frame_path)

        img_resized = cv2.resize(img, dsize=(0,0), fx=1/downsample, fy=1/downsample)

        save_path = f"{root}/images_{downsample}/cam{cam_idx:02d}/{time_stamp:04d}.png"
        print(f"[INFO] : {frame_path} ; {img.shape} > {save_path} ; {img_resized.shape}")
        cv2.imwrite(save_path, img_resized)




