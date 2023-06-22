## Metrics
| Path                          | Metric     | main    | workspace   | Change   |
|-------------------------------|------------|---------|-------------|----------|
| results/evaluate/metrics.json | dice_multi | 0.89711 | 0.88533     | -0.01177 |
| results/train/metrics.json    | dice_multi | 0.87031 | 0.87448     | 0.00417  |
| results/train/metrics.json    | eval.loss  | 0.02593 | 0.02366     | -0.00226 |
| results/train/metrics.json    | step       | 8       | 5           | -3       |
| results/train/metrics.json    | train.loss | 0.02715 | 0.03502     | 0.00787  |

## Params
| Path        | Param                        | main   | workspace   |
|-------------|------------------------------|--------|-------------|
| params.yaml | train.fine_tune_args.base_lr | 0.01   | 0.03        |
| params.yaml | train.fine_tune_args.epochs  | 8      | 5           |

