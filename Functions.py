
class BaseFunction(object): 
    def __init__(self, x, y):
        self.x_values = x
        self.y_values = y


class IdealFunction(BaseFunction):
    #max_delta = None
    column = None
    def __init__(self, x, y, name):
        super().__init__(x, y)
        self.name = name


class TrainingFunction(BaseFunction): 
    mse = 9999999
    max_delta = 0  
    # will be assigned withObject of Type IdealFunction
    matching_ideal_f = None

    def __init__(self, x, y, name):
        super().__init__(x, y)
        self.name = name
        self.length = len(self.x_values)


class TestFunction(BaseFunction): 
    delta = None
    matching_ideal_f_name = None
    def __init__(self, x, y):
        super().__init__(x, y)


def createFunctions(length, table_array, function_type):
    functions = []
    i = 1
    while i < length:
        functions.append(function_type(table_array[0], table_array[i], "Y {}".format(i)))
        i += 1
    return functions

def createTestValuePairs(length, table_array, function_type):
    value_pairs = []
    i = 0
    while i < length:
        value_pairs.append(function_type(table_array[0][i], table_array[1][i]))
        i+= 1
    return value_pairs