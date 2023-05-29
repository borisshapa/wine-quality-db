import os
import unittest

from src import dao, utils


class TestDao(unittest.TestCase):
    def setUp(self) -> None:
        self.sql = dao.MsSql(
            "WineQuality",
            os.getenv(utils.SERVER_ENV),
            os.getenv(utils.USER_ID_ENV),
            os.getenv(utils.PASSWORD_ENV),
        )

    def test_insert(self):
        table_name = "Metrics"
        model_id = "'model1'"
        row = (model_id, 0.15, 0.943)

        self.sql.insert_row(table_name, row)
        df = self.sql.get_data("Metrics", condition={"modelId": model_id})
        rows = list(df.itertuples(index=False, name=None))
        first_row = rows[0]

        self.sql.delete_row(table_name, {"modelId": model_id})
        empty_df = self.sql.get_data("Metrics", condition={"modelId": model_id})

        self.assertEqual(len(rows), 1)
        self.assertEqual(first_row[1], 0.15)
        self.assertEqual(first_row[2], 0.943)
        self.assertTrue(empty_df.empty)

    def test_update(self):
        table_name = "Metrics"
        model_id = "'model1'"
        row = (model_id, 0.15, 0.943)

        self.sql.insert_row(table_name, row)
        self.sql.update_row(
            table_name=table_name,
            update_condition={"modelId": model_id},
            updated_values={"accuracy": 0.8},
        )
        df = self.sql.get_data("Metrics", condition={"modelId": model_id})
        rows = list(df.itertuples(index=False, name=None))
        first_row = rows[0]

        self.sql.delete_row(table_name, {"modelId": model_id})
        empty_df = self.sql.get_data("Metrics", condition={"modelId": model_id})

        self.assertEqual(len(rows), 1)
        self.assertEqual(first_row[1], 0.8)
        self.assertEqual(first_row[2], 0.943)
        self.assertTrue(empty_df.empty)
