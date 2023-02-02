# DVC Report

params.yaml

| model       |   batch_size |   batch_per_epoch | frozen   |   frozen_idx | transforms                                                      |
|-------------|--------------|-------------------|----------|--------------|-----------------------------------------------------------------|
| DynamicUnet |            8 |                 8 | False    |            0 | [Pipeline: PILBase.create, Pipeline: partial -> PILBase.create] |

metrics.json

| train                          | eval                           |   dice_multi |   step |
|--------------------------------|--------------------------------|--------------|--------|
| {'loss': 0.027396978810429573} | {'loss': 0.016742641106247902} |     0.909054 |      8 |

![static/dice_multi](static/dice_multi.png)

![static/eval/loss](static/eval/loss.png)

![static/train/loss](static/train/loss.png)
