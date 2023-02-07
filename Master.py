from unicodedata import numeric
import sqlalchemy as db 
from sqlalchemy import inspect
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text, column
from CSV_SQLHelper import Table_Helper
from PandasHelper import PD_Helper
import Functions
from Functions import F_Creator
from CalculationsHelper import Calculations
from VisualizationHelper import Visualization

def main(): 
    # creating the engine for root user @ localhost 
    # and initialising all needed variables wo work with the SQL DB
    engine = db.create_engine("mysql+pymysql://root:password@localhost/ui-sem1-python-assignment")
    meta_data = db.MetaData()
    meta_data.create_all(engine)
    Session = sessionmaker(bind = engine)
    session = Session()


    table_helper = Table_Helper()
    # saving  file paths of the given csv files as string. 
    # csv files are located in the sub folder /input-data
    train_file_path = table_helper.getCSVFilePath("train.csv")
    test_file_path = table_helper.getCSVFilePath("test.csv")
    ideal_file_path = table_helper.getCSVFilePath("ideal.csv")

    # creating a pandas dataframe from each of the given csv files
    train_table_df = PD_Helper.createPandasDF(train_file_path)
    ideal_table_df = PD_Helper.createPandasDF(ideal_file_path)
    test_table_df = PD_Helper.createPandasDF(test_file_path)

    # altering the column names of the dataframes with training data and ideal data
    # according to the example given
    PD_Helper.alterColumnNames(train_table_df, 'x','X','y','Y', ' (training func)')
    PD_Helper.alterColumnNames(ideal_table_df, 'x','X','y','Y', ' (ideal func)')

    # creating sql tables for train, ideal and test dataframes 
    train_table = table_helper.createTablesFromDF("TrainingData", train_table_df, engine, meta_data)
    ideal_table = table_helper.createTablesFromDF("IdealFunctions", ideal_table_df, engine, meta_data)
    test_table = table_helper.createTablesFromDF("TestingData", test_table_df, engine, meta_data)

    # loading all values from the sql tables train, ideal, test into seperate 2 dimensional arrays 
    # this step could be skipped as I could work with the pandas dataframes, but it was a good exercise 
    # to retrieve data from a sql db
    train_array = table_helper.sqlToArray(session, train_table, len(train_table_df.axes[1]))
    ideal_array = table_helper.sqlToArray(session, ideal_table, len(ideal_table_df.axes[1]))
    test_array = table_helper.sqlToArray(session, test_table, len(test_table_df.axes[1]))

    # creating objects of type TrainingFunction, IdealFunction and TestFunction
    training_functions = F_Creator.createFunctions(len(train_table_df.axes[1]), train_array, Functions.TrainingFunction)
    ideal_functions = F_Creator.createFunctions(len(ideal_table_df.axes[1]), ideal_array, Functions.IdealFunction)
    test_values = F_Creator.createTestValuePairs(len(test_array[0]), test_array, Functions.TestValue)

    # calculating the smalles MeanSquareError for every training function 
    # finding the ideal function for every training function 
    # calculating the biggest deviation (maxDelta) between training data values und ideal data values 
    for tf in training_functions: 
        Calculations.findSmallestMSEAndIdealFunction(tf, ideal_functions)
        Calculations.findMaxDelta(tf)

    # mapping the test data to suitable ideal functions
    Calculations.findIdealFunctionsForTestData(test_values, training_functions)

    # creating a pandas dataframe based on the list test_vales of Type TestFunction
    test_df = PD_Helper.createTestDataFrame(test_values)
    # creating an SQL table based on the pandas dataframe test_df 
    test_table = table_helper.createTablesFromDF('Test Data with Ideal Funcitons', test_df, engine, meta_data)

    # visualizing the functions with the help of bokeh library 
    Visualization.plotGraphs(training_functions, test_values)

if __name__ == '__main__':
    main()