# DVC Report

params.yaml

| model       |   batch_size |   batch_per_epoch | frozen   |   frozen_idx | transforms                                                      |
|-------------|--------------|-------------------|----------|--------------|-----------------------------------------------------------------|
| DynamicUnet |           16 |                 4 | False    |            0 | [Pipeline: PILBase.create, Pipeline: partial -> PILBase.create] |

metrics.json

| train                        | eval                          |   dice_multi |   step |
|------------------------------|-------------------------------|--------------|--------|
| {'loss': 227.23007202148438} | {'loss': 0.04083644598722458} |     0.800886 |      8 |

![static/dice_multi](static/dice_multi.png)

![static/train/loss](static/train/loss.png)

![static/eval/loss](static/eval/loss.png)
