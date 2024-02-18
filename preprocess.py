import os
import glob
import cv2
import numpy as np
"""
root = 'coffee_martini'
root
- cam00.mp4
- cam01.mp4
- ...
- cam20.mp4

I want to extract frames from each video and save them as png following the structure like
cam00 
- images
  - 0000.png
  - 0001.png
  - 0002.png
  - ...
cam01
- images
  - 0000.png
  - 0001.png
  - ...

Give me the python code!
"""

import os
import cv2
import numpy as np

DOWNSAMPLES = 2

def extract_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    count = 0

    while success:
        ext = '.png' if "00" in output_folder else '.jpg'
        frame_path = os.path.join(output_folder, f'{count:04d}{ext}')
        if DOWNSAMPLES != 1:
            frame = cv2.resize(frame, dsize=None, fx=1/DOWNSAMPLES, fy=1/DOWNSAMPLES)
        cv2.imwrite(frame_path, frame)
        count += 1
        success, frame = cap.read()
    print(f"[INFO] : {video_path} > extract frames Done!")
    cap.release()

def process_videos(root_folder):
    """
    example folder hierarchy
    cut_roasted_beef
    - videos (downloaded)
        - cam00.mp4
        - cam01.mp4
        ...
    - frames{downsample_factor} (output)
        - cam00/images
            - 0000.png
            - 0001.png
            ...
        - cam11/images
            - 0000.jpg
            - 0001.jpg
            ...
    """
    video_paths = glob.glob(os.path.join(root_folder, 'videos', '*.mp4'))

    for video_path in video_paths:
        video_name = os.path.basename(video_path).split('.mp4')[0]
        output_folder = os.path.join(root_folder, f'frames{DOWNSAMPLES}', video_name, 'images')

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        extract_frames(video_path, output_folder)

def process_frames(root_folder):
    """
    example folder hierarchy
    taekwondo
    - frames (given)
        - 0
            - 0.png
            - 1.png
            ...
        - 1
            - 0.png
            - 1.png
            ...
        ...
    - frames{downsample_factor} (output)
        - cam00/images
            - 0000.png
            - 0001.png
            ...
        - cam11/images
            - 0000.jpg
            - 0001.jpg
            ...
    """
    image_dir_paths = glob.glob(root_folder + '/frames/*')
    for idx, image_dir in enumerate(sorted(image_dir_paths)):
        new_img_dir = image_dir.replace("frames", f"frames{DOWNSAMPLES}")
        new_img_dir = "/".join(new_img_dir.split('/')[:-1]) + '/' + os.path.basename(image_dir).zfill(3)
        os.makedirs(new_img_dir, exist_ok=True)
        imgs = sorted(glob.glob(image_dir + '/*'))
        for img_path in imgs:
            frame = cv2.imread(img_path)
            if DOWNSAMPLES != 1:
                frame = cv2.resize(frame, dsize=None, fx=1/DOWNSAMPLES, fy=1/DOWNSAMPLES)
            ext = '.png' if idx == 0 else '.jpg'
            new_basename = f"{os.path.basename(img_path).split('.')[0].zfill(3)}{ext}"
            new_img_path = os.path.join(new_img_dir, new_basename)
            cv2.imwrite(new_img_path, frame)
        print(f"[INFO] {image_dir} > {new_img_dir} Done!")

def process_frames2(root_folder):
    """
    example folder hierarchy
    taekwondo
    - frames (given)
        - cam00/images
            - 0.png
            - 1.png
            ...
        - cam11/images
            - 0.png
            - 1.png
            ...
        ...
    - frames{downsample_factor} (output)
        - cam00/images
            - 0000.png
            - 0001.png
            ...
        - cam11/images
            - 0000.jpg
            - 0001.jpg
            ...
    """
    image_dir_paths = glob.glob(root_folder + '/frames/*')
    for idx, image_dir in enumerate(sorted(image_dir_paths)):
        new_img_dir = image_dir.replace("frames", f"frames{DOWNSAMPLES}")
        new_img_dir = "/".join(new_img_dir.split('/')[:-1]) + '/' + os.path.basename(image_dir).zfill(3)
        os.makedirs(new_img_dir, exist_ok=True)
        imgs = sorted(glob.glob(image_dir + '/images/*'))
        for img_path in imgs:
            frame = cv2.imread(img_path)
            if DOWNSAMPLES != 1:
                frame = cv2.resize(frame, dsize=None, fx=1/DOWNSAMPLES, fy=1/DOWNSAMPLES)
            ext = '.png' if idx == 0 else '.jpg'
            new_basename = f"{os.path.basename(img_path).split('.')[0].zfill(3)}{ext}"
            new_img_path = os.path.join(new_img_dir, new_basename)
            cv2.imwrite(new_img_path, frame)
        print(f"[INFO] {image_dir} > {new_img_dir} Done!")

if __name__ == "__main__":

    # n3dv_root = 'N3DV'
    # for vidoe_name in ['cook_spinach', 'cut_roasted_beef', 'flame_steak', 'flame_salmon_1', 'sear_steak']:
    #     process_videos(os.path.join(n3dv_root, video_name))
    #     print("Done : ", video_name)

    # stnerf_root = '/workspace/dataset/samsung2024'
    # for video_name in ['walking', 'taekwondo']:
    #     process_frames(os.path.join(stnerf_root, video_name))
    #     print("Done : ",video_name)

    root = '/workspace/dataset/samsung2024'
    for video_name in ['room1', 'room2', 'room3', 'room4']:
        process_frames2(os.path.join(root, video_name))
        print("Done : ", video_name)