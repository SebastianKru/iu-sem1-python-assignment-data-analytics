import unittest
from CSV_SQLHelper import Table_Helper
import ErrorFunctions

class TestCalculations(unittest.TestCase):

    def test_MSE(self):
        test_train_y = [1, 2, 4]
        test_ideal_y = [3, 6, 2]
        i = 0
        assert ErrorFunctions.calculateMSE(test_train_y, test_ideal_y, i) == 8

    def test_RMSE(self): 
        test_train_y = [1, 2, 4]
        test_ideal_y = [3, 4, 2]
        i = 0
        assert ErrorFunctions.calculateRMSE(test_train_y, test_ideal_y, i) == 2

    def test_MAE(self): 
        test_train_y = [1, 2, 4]
        test_ideal_y = [3, 4, 2]
        i = 0
        assert ErrorFunctions.calculateMAE(test_train_y, test_ideal_y, i) == 2

    def test_MAPE(self): 
        test_train_y = [4, 3, 8]
        test_ideal_y = [2, 1, 2]
        i = 0
        assert ErrorFunctions.calculateMAPE(test_train_y, test_ideal_y, i) == 2

    def test_SMAPE(self): 
        test_train_y = [6, 3, 12]
        test_ideal_y = [2, 1, 4]
        i = 0
        assert ErrorFunctions.calculateSMAPE(test_train_y, test_ideal_y, i) == 1      

class TestFilePath(unittest.TestCase):
    
    def test_path(self):
        table_helper = Table_Helper()
        self.assertIsNotNone(table_helper.getCSVFilePath("path.csv"))  

if __name__ == '__main__':
    unittest.main()