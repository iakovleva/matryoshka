import logging
import shelve
from time import sleep
from datetime import datetime, timedelta
from collections import defaultdict
from typing import DefaultDict

from matryoshka.spiders import tokens
from gspread_authorize import Spreadsheet
from gspread.exceptions import CellNotFound


# 'Name': (column, price)
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

DAYS = 16
LEADS_FILE = 'leads.csv'
MATR_DB = 'matr'
LOG_FILE = 'daily.log'

# GSPREAD
sh = Spreadsheet(tokens.SPREADSHEET_INCOME)
WS_MATR = sh.open_worksheet('matr')
WS_DAILY = sh.open_worksheet('daily')


class MatryoshkaOrder:
    """
    Example of created defaultdict:
    defaultdict(<class 'int'>, {'дэнбелг': 0, 'дэнворон': 7, 'дэнкол': 4})
    """

    def __init__(self, date: str) -> None:
        self.date = date
        self.order_dict = self.create_order_dict()

    def create_order_dict(self) -> DefaultDict[str, int]:
        """Retrieve data from csv and count number of orders for each day. """

        order_dict = defaultdict(int, **{k: 0 for k in SOURCES.keys()})
        with open(LEADS_FILE) as f:
            for line in f:
                order_id, status, source, order_date = line.split(',')
                order_date = order_date.strip()
                for key in SOURCES.keys():
                    if source == key and order_date == self.date:
                        order_dict[source] += 1
        return order_dict

    def data_changed(self, db_name: str) -> bool:
        """If data of the date is already in db and was changed -> return True.
           If no data for this date, add it -> return True.
        """

        with shelve.open(db_name) as db:
            if self.date not in db or db[self.date] != self.order_dict:
                db[self.date] = self.order_dict
                logging.info('Data for %s saved in %s DB.', self.date, db_name)
                return True
            else:
                logging.info("Data for %s is in db and hasn't changed.",
                             self.date)

    def write_matr_in_daily_sheet(self, day_sum: str) -> None:
        """ Write sum of matroyshka income to daily tab. """

        try:
            date_cell = WS_DAILY.find('{}'.format(self.date))
            WS_DAILY.update_cell(date_cell.row, 7, day_sum)
        except CellNotFound:
            logging.info('There is no date %s in daily tab', self.date)

    def write_row_to_matr_sheet(self) -> None:
        """Write data from defaultdict into spreadsheet. """

        try:
            date_cell = WS_MATR.find('{}'.format(self.date))
        except CellNotFound:
            sh.add_new_row_at_the_top([self.date], WS_MATR)
            date_cell = WS_MATR.find('{}'.format(self.date))
            self.add_formulas_to_cells(date_cell)

        for source, quantity in self.order_dict.items():
            col, price = SOURCES[source]
            if quantity > 0:    # Don't write zeros
                sh.update_cell(WS_MATR, date_cell.row, col+1, quantity)
                sh.update_cell(WS_MATR, date_cell.row, col, quantity * price)
                # To avoid gspread.exceptions.APIError: Quota exceeded
                sleep(2)

        logging.info('Matryoshka data for %s is written at %s', self.date,
                     datetime.now())

    def add_formulas_to_cells(self, date_cell):
        """ Insert formulas of sum in columns (22, 23)."""

        frml = f'=SUM(B{date_cell.row},D{date_cell.row},F{date_cell.row},H{date_cell.row},J{date_cell.row},L{date_cell.row},N{date_cell.row},P{date_cell.row},R{date_cell.row},T{date_cell.row})'
        frml2 = f'=SUM(C{date_cell.row},E{date_cell.row},G{date_cell.row},I{date_cell.row},K{date_cell.row},M{date_cell.row},O{date_cell.row},Q{date_cell.row},S{date_cell.row},U{date_cell.row})'
        return sh.update_cell(WS_MATR, date_cell.row, 22, frml), \
               sh.update_cell(WS_MATR, date_cell.row, 23, frml)


def proceed_order_dict() -> None:
    """Creare dictionaries for each day in range of DAYS.
       If data is changed, write it to spreadsheet.
    """

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S'
        )

    for i in range(DAYS):
        d = timedelta(days=i)
        date = (datetime.today() - d).strftime('%d/%m/%Y')
        try:
            order_dict = MatryoshkaOrder(date)
            if order_dict.data_changed(MATR_DB) is True:
                order_dict.write_row_to_matr_sheet()
                date_cell = WS_MATR.find('{}'.format(date))
                day_sum = WS_MATR.cell(date_cell.row, 22).value
                order_dict.write_matr_in_daily_sheet(day_sum)
        except FileNotFoundError as e:
            logging.exception(e)
            raise


proceed_order_dict()
