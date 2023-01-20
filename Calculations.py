import math

def findSmallestMSEAndIdealFunction(trainf, idealf):
    for ideal in idealf:
        squared_error = row = 0
        for value in range(0, trainf.length): 
            squared_error += (trainf.y_values[row] - ideal.y_values[row]) ** 2
            row += 1
        
        mse = squared_error / trainf.length
        if(mse < trainf.mse): 
            trainf.mse = mse
            trainf.matching_ideal_f = ideal
        
    print ('the smallest MSE for training function', trainf.name, ' is: ', trainf.mse, ' in ideal function: ', trainf.matching_ideal_f.name)

def findMaxDelta(trainf):
    #ideal function, loop through rows to find biggest deviation 
    row = 0
    for value in range(0, trainf.length): 
        delta = (trainf.y_values[row] - trainf.matching_ideal_f.y_values[row])
        if delta > trainf.max_delta:
            trainf.max_delta = delta
        row += 1
    print('the biggest delta in Training Function', trainf.name,  "is: ", trainf.max_delta)


def findIdealFunctionsForTestData(test_values, training_functions):
    i = 0    
    while i < len(test_values):
        for trainf in training_functions:
            matching_row = trainf.x_values.index(test_values[i].x_values)
            index_trainf = training_functions.index(trainf)
            delta = [0,0,0,0]
            delta[index_trainf] = (
                abs(trainf.matching_ideal_f.y_values[matching_row] - test_values[i].y_values))
            
            if delta[index_trainf] < (float(trainf.max_delta) * math.sqrt(2)): 
                test_values[i].matching_ideal_f_name = trainf.matching_ideal_f.name
                test_values[i].delta = delta[index_trainf]

        #print(" x: ", test_values[i].x_values, " y: ",test_values[i].y_values, " delta: ", 
        #test_values[i].delta, " Ideal Function:  ", test_values[i].matching_ideal_f_name)
        i += 1