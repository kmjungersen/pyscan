"""
pyscan
======

main.py

This file houses the core of the application
"""

# imports
import csv
import pprint

import requests
from bs4 import BeautifulSoup

from pyscan.local import *


class Barcode():

    def __init__(self, barcode_id=None, barcode_ids=None, autosave=False):
        """

        :return:
        """

        self.number = barcode_id
        self.autosave = autosave

        self.base_url = BASE_URL

        self.data = {}
        self.item_name = ''
        self.description = ''

        self.pp = pprint.PrettyPrinter()

        if barcode_id:

            self.data = self.retrieve()

            self.item_name = self.data.get('itemname').decode('ascii')
            self.description = self.data.get('description').decode('ascii')

        elif barcode_ids:

            pass

        self.save_file = SAVE_FILE_PATH

    def retrieve(self, barcode=None):
        """

        :param barcode:
        :return:
        """

        if barcode:

            self.number = barcode

        url = self.base_url.format(
            API_KEY=API_KEY,
            number=self.number,
        )

        r = requests.get(url)

        document = r.json()

        self.data = document

        # self.__convert_unicode_characters()

        return document

    def save(self, file_path=None):
        """

        """

        with open(self.save_file, 'a') as save_file:
            save_file.write(str('{number}\n'.format(
                number=self.number,
            )))

    def continuous_input(self):
        """

        :return:
        """

        done = False

        print('Keep scanning codes to save them.  When finished, type "done"!')

        while not done:

            code = input('Enter a barcode ---> ')

            if code == 'done':
                break

            self.pp.pprint(self.retrieve(code))

            self.save()

    def batch_retrieve(self, barcode_ids):
        """

        :return:
        """

        barcode_metadata_list = []

        for barcode in barcode_ids:

            metadata = self.retrieve(barcode)

            barcode_metadata_list.append(metadata)



    def csv_write(self):
        """

        :return:
        """

        with open('foo.csv', 'a') as csvfile:
            code_writer = csv.writer(csvfile, delimiter=',')

            row = [
                self.number,
                self.item_name,
                self.description
            ]

            code_writer.writerow(row)

    def __convert_unicode_characters(self):
        """

        :return:
        """

        for key, value in self.data.items():

            if type(value) is not int:

                converted_string = BeautifulSoup(value)
                self.data[key] = converted_string

    def __eq__(self, other):
        """

        :param other:
        :return:
        """

        return self.number

    def __repr__(self):
        """

        :return:
        """

        return str(self.data)

if __name__ == '__main__':
    b = Barcode(pretzel)
