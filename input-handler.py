from unicodedata import numeric
import pandas as pd 
import numpy as np 
import config 
import os 
import sys 
import datetime 
import time 
import sqlalchemy
import pymysql 
import sqlalchemy as db 
from alembic import op
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import inspect

# declare strings of csv file names
train_csv_name = "train.csv"
test_csv_name = "test.csv"
ideal_csv_name = "ideal.csv"

train_file_path = test_file_path = ideal_file_path = None

train_table_name = "TrainingData"
ideal_table_name = "IdealFunctions"
test_table_name = "TestingData"

train_table = ideal_table = test_table = None



# get the csv file paths. csv files are in the folder "input-data"
# return the file path of given csv_name
def getCSVFilePath(csv_name):
    proj_path = os.path.dirname(sys.argv[0])
    input_folder_path = "input-data"
    filePath = os.path.join(proj_path, input_folder_path, csv_name)
    return filePath

# create a pandas Data Frame for the given csv file
# return the pandas Data Frame 
def createPandasDF(file_path):
    with open(file_path, 'r') as file:
        pandas_df = pd.read_csv(file, sep=',', encoding="UTF-8")
    return pandas_df 

# use a given pandas Data Frame to create a sql table 
# return the sql table 
def createTablesFromDF(table_name, pandas_df, eng, meta_d):
    pandas_df.to_sql(table_name, con=eng, index=False, if_exists='replace')
    table = db.Table(table_name, meta_d, autoload=True, autoload_with = eng)
    return table

# loop over a sql table and change the column headings 
# e.g. from lowercase x to uppercase X and lowercase y to uppercase Y
def alterColumnNames(engine, table_name, columns, x, x_new, y, y_new, y_label):
    alterOneColumnName(engine, table_name, x, x_new)
    i = 1
    while i < columns: 
       alterOneColumnName(engine, table_name, y + str(i), y_new + str(i) + y_label)
       i+=1

# helper function for 'alterColumntNames' 
# using alembic library to change the heading of a column 
def alterOneColumnName(engine, table, name, name_new):
    # Create migration context
    mc = MigrationContext.configure(engine.connect())
    # Creation operations object
    ops = Operations(mc)
    ops.alter_column(table,column_name = name,new_column_name = name_new,existing_type = db.String(100))

def main(): 
    engine = db.create_engine("mysql+pymysql://root:password@localhost/ui-sem1-python-assignment")
    connection = engine.connect()
    meta_data = db.MetaData()
    meta_data.create_all(engine)

    train_file_path = getCSVFilePath(train_csv_name)
    test_file_path = getCSVFilePath(test_csv_name)
    ideal_file_path = getCSVFilePath(ideal_csv_name)

    train_table_df = createPandasDF(train_file_path)
    ideal_table_df = createPandasDF(ideal_file_path)
    test_table_df = createPandasDF(test_file_path)

    train_table = createTablesFromDF(train_table_name, train_table_df, engine, meta_data)
    ideal_table = createTablesFromDF(ideal_table_name, ideal_table_df, engine, meta_data)
    test_table = createTablesFromDF(test_table_name, test_table_df, engine, meta_data)

    alterColumnNames(engine, train_table_name, train_table_df.shape[1], 'x','X','y','Y', ' (training func)')
    alterColumnNames(engine, ideal_table_name, ideal_table_df.shape[1], 'x','X','y','Y', ' (ideal func)')


if __name__ == '__main__':
    main()