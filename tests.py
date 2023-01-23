import unittest
from CSV_SQLHelper import Table_Helper

class TestCalculations(unittest.TestCase):
    def test_path(self):
        table_helper = Table_Helper()
        self.assertIsNotNone(table_helper.getCSVFilePath("path.csv"))

if __name__ == '__main__':
    unittest.main()