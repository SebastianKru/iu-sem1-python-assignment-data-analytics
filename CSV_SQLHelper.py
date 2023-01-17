import os 
import sqlalchemy as db 
import sys 

class CSV_SQL_Helper(object): 

    # get the csv file paths. csv files are in the folder "input-data"
    # return the file path of given csv_name
    def getCSVFilePath(self, csv_name):
        proj_path = os.path.dirname(sys.argv[0])
        input_folder_path = "input-data"
        filePath = os.path.join(proj_path, input_folder_path, csv_name)
        return filePath

    # use a given pandas Data Frame to create a sql table 
    # return the sql table 
    def createTablesFromDF(self, table_name, pandas_df, eng, meta_d):
        pandas_df.to_sql(table_name, con=eng, index=False, if_exists='replace')
        table = db.Table(table_name, meta_d, autoload=True, autoload_with = eng)
        return table

    def sqlToArray(self, session, table, nr_of_columns):
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