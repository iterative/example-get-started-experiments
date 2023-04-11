[![DVC](https://img.shields.io/badge/-Open_in_Studio-grey.svg?style=flat-square&logo=dvc)](https://studio.iterative.ai/team/Iterative/projects/example-get-started-experiments-y8toqd433r) 
[![DVC-metrics](https://img.shields.io/badge/dynamic/json?style=flat-square&colorA=grey&colorB=F46737&label=Dice%20Metric&url=https://github.com/iterative/example-get-started-experiments/raw/main/results/evaluate/metrics.json&query=dice_multi)](https://github.com/iterative/example-get-started-experiments/raw/main/results/evaluate/metrics.json)

[Train Report](./results/train/report.md) - [Evaluation Report](./results/evaluate/report.md)

# DVC Get Started: Experiments

This is an auto-generated repository for use in [DVC](https://dvc.org)
[Get Started: Experiments](https://dvc.org/doc/start/experiment-management).

This is a Computer Vision (CV) project that solves the problem of segmenting out 
swimming pools from satellite images. 

![Example results](./results/evaluate/plots/images/)

We use a slightly modified version of the [BH-Pools dataset](http://patreo.dcc.ufmg.br/2020/07/29/bh-pools-watertanks-datasets/):
we split the original 4k images into tiles of 1024x1024 pixels.


🐛 Please report any issues found in this project here -
[example-repos-dev](https://github.com/iterative/example-repos-dev).

## Installation

Python 3.8+ is required to run code from this repo.

```console
$ git clone https://github.com/iterative/example-get-started-experiments
$ cd example-get-started-experiments
```

Now let's install the requirements. But before we do that, we **strongly**
recommend creating a virtual environment with a tool such as
[virtualenv](https://virtualenv.pypa.io/en/stable/):

```console
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

This DVC project comes with a preconfigured DVC
[remote storage](https://dvc.org/doc/commands-reference/remote) that holds raw
data (input), intermediate, and final results that are produced. This is a
read-only HTTP remote.

```console
$ dvc remote list
storage  https://remote.dvc.org/get-started-pools
```

You can run [`dvc pull`](https://man.dvc.org/pull) to download the data:

```console
$ dvc pull
```

## Running in your environment

Run [`dvc exp run`](https://man.dvc.org/exp/run) to reproduce the
[pipeline](https://dvc.org/doc/user-guide/pipelines/defining-pipelinese):

```console
$ dvc exp run
Data and pipelines are up to date.
```

If you'd like to test commands like [`dvc push`](https://man.dvc.org/push),
that require write access to the remote storage, the easiest way would be to set
up a "local remote" on your file system:

> This kind of remote is located in the local file system, but is external to
> the DVC project.

```console
$ mkdir -p /tmp/dvc-storage
$ dvc remote add local /tmp/dvc-storage
```

You should now be able to run:

```console
$ dvc push -r local
```

## Existing stages

There is a couple of git tags in this project :

### [1-notebook-dvclive](https://github.com/iterative/example-get-started-experiments/tree/1-notebook-dvclive)

Contains an end-to-end Jupyter notebook that loads data, trains a model and 
reports model performance. 
[DVCLive](https://dvc.org/doc/dvclive) is used for experiment tracking. 
See this [blog post](https://iterative.ai/blog/exp-tracking-dvc-python) for more
details.

### [2-dvc-pipeline](https://github.com/iterative/example-get-started-experiments/tree/2-dvc-pipeline)

Contains a DVC pipeline `dvc.yaml` that was created by refactoring the above 
notebook into individual pipeline stages. 

The pipeline artifacts (processed data, model file, etc) are automatically 
versioned. 

This tag also contains a GitHub Actions workflow that reruns the pipeline if any
 changes are introduced to the pipeline-related files. 
[CML](https://cml.dev/) is used in this workflow to provision a cloud-based GPU 
machine as well as report model performance results in Pull Requests.

## Project structure

The data files, DVC files, and results change as stages are created one by one.
After cloning and using [`dvc pull`](https://man.dvc.org/pull) to download
data, models, and plots tracked by DVC, the workspace should look like this:

```console
$ tree -L 2
.
├── LICENSE
├── README.md
├── data.            # <-- Directory with raw and intermediate data
│   ├── pool_data    # <-- Raw image data
│   ├── pool_data.dvc # <-- .dvc file - a placeholder/pointer to raw data
│   ├── test_data    # <-- Processed test data
│   └── train_data   # <-- Processed train data
├── dvc.lock
├── dvc.yaml         # <-- DVC pipeline file
├── models
│   └── model.pkl    # <-- Trained model file
├── notebooks
│   └── TrainSegModel.ipynb # <-- Initial notebook (refactored into `dvc.yaml`) 
├── params.yaml      # <-- Parameters file
├── requirements.txt # <-- Python dependencies needed in the project
├── results          # <-- DVCLive reports and plots
│   ├── evaluate
│   └── train
└── src              # <-- Source code to run the pipeline stages
    ├── data_split.py
    ├── evaluate.py
    └── train.py
```
