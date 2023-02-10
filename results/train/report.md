# DVC Report

params.yaml

| model       |   batch_size |   batch_per_epoch | frozen   |   frozen_idx | transforms                                                      |
|-------------|--------------|-------------------|----------|--------------|-----------------------------------------------------------------|
| DynamicUnet |            8 |                 8 | False    |            0 | [Pipeline: PILBase.create, Pipeline: partial -> PILBase.create] |

metrics.json

| train                          | eval                          |   dice_multi |   step |
|--------------------------------|-------------------------------|--------------|--------|
| {'loss': 0.017254043370485306} | {'loss': 0.01514338981360197} |     0.918244 |     12 |

![static/dice_multi](static/dice_multi.png)

![static/train/loss](static/train/loss.png)

![static/eval/loss](static/eval/loss.png)
