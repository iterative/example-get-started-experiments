import logging
import sys
from datetime import datetime

from fire import Fire

from sagemaker.deserializers import JSONDeserializer
from sagemaker.pytorch import PyTorchModel


def deploy(
    name: str,
    model_data: str,
    role: str,
    instance_type: str = "ml.c4.xlarge",
):
    sagemaker_logger = logging.getLogger("sagemaker")
    sagemaker_logger.setLevel(logging.DEBUG)
    sagemaker_logger.addHandler(logging.StreamHandler(sys.stdout))

    model = PyTorchModel(
        name=name,
        model_data=model_data,
        framework_version="1.12",
        py_version="py38",
        role=role,
        env={
            "SAGEMAKER_MODEL_SERVER_TIMEOUT": "3600",
            "TS_MAX_RESPONSE_SIZE": "2000000000",
            "TS_MAX_REQUEST_SIZE": "2000000000",
            "MMS_MAX_RESPONSE_SIZE": "2000000000",
            "MMS_MAX_REQUEST_SIZE": "2000000000",
        },
    )

    return model.deploy(
        initial_instance_count=1,
        instance_type=instance_type,
        deserializer=JSONDeserializer(),
        endpoint_name=f"{name}-{datetime.utcnow().strftime('%Y-%m-%d-%H-%M')}"
    )


if __name__ == "__main__":
    Fire(deploy)