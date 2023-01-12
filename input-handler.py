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

train_table_name ="TrainingData"
ideal_table_name = "IdealFunctions"

train_file_path = test_file_path = ideal_file_path = None

# import the data from csv files. 
# 1. find the files within the project folder by appending "csv_name" to the path 
# 2. save csv file content with pd.read_csv and return it
def getCSVFilePath(csv_name):
    proj_path = os.path.dirname(sys.argv[0])
    input_folder_path = "input-data"
    filePath = os.path.join(proj_path, input_folder_path, csv_name)
    return filePath

def createTablesFromCSV():
    engine = db.create_engine("mysql+pymysql://root:password@localhost/ui-sem1-python-assignment")
    connection = engine.connect()
    inspector = inspect(engine)
    meta_data = db.MetaData()
    meta_data.create_all(engine)

    training_data_table = createTable(engine, meta_data, train_file_path, train_table_name)
    ideal_data_table = createTable(engine, meta_data, ideal_file_path, ideal_table_name)

    alterColumnName(engine, train_table_name,'x','X')
    alterColumnName(engine, train_table_name,'y1','Y1(training func)')
    alterColumnName(engine, train_table_name,'y2','Y2(training func)')
    alterColumnName(engine, train_table_name,'y3','Y3(training func)')
    alterColumnName(engine, train_table_name,'y4','Y4(training func)')

def createTable(engine, meta_data, file_path, table_name):
    with open(file_path, 'r') as file:
        data_df = pd.read_csv(file, sep=',', encoding="UTF-8")
        data_df.to_sql(table_name, con=engine, index=False, if_exists='replace')
    table = db.Table(table_name, meta_data, autoload=True, autoload_with = engine)
    return table


def alterColumnName(engine, table, name, name_new):
    # Create migration context
    mc = MigrationContext.configure(engine.connect())
    # Creation operations object
    ops = Operations(mc)
    ops.alter_column(table,column_name = name,new_column_name = name_new,existing_type = db.String(100))



train_file_path = getCSVFilePath(train_csv_name)
test_file_path = getCSVFilePath(test_csv_name)
ideal_file_path = getCSVFilePath(ideal_csv_name)

createTablesFromCSV()


