import pandas as pd
import pyodbc
from typing import Any
import loguru

from src import utils


class MsSql:
    def __init__(self, db_name: str, server: str, user_id: str, password: str):
        connectionString = (
            "Driver={ODBC Driver 18 for SQL Server};"
            f"Server={server};"
            f"Database={db_name};"
            f"uid={user_id};"
            f"pwd={password};"
            "TrustServerCertificate=yes;"
        )
        connection = pyodbc.connect(connectionString, autocommit=True)
        self.cursor = connection.cursor()

    def get_data(
        self,
        table_name: str,
        n_rows: int | None = None,
        condition: dict[str, Any] | None = None,
    ) -> pd.DataFrame:
        request_builder = [f"SELECT"]
        if n_rows is not None:
            request_builder.append(f" TOP {n_rows}")
        request_builder.append(f" * FROM {table_name}")
        if condition is not None:
            where_str = utils.get_condition_str(condition)
            request_builder.append(f" WHERE {where_str}")
        request_builder.append(";")
        request = "".join(request_builder)

        self.cursor.execute(request)
        data = self.cursor.fetchall()

        self.cursor.execute(
            f"""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME='{table_name}'"""
        )

        columns = [row[0] for row in self.cursor.fetchall()]
        df = pd.DataFrame.from_records(data, columns=columns)
        return df

    def insert_row(self, table_name: str, row: tuple[Any, ...]):
        row_str = ", ".join(map(str, row))
        self.cursor.execute(f"""INSERT INTO {table_name} VALUES ({row_str});""")

    def update_row(
        self,
        table_name: str,
        update_condition: dict[str, Any],
        updated_values: dict[str, Any],
    ):
        set_str = ", ".join(
            [f"{key}={value}" for key, value in updated_values.items()]
        )
        where_str = utils.get_condition_str(update_condition)
        self.cursor.execute(
            f"""UPDATE {table_name} SET {set_str} WHERE {where_str}"""
        )

    def delete_row(self, table_name, condition: dict[str, Any]):
        self.cursor.execute(
            f"""DELETE FROM {table_name} WHERE {utils.get_condition_str(condition)}"""
        )
