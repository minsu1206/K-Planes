import argparse
import importlib.util
import logging
import os
import pprint
import sys
from typing import List, Dict, Any
import tempfile

import numpy as np


# def get_freer_gpu():
#     with tempfile.TemporaryDirectory() as tmpdir:
#         tmp_fname = os.path.join(tmpdir, "tmp")
#         os.system(f'nvidia-smi -q -d Memory |grep -A5 GPU|grep Free >"{tmp_fname}"')
#         if os.path.isfile(tmp_fname):
#             memory_available = [int(x.split()[2]) for x in open(tmp_fname, 'r').readlines()]
#             if len(memory_available) > 0:
#                 return np.argmax(memory_available)
#     return None  # The grep doesn't work with all GPUs. If it fails we ignore it.

# gpu = get_freer_gpu()
# if gpu is not None:
#     os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu)
#     print(f"CUDA_VISIBLE_DEVICES set to {gpu}")
# else:
#     print(f"Did not set GPU.")

import torch
import torch.utils.data
from plenoxels.runners import video_trainer
from plenoxels.runners import phototourism_trainer
from plenoxels.runners import static_trainer
from plenoxels.utils.create_rendering import render_to_path, decompose_space_time
from plenoxels.utils.parse_args import parse_optfloat

import wandb

def setup_logging(log_level=logging.INFO):
    handlers = [logging.StreamHandler(sys.stdout)]
    logging.basicConfig(level=log_level,
                        format='%(asctime)s|%(levelname)8s| %(message)s',
                        handlers=handlers,
                        force=True)


def load_data(model_type: str, data_downsample, data_dirs, validate_only: bool, render_only: bool, render_only_arc=False, **kwargs):
    data_downsample = parse_optfloat(data_downsample, default_val=1.0)

    if model_type == "video":
        return video_trainer.load_data(
            data_downsample, data_dirs, validate_only=validate_only,
            render_only=render_only, render_only_arc=render_only_arc, **kwargs)
    elif model_type == "phototourism":
        return phototourism_trainer.load_data(
            data_downsample, data_dirs, validate_only=validate_only,
            render_only=render_only, **kwargs
        )
    else:
        return static_trainer.load_data(
            data_downsample, data_dirs, validate_only=validate_only,
            render_only=render_only, **kwargs)


def init_trainer(model_type: str, **kwargs):
    if model_type == "video":
        from plenoxels.runners import video_trainer
        return video_trainer.VideoTrainer(**kwargs)
    elif model_type == "phototourism":
        from plenoxels.runners import phototourism_trainer
        return phototourism_trainer.PhototourismTrainer(**kwargs)
    else:
        from plenoxels.runners import static_trainer
        return static_trainer.StaticTrainer(**kwargs)


def save_config(config):
    log_dir = os.path.join(config['logdir'], config['expname'])
    os.makedirs(log_dir, exist_ok=True)

    with open(os.path.join(log_dir, 'config.py'), 'wt') as out:
        out.write('config = ' + pprint.pformat(config))

    with open(os.path.join(log_dir, 'config.csv'), 'w') as f:
        for key in config.keys():
            f.write("%s\t%s\n" % (key, config[key]))


def main():
    setup_logging()

    p = argparse.ArgumentParser(description="")

    p.add_argument('--render-only', action='store_true')
    p.add_argument('--validate-only', action='store_true')
    p.add_argument('--spacetime-only', action='store_true')
    p.add_argument('--render-only-arc', action='store_true')
    p.add_argument('--config-path', type=str, required=True)
    p.add_argument('--log-dir', type=str, default=None)
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--device', type=int, default=0)
    p.add_argument('override', nargs=argparse.REMAINDER)

    args = p.parse_args()
    os.environ["CUDA_VISIBLE_DEVICES"] = f"cuda:{args.device}"

    # Set random seed
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    # Import config
    spec = importlib.util.spec_from_file_location(os.path.basename(args.config_path), args.config_path)
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    config: Dict[str, Any] = cfg.config
    # Process overrides from argparse into config
    # overrides can be passed from the command line as key=value pairs. E.g.
    # python plenoxels/main.py --config-path plenoxels/config/cfg.py max_ts_frames=200
    # note that all values are strings, so code should assume incorrect data-types for anything
    # that's derived from config - and should not a string.
    overrides: List[str] = args.override
    print("overrides : ", overrides)
    
    overrides_dict = {ovr.split("=")[0]: ovr.split("=")[1] for ovr in overrides}
    config.update(overrides_dict)
    print("[DEBUG] : config.keys()")
    print(config.keys())
    
    if not (args.validate_only or args.render_only or args.spacetime_only or args.render_only_arc):
        wandb.init(project="K-planes", 
                name=f"{config['expname']}_useK={config['use_intrinsic']}", 
                sync_tensorboard=True)

    # config['data_dirs'] = [config['data_dirs'][0] + config['expname']]

    if "keyframes" in config:
        model_type = "video"
    elif "appearance_embedding_dim" in config:
        model_type = "phototourism"
    else:
        model_type = "static"
    validate_only = args.validate_only
    render_only = args.render_only
    spacetime_only = args.spacetime_only
    render_only_arc = args.render_only_arc
    if validate_only and render_only:
        raise ValueError("render_only and validate_only are mutually exclusive.")
    if render_only and spacetime_only:
        raise ValueError("render_only and spacetime_only are mutually exclusive.")
    if validate_only and spacetime_only:
        raise ValueError("validate_only and spacetime_only are mutually exclusive.")
    if render_only_arc:
        if (validate_only or render_only or spacetime_only):
            raise ValueError("use render_only_arc as unique option. others are exclusive")

    pprint.pprint(config)
    if validate_only or render_only or render_only_arc:
        if not (args.log_dir is not None and os.path.isdir(args.log_dir)):
            raise ValueError("[ERROR] : wrong log_dir = ", args.log_dir)
    else:
        save_config(config)

    data = load_data(model_type, validate_only=validate_only, render_only=render_only or spacetime_only, render_only_arc=render_only_arc, **config)
    config.update(data)
    trainer = init_trainer(model_type, **config)
    if args.log_dir is not None:
        checkpoint_path = os.path.join(args.log_dir, "model.pth")
        training_needed = not (validate_only or render_only or spacetime_only)
        trainer.load_model(torch.load(checkpoint_path), training_needed=training_needed)

    if validate_only:
        trainer.validate()
    elif render_only or render_only_arc:
        render_to_path(trainer, extra_name="")
    elif spacetime_only:
        decompose_space_time(trainer, extra_name="")
    else:
        trainer.train()
    if not (args.validate_only or args.render_only or args.spacetime_only or args.render_only_arc):
        wandb.finish()

if __name__ == "__main__":
    main()
