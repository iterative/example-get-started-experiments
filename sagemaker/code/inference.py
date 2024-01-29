"""
Reference:
https://sagemaker.readthedocs.io/en/stable/frameworks/pytorch/using_pytorch.html#id4
"""
import io
import os

import numpy as np
import torch
from PIL import Image
from torchvision.transforms import Compose, Normalize, Resize, ToTensor


def model_fn(model_dir, context):
    kwargs = {
        "f": os.path.join(model_dir, "code/model.pth")
    }
    if not torch.cuda.is_available():
        kwargs["map_location"] = torch.device("cpu")
    model = torch.load(**kwargs)
    return model


def input_fn(request_body, request_content_type, context):
    if request_content_type:
        img_pil = Image.open(io.BytesIO(request_body))
        img_transform = Compose([Resize(512), ToTensor(), Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
        img_tensor = img_transform(img_pil).unsqueeze_(0)
        return img_tensor
    else:
        raise ValueError(f"Unsupported request_content_type {request_content_type}")


def predict_fn(input_object, model, context):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    with torch.no_grad():
        result = model(input_object)
    return result


def output_fn(prediction_output, content_type):
    output = np.array(
        prediction_output[:, 1, :] > 0.5, dtype=np.uint8
    )
    if torch.cuda.is_available():
        output = output.cpu()
    buffer = io.BytesIO()
    np.save(buffer, output)
    return buffer.getvalue()
