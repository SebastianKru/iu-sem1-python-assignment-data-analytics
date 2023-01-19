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
import math

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


class IdealFunction(BaseFunction):
    #max_delta = None
    column = None
    def __init__(self, x, y, name):
        super().__init__(x, y)
        self.name = name


class TrainingFunction(BaseFunction): 
    name = ""
    ideal_function = None
    mse = 9999999
    max_delta = 0  
    length = None
    matching_ideal_f = None

    def __init__(self, x, y, name):
        super().__init__(x, y)
        self.name = name
        self.length = len(self.x_values)


class TestFunction(BaseFunction): 
    delta = [0,0,0,0]

    def __init__(self, x, y, matching_function):
        super().__init__(x, y)
        self.matching_function = matching_function

def calculateSmallestMSE(trainf, idealf):

    for ideal in idealf:
        squared_error = row = 0
        for value in range(0, trainf.length): 
            squared_error += (trainf.y_values[row] - ideal.y_values[row]) ** 2
            row += 1
        
        mse = squared_error / trainf.length
        if(mse < trainf.mse): 
            trainf.mse = mse
            trainf.matching_ideal_f = ideal

    #ideal function, loop through rows to find biggest deviation 
    row = 0
    for value in range(0, trainf.length): 
        delta = (trainf.y_values[row] - trainf.matching_ideal_f.y_values[row])
        if delta > trainf.max_delta:
            trainf.max_delta = delta
        row += 1

    print ('the smallest MSE for training function', trainf.name, ' is: ', 
    trainf.mse, ' in ideal function: ', trainf.matching_ideal_f.name)
    print('the biggest delta is: ', trainf.max_delta)

def calculateSmallestMSE2(tf, ideal_array):
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
            #tf.matching_ideal_f.column = i

    #ideal function, loop through rows to find biggest deviation 
    deltas = []
    row = 0
    for value in range(0, tf.length): 
        tf.matching_ideal_f = IdealFunction(ideal_array[0], ideal_array[tf.ideal_function]) 
        deltas.append(tf.y_values[row] - ideal_array[tf.ideal_function ][row])
        print(tf.matching_ideal_f.x_values[row], " ", tf.matching_ideal_f.y_values[row])
        row += 1
    
    tf.max_delta = deltas[0]
    for i in range(0, len(deltas)):
        if deltas[i] > tf.max_delta: 
            tf.max_delta = deltas[i]
            tf.matching_ideal_f.max_delta = deltas[i]

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
    test_array = csv_sql_helper.sqlToArray(session, test_table, len(test_table_df.axes[1]))

    training_functions = []
    i = 1
    while i < len(train_table_df.axes[1]):
        training_functions.append(TrainingFunction(train_array[0], train_array[i], "Training Function {}".format(i)))
        i += 1

    ideal_functions = []
    i = 1
    while i < len(ideal_table_df.axes[1]):
        ideal_functions.append(TrainingFunction(ideal_array[0], ideal_array[i], "Y {}".format(i)))
        i += 1

    for tf in training_functions: 
        calculateSmallestMSE(tf, ideal_functions)


    #test_function = TestFunction(test_array[0], test_array[1])

    test_values = []
    i = 0
    while i < len(test_array[0]):
        test_values.append(TestFunction(test_array[0][i], test_array[1][i], None))
        i+= 1


    index = 0    
    while index < len(test_values):
        smallestValue = 99999999999
        # differenz zw test und train berechnen 


        for trainfunc in training_functions:
            matching_index = trainfunc.x_values.index(test_values[index].x_values)
            test_values[index].delta[training_functions.index(trainfunc)] = (
                abs(trainfunc.y_values[matching_index] - test_values[index].y_values))

        # check if calculated deltas are smaller than the largest delta existing for the 4 functions 
        # save the 4 results 

        #for t in test_values[index].delta:
            #print("the delta for test value x: ", test_values[index].x_values, "at index: ", index, " is ", t)
        #print()
        index += 1

        #training_functions[0-4].x_values[test_values[index]]
        #for trainfunc in training_functions:
        #    if ((abs(test_values[index].y_values) < (float(trainfunc.max_delta)) * math.sqrt(2))
        #    and (trainfunc.max_delta < smallestValue)): 
        #        smallestValue = trainfunc.max_delta 
        #        test_values[index].matching_function = trainfunc.ideal_function
        #        #print(test_values[index].x_values, "y value  ", test_values[index].y_values, "smallest value: ", smallestValue, "matching function: ", trainfunc.ideal_function)
        #index += 1

   # for t in test_values:
   #     print("best match for ", t.x_values , ", ", t.y_values, 
   #     " is ", t.matching_function)


 ##### make testfunction oly one value par of x and y and create a list with for x in test.x.len 
 # base class x und y ### vererbung wertepaar # vererbung array of wertepaar 

if __name__ == '__main__':
    main()

