import logging
import gspread
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

    def open_worksheet(self, worksheet: str) -> \
                                    gspread.models.Spreadsheet.worksheet:
        """Open worksheet by name."""

        logging.basicConfig(
            filename='daily.log',
            level=logging.INFO,
            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S'
            )

        try:
            worksheet = self.spreadsheet.worksheet(worksheet)
        except gspread.exceptions.GSpreadException as e:
            logging.warning(e)
        except:
            logging.warning('Worksheet %s was not opened', worksheet)
        return worksheet

    def add_new_row_at_the_top(self, values: list, worksheet: str) -> \
                                    gspread.models.Spreadsheet.worksheet:
        """Add row with values after header row. """

        worksheet = self.open_worksheet(worksheet)
        return worksheet.insert_row(values, index=2,
                             value_input_option='USER_ENTERED')

    def update_cell(self, worksheet: str, row: int, column: int, values: str)\
                                     -> gspread.models.Spreadsheet.worksheet:
        """Insert values in the cell. """

        worksheet = self.open_worksheet(worksheet)
        return worksheet.update_cell(row, column, values)
