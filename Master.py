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

