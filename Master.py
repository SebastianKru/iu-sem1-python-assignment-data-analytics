from unicodedata import numeric
import pandas as pd 
import numpy as np 
import sqlalchemy
import pymysql 
import sqlalchemy as db 
from sqlalchemy import inspect
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text, column
import CSV_SQLHelper
import PandasHelper
import Functions
import Calculations

#Fehler abfangen: filePath does not exist 
#Fehler abfangen: anzahl der zeilen != 40 
#Objektorientierung. Klasse mit x und y wert anlegen und vererben zu klasse training data, test data und ideal data klasse 

train_file_path = test_file_path = ideal_file_path = None
train_table = ideal_table = test_table = None

# declare strings of csv file names
train_csv_name = "train.csv"
test_csv_name = "test.csv"
ideal_csv_name = "ideal.csv"

train_table_name = "TrainingData"
ideal_table_name = "IdealFunctions"
test_table_name = "TestingData"



def main(): 
    engine = db.create_engine("mysql+pymysql://root:password@localhost/ui-sem1-python-assignment")
    connection = engine.connect()
    meta_data = db.MetaData()

    meta_data.create_all(engine)
    Session = sessionmaker(bind = engine)
    session = Session()

    csv_sql_helper = CSV_SQLHelper.CSV_SQL_Helper()
    pd_helper = PandasHelper.PD_Helper()

    train_file_path = csv_sql_helper.getCSVFilePath(train_csv_name)
    test_file_path = csv_sql_helper.getCSVFilePath(test_csv_name)
    ideal_file_path = csv_sql_helper.getCSVFilePath(ideal_csv_name)

    train_table_df = pd_helper.createPandasDF(train_file_path)
    ideal_table_df = pd_helper.createPandasDF(ideal_file_path)
    test_table_df = pd_helper.createPandasDF(test_file_path)

    pd_helper.alterColumnNames(train_table_df, 'x','X','y','Y', '_training_func')
    pd_helper.alterColumnNames(ideal_table_df, 'x','X','y','Y', '(ideal-func)')

    train_table = csv_sql_helper.createTablesFromDF(train_table_name, train_table_df, engine, meta_data)
    ideal_table = csv_sql_helper.createTablesFromDF(ideal_table_name, ideal_table_df, engine, meta_data)
    test_table = csv_sql_helper.createTablesFromDF(test_table_name, test_table_df, engine, meta_data)

    train_array = csv_sql_helper.sqlToArray(session, train_table, len(train_table_df.axes[1]))
    ideal_array = csv_sql_helper.sqlToArray(session, ideal_table, len(ideal_table_df.axes[1]))
    test_array = csv_sql_helper.sqlToArray(session, test_table, len(test_table_df.axes[1]))

    training_functions = Functions.createFunctions(len(train_table_df.axes[1]), train_array, Functions.TrainingFunction)
    ideal_functions = Functions.createFunctions(len(ideal_table_df.axes[1]), ideal_array, Functions.IdealFunction)
    test_values = Functions.createTestValuePairs(len(test_array[0]), test_array, Functions.TestFunction)

    for tf in training_functions: 
        Calculations.findSmallestMSEAndIdealFunction(tf, ideal_functions)
        Calculations.findMaxDelta(tf)

    Calculations.findIdealFunctionsForTestData(test_values, training_functions)

if __name__ == '__main__':
    main()

