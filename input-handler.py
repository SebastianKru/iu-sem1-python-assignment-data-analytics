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

# declare strings of csv file names
train_csv_name = "train.csv"
test_csv_name = "test.csv"
ideal_csv_name = "ideal.csv"

train_file = test_file = ideal_file = None

# import the data from csv files. 
# 1. find the files within the project folder by appending "csv_name" to the path 
# 2. save csv file content with pd.read_csv and return it
def importCSV(csv_name):
    proj_path = os.path.dirname(sys.argv[0])
    input_folder_path = "input-data"
    filePath = os.path.join(proj_path, input_folder_path, csv_name)
    print(csv_name, " file path: ", filePath)
    csv_File = pd.read_csv(filepath_or_buffer=filePath, sep=';', encoding="UTF-8")
    print(csv_File)
    return csv_File,

train_file = importCSV(train_csv_name)
#test_file = importCSV(test_csv_name)
#ideal_file = importCSV(ideal_csv_name)


def createTablesFromCSV():
    engine = db.create_engine("mysql+pymysql://root:password@localhost/ui-sem1-python-assignment")
    connection = engine.connect()
    meta_data = db.MetaData()

    training_data = db.Table(
        "Training Data", meta_data,
        db.Column("X", db.Float, primary_key=True),
        db.Column("Y1(training func)", db.Float),
        db.Column("Y2(training func)", db.Float),
        db.Column("Y3(training func)", db.Float), 
        db.Column("Y4(training func)", db.Float)
    )

    meta_data.create_all(engine)


createTablesFromCSV()



