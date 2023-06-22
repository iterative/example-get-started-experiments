## Metrics
| Path                          | Metric     | main    | workspace   | Change   |
|-------------------------------|------------|---------|-------------|----------|
| results/train/metrics.json    | dice_multi | 0.87031 | 0.93485     | 0.06454  |
| results/train/metrics.json    | eval.loss  | 0.02593 | 0.01253     | -0.0134  |
| results/train/metrics.json    | step       | 8       | 10          | 2        |
| results/train/metrics.json    | train.loss | 0.02715 | 0.01639     | -0.01076 |
| results/evaluate/metrics.json | dice_multi | 0.89711 | 0.92214     | 0.02503  |

## Params
| Path        | Param                        | main               | workspace   |
|-------------|------------------------------|--------------------|-------------|
| params.yaml | train.arch                   | shufflenet_v2_x2_0 | resnet34    |
| params.yaml | train.fine_tune_args.base_lr | 0.01               | 0.003       |
| params.yaml | train.fine_tune_args.epochs  | 8                  | 10          |
| params.yaml | train.img_size               | 256                | 384         |

