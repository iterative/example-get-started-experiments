# DVC Report

params.yaml

| model       |   batch_size |   batch_per_epoch | frozen   |   frozen_idx | transforms                                                      |
|-------------|--------------|-------------------|----------|--------------|-----------------------------------------------------------------|
| DynamicUnet |            8 |                 8 | False    |            0 | [Pipeline: PILBase.create, Pipeline: partial -> PILBase.create] |

metrics.json

| train                         | eval                           |   dice_multi |   step |
|-------------------------------|--------------------------------|--------------|--------|
| {'loss': 0.04961903765797615} | {'loss': 0.029142256826162338} |     0.886355 |      2 |

![static/dice_multi](static/dice_multi.png)

![static/train/loss](static/train/loss.png)

![static/eval/loss](static/eval/loss.png)
