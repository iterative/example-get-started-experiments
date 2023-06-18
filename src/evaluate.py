from pathlib import Path

import numpy as np
from box import ConfigBox
from dvclive import Live
from fastai.vision.all import get_files, load_learner
from PIL import Image
from ruamel.yaml import YAML


yaml = YAML(typ="safe")


def dice(mask_pred, mask_true, classes=[0, 1], eps=1e-6):
    dice_list = []
    for c in classes:
        y_true = mask_true == c
        y_pred = mask_pred == c
        intersection = 2.0 * np.sum(y_true * y_pred)
        dice = intersection / (np.sum(y_true) + np.sum(y_pred) + eps)
        dice_list.append(dice)
    return np.mean(dice_list)


def paint_mask(mask, color_map={0: (0, 0, 0), 1: (0, 0, 255)}):
    vis_shape = mask.shape + (3,)
    vis = np.zeros(vis_shape)
    for i, c in color_map.items():
        vis[mask == i] = color_map[i]
    return Image.fromarray(vis.astype(np.uint8))


def stack_images(im1, im2):
    dst = Image.new("RGB", (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def get_overlay_image(img_fpath, mask_true, mask_pred):
    img_pil = Image.open(img_fpath)
    overlay_img_true = Image.blend(
        img_pil.convert("RGBA"), paint_mask(mask_true).convert("RGBA"), 0.5
    )

    new_color_map = {
        0: (0, 0, 0),  # no color - TN
        1: (255, 0, 255),  # purple - FN
        2: (255, 255, 0),  # yellow - FP
        3: (0, 0, 255),  # blue - TP
    }
    combined_mask = mask_true + 2 * mask_pred

    overlay_img_pred = Image.blend(
        img_pil.convert("RGBA"),
        paint_mask(combined_mask, color_map=new_color_map).convert("RGBA"),
        0.5,
    )
    stacked_image = stack_images(overlay_img_true, overlay_img_pred)
    return stacked_image


def get_mask_path(x, train_data_dir):
    return Path(train_data_dir) / f"{Path(x).stem}.png"


def evaluate():
    params = ConfigBox(yaml.load(open("params.yaml", encoding="utf-8")))
    img_size = params.train.img_size
    model_fpath = Path("models") / "model.pkl"
    learn = load_learner(model_fpath, cpu=False)
    test_img_fpaths = get_files(Path("data") / "test_data", extensions=".jpg")
    test_dl = learn.dls.test_dl(test_img_fpaths)
    preds, _ = learn.get_preds(dl=test_dl)
    masks_pred = np.array(preds[:, 1, :] > 0.5, dtype=np.uint8)
    test_mask_fpaths = [
        get_mask_path(fpath, Path("data") / "test_data") for fpath in test_img_fpaths
    ]
    masks_true = [Image.open(mask_path) for mask_path in test_mask_fpaths]
    with Live("results/evaluate", report="md") as live:
        dice_multi = 0.0
        for ii in range(len(masks_true)):
            mask_pred, mask_true = masks_pred[ii], masks_true[ii]
            mask_pred = np.array(
                Image.fromarray(mask_pred).resize((mask_true.shape[1], mask_true.shape[0])),
                dtype=int
            )
            mask_true = np.array(mask_true, dtype=int)
            dice_multi += dice(mask_true, mask_pred) / len(masks_true)

            if ii < params.evaluate.n_samples_to_save:
                stacked_image = get_overlay_image(
                    test_img_fpaths[ii], mask_true, mask_pred
                )
                stacked_image = stacked_image.resize((512, 256))
                live.log_image(f"{Path(test_img_fpaths[ii]).stem}.png", stacked_image)

        live.summary["dice_multi"] = dice_multi


if __name__ == "__main__":
    evaluate()
