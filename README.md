## TANGOS: Regularizing Tabular Neural Networks through Gradient Orthogonalization and Specialization

[![pdf](https://img.shields.io/badge/PDF-ICLR%202023-red)](https://openreview.net/forum?id=n6H86gW8u0d)
[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD-blue.svg)](https://github.com/alanjeffares/TANGOS/blob/main/LICENSE)

![TANGOS](figure.jpg?raw=true "TANGOS")

This repository contains the code associated with [our ICLR 2023 paper](https://openreview.net/forum?id=n6H86gW8u0d) where we introduce a novel regularizer for training deep neural networks. Tabular Neural Gradient Orthogonalization and Specialization (TANGOS) provides a framework for regularization in the tabular setting built on latent unit attributions. For further details, please see our paper.


### Getting Started With TANGOS
To quickly get started with integrating TANGOS into a PyTorch workflow, we have provided a handy quickstart guide. This consists of a simple MLP training routine with a drop-in function that calculates and applies TANGOS regularization. This example notebook can be found in [TANGOS_quickstart.ipynb](https://github.com/alanjeffares/TANGOS/blob/main/TANGOS_quickstart.ipynb).

### Experiments
**Setup**

Clone this repository and navigate to the root folder.
```
git clone https://github.com/alanjeffares/TANGOS.git
cd TANGOS
```

Using conda, create and activate a new environment.
```
conda create -n <environment name> pip python
conda activate <environment name>
```

Install from source:
```
pip install .
```

Then install the repository requirements.
```
pip install -r requirements.txt
```

**Data**

Datasets can be downloaded using `wget` and the `<UCISource>` described in Appendix L of the paper.
```
wget -P /path/to/data/folder/ https://archive.ics.uci.edu/ml/machine-
learning-databases/<UCISource>/
```
Then set the path to your local data folder in `src/data_config.json`.
```
{"path_to_data": "path/to/data/folder/"}
```


**Running**

These folders are associated with the commented experiments from the paper.
```
└── src
    └── tangos
        └── experiments
            ├── behavior-analysis            # TANGOS Behavior Analysis.
            ├── compute                      # Approximation and Algorithm.
            ├── in-tandem-regularization     # Generalisaton: In Tandem Regularization.
            ├── larger-data                  # Performance With Increasing Data Size.
            └── stand-alone-regularization   # Generalization: Stand-Alone Regularization.
```

The main experiments can be run by navigating to the root folder and running the following command.

```python src/tangos/experiments/<experiment name>/main.py```

Results and hyperparameters of these experiments are saved in json format to the results folder.

```src/tangos/experiments/<experiment name>/results```

The behavior analysis and compute experiments are included in ```.ipynb``` notebooks with instructions included. Please note that all jupyter notebooks are self contained and designed to be run in colab by clicking the link at the top of each notebook (e.g. [![open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alanjeffares/TANGOS/blob/main/TANGOS_quickstart.ipynb)).

_Note: To run in tandem experiments with batch norm please see [our comment](https://github.com/alanjeffares/TANGOS/blob/main/src/legacy/comment.md)._

### Citation
If you use this code, please cite the associated paper.
```
@inproceedings{
jeffares2023tangos,
title={{TANGOS}: Regularizing Tabular Neural Networks through Gradient Orthogonalization and Specialization},
author={Alan Jeffares and Tennison Liu and Jonathan Crabb{\'e} and Fergus Imrie and Mihaela van der Schaar},
booktitle={International Conference on Learning Representations},
year={2023},
url={https://openreview.net/forum?id=n6H86gW8u0d}
}
```
