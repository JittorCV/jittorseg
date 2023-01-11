_base_ = [
    '../_base_/datasets/ade20k.py', '../_base_/default_runtime.py',
    '../_base_/schedules/schedule_160k.py'
]

norm_cfg = dict(type='BN')
model = dict(
    type='CascadeEncoderDecoder',
    num_stages=2,
    pretrained='jittorhub://resnet50_v1c-2cccc1ad.pkl',
    backbone=dict(type='ResNetV1c',
                  depth=50,
                  num_stages=4,
                  out_indices=(0, 1, 2, 3),
                  dilations=(1, 1, 1, 1),
                  strides=(1, 2, 2, 2),
                  norm_cfg=norm_cfg,
                  norm_eval=False,
                  contract_dilation=True),
    neck=dict(type='FPN',
              in_channels=[256, 512, 1024, 2048],
              out_channels=256,
              num_outs=4),
    decode_head=[
        dict(type='FPNHead',
             in_channels=[256, 256, 256, 256],
             in_index=[0, 1, 2, 3],
             feature_strides=[4, 8, 16, 32],
             channels=128,
             dropout_ratio=-1,
             num_classes=150,
             norm_cfg=norm_cfg,
             align_corners=False,
             loss_decode=dict(type='CrossEntropyLoss',
                              use_sigmoid=False,
                              loss_weight=1.0)),
        dict(type='PointHead',
             in_channels=[256],
             in_index=[0],
             channels=256,
             num_fcs=3,
             coarse_pred_each_layer=True,
             dropout_ratio=-1,
             num_classes=150,
             align_corners=False,
             loss_decode=dict(type='CrossEntropyLoss',
                              use_sigmoid=False,
                              loss_weight=1.0))
    ],
    # model training and testing settings
    train_cfg=dict(num_points=2048,
                   oversample_ratio=3,
                   importance_sample_ratio=0.75),
    test_cfg=dict(mode='whole',
                  subdivision_steps=2,
                  subdivision_num_points=8196,
                  scale_factor=2))

scheduler = dict(type='PolyLR',
                 warmup='linear',
                 warmup_iters=200,
                 warmup_ratio=1e-6,
                 max_steps=160000,
                 power=1.0,
                 min_lr=0)
