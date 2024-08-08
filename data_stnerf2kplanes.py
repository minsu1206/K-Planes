import cv2
import os
import glob
from tqdm import tqdm
root = "/workspace/lustre/datasets/nerf_team/taekwondo"

downsample = 4

os.makedirs(f"{root}/images_{downsample}", exist_ok=True)

time_dirs = glob.glob(f"{root}/frame*")

for i, time_dir in tqdm(enumerate(time_dirs)):

    frame_paths = glob.glob(f"{time_dir}/images/*.png")

    for frame_path in frame_paths:

        cam_idx = int(os.path.basename(frame_path).replace(".png", ""))

        os.makedirs(f"{root}/images_{downsample}/cam{cam_idx:02d}", exist_ok=True)

        img = cv2.imread(frame_path)

        img_resized = cv2.resize(img, dsize=(0,0), fx=1/downsample, fy=1/downsample)

        cv2.imwrite(f"{root}/images_{downsample}/cam{cam_idx:02d}/{i:04d}.png", img_resized)

print("DONE !")