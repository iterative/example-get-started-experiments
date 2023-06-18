import random
from functools import partial
from pathlib import Path

import numpy as np
import torch
from box import ConfigBox
from dvclive.fastai import DVCLiveCallback
from fastai.data.all import Normalize, get_files
from fastai.metrics import DiceMulti
from fastai.vision.all import (
    Resize,
    SegmentationDataLoaders,
    imagenet_stats,
    models,
    unet_learner,
)
from ruamel.yaml import YAML

yaml = YAML(typ="safe")


def get_mask_path(x, train_data_dir):
    return Path(train_data_dir) / f"{Path(x).stem}.png"


def train():
    params = ConfigBox(yaml.load(open("params.yaml", encoding="utf-8")))

    np.random.seed(params.base.random_seed)
    torch.manual_seed(params.base.random_seed)
    random.seed(params.base.random_seed)
    train_data_dir = Path("data") / "train_data"

    data_loader = SegmentationDataLoaders.from_label_func(
        path=train_data_dir,
        fnames=get_files(train_data_dir, extensions=".jpg"),
        label_func=partial(get_mask_path, train_data_dir=train_data_dir),
        codes=["not-pool", "pool"],
        bs=params.train.batch_size,
        valid_pct=params.train.valid_pct,
        item_tfms=Resize(params.train.img_size),
        batch_tfms=[
            Normalize.from_stats(*imagenet_stats),
        ],
    )

    model_names = [
        name
        for name in dir(models)
        if not name.startswith("_")
        and name.islower()
        and name not in ("all", "tvm", "unet", "xresnet")
    ]
    if params.train.arch not in model_names:
        raise ValueError(f"Unsupported model, must be one of:\n{model_names}")

    learn = unet_learner(
        data_loader, arch=getattr(models, params.train.arch), metrics=DiceMulti
    )

    learn.fine_tune(
        **params.train.fine_tune_args,
        cbs=[DVCLiveCallback(dir="results/train", report="md")],
    )
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    learn.export(fname=(models_dir / "model.pkl").absolute())


if __name__ == "__main__":
    train()
