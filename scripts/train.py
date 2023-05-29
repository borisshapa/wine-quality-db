import argparse
import os.path

import catboost
import loguru
import omegaconf
import pandas as pd
import wandb

from src import utils, callbacks, dao


def _configure_arg_parser() -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--config", type=str, default="configs/db.yaml")
    argparser.add_argument("--experiments-dir", type=str, default="experiments")
    argparser.add_argument("--save-to", type=str, default="latest")
    return argparser


def main(args: argparse.Namespace):
    yaml_config = omegaconf.OmegaConf.load(args.config)
    loguru.logger.info("Set random seed: {}", yaml_config["seed"])

    seed = yaml_config["seed"]
    utils.set_deterministic_mode(seed)

    data_config = yaml_config["data"]
    model_config = yaml_config["model"]

    use_wandb = (
        model_config["task_type"] == "CPU"
        and "wandb" in yaml_config
        and yaml_config["wandb"] is not None
    )

    if use_wandb:
        wandb.init(
            project=yaml_config["wandb"],
            config=omegaconf.OmegaConf.to_container(model_config, resolve=True),
        )

    if "db_name" in data_config:
        loguru.logger.info(
            f"Loading data from database {data_config['db_name']}"
        )
        sql = dao.MsSql(
            db_name=data_config["db_name"],
            server=os.getenv(utils.SERVER_ENV),
            user_id=os.getenv(utils.USER_ID_ENV),
            password=os.getenv(utils.PASSWORD_ENV),
        )

        full_data = sql.get_data(data_config["data_table"])
        partition = utils.split_into_train_val_test(
            full_data,
            data_config["val_ratio"],
            data_config["test_ratio"],
        )
        train_data = partition["train"]
        val_data = partition["val"]
    else:
        loguru.logger.info(
            "Loading train data from {}", data_config["train_data"]
        )
        train_data = pd.read_csv(
            data_config["train_data"], sep=utils.CSV_SEPARATOR
        )

        loguru.logger.info("Loading val data from {}", data_config["val_data"])
        val_data = pd.read_csv(data_config["val_data"], sep=utils.CSV_SEPARATOR)

    x_train, y_train = utils.split_into_x_y(train_data)
    x_val, y_val = utils.split_into_x_y(val_data)

    train_dir = os.path.join(
        args.experiments_dir, args.save_to or utils.get_current_time()
    )
    loguru.logger.info("Training... | train dir: {}", train_dir)

    model = catboost.CatBoostClassifier(
        loss_function="MultiClass",
        eval_metric="TotalF1:average=Micro",
        random_seed=yaml_config["seed"],
        train_dir=train_dir,
        **model_config,
    )

    verbose = True
    _callbacks = None

    if use_wandb:
        verbose = False
        _callbacks = [callbacks.WAndBCallback(model_config["iterations"])]

    model.fit(
        x_train,
        y_train,
        eval_set=(x_val, y_val),
        cat_features=data_config["cat_features_indices"],
        verbose=verbose,
        callbacks=_callbacks,
        plot=False,
    )

    save_to = os.path.join(train_dir, "model.cbm")
    loguru.logger.info("Saving model into {}", save_to)
    model.save_model(save_to)


if __name__ == "__main__":
    _args = _configure_arg_parser().parse_args()
    main(_args)
