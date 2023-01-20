import math

def findSmallestMSEAndIdealFunction(trainf, idealf_list):
    '''
    Finds the smallest Mean Square Error for a given function(trainf) and a list of functions(idealf_list)
            Parameters:
                    trainf (TrainingFunction): the given training function
                    idealf_list (list of IdealFunction): a list of all ideal functions
    '''
    # loop through given list of ideal functions
    for ideal in idealf_list:
        squared_error = 0
        row = 0
        # loop through all y values of the training function
        for value in range(0, trainf.length): 
            # calculate the squared error between y of train and y of ideal
            squared_error += (trainf.y_values[row] - ideal.y_values[row]) ** 2
            row += 1
        
        # mean squared error = squared error / amount of data records
        mse = squared_error / trainf.length
        # if mse smaller than current trainf.mse, replace it with the smaller value 
        if(mse < trainf.mse): 
            trainf.mse = mse
            # saving the ideal function, as the smallest mse also reveals the best fitting ideal function
            trainf.matching_ideal_f = ideal
        
    print ('the smallest MSE for training function', trainf.name, ' is: ', trainf.mse, ' in ideal function: ', trainf.matching_ideal_f.name)

def findMaxDelta(trainf):
    '''
    Finding the biggest deviation for a given TrainingFunction (trainf.max_delta)
    The deviation describes the delta between the TrainingFunction y_values and the corresponding IdealFunction y_values
            Parameters:
                    trainf (TrainingFunction): the given training function
    '''
    row = 0
    # loop through all data records of one training function
    for value in range(0, trainf.length): 
        # calculate the deviation between train y and ideal y
        delta = (trainf.y_values[row] - trainf.matching_ideal_f.y_values[row])
        # if delta is bigger than current max_delta, exchange it 
        if delta > trainf.max_delta:
            trainf.max_delta = delta
        row += 1
    print('the biggest delta in Training Function', trainf.name,  "is: ", trainf.max_delta)


def findIdealFunctionsForTestData(test_values, training_functions):
    '''
    Finding best fitting ideal functions for given Test data sets
            Parameters:
                    test_values (TestFunction): the given Test Values
                    training_functions (list of TrainingFunction): a list of all 4 training functions
    '''
    i = 0    
    # iterating through all test values
    while i < len(test_values):
        # iterating through all 4 training functions.
        # the Object Training function is used to acces it's matching ideal functions 
        for trainf in training_functions:
            # using the .index() method to find the correct row in training_functions 
            # for given x value of test values, as the test value table is not sorted, 
            matching_row = trainf.x_values.index(test_values[i].x_values)
            # saving the current iterator index of the foor loop
            index_trainf = training_functions.index(trainf)
            # declaring an array with 4 values, one delta value for every ideal function
            delta = [0,0,0,0]
            # calculating the distance between training y and test y 
            # with .abs() method to get a positive result 
            delta[index_trainf] = (abs(trainf.matching_ideal_f.y_values[matching_row] - test_values[i].y_values))
            
            # if the delta is smaller than the biggest deviation between training function and ideal function * sqrt2
            if delta[index_trainf] < (float(trainf.max_delta) * math.sqrt(2)): 
                # save the ideal function name in the current TestFunction object 
                test_values[i].matching_ideal_f_name = trainf.matching_ideal_f.name
                # save the delta in the current TestFunction object 
                test_values[i].delta = delta[index_trainf]
        i += 1