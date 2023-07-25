from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from fire import Fire
from sagemaker.deserializers import JSONDeserializer
from sagemaker.pytorch import PyTorchPredictor
from ultralytics import YOLO


def inference(
    img_path: str,
    endpoint_name: Optional[str] = None,
    model_path: Optional[str] = None,
    output_path: str = "predictions",
):

    if endpoint_name is not None and model_path is not None:
        raise ValueError("Only one of endpoint_name or model_path must be provided")
    if endpoint_name:
        predictor = PyTorchPredictor(endpoint_name, deserializer=JSONDeserializer())
        name = endpoint_name
    elif model_path:
        predictor = YOLO(model_path)
        name = model_path
    else:
        raise ValueError("Either endpoint_name or model_path must be provided")
    
    if img_path is not None:    
        output_file = Path(output_path) / name / Path(img_path).name
        output_file.parent.mkdir(exist_ok=True, parents=True)

        img = cv2.imread(img_path)
        img_bytes = cv2.imencode(".jpg", img)[1].tobytes()

        result = predictor.predict(img_bytes)

        for polygon in result:
            polygon = np.array(polygon, dtype=np.int32).reshape((-1, 1, 2))
            img = cv2.polylines(img, [polygon], True, (0, 0, 255), 2)

        cv2.imwrite(str(output_file), img)

if __name__ == "__main__":
    Fire(inference)
