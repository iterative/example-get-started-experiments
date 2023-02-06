# DVC Report

params.yaml

| model       |   batch_size |   batch_per_epoch | frozen   |   frozen_idx | transforms                                                      |
|-------------|--------------|-------------------|----------|--------------|-----------------------------------------------------------------|
| DynamicUnet |            8 |                 8 | False    |            0 | [Pipeline: PILBase.create, Pipeline: partial -> PILBase.create] |

metrics.json

| train                         | eval                           |   dice_multi |   step |
|-------------------------------|--------------------------------|--------------|--------|
| {'loss': 0.02374456264078617} | {'loss': 0.019713368266820908} |     0.911645 |      8 |

![static/dice_multi](static/dice_multi.png)

![static/eval/loss](static/eval/loss.png)

![static/train/loss](static/train/loss.png)
