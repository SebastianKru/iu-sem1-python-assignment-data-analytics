from unicodedata import numeric
import sqlalchemy as db 
from sqlalchemy import inspect
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text, column
import CSV_SQLHelper
import PandasHelper
import Functions
import Calculations
import VisualizationHelper


#Fehler abfangen: filePath does not exist 
#Fehler abfangen: anzahl der zeilen != 40 
#Objektorientierung. Klasse mit x und y wert anlegen und vererben zu klasse training data, test data und ideal data klasse 

def main(): 

    # creating the engine for root user @ localhost 
    # and initialising all needed variables wo work with the SQL DB
    engine = db.create_engine("mysql+pymysql://root:password@localhost/ui-sem1-python-assignment")
    meta_data = db.MetaData()
    meta_data.create_all(engine)
    Session = sessionmaker(bind = engine)
    session = Session()

    # saving  file paths of the given csv files as string. 
    # csv files are located in the sub folder /input-data
    train_file_path = CSV_SQLHelper.getCSVFilePath("train.csv")
    test_file_path = CSV_SQLHelper.getCSVFilePath("test.csv")
    ideal_file_path = CSV_SQLHelper.getCSVFilePath("ideal.csv")

    # creating a pandas dataframe from each of the given csv files
    train_table_df = PandasHelper.createPandasDF(train_file_path)
    ideal_table_df = PandasHelper.createPandasDF(ideal_file_path)
    test_table_df = PandasHelper.createPandasDF(test_file_path)

    # altering the column names of the dataframes with training data and ideal data
    # according to the example given
    PandasHelper.alterColumnNames(train_table_df, 'x','X','y','Y', ' (training func)')
    PandasHelper.alterColumnNames(ideal_table_df, 'x','X','y','Y', ' (ideal func)')

    # creating sql tables for train, ideal and test dataframes 
    train_table = CSV_SQLHelper.createTablesFromDF("TrainingData", train_table_df, engine, meta_data)
    ideal_table = CSV_SQLHelper.createTablesFromDF("IdealFunctions", ideal_table_df, engine, meta_data)
    test_table = CSV_SQLHelper.createTablesFromDF("TestingData", test_table_df, engine, meta_data)

    # loading all values from the sql tables train, ideal, test into seperate 2 dimensional arrays 
    # this step could be skipped as I could work with the pandas dataframes, but it was a good exercise 
    # to retrieve data from a sql db
    train_array = CSV_SQLHelper.sqlToArray(session, train_table, len(train_table_df.axes[1]))
    ideal_array = CSV_SQLHelper.sqlToArray(session, ideal_table, len(ideal_table_df.axes[1]))
    test_array = CSV_SQLHelper.sqlToArray(session, test_table, len(test_table_df.axes[1]))

    # creating objects of type TrainingFunction, IdealFunction and TestFunction
    training_functions = Functions.createFunctions(len(train_table_df.axes[1]), train_array, Functions.TrainingFunction)
    ideal_functions = Functions.createFunctions(len(ideal_table_df.axes[1]), ideal_array, Functions.IdealFunction)
    test_values = Functions.createTestValuePairs(len(test_array[0]), test_array, Functions.TestValue)

    # calculating the smalles MeanSquareError for every training function 
    # finding the ideal function for every training function 
    # calculating the biggest deviation (maxDelta) between training data values und ideal data values 
    for tf in training_functions: 
        Calculations.findSmallestMSEAndIdealFunction(tf, ideal_functions)
        Calculations.findMaxDelta(tf)

    # mapping the test data to suitable ideal functions
    Calculations.findIdealFunctionsForTestData(test_values, training_functions)

    # creating a pandas dataframe based on the list test_vales of Type TestFunction
    test_df = PandasHelper.createTestDataFrame(test_values)
    # creating an SQL table based on the pandas dataframe test_df 
    test_table = CSV_SQLHelper.createTablesFromDF('Test Data with Ideal Funcitons', test_df, engine, meta_data)

    # visualizing the functions with the help of bokeh library 
    VisualizationHelper.plotGraphs(training_functions, test_values)

    

if __name__ == '__main__':
    main()

