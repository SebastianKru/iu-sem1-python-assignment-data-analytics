import pandas as pd 

# create a pandas Data Frame for the given csv file
# return the pandas Data Frame 
def createPandasDF(file_path):
    with open(file_path, 'r') as file:
        pandas_df = pd.read_csv(file, sep=',', encoding="UTF-8")
    return pandas_df 

# loop over the pandas dataframe and change the column headings 
# e.g. from lowercase x to uppercase X and lowercase y to uppercase Y
def alterColumnNames(table_df, x, x_new, y, y_new, y_label):
    number_of_cols = len(table_df.axes[1])
    i = 1

    table_df.rename(columns = {x:x_new}, inplace = True)
    while i < number_of_cols: 
        table_df.rename(columns = {y + str(i):y_new + str(i) + y_label}, inplace = True)
        i+=1

def createTestDataFrame(test_values):
    test_df = pd.DataFrame({'X (test func)': pd.Series(dtype='float'),
                            'Y (test func)': pd.Series(dtype='float'),
                            'Delta Y (test func)': pd.Series(dtype='float'),
                            'Ideal Function': pd.Series(dtype='str')})
    x = [] 
    y = []
    delta = [] 
    idealf = []

    #i = 0
    #while i < len(test_values):
    for t in test_values:
        x.append(t.x_values)
        y.append(t.y_values)
        delta.append(t.delta)
        idealf.append(t.matching_ideal_f_name)
        #i += 1
    
    test_df['X (test func)'] = x
    test_df['Y (test func)'] = y
    test_df['Delta Y (test func)'] = delta
    test_df['Ideal Function'] = idealf

    return test_df