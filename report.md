## Metrics
| Path                          | Metric     | main    | workspace   | Change   |
|-------------------------------|------------|---------|-------------|----------|
| results/train/metrics.json    | dice_multi | 0.87041 | 0.92903     | 0.05863  |
| results/train/metrics.json    | eval.loss  | 0.02593 | 0.01588     | -0.01005 |
| results/train/metrics.json    | step       | 8       | 10          | 2        |
| results/train/metrics.json    | train.loss | 0.02715 | 0.01346     | -0.01369 |
| results/evaluate/metrics.json | dice_multi | 0.89709 | 0.91989     | 0.0228   |

## Params
| Path        | Param                        | main               | workspace   |
|-------------|------------------------------|--------------------|-------------|
| params.yaml | train.arch                   | shufflenet_v2_x2_0 | resnet34    |
| params.yaml | train.fine_tune_args.base_lr | 0.01               | 0.003       |
| params.yaml | train.fine_tune_args.epochs  | 8                  | 10          |

