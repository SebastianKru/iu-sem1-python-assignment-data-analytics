import pandas as pd 
from CustomException import CustomParameterException

class PD_Helper:
    """
    A helper class to handle custom interactions with pandas  
    """

    def createPandasDF(file_path):
        '''
        create a pandas Data Frame for a given csv file, if the file path exists
            Parameters:
                file_path (string): The local file path to the csv file
            Returns:
                pandas_df (DataFrame): return the pandas Data Frame 
        '''
        try: 
            with open(file_path, 'r') as file:
                pandas_df = pd.read_csv(file, sep=',', encoding="UTF-8")
        except:
            raise CustomParameterException(file_path, "File path wrong")
        else:
            return pandas_df 


    def alterColumnNames(table_df, x, x_new, y, y_new, y_label):
        '''
        loop over the pandas dataframe and change the column headings 
        e.g. from lowercase x to uppercase X and lowercase y to uppercase Y
            Parameters:
                table_df (string): The local file path to the csv file
                x        (string): The current name of the x column
                x_new    (string): The new name of the x column
                y        (string): The current name of the y column
                y_new    (string): The new name of the y column
                y_label  (string): additional ending for the y column 
            Returns:
        '''
        number_of_cols = len(table_df.axes[1])
        i = 1

        if x in table_df.columns:
            table_df.rename(columns = {x:x_new}, inplace = True)
        else:
            raise CustomParameterException(x, "Column name does not exist")
        
        
        while i < number_of_cols:
            if (y + str(i)) in table_df.columns:
                table_df.rename(columns = {y + str(i):y_new + str(i) + y_label}, inplace = True)
                i+=1
            else:       
                raise CustomParameterException(y, "Column name does not exist")


           
    def createTestDataFrame(test_values):
        '''
        loop through the two dimenisonal list and create a pd DataFrame with given column names 
            Parameters:
                test_values (list): a two dimensional list

            Returns:
                test_df (DataFrame): the DataFrame, created from the fiven two dimensional list 
        '''
        test_df = pd.DataFrame({'X (test func)': pd.Series(dtype='float'),
                                'Y (test func)': pd.Series(dtype='float'),
                                'Delta Y (test func)': pd.Series(dtype='float'),
                                'Ideal Function': pd.Series(dtype='str')})
        x = [] 
        y = []
        delta = [] 
        idealf = []

        for t in test_values:
            x.append(t.x_values)
            y.append(t.y_values)
            delta.append(t.delta)
            idealf.append(t.matching_ideal_f_name)
        
        test_df['X (test func)'] = x
        test_df['Y (test func)'] = y
        test_df['Delta Y (test func)'] = delta
        test_df['Ideal Function'] = idealf

        return test_df