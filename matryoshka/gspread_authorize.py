import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from matryoshka.spiders import tokens


class Spreadsheet:

    def __init__(self):
        """Make authorization in a Google Spreadsheet."""

        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        cred_file = tokens.CRED_FILE
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            cred_file,
            self.scope
            )
        self.gc = gspread.authorize(self.credentials)

    def open_sheet(self, url, worksheet):
        """Open Google Spreadsheet."""

        logging.basicConfig(
            filename='daily.log',
            level=logging.INFO,
            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S'
            )

        try:
            spreadsheet = self.gc.open_by_url(url)
            worksheet = spreadsheet.worksheet(worksheet)
        except gspread.exceptions.GSpreadException as e:
            logging.warning(e)
        except:
            logging.warning('Spreadsheet %s was not opened', worksheet)
        return worksheet
