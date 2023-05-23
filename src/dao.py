import pyodbc

connectionString = ("Driver={ODBC Driver 18 for SQL Server};"
                    "Server=mssql,1433"
                    "Database=audTv;"
                    "Trusted_Connection=yes")

if __name__ == "__main__":
    connection = pyodbc.connect(connectionString, autocommit=True)
    cursor = connection.cursor()
