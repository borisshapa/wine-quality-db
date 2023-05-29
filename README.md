# 🍷 Wine Quality

A service for determining the quality of wine by its numerical parameters.

## Structure
* `cd` contains Jenkinsfile for setting up cd pipeline;
* `ci` contains Jenkinsfile for setting up ci pipeline;
* `configs` contains the yaml files that define model hyperparameters;
* `data` ‒ the directory with train/val/test datasets;
* `db` ‒ database initialization scripts;
* `experiments` contains catboost meta info and a model in binary file;
* `notebooks` ‒ the directory with ipynb files with experiments and data analysis;
* `scripts` ‒ executable files (`python -m scripts.<script-name> [ARGS]`);
* `src` ‒ source code of the function used by scripts, also contains unit test of its functions;
* `tests` ‒ functional tests;

## Instalation
Local installation via pip:
```shell
git clone https://github.com/borisshapa/wine-quality
cd wine-quality
pip install -r requirements.txt
```

## Data
For data we are using `.csv` format with `;` as separator. Each line looks like this:
```text
1;6.8;0.11;0.27;8.6;0.044;45.0;104.0;0.99454;3.2;0.37;9.9;6
```

The parameters go in the following order:
0. wine type (categorical feature: 0 ‒ red wine, 1 ‒ white wine)
1. fixed acidity
2. volatile acidity
3. citric acid
4.  residual sugar
5. chlorides
6. free sulfur dioxide
7. total sulfur dioxide
8. density
9. pH
10. sulphates
11. alcohol
12. **quality** (score between 0 and 10) ‒ target variable.

## Database
To fill database with data from csv file and read it from MSSql database, run the docker:
```shell
docker build -t mssql -f --build-arg PASSWORD=<password> .
docker run -v ./data/train_val.csv:/data/train_val.csv -p 1433:1433 -d mssql
```

## Model
The algorithm is based on gradient boosting on decision trees. The service uses the [catboost](https://catboost.ai/) library.
The model is defined by the yaml file. Example:
```yaml
seed: 21
wandb: ~

data:
  train_data: data/train.csv
  val_data: data/val.csv
  cat_features_indices: [0]

model:
  iterations: 1000
  learning_rate: 0.1
  depth: 10
  l2_leaf_reg: 3
  task_type: "CPU"
```

If `data.db_name` is not specified, the data will be read from csv files (`train_data` and `val_data`).
Otherwise, the data will be read from database. In this case the data section must look as follow:

```yaml
data:
  db_name: "WineQuality"
  data_table: "Wines"
  val_ratio: 0.1
  test_ratio: 0.1
  cat_features_indices: [0]
```

Since in this case there is no direct division into training and validation samples, it is necessary to set the shares of the validation and test samples.

## Training
When training the model on the CPU, it is possible to log metrics and loss in [wandb](https://wandb.ai/site).
So pay attention to the parameter model.task_type ("CPU" or "GPU") in yaml file that defines model hyper parameters.

Also, to send data to wandb, parameter `wandb` must be defined in the yaml config.

If you decide to log data in wandb, log in first:
```shell
wandb login
```

To run training, use `scripts.train`:
```shell
python -m scripts.train --config configs/default.yaml \
    --experiments-dir experiments \
    --save-to latest
```

## Inference
To run model on test dataset use the `scripts.eval`:
```shell
python -m scripts.eval experiments/latest/model.cbm \
    --test-data data/test.csv
```

To train model, evaluate it on test dataset and run unit tests you can use docker compose:
```shell
docker compose up -d
```

To check the results use:
```shell
docker compose logs
```