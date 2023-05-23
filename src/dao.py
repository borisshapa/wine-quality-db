import pyodbc

connectionString = ("Driver={SQL Server Native Client 11.0};"
                    "Server=mssql,1433"
                    "Database=audTv;"
                    "Trusted_Connection=yes")

if __name__ == "__main__":
    connection = pyodbc.connect(connectionString, autocommit=True)
    cursor = connection.cursor()
