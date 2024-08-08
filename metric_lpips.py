import os
from PIL import Image
import torch
import lpips
import glob
import numpy as np
from tqdm import tqdm
loss_fn_vgg = lpips.LPIPS(net='vgg').cuda()

scene = "sear_steak"
gt_dir = f"/workspace/lustre/datasets/nerf_team/n3dv/{scene}/frames2/cam00/images"
gt_images = sorted(glob.glob(gt_dir + '/*.png'))

pred_dir = f"/workspace/K-Planes/logs/sparse4/{scene}/step90k_pred"
pred_images = sorted(glob.glob(pred_dir + '/*.png'))

print("[DEBUG] : len(gt_images) = ", len(gt_images))
print("[DEBUG] : len(pred_images) = ", len(pred_images))

lpipss = []
for gt_image_path, pred_image_path in tqdm(zip(gt_images, pred_images)):
    # 1. READ image , using Image
    gt_image = Image.open(gt_image_path).convert('RGB')
    pred_image = Image.open(pred_image_path).convert('RGB')

    # 2. CONVERT image into image tensor. normalized into [-1, 1]
    #   image tensor shape should be [1, 3, H, W]
    # 3. Apply 1 & 2 into gt_image and pred_image
    gt_image_tensor = (torch.tensor(np.array(gt_image)).permute(2, 0, 1).unsqueeze(0).float() / 127.5) - 1
    pred_image_tensor = (torch.tensor(np.array(pred_image)).permute(2, 0, 1).unsqueeze(0).float() / 127.5) - 1

    lpips_ = loss_fn_vgg(gt_image_tensor.cuda(), pred_image_tensor.cuda())
    lpipss.append(lpips_.mean().item())
    # print(lpipss[-1])
    # break

print(f"[INFO] : scene = {scene} / AVG of LPIPS = {(sum(lpipss) / len(lpipss)):.4f}")

