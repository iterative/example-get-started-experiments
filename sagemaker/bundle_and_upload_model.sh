cp $1 sagemaker/code/best.pt
cd sagemaker && tar -cpzf model.tar.gz code/ && cd .. && mv sagemaker/model.tar.gz .
aws s3 cp model.tar.gz $2