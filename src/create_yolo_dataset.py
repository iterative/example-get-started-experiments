import shutil
from pathlib import Path
from typing import List, Union

import cv2
from fire import Fire
from shapely import Polygon


def mask_to_yolo_annotation(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    annotation = ""
    for contour in contours:
        if contour.shape[0] < 3:
            continue
        polygon = Polygon(contour.squeeze()).simplify(1, preserve_topology=False)
        single_annotation = "0"
        for col, row in polygon.exterior.coords:
            single_annotation += f" {round(col / mask.shape[1], 3)} {round(row / mask.shape[0], 3)}"
        annotation += f"{single_annotation}\n"
    return annotation


def create_yolo_dataset(test_regions: Union[str, List[str]]):
    if isinstance(test_regions, str):
        test_regions = [test_regions]
    data = Path("data")
    train_data_dir = data / "yolo_dataset" / "train"
    train_data_dir.mkdir(exist_ok=True, parents=True)
    test_data_dir = data / "yolo_dataset" / "val"
    test_data_dir.mkdir(exist_ok=True, parents=True)

    for img_path in data.glob("pool_data/images/*.jpg"):
        yolo_annotation = mask_to_yolo_annotation(
            cv2.imread(
                str(data / "pool_data" / "masks" / f"{img_path.stem}.png"),
                cv2.IMREAD_GRAYSCALE
            )
        )

        if any(region in str(img_path) for region in test_regions):
            dst = test_data_dir / img_path.name
        else:
            dst = train_data_dir / img_path.name
        shutil.copy(img_path, dst)
        dst.with_suffix(".txt").write_text(yolo_annotation)

if __name__ == "__main__":
    Fire(create_yolo_dataset)
