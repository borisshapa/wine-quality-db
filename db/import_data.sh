#!/bin/bash

for i in {1..50};
do
    /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P Password123 -i create_db.sql
    if [ $? -eq 0 ]
    then
        echo "setup.sql completed"
        break
    else
        echo "not ready yet..."
        sleep 1
    fi
done

/opt/mssql-tools/bin/bcp WineQuality.dbo.Wines in "/data/train_val.csv" -c -t';' -F2 -S localhost -U SA -P Password123