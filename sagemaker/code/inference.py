"""
Reference:
https://sagemaker.readthedocs.io/en/stable/frameworks/pytorch/using_pytorch.html#id4
"""
import io
import json
import os

import cv2
import numpy as np
import torch
from ultralytics import YOLO


def model_fn(model_dir, context):
    model = YOLO(os.path.join(model_dir, "code/best.pt"))
    return model


def input_fn(request_body, request_content_type, context):
    if request_content_type:
        # ¯\_(ツ)_/¯
        img = cv2.imdecode(
            np.frombuffer(
                np.load(io.BytesIO(request_body), allow_pickle=True), dtype=np.uint8
            ),
            flags=-1,
        )
        return img
    else:
        raise ValueError(f"Unsupported request_content_type {request_content_type}")


def predict_fn(input_object, model, context):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    with torch.no_grad():
        result = model(input_object, conf=0.5, iou=0.5)
    return result


def output_fn(prediction_output, content_type):
    result = prediction_output[0]
    if "masks" in result.keys:
        return json.dumps([mask.tolist() for mask in result.masks.xy])
    return "[]"
