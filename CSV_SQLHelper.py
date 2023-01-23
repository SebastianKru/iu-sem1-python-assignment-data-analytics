import os 
import sqlalchemy as db 
import sys 
from CustomException import CustomParameterException


class Table_Helper: 
    """
    A helper class for  CSV import and SQL related functions
    """

    def getCSVFilePath(self, csv_name):
        '''
        Gets a system file path for a given csv file name. Looks in the specified directory "input-data"
            Parameters:
                csv_name (string): The name of a csv file
            Returns:
                filePath (string): The System File Path leading to the csv_name file in "input_data" folder
        '''
        proj_path = os.path.dirname(sys.argv[0])
        input_folder_path = "input-data"
        try: 
            filePath = os.path.join(proj_path, input_folder_path, csv_name)
        except: 
            raise CustomParameterException(filePath, "File path wrong")
        else:     
            return filePath

    def createTablesFromDF(self, table_name, pandas_df, eng, meta_d):
        '''
        Gets a system file path for a given csv file name. Looks in the specified directory "input-data"
            Parameters:
                table_name (string):    The name which will be used to name the SQL Table
                pandas_df  (DataFrame): a Data Frame, which holds the table values, used for the SQL Table 
                eng        (Engine):    The Engine Object of SQL server
                meta_d     (MetaDta):   The MetaData Object of SQL Server     
            Returns:
                table (Table): The SQL Table Object
        '''
        pandas_df.to_sql(table_name, con=eng, index=False, if_exists='replace')
        table = db.Table(table_name, meta_d, autoload=True, autoload_with = eng)
        return table

    def sqlToArray(self, session, table, nr_of_columns):
        '''
        HelperFunction. Reads an SQL Table and transforms the Table into a 2 dimensional array. 
        I could have skipped this step and work with the Pandas DF instead, but I wanted to
            a) load data from the SQL Table to mimic the optimal Data Engineering process 
            b) use as many data types as possible and therefore included the two dimensional array 
            Parameters:
                session       (Session): The SQL Session
                table         (Table):   The SQL Table
                nr_of_columns (int):     Amount of columns  
            Returns:
                two_dim_array (list):    The SQL Table transformed to a two dimensional array 
        '''
        sqlTable = session.query(table).all()
        two_dim_array = []
        i = 0
        # loop through each column of the sql table 
        while i < nr_of_columns:
            col = []
            # loop through rows of column
            for column in sqlTable:
                # add all the data in one column one by one to temp array col[]
                col.append(column[i])
            # append the columns one by one to the two_dim_array
            two_dim_array.append(col)
            i+=1
        return two_dim_array