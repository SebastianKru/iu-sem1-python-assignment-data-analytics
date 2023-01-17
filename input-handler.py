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
#import sqlalchemy
from alembic import op
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import inspect
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text, column

#Fehler abfangen: filePath does not exist 
#Fehler abfangen: anzahl der zeilen != 40 
#Objektorientierung. Klasse mit x und y wert anlegen und vererben zu klasse training data, test data und ideal data klasse 

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

# loop over the pandas dataframe and change the column headings 
# e.g. from lowercase x to uppercase X and lowercase y to uppercase Y
def alterColumnNames(table_df, x, x_new, y, y_new, y_label):
    number_of_cols = len(table_df.axes[1])
    i = 1

    table_df.rename(columns = {x:x_new}, inplace = True)
    while i < number_of_cols: 
       table_df.rename(columns = {y + str(i):y_new + str(i) + y_label}, inplace = True)
       i+=1

#def getColumnByID(table, columnID, connection):
#    selector = db.select([table.columns[columnID]])
#    column = connection.execute(selector).fetchall()
#    return column

def sqlToArray(session, table, nr_of_columns):
    sqlTable = session.query(table).all()
    two_dim_array = []
    i = 0
    while i < nr_of_columns:
        col = []
        for column in sqlTable:
            col.append(column[i])
        two_dim_array.append(col)
        i+=1
    return two_dim_array


class BaseFunction(object): 
    def __init__(self, x, y):
        self.x_values = x
        self.y_values = y

class TrainingFunction(BaseFunction): 
    name = ""
    ideal_function = None
    mse = None
    max_delta = None  
    length = None

    def __init__(self, x, y, name):
        super().__init__(x, y)
        self.name = name
        self.length = len(self.x_values)

class TestFunction(BaseFunction): 
    pass

def calculateSmallestMSE(tf, ideal_array):
    columns_ideal_array = len(ideal_array) 
    col = 1
    mse_array = []

    while col < columns_ideal_array:
        squared_error = 0
        row = 0
        for value in range(0, tf.length): 
            squared_error += (tf.y_values[row] - ideal_array[col][row]) ** 2
            row += 1
        mse_array.append(squared_error / tf.length)
        #print('mse of ', col, ' = ', mse_array[col-1])
        col += 1

    tf.mse = mse_array[0]
    for i in range(0, len(mse_array)):
        if mse_array[i] < tf.mse:
            tf.mse = mse_array[i]
            tf.ideal_function = i

    #ideal function, loop through rows to find biggest deviation 
    deltas = []
    row = 0
    for value in range(0, tf.length): 
       deltas.append(tf.y_values[row] - ideal_array[tf.ideal_function ][row])
       row += 1
    
    tf.max_delta = deltas[0]
    for i in range(0, len(deltas)):
        if deltas[i] > tf.max_delta: 
            tf.max_delta = deltas[i]

    print ('the smallest MSE for training function', tf.name, ' is: ', 
    tf.mse, ' in ideal function: ', tf.ideal_function)
    print('the biggest delta is: ', tf.max_delta)


def main(): 
    engine = db.create_engine("mysql+pymysql://root:password@localhost/ui-sem1-python-assignment")
    connection = engine.connect()
    meta_data = db.MetaData()

    meta_data.create_all(engine)
    Session = sessionmaker(bind = engine)
    session = Session()

    train_file_path = getCSVFilePath(train_csv_name)
    test_file_path = getCSVFilePath(test_csv_name)
    ideal_file_path = getCSVFilePath(ideal_csv_name)

    train_table_df = createPandasDF(train_file_path)
    ideal_table_df = createPandasDF(ideal_file_path)
    test_table_df = createPandasDF(test_file_path)

    alterColumnNames(train_table_df, 'x','X','y','Y', '_training_func')
    alterColumnNames(ideal_table_df, 'x','X','y','Y', '(ideal-func)')

    train_table = createTablesFromDF(train_table_name, train_table_df, engine, meta_data)
    ideal_table = createTablesFromDF(ideal_table_name, ideal_table_df, engine, meta_data)
    test_table = createTablesFromDF(test_table_name, test_table_df, engine, meta_data)

    train_array = sqlToArray(session, train_table, len(train_table_df.axes[1]))
    ideal_array = sqlToArray(session, ideal_table, len(ideal_table_df.axes[1]))

    tf1 = TrainingFunction(train_array[0], train_array[1], "Training Function 1")
    tf2 = TrainingFunction(train_array[0], train_array[2], "Training Function 2")
    tf3 = TrainingFunction(train_array[0], train_array[3], "Training Function 3")
    tf4 = TrainingFunction(train_array[0], train_array[4], "Training Function 4")

    calculateSmallestMSE(tf1, ideal_array)
    calculateSmallestMSE(tf2, ideal_array)
    calculateSmallestMSE(tf3, ideal_array)
    calculateSmallestMSE(tf4, ideal_array)



if __name__ == '__main__':
    main()

