config = {
 'expname': 'stnerf_walking',
 'logdir': './logs/full',
 'device': 'cuda:0',

 # Run first for 1 step with data_downsample=4 to generate weights for ray importance sampling
 'data_downsample': 1,
 'data_dirs': ['/workspace/lustre/datasets/nerf_team/walking'],
 'contract': False,
 'ndc': True,
 'ndc_far': 2.6,
 'near_scaling': 0.95,
 'isg': True,
 'isg_step': -1,
 'ist_step': 50000,
 'keyframes': False,
 'cam_scale': 1.0,
 'scene_bbox': [[-3.0, -1.8, -1.2], [3.0, 1.8, 1.2]],

 # Optimization settings
 'num_steps': 90001,
 'batch_size': 4096,
 'scheduler_type': 'warmup_cosine',
 'optim_type': 'adam',
 'lr': 0.01,

 # Regularization
 'distortion_loss_weight': 0.001,
 'histogram_loss_weight': 1.0,
 'l1_time_planes': 0.0001,
 'l1_time_planes_proposal_net': 0.0001,
 'plane_tv_weight': 0.0002,
 'plane_tv_weight_proposal_net': 0.0002,
 'time_smoothness_weight': 0.001,
 'time_smoothness_weight_proposal_net': 1e-05,

 # Training settings
 'save_every': 30000,
 'valid_every': 30000,
 'save_outputs': True,
 'train_fp16': True,

 # Raymarching settings
 'single_jitter': False,
 'num_samples': 48,
 'num_proposal_samples': [256, 128],
 'num_proposal_iterations': 2,
 'use_same_proposal_network': False,
 'use_proposal_weight_anneal': True,
 'proposal_net_args_list': [
  {'num_input_coords': 4, 'num_output_coords': 8, 'resolution': [128, 128, 128, 150]},
  {'num_input_coords': 4, 'num_output_coords': 8, 'resolution': [256, 256, 256, 150]}
 ],

 # Model settings
 'concat_features_across_scales': True,
 'density_activation': 'trunc_exp',
 'linear_decoder': False,
 'multiscale_res': [1, 2, 4, 8],
 'grid_config': [{
  'grid_dimensions': 2,
  'input_coordinate_dim': 4,
  'output_coordinate_dim': 16,
  'resolution': [64, 64, 64, 150]
 }],

 'use_intrinsic': False
}