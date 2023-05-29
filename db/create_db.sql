IF NOT EXISTS(SELECT * FROM sys.databases WHERE name='WineQuality') BEGIN
    CREATE DATABASE WineQuality;
END
GO
USE WineQuality;
GO
IF NOT EXISTS(SELECT * FROM sysobjects WHERE name='Wines' and xtype='U') BEGIN
    CREATE TABLE Wines(
        [wine type] TINYINT,
        [fixed acidity] FLOAT,
        [volatile acidity] FLOAT,
        [citric acid] FLOAT,
        [residual sugar] FLOAT,
        chlorides FLOAT,
        [free sulfur dioxide] FLOAT,
        [total sulfur dioxide] FLOAT,
        density FLOAT,
        pH FLOAT,
        sulphates FLOAT,
        alcohol FLOAT,
        quality TINYINT
    );
END
GO
IF NOT EXISTS(SELECT * FROM sysobjects WHERE name="Metrics" and xtype="U") BEGIN
    CREATE TABLE Metrics(
        modelId NVARCHAR(50) PRIMARY KEY,
        accuracy FLOAT,
        f1Micro FLOAT
    );
END
GO