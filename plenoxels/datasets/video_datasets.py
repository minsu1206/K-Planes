import glob
import json
import logging as log
import math
import os
import time
from collections import defaultdict
from typing import Optional, List, Tuple, Any, Dict

import numpy as np
import torch

from .base_dataset import BaseDataset
from .data_loading import parallel_load_images
from .intrinsics import Intrinsics
from .llff_dataset import load_llff_poses_helper
from .ray_utils import (
    generate_spherical_poses, create_meshgrid, stack_camera_dirs, get_rays, generate_spiral_path, generate_arc_orbit
)
from .synthetic_nerf_dataset import (
    load_360_images, load_360_intrinsics,
)
import ast

class Video360Dataset(BaseDataset):
    len_time: int
    max_cameras: Optional[int]
    max_tsteps: Optional[int]
    timestamps: Optional[torch.Tensor]

    def __init__(self,
                 datadir: str,
                 split: str,
                 batch_size: Optional[int] = None,
                 downsample: float = 1.0,
                 keyframes: bool = False,
                 max_cameras: Optional[int] = None,
                 max_tsteps: Optional[int] = None,
                 isg: bool = False,
                 contraction: bool = False,
                 ndc: bool = False,
                 scene_bbox: Optional[List] = None,
                 near_scaling: float = 0.9,
                 ndc_far: float = 2.6,
                 ndc_near: float = 1.0, 
                 use_intrinsic: bool = False,
                 pose_npy_suffix: str = '',
                 selection:list=None,
                 pose_selection:list=None,
                 cam_scale:float=None,
                 bbox_mult:list=None
                 ):
        self.keyframes = keyframes
        self.max_cameras = max_cameras
        self.max_tsteps = max_tsteps
        self.downsample = downsample
        self.isg = isg
        self.ist = False
        print("[DEBUG] : ? : self.isg = ", self.isg, "self.ist = ", self.ist)

        # self.lookup_time = False
        self.per_cam_near_fars = None
        self.global_translation = torch.tensor([0, 0, 0])
        self.global_scale = torch.tensor([1, 1, 1])
        self.near_scaling = near_scaling
        self.ndc_far = ndc_far
        self.ndc_near = ndc_near
        self.median_imgs = None
        if contraction and ndc:
            raise ValueError("Options 'contraction' and 'ndc' are exclusive.")
        if "lego" in datadir or "dnerf" in datadir:
            dset_type = "synthetic"
        else:
            dset_type = "llff"

        if isinstance(selection, str):
            selection = ast.literal_eval(selection)
        if isinstance(pose_selection, str):
            pose_selection = ast.literal_eval(pose_selection)
        if isinstance(cam_scale, str):
            cam_scale = float(cam_scale)
        if isinstance(bbox_mult, str):
            bbox_mult = ast.literal_eval(bbox_mult)
            bbox_mult = np.array(bbox_mult)
            
        # Note: timestamps are stored normalized between -1, 1.
        if dset_type == "llff":
            if split == "render" or split == "render_arc":
                assert ndc, "Unable to generate render poses without ndc: don't know near-far."
                per_cam_poses, per_cam_near_fars, intrinsics, _ = load_llffvideo_poses(
                    datadir, downsample=self.downsample, split='all', near_scaling=self.near_scaling,
                    pose_npy_suffix=pose_npy_suffix, selection=selection, pose_selection=pose_selection, cam_scale=cam_scale)
                if "arc" in split:
                    print("[INFO] : video_datasets.py / Video360Dataset : load arc-shaped camera path")
                    render_poses = generate_arc_orbit(
                        per_cam_poses.numpy(), per_cam_near_fars.numpy(), n_frames=300,
                        n_cycle=4, dt=self.near_scaling, percentile=60)
                else:
                    render_poses = generate_spiral_path(
                        per_cam_poses.numpy(), per_cam_near_fars.numpy(), n_frames=300,
                        n_rots=2, zrate=0.5, dt=self.near_scaling, percentile=60)
                self.poses = torch.from_numpy(render_poses).float()
                self.per_cam_near_fars = torch.tensor([[0.4, self.ndc_far]])
                timestamps = torch.linspace(0, 299, len(self.poses))
                imgs = None
            else:
                per_cam_poses, per_cam_near_fars, intrinsics, videopaths = load_llffvideo_poses(
                    datadir, downsample=self.downsample, split=split, near_scaling=self.near_scaling,
                    pose_npy_suffix=pose_npy_suffix, selection=selection, pose_selection=pose_selection, cam_scale=cam_scale)
                if split == 'test':
                    keyframes = False
                poses, imgs, timestamps, self.median_imgs = load_llffvideo_data(
                    videopaths=videopaths, cam_poses=per_cam_poses, intrinsics=intrinsics,
                    split=split, keyframes=keyframes, keyframes_take_each=30)
                self.poses = poses.float()
                if contraction:
                    self.per_cam_near_fars = per_cam_near_fars.float()
                else:
                    self.per_cam_near_fars = torch.tensor(
                        [[self.ndc_near, self.ndc_far]]).repeat(per_cam_near_fars.shape[0], 1)
            # These values are tuned for the salmon video
            self.global_translation = torch.tensor([0, 0, 2.])
            self.global_scale = torch.tensor([0.5, 0.6, 1])
            # Normalize timestamps between -1, 1
            timestamps = (timestamps.float() / 299) * 2 - 1
        elif dset_type == "synthetic":
            assert not contraction, "Synthetic video dataset does not work with contraction."
            assert not ndc, "Synthetic video dataset does not work with NDC."
            if split == 'render':
                num_tsteps = 120
                dnerf_durations = {'hellwarrior': 100, 'mutant': 150, 'hook': 100, 'bouncingballs': 150, 'lego': 50, 'trex': 200, 'standup': 150, 'jumpingjacks': 200}
                for scene in dnerf_durations.keys():
                    if 'dnerf' in datadir and scene in datadir:
                        num_tsteps = dnerf_durations[scene]
                render_poses = torch.stack([
                    generate_spherical_poses(angle, -30.0, 4.0)
                    for angle in np.linspace(-180, 180, num_tsteps + 1)[:-1]
                ], 0)
                imgs = None
                self.poses = render_poses
                timestamps = torch.linspace(0.0, 1.0, render_poses.shape[0])
                _, transform = load_360video_frames(
                    datadir, 'train', max_cameras=self.max_cameras, max_tsteps=self.max_tsteps)
                img_h, img_w = 800, 800
            else:
                frames, transform = load_360video_frames(
                    datadir, split, max_cameras=self.max_cameras, max_tsteps=self.max_tsteps)
                imgs, self.poses = load_360_images(frames, datadir, split, self.downsample)
                timestamps = torch.tensor(
                    [fetch_360vid_info(f)[0] for f in frames], dtype=torch.float32)
                img_h, img_w = imgs[0].shape[:2]
            if ndc:
                self.per_cam_near_fars = torch.tensor([[0.0, self.ndc_far]])
            else:
                self.per_cam_near_fars = torch.tensor([[2.0, 6.0]])
            if "dnerf" in datadir:
                # dnerf time is between 0, 1. Normalize to -1, 1
                timestamps = timestamps * 2 - 1
            else:
                # lego (our vid) time is like dynerf: between 0, 30.
                timestamps = (timestamps.float() / torch.amax(timestamps)) * 2 - 1
            intrinsics = load_360_intrinsics(
                transform, img_h=img_h, img_w=img_w, downsample=self.downsample)
        else:
            raise ValueError(datadir)

        self.timestamps = timestamps
        if split == 'train':
            self.timestamps = self.timestamps[:, None, None].repeat(
                1, intrinsics.height, intrinsics.width).reshape(-1)  # [n_frames * h * w]
        assert self.timestamps.min() >= -1.0 and self.timestamps.max() <= 1.0, "timestamps out of range."
        # print("[DEBUG] : intermediate imgs = ", imgs.shape)

        if imgs is not None and imgs.dtype != torch.uint8:
            imgs = (imgs * 255).to(torch.uint8)
        if self.median_imgs is not None and self.median_imgs.dtype != torch.uint8:
            self.median_imgs = (self.median_imgs * 255).to(torch.uint8)
        if split == 'train':
            imgs = imgs.view(-1, imgs.shape[-1])
        elif imgs is not None:
            imgs = imgs.view(-1, intrinsics.height * intrinsics.width, imgs.shape[-1])

        # ISG/IST weights are computed on 4x subsampled data.
        weights_subsampled = int(4 / downsample)
        if scene_bbox is not None:
            scene_bbox = torch.tensor(scene_bbox)
        else:
            scene_bbox = get_bbox(datadir, is_contracted=contraction, dset_type=dset_type)
        
        if bbox_mult is not None:
            scene_bbox *= torch.from_numpy(bbox_mult)
            
        super().__init__(
            datadir=datadir,
            split=split,
            batch_size=batch_size,
            is_ndc=ndc,
            is_contracted=contraction,
            scene_bbox=scene_bbox,
            rays_o=None,
            rays_d=None,
            intrinsics=intrinsics,
            imgs=imgs,
            sampling_weights=None,  # Start without importance sampling, by default
            weights_subsampled=weights_subsampled,
        )

        self.isg_weights = None
        self.ist_weights = None
        if split == "train" and dset_type == 'llff':  # Only use importance sampling with DyNeRF videos
            isg_weight_name = f"isg_weights_{selection}.pt" if selection is not None else "isg_weights.pt"
            if os.path.exists(os.path.join(datadir, isg_weight_name)):
                self.isg_weights = torch.load(os.path.join(datadir, isg_weight_name))
                log.info(f"Reloaded {self.isg_weights.shape[0]} ISG weights from file.")
            else:
                # Precompute ISG weights
                t_s = time.time()
                gamma = 1e-3 if self.keyframes else 2e-2
                self.isg_weights = dynerf_isg_weight(
                    imgs.view(-1, intrinsics.height, intrinsics.width, imgs.shape[-1]),
                    median_imgs=self.median_imgs, gamma=gamma)
                # Normalize into a probability distribution, to speed up sampling
                self.isg_weights = (self.isg_weights.reshape(-1) / torch.sum(self.isg_weights))
                torch.save(self.isg_weights, os.path.join(datadir, isg_weight_name))
                t_e = time.time()
                log.info(f"Computed {self.isg_weights.shape[0]} ISG weights in {t_e - t_s:.2f}s.")

            ist_weight_name = f"ist_weights_{selection}.pt" if selection is not None else "ist_weights.pt"
            if os.path.exists(os.path.join(datadir, ist_weight_name)):
                self.ist_weights = torch.load(os.path.join(datadir, ist_weight_name))
                log.info(f"Reloaded {self.ist_weights.shape[0]} IST weights from file.")
            else:
                # Precompute IST weights
                t_s = time.time()
                self.ist_weights = dynerf_ist_weight(
                    imgs.view(-1, self.img_h, self.img_w, imgs.shape[-1]),
                    num_cameras=self.median_imgs.shape[0])
                # Normalize into a probability distribution, to speed up sampling
                self.ist_weights = (self.ist_weights.reshape(-1) / torch.sum(self.ist_weights))
                torch.save(self.ist_weights, os.path.join(datadir, ist_weight_name))
                t_e = time.time()
                log.info(f"Computed {self.ist_weights.shape[0]} IST weights in {t_e - t_s:.2f}s.")

        if self.isg:
            self.enable_isg()

        self.use_intrinsic = use_intrinsic
        if self.use_intrinsic:
            suffix = '_' + pose_npy_suffix if pose_npy_suffix != '' else ''
            intrinsic_npy = np.load(os.path.join(datadir, f'intrinsic{suffix}.npy'))
            print(f"[INFO] : load camera extra intrinsics from {os.path.join(datadir, f'intrinsic{suffix}.npy')}")
            self.extra_intrinsic = []
            for intrinsic_mat in intrinsic_npy:
                intrinsic_mat3x3 = intrinsic_mat.reshape(3,3)
                intrinsic_mat3x3 /= self.downsample
                intrinsic_mat3x3 = np.float32(intrinsic_mat3x3)
                fx = intrinsic_mat3x3[0,0]
                fy = intrinsic_mat3x3[1,1]
                cx = intrinsic_mat3x3[0,2]
                cy = intrinsic_mat3x3[1,2]
                print(f"[INFO] : extra_intrinsic w/ downsample effect : ", [fx, fy, cx, cy])
                self.extra_intrinsic.append(torch.tensor([fx,fy,cx,cy]))
            self.extra_intrinsic = torch.stack(self.extra_intrinsic)
            print(f"[INFO] : check camera extra intrinsics : ", self.extra_intrinsic, self.extra_intrinsic.dtype)
            # print(self.extra_intrinsic)       # [num of cam, 4]

        else: 
            self.extra_intrinsic = None
        
        log.info(f"VideoDataset contracted={self.is_contracted}, ndc={self.is_ndc}. "
                 f"Loaded {self.split} set from {self.datadir}: "
                 f"{len(self.poses)} images of size {self.img_h}x{self.img_w}. "
                 f"Images loaded: {self.imgs is not None}. "
                 f"{len(torch.unique(timestamps))} timestamps. Near-far: {self.per_cam_near_fars}. "
                 f"ISG={self.isg}, IST={self.ist}, weights_subsampled={self.weights_subsampled}. "
                 f"Sampling without replacement={self.use_permutation}. {intrinsics}")

    def enable_isg(self):
        self.isg = True
        self.ist = False
        self.sampling_weights = self.isg_weights
        log.info(f"Enabled ISG weights.")

    def switch_isg2ist(self):
        self.isg = False
        self.ist = True
        self.sampling_weights = self.ist_weights
        log.info(f"Switched from ISG to IST weights.")

    def __getitem__(self, index):
        h = self.intrinsics.height
        w = self.intrinsics.width
        dev = "cpu"
        if self.split == 'train':
            index = self.get_rand_ids(index)  # [batch_size // (weights_subsampled**2)]
            if self.weights_subsampled == 1 or self.sampling_weights is None:
                # Nothing special to do, either weights_subsampled = 1, or not using weights.
                image_id = torch.div(index, h * w, rounding_mode='floor')
                y = torch.remainder(index, h * w).div(w, rounding_mode='floor')
                x = torch.remainder(index, h * w).remainder(w)
            else:
                # We must deal with the fact that ISG/IST weights are computed on a dataset with
                # different 'downsampling' factor. E.g. if the weights were computed on 4x
                # downsampled data and the current dataset is 2x downsampled, `weights_subsampled`
                # will be 4 / 2 = 2.
                # Split each subsampled index into its 16 components in 2D.
                hsub, wsub = h // self.weights_subsampled, w // self.weights_subsampled
                image_id = torch.div(index, hsub * wsub, rounding_mode='floor')
                ysub = torch.remainder(index, hsub * wsub).div(wsub, rounding_mode='floor')
                xsub = torch.remainder(index, hsub * wsub).remainder(wsub)
                # xsub, ysub is the first point in the 4x4 square of finely sampled points
                x, y = [], []
                for ah in range(self.weights_subsampled):
                    for aw in range(self.weights_subsampled):
                        x.append(xsub * self.weights_subsampled + aw)
                        y.append(ysub * self.weights_subsampled + ah)
                x = torch.cat(x)
                y = torch.cat(y)
                image_id = image_id.repeat(self.weights_subsampled ** 2)
                # Inverse of the process to get x, y from index. image_id stays the same.
                index = x + y * w + image_id * h * w
            x, y = x + 0.5, y + 0.5
        else:
            image_id = torch.tensor([index])
            x, y = create_meshgrid(height=h, width=w, dev=dev, add_half=True, flat=True)

        out = {
            "timestamps": self.timestamps[index],      # (num_rays or 1, )
            "imgs": None,
        }
        if self.split == 'train':
            num_frames_per_camera = len(self.imgs) // (len(self.per_cam_near_fars) * h * w)
            camera_id = torch.div(image_id, num_frames_per_camera, rounding_mode='floor')  # (num_rays)
            out['near_fars'] = self.per_cam_near_fars[camera_id, :]
        else:
            out['near_fars'] = self.per_cam_near_fars  # Only one test camera
        
        # print(f"[DEBUG] : Video360Dataset : {self.split} / {out['near_fars'].shape}")
        if self.imgs is not None:
            out['imgs'] = (self.imgs[index] / 255.0).view(-1, self.imgs.shape[-1])
        
        # print(self.poses.shape, len(image_id), image_id[0]) # (2700,3,4) / 4096 / tensor(id)
        c2w = self.poses[image_id]                                    # [num_rays or 1, 3, 4]
        # 0131/0201-------------------------------------------------------------------- #
        if self.extra_intrinsic is not None:
            intrinsic_input = self.extra_intrinsic[(image_id/len(self.timestamps)).floor().long()]
        else:
            intrinsic_input = self.intrinsics
        camera_dirs = stack_camera_dirs(x, y, intrinsic_input, True)  # [num_rays, 3]
        out['rays_o'], out['rays_d'] = get_rays(
            camera_dirs, c2w, ndc=self.is_ndc, intrinsics=intrinsic_input,
            normalize_rd=True)                                        # [num_rays, 3]
        # ----------------------------------------------------------------------------- #
        if torch.isnan(out['rays_o']).sum() > 0:
            raise ValueError("[ERROR] : ray origin is None ?! = ", torch.isnan(out['rays_o']).sum() / out['rays_o'].numel())
        if torch.isnan(out['rays_d']).sum() > 0:
            raise ValueError("[ERROR] : ray direction is None ?! = ", torch.isnan(out['rays_d']).sum() / out['rays_d'].numel())

        imgs = out['imgs']
        # Decide BG color
        bg_color = torch.ones((1, 3), dtype=torch.float32, device=dev)
        if self.split == 'train' and imgs.shape[-1] == 4:
            bg_color = torch.rand((1, 3), dtype=torch.float32, device=dev)
        out['bg_color'] = bg_color
        # Alpha compositing
        if imgs is not None and imgs.shape[-1] == 4:
            imgs = imgs[:, :3] * imgs[:, 3:] + bg_color * (1.0 - imgs[:, 3:])
        out['imgs'] = imgs

        return out


def get_bbox(datadir: str, dset_type: str, is_contracted=False) -> torch.Tensor:
    """Returns a default bounding box based on the dataset type, and contraction state.

    Args:
        datadir (str): Directory where data is stored
        dset_type (str): A string defining dataset type (e.g. synthetic, llff)
        is_contracted (bool): Whether the dataset will use contraction

    Returns:
        Tensor: 3x2 bounding box tensor
    """
    if is_contracted:
        radius = 2
    elif dset_type == 'synthetic':
        radius = 1.5
    elif dset_type == 'llff':
        return torch.tensor([[-3.0, -1.67, -1.2], [3.0, 1.67, 1.2]])
    else:
        radius = 1.3
    return torch.tensor([[-radius, -radius, -radius], [radius, radius, radius]])


def fetch_360vid_info(frame: Dict[str, Any]):
    timestamp = None
    fp = frame['file_path']
    if '_r' in fp:
        timestamp = int(fp.split('t')[-1].split('_')[0])
    if 'r_' in fp:
        pose_id = int(fp.split('r_')[-1])
    else:
        pose_id = int(fp.split('r')[-1])
    if timestamp is None:  # will be None for dnerf
        timestamp = frame['time']
    return timestamp, pose_id


def load_360video_frames(datadir, split, max_cameras: int, max_tsteps: Optional[int]) -> Tuple[Any, Any]:
    with open(os.path.join(datadir, f"transforms_{split}.json"), 'r') as fp:
        meta = json.load(fp)
    frames = meta['frames']

    timestamps = set()
    pose_ids = set()
    fpath2poseid = defaultdict(list)
    for frame in frames:
        timestamp, pose_id = fetch_360vid_info(frame)
        timestamps.add(timestamp)
        pose_ids.add(pose_id)
        fpath2poseid[frame['file_path']].append(pose_id)
    timestamps = sorted(timestamps)
    pose_ids = sorted(pose_ids)

    if max_cameras is not None:
        num_poses = min(len(pose_ids), max_cameras or len(pose_ids))
        subsample_poses = int(round(len(pose_ids) / num_poses))
        pose_ids = set(pose_ids[::subsample_poses])
        log.info(f"Selected subset of {len(pose_ids)} camera poses: {pose_ids}.")

    if max_tsteps is not None:
        num_timestamps = min(len(timestamps), max_tsteps or len(timestamps))
        subsample_time = int(math.floor(len(timestamps) / (num_timestamps - 1)))
        timestamps = set(timestamps[::subsample_time])
        log.info(f"Selected subset of timestamps: {sorted(timestamps)} of length {len(timestamps)}")

    sub_frames = []
    for frame in frames:
        timestamp, pose_id = fetch_360vid_info(frame)
        if timestamp in timestamps and pose_id in pose_ids:
            sub_frames.append(frame)
    # We need frames to be sorted by pose_id
    sub_frames = sorted(sub_frames, key=lambda f: fpath2poseid[f['file_path']])
    return sub_frames, meta


def load_llffvideo_poses(datadir: str,
                         downsample: float,
                         split: str,
                         near_scaling: float,
                         pose_npy_suffix:str='', # 0131
                         selection:list=None,
                         pose_selection:list=None,
                         cam_scale:float=None
                         ) -> Tuple[torch.Tensor, torch.Tensor, Intrinsics, List[str]]:
    """Load poses and metadata for LLFF video.

    Args:
        datadir (str): Directory containing the videos and pose information
        downsample (float): How much to downsample videos. The default for LLFF videos is 2.0
        split (str): 'train' or 'test'.
        near_scaling (float): How much to scale the near bound of poses.

    Returns:
        Tensor: A tensor of size [N, 4, 4] containing c2w poses for each camera.
        Tensor: A tensor of size [N, 2] containing near, far bounds for each camera.
        Intrinsics: The camera intrinsics. These are the same for every camera.
        List[str]: List of length N containing the path to each camera's data.
    """
    # 0131
    poses, near_fars, intrinsics = load_llff_poses_helper(datadir, downsample, near_scaling,
                                                            pose_npy_suffix=pose_npy_suffix,
                                                            cam_scale=cam_scale)

    # videopaths = np.array(glob.glob(os.path.join(datadir, '*.mp4')))  # [n_cameras]
    videopaths = []
    if len(videopaths) == 0:
        print(f"[INFO] : video_datasets.py / load_llff_poses : set video/image path")
        # print(" "*10, os.path.join(datadir, f"frames{int(downsample)}"))
        # videopaths = np.array(glob.glob(os.path.join(datadir, f"frames{int(downsample)}/*")))
        print(" "*10, os.path.join(datadir, f"images_{int(downsample)}"))
        videopaths = np.array(glob.glob(os.path.join(datadir, f"images_{int(downsample)}/*")))
    
    print("pose_selection = ", pose_selection)

    if pose_selection is None:
        assert poses.shape[0] == len(videopaths), \
            f'Mismatch between number of cameras and number of poses! : {poses.shape[0]} != {len(videopaths)}'
    videopaths.sort()

    # The first camera is reserved for testing, following https://github.com/facebookresearch/Neural_3D_Video/releases/tag/v1.0
    if selection is None:
        if split == 'train':
            split_ids = np.arange(1, poses.shape[0])
        elif split == 'test':
            split_ids = np.array([0])   # TODO: give this value as argument, not hardcoded
        else:
            split_ids = np.arange(poses.shape[0])
    else:
        if split == 'train':
            if selection[0] == None:
                split_ids = np.arange(1, poses.shape[0])
            else:
                split_ids = np.array(selection[0])
        elif split == 'test':
            split_ids = np.array(selection[1])
        else:
            split_ids = np.arange(poses.shape[0])
    print('selection : ', selection, 'pose_selection', pose_selection)
    print('split_ids : ', split_ids)
    if pose_selection is None:
        pose_split_ids = split_ids
    else:
        if split == 'train':
            pose_split_ids = np.array(pose_selection[0])
        elif split == 'test':
            pose_split_ids = np.array(pose_selection[1])
        else:
            pose_split_ids = split_ids # ??
    print('pose_split_ids : ', pose_split_ids)

    if 'coffee_martini' in datadir:
        # https://github.com/fengres/mixvoxels/blob/0013e4ad63c80e5f14eb70383e2b073052d07fba/dataLoader/llff_video.py#L323
        log.info(f"Deleting unsynchronized camera from coffee-martini video.")
        split_ids = np.setdiff1d(split_ids, 12)
    poses = torch.from_numpy(poses[pose_split_ids])
    near_fars = torch.from_numpy(near_fars[pose_split_ids])
    videopaths = videopaths[split_ids].tolist()
    print("[DEBUG] : splitted videos : ", videopaths)
    # WARNING: for st-nerf dataset
    if isinstance(videopaths, str): 
        videopaths = [videopaths] # when test case ...
    if len(poses.shape) == 2:
        poses = poses[None]
    # if len(near_fars.shape) == 2:
    #     near_fars = near_fars[None]
    if split == "test":
        near_fars = near_fars[None]
    print(f"[DEBUG] : poses.shape = {poses} / near_far.shape = {near_fars}")
    return poses, near_fars, intrinsics, videopaths


def load_llffvideo_data(videopaths: List[str],
                        cam_poses: torch.Tensor,
                        intrinsics: Intrinsics,
                        split: str,
                        keyframes: bool,
                        keyframes_take_each: Optional[int] = None,
                        ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    if keyframes and (keyframes_take_each is None or keyframes_take_each < 1):
        raise ValueError(f"'keyframes_take_each' must be a positive number, "
                         f"but is {keyframes_take_each}.")

    loaded = parallel_load_images(
        dset_type="video",
        tqdm_title=f"Loading {split} data",
        num_images=len(videopaths),
        paths=videopaths,
        poses=cam_poses,
        out_h=intrinsics.height,
        out_w=intrinsics.width,
        load_every=keyframes_take_each if keyframes else 1,
        test=split=="test" or split=="render"
    )
    imgs, poses, median_imgs, timestamps = zip(*loaded)
    # Stack everything together
    timestamps = torch.cat(timestamps, 0)  # [N]
    poses = torch.cat(poses, 0)            # [N, 3, 4]
    imgs = torch.cat(imgs, 0)              # [N, h, w, 3]
    median_imgs = torch.stack(median_imgs, 0)  # [num_cameras, h, w, 3]

    return poses, imgs, timestamps, median_imgs


@torch.no_grad()
def dynerf_isg_weight(imgs, median_imgs, gamma):
    # imgs is [num_cameras * num_frames, h, w, 3]
    # median_imgs is [num_cameras, h, w, 3]
    assert imgs.dtype == torch.uint8
    assert median_imgs.dtype == torch.uint8
    num_cameras, h, w, c = median_imgs.shape
    squarediff = (
        imgs.view(num_cameras, -1, h, w, c)
            .float()  # creates new tensor, so later operations can be in-place
            .div_(255.0)
            .sub_(
                median_imgs[:, None, ...].float().div_(255.0)
            )
            .square_()  # noqa
    )  # [num_cameras, num_frames, h, w, 3]
    # differences = median_imgs[:, None, ...] - imgs.view(num_cameras, -1, h, w, c)  # [num_cameras, num_frames, h, w, 3]
    # squarediff = torch.square_(differences)
    psidiff = squarediff.div_(squarediff + gamma**2)
    psidiff = (1./3) * torch.sum(psidiff, dim=-1)  # [num_cameras, num_frames, h, w]
    return psidiff  # valid probabilities, each in [0, 1]


@torch.no_grad()
def dynerf_ist_weight(imgs, num_cameras, alpha=0.1, frame_shift=25):  # DyNerf uses alpha=0.1
    assert imgs.dtype == torch.uint8
    N, h, w, c = imgs.shape
    frames = imgs.view(num_cameras, -1, h, w, c).float()  # [num_cameras, num_timesteps, h, w, 3]
    max_diff = None
    shifts = list(range(frame_shift + 1))[1:]
    for shift in shifts:
        shift_left = torch.cat([frames[:, shift:, ...], torch.zeros(num_cameras, shift, h, w, c)], dim=1)
        shift_right = torch.cat([torch.zeros(num_cameras, shift, h, w, c), frames[:, :-shift, ...]], dim=1)
        mymax = torch.maximum(torch.abs_(shift_left - frames), torch.abs_(shift_right - frames))
        if max_diff is None:
            max_diff = mymax
        else:
            max_diff = torch.maximum(max_diff, mymax)  # [num_timesteps, h, w, 3]
    max_diff = torch.mean(max_diff, dim=-1)  # [num_timesteps, h, w]
    max_diff = max_diff.clamp_(min=alpha)
    return max_diff
