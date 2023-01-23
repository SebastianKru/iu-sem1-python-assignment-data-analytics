from CustomException import CustomTextException

class BaseFunction(object): 
    """
    A class to hold x and y values.

    Attributes
    ----------
    x_values : float
        the x value 
    y_values : float
        the y value
    """

    number_of_data_entries = 400

    def __init__(self, x, y):
        self.x_values = x
        self.y_values = y

class IdealFunction(BaseFunction):
    """
    A class inheriting from Base Function.
    The class represents one of the ideal functions

    Attributes
    ----------
    x_values : float
        the x values used as a list
    y_values : float
        the y values used as a list 
    name : string
        the name of the ideal function
    """
    def __init__(self, x, y, name):
        if len(x) == len(y) == self.number_of_data_entries:
            super().__init__(x, y)
            self.name = name
        else: 
            raise Exception(
                "Number of rows is not {}.Check the csv files for correct data input"
                .format(self.number_of_data_entries))

class TrainingFunction(BaseFunction): 
    """
    A class inheriting from Base Function.
    The class represents one of the Training functions

    Attributes
    ----------
    x_values : float
        the x values used as a list
    y_values : float
        the y values used as a list
    name : string
        the name of the ideal function
    length : int 
        the amount of x_values / amount of rows 
    mse : float 
        mean square error between training function and ideal function
    max_delta : float
        biggest deviation between training y and ideal y values 
    matching_ideal_f : IdealFujnction
        the matching functino as an object of IdealFunction
    """

    mse = 9999
    max_delta = 0  
    # will be assigned with Object of Type IdealFunction
    matching_ideal_f = None

    def __init__(self, x, y, name):
        if len(x) == len(y) == self.number_of_data_entries:
            super().__init__(x, y)
            self.name = name
            self.length = len(self.x_values)
        else: 
            raise CustomTextException(
                "Number of rows is not {}.Check the csv files for correct data input"
                .format(self.number_of_data_entries))


class TestValue(BaseFunction):
    """
    A class inheriting from Base Function.
    The class represents a value pair of test values

    Attributes
    ----------
    delta : float
        the deviation between this test y value and the matching ideal function y value 
    matching_ideal_f_name : string
        the name of the matching ideal function like "Y 23"
    """ 
    delta = None
    matching_ideal_f_name = None
    def __init__(self, x, y):
        super().__init__(x, y)


class F_Creator:
    def createFunctions(length, table_array, function_type):
        '''
        creates an Object of Type function_type from a given 2 dim list
                Parameters:
                        length (int): the given training function list 
                        table_array (two dimensional list): a table with values stored in a two dimensional array
                        function_type: (Object): object of one type of the Function Objects
                Returns: 
                        returns a list of functions of Type function_type
        '''
        functions = []
        i = 1
        while i < length:
            functions.append(function_type(table_array[0], table_array[i], "Y{}".format(i)))
            i += 1
        return functions

    def createTestValuePairs(length, table_array, function_type):
        '''
            creates an Object of Type function_type from a given 2 dim list
                Parameters:
                        length (int): the given training function list 
                        table_array (two dimensional list): a table with values stored in a two dimensional array
                        function_type: (Object): object of one type of the Function Objects
                Returns: 
                        returns a list of value_pairs of Type function_type
        '''
        value_pairs = []
        i = 0
        while i < length:
            value_pairs.append(function_type(table_array[0][i], table_array[1][i]))
            i+= 1
        return value_pairs