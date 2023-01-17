import pandas as pd 

class PD_Helper(object):

    # create a pandas Data Frame for the given csv file
    # return the pandas Data Frame 
    def createPandasDF(self, file_path):
        with open(file_path, 'r') as file:
            pandas_df = pd.read_csv(file, sep=',', encoding="UTF-8")
        return pandas_df 

    # loop over the pandas dataframe and change the column headings 
    # e.g. from lowercase x to uppercase X and lowercase y to uppercase Y
    def alterColumnNames(self, table_df, x, x_new, y, y_new, y_label):
        number_of_cols = len(table_df.axes[1])
        i = 1

        table_df.rename(columns = {x:x_new}, inplace = True)
        while i < number_of_cols: 
            table_df.rename(columns = {y + str(i):y_new + str(i) + y_label}, inplace = True)
            i+=1