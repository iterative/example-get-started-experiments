import os
import shutil

from dvclive import Live
from fire import Fire
from ultralytics import YOLO


def add_callbacks(live, yolo):
    def _log_confusion_matrix(validator, live):
        targets = []
        preds = []
        matrix = validator.confusion_matrix.matrix
        names = list(validator.names.values())
        if validator.confusion_matrix.task == "detect":
            names += ["background"]

        for ti, pred in enumerate(matrix.T.astype(int)):
            for pi, num in enumerate(pred):
                targets.extend([names[ti]] * num)
                preds.extend([names[pi]] * num)

        live.log_sklearn_plot("confusion_matrix", targets, preds)

    def on_train_epoch_start(trainer):
        trainer.__training_epoch = True

    def on_fit_epoch_end(trainer):
        if trainer.__training_epoch:
            all_metrics = {
                **trainer.label_loss_items(trainer.tloss, prefix="train"),
                **trainer.metrics,
            }
            for metric, value in all_metrics.items():
                live.log_metric(metric, value)

            live.next_step()
            trainer.__training_epoch = False

    def on_train_end(trainer):
        all_metrics = {
            **trainer.label_loss_items(trainer.tloss, prefix="train"),
            **trainer.metrics,
        }
        for metric, value in all_metrics.items():
            live.log_metric(metric, value, plot=False)

        _log_confusion_matrix(trainer.validator, live)

        for image_path in trainer.validator.plots.keys():
            if "val_batch" in image_path.name:
                live.log_image(image_path.name, image_path)

        if trainer.best.exists():
            live.log_artifact(
                trainer.best, name="pool-segmentation", type="model", copy=True,
                desc="This is a Computer Vision (CV) model that's segmenting out swimming pools from satellite images.",
                labels=["cv", "segmentation", "satellite-images", "yolo"],
            )

    yolo.callbacks["on_train_epoch_start"].append(on_train_epoch_start)
    yolo.callbacks["on_fit_epoch_end"].append(on_fit_epoch_end)
    yolo.callbacks["on_train_end"].append(on_train_end)

    return yolo


def train(data: str = "data/yolo_dataset.yaml", epochs: int = 10, imgsz: int = 384, model: str = "yolov8n-seg.pt"):
    yolo = YOLO(model)

    with Live("results/train", save_dvc_exp=True, report=None, cache_images=True) as live:
        yolo = add_callbacks(live, yolo)
        yolo.train(data=data, epochs=epochs, imgsz=imgsz)

    try:
        os.remove("data/yolo_dataset/train.cache")
        os.remove("data/yolo_dataset/val.cache")
    except FileNotFoundError:
        pass
    shutil.rmtree("./runs", ignore_errors=True)
    shutil.rmtree("./weights", ignore_errors=True)


if __name__ == "__main__":
    Fire(train)