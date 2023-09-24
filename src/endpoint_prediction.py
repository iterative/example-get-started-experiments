from io import BytesIO
from pathlib import Path

import dvc.api
import numpy as np
from PIL import Image
from sagemaker.deserializers import NumpyDeserializer
from sagemaker.pytorch import PyTorchPredictor
from sagemaker.serializers import IdentitySerializer


def paint_mask(mask, color_map={0: (0, 0, 0), 1: (0, 0, 255)}):
    vis_shape = mask.shape + (3,)
    vis = np.zeros(vis_shape)
    for i, c in color_map.items():
        vis[mask == i] = color_map[i]
    return Image.fromarray(vis.astype(np.uint8))


def endpoint_prediction(
    img_path: str,
    endpoint_name: str,
    output_path: str = "predictions",
):
    params = dvc.api.params_show()
    img_size = params["train"]["img_size"]
    predictor = PyTorchPredictor(endpoint_name, serializer=IdentitySerializer(), deserializer=NumpyDeserializer())
    name = endpoint_name
    
    output_file = Path(output_path) / name / Path(img_path).name
    output_file.parent.mkdir(exist_ok=True, parents=True)

    io = BytesIO()
    Image.open(img_path).resize((img_size, img_size)).save(io, format="PNG")
    result = predictor.predict(io.getvalue())[0]

    img_pil = Image.open(img_path)
    overlay_img_pil = Image.blend(
        img_pil.convert("RGBA"), 
        paint_mask(result).convert("RGBA").resize(img_pil.size), 
        0.5
    )
    overlay_img_pil.save(str(output_file.with_suffix(".png")))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Run inference on an image using a SageMaker endpoint')
    parser.add_argument('--img_path', type=str, help='path to the input image')
    parser.add_argument('--endpoint_name', type=str, help='name of the SageMaker endpoint to use')
    parser.add_argument('--output_path', type=str, default='predictions', help='path to save the output predictions')

    args = parser.parse_args()

    endpoint_prediction(args.img_path, args.endpoint_name, args.output_path)
