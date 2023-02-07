import math
from decimal import Decimal


def calculateMSE(train_y, ideal_y, row):
    '''
    calculates the MSE between 2 given lists
            Parameters:
                    train_y (list): y values of the given training function
                    ideal_y (list): y values of the given ideal function
    ''' 
    squared_error = 0
    for value in range(0, len(train_y)): 
        squared_error += (train_y[row] - ideal_y[row]) ** 2
        row += 1
    mse = squared_error / len(train_y)
    return mse

def calculateRMSE(train_y, ideal_y, row): 
    '''
    calculates the RMSE between 2 given lists
            Parameters:
                    train_y (list): y values of the given training function
                    ideal_y (list): y values of the given ideal function
    ''' 
    squared_error = 0
    for value in range(0, len(train_y)): 
        squared_error += (train_y[row] - ideal_y[row]) ** 2
        row += 1
    rmse = math.sqrt(squared_error / len(train_y))
    return rmse

def calculateMAE(train_y, ideal_y, row): 
    '''
    calculates the MAE between 2 given lists
            Parameters:
                    train_y (list): y values of the given training function
                    ideal_y (list): y values of the given ideal function
    ''' 
    absolute_error = 0
    for value in range(0, len(train_y)): 
        absolute_error += abs(train_y[row] - ideal_y[row])
        row += 1
    mae = absolute_error / len(train_y)
    return mae

def calculateMAPE(train_y, ideal_y, row): 
    '''
    calculates the MAPE between 2 given lists
            Parameters:
                    train_y (list): y values of the given training function
                    ideal_y (list): y values of the given ideal function
    ''' 
    absolute_error = 0
    for value in range(0, len(train_y)): 
        if(ideal_y[row] == 0): 
            absolute_error += abs((train_y[row] - ideal_y[row]) / Decimal(0.01) )
        else: 
            absolute_error += abs((train_y[row] - ideal_y[row]) / ideal_y[row] )  
        row += 1
        
    mape = absolute_error / len(train_y)
    return mape    

def calculateSMAPE(train_y, ideal_y, row): 
    '''
    calculates the SMAPE between 2 given lists
            Parameters:
                    train_y (list): y values of the given training function
                    ideal_y (list): y values of the given ideal function
    ''' 
    absolute_error = 0
    for value in range(0, len(train_y)): 
        absolute_error += abs(train_y[row] - ideal_y[row]) / (
            (abs(train_y[row]) + abs(ideal_y[row])) / 2)
        row += 1
    smape = absolute_error / len(train_y)
    return smape   

def calculateRSquared(train_y, ideal_y, row):
    '''
    calculates the R-Squared between 2 given lists
            Parameters:
                    train_y (list): y values of the given training function
                    ideal_y (list): y values of the given ideal function
    '''  
    r_squared_error = 0
    y_mean = 0
    numerator = 0
    denominator = 0

    i = 0
    for value in range(0, len(train_y)): 
        y_mean += ideal_y
        i += 1
    y_mean = y_mean / len(train_y)
    for value in range(0, len(train_y)): 
        numerator += (train_y[row] - ideal_y[row]) ** 2
        denominator += (y_mean - ideal_y[row]) ** 2
        row += 1

    r_squared_error = 1 - (numerator / denominator)
    return r_squared_error  