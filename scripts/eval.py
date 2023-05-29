import argparse
import os

import catboost
import loguru
import pyodbc
import pandas as pd
from sklearn import metrics

from src import utils, dao


def _configure_parser() -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--model",
        type=str,
        default="experiments/latest/model.cbm",
        help="Catboost model in binary file.",
    )
    argparser.add_argument(
        "--test-data",
        type=str,
        default="data/test.csv",
        help="Test dataset in csv format (sep = ';').",
    )
    argparser.add_argument(
        "--db",
        type=str,
        default=None,
        help="Database name if you need to write the results to the database",
    )
    argparser.add_argument(
        "--table",
        type=str,
        default=None,
        help="Table name if you need to write the results to the database",
    )
    return argparser


def main(args: argparse.Namespace):
    model = catboost.CatBoostClassifier()

    loguru.logger.info("Loading model from {}", args.model)
    model.load_model(args.model)

    loguru.logger.info("Loading data from {}", args.test_data)
    data = pd.read_csv(args.test_data, sep=";")
    features, labels = utils.split_into_x_y(data)
    predictions = model.predict(features)

    f1_micro = metrics.f1_score(predictions, labels, average="micro")
    accuracy = metrics.accuracy_score(predictions, labels)

    loguru.logger.info(f"\nF1 micro: {f1_micro}\nAccuracy: {accuracy}")

    if args.db is not None:
        sql = dao.MsSql(
            db_name=args.db,
            server=os.getenv(utils.SERVER_ENV),
            user_id=os.getenv(utils.USER_ID_ENV),
            password=os.getenv(utils.PASSWORD_ENV),
        )
        loguru.logger.info(f"Saving metrics into database {args.db}")
        try:
            sql.insert_row(args.table, (f"'{args.model}'", accuracy, f1_micro))
        except pyodbc.IntegrityError:
            sql.update_row(
                args.table,
                updated_values={"accuracy": accuracy, "f1Micro": f1_micro},
                update_condition={"modelId": f"'args.model'"},
            )


if __name__ == "__main__":
    _args = _configure_parser().parse_args()
    main(_args)
