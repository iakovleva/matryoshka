import unittest
import warnings

from datetime import datetime, timedelta
from collections import defaultdict

from matryoshka.matreshka_data import MatryoshkaOrder

import matryoshka.gspread_authorize
from gspread.exceptions import CellNotFound


SOURCES = {
    'дэнч': (2, 1550),
    'дэнкол': (4, 1550),
    'дэнспб': (6, 1000),
    'колспб': (8, 1000),
    'дэнворон': (10, 350),
    'колворон': (12, 350),
    'дэнбелг': (14, 350),
    'колбелг': (16, 350),
    'дэнкраснодар': (18, 600),
    'колкраснодар': (20, 600)
}

LEADS_FILE = 'test_leads.csv'
# EMPTY_FILE = 'test_leads_empty.csv'

TEST_DATE = '10/01/2020'

class TestMatryoshkaOrder(unittest.TestCase):

    def setUp(self):
        # To avoid  "ResourceWarning: unclosed <ssl.SSLSocket ..."
        warnings.filterwarnings(action="ignore", message="unclosed",
                                category=ResourceWarning)

        self.order_dict = MatryoshkaOrder(TEST_DATE, LEADS_FILE)
        self.sheet = gspread_authorize.Spreadsheet('https://docs.google.com/spreadsheets/d/19JFl_56TXN1nfd-ltwadz-pC8qbDzeV8uU2ZxgJqe1E/edit#gid=0')

    def test_create_order_dict(self):
        values = {
            'дэнч': 0, 'дэнкол': 1, 'дэнспб': 0, 'колспб': 0, 'дэнворон': 0,
            'колворон': 0, 'дэнбелг': 0, 'колбелг': 0, 'дэнкраснодар': 0,
            'колкраснодар': 0
        }
        result = defaultdict(dict, values)
        order_dict = self.order_dict.create_order_dict()
        self.assertEqual(order_dict, result)

    def test_date_cell_in_sheet(self):
        date_cell = self.sheet.find_in_worksheet('matr', '{}'.format(TEST_DATE))
        self.assertEqual(date_cell.row, 2)
        self.assertEqual(date_cell.col, 1)

    def test_date_cell_not_in_sheet(self):
        with self.assertRaises(CellNotFound):
            self.sheet.find_in_worksheet('matr', '10/05/2018')

# TODO adds new rows even if date exists
    def test_write_row_to_matr_sheet(self):
        self.order_dict.write_row_to_matr_sheet(self.sheet)
        date_cell = self.sheet.find_in_worksheet('matr', '{}'.format(TEST_DATE))
        result = self.sheet.get_row_values('matr', date_cell.row)
        self.assertEqual(result, ['10/01/2020', '', '', '1550', '1'])

    def test_write_matr_in_daily_sheet(self):    #(day_sum: str) -> None:
        self.order_dict.write_matr_in_daily_sheet(self.sheet, '5000')
        date_cell = self.sheet.find_in_worksheet('daily', '{}'.format(TEST_DATE))
        # result = self.sheet.get_row_values('daily', date_cell.row)
        # self.assertEqual(result, ['10/01/2020', '', '', '1550', '1'])

    def test_add_formulas_to_cells(self):
    # date_cell: gspread.models.Cell):
        pass

    def tearDown(self):
        pass


class TestShelve(unittest.TestCase):

    def setUp(self):
        self.db = 'test_db'

    def test_data_in_shelve(self):
        # data =
        pass

    def test_data_not_in_shelve(self):
        # data =
        pass


def test_proceed_order_dict() -> None:
    pass


if __name__ == '__main__':
    unittest.main()
