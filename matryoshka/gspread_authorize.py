import logging
import gspread
from typing import List, Union
from gspread.exceptions import CellNotFound
from oauth2client.service_account import ServiceAccountCredentials
from matryoshka.spiders import tokens


class Spreadsheet:

    def __init__(self, url: str) -> None:
        """Make authorization in a Google Spreadsheet.
        Open a Spreadsheet by url.
        """

        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        cred_file = tokens.CRED_FILE
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            cred_file,
            self.scope
            )
        self.gc = gspread.authorize(self.credentials)
        self.spreadsheet = self.gc.open_by_url(url)

    def _open_worksheet(self, worksheet: str) -> \
                                    gspread.models.Worksheet:
        """Open worksheet by name."""

        logging.basicConfig(
            filename='daily.log',
            level=logging.INFO,
            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S'
            )

        try:
            worksheet = self.spreadsheet.worksheet(worksheet)
        except gspread.exceptions.GSpreadException as e:
        # from gspread.exceptions import SpreadsheetNotFound
            logging.warning(e)
            raise
        except:
            logging.warning('Worksheet %s was not opened', worksheet)
        return worksheet


    def find_in_worksheet(self, worksheet: gspread.Worksheet, value: str) -> \
                                                                gspread.Cell:
        """Find cell with defined value. """

        worksheet = self._open_worksheet(worksheet)
        try:
            return worksheet.find(value)
        except CellNotFound as e:
            logging.warning(e)
            raise

    def add_new_row_at_the_top(self, worksheet: str, values: list) -> \
                                    gspread.Worksheet:
        """Add row with values after header row. """

        worksheet = self._open_worksheet(worksheet)
        return worksheet.insert_row(values, index=2,
                             value_input_option='USER_ENTERED')

    def update_cell(self, worksheet:str, row:int, column:int, values:str) -> \
                                       gspread.Worksheet:

        """Insert values in the cell. """

        worksheet = self._open_worksheet(worksheet)
        return worksheet.update_cell(row, column, values)

    def get_row_values(self, worksheet: str, row: int) -> List[Union[str, int]]:
        """Get all values from the row. """

        worksheet = self._open_worksheet(worksheet)
        return worksheet.row_values(row)

    def get_cell_value(self, worksheet: str, row: int, col: int) -> str:
        """Return value of the cell. """

        worksheet = self._open_worksheet(worksheet)
        return worksheet.cell(row, col).value
