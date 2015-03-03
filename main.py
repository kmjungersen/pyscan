"""
pyscan
======

main.py

This file houses the core of the application
"""

# imports
import csv
import json
import urllib

from bs4 import BeautifulSoup as bs

from local import *


class Barcode():

    def __init__(self, barcode_number, autosave=False):
        """

        :return:
        """

        self.number = barcode_number
        self.autosave = False

        self.base_url = 'http://api.upcdatabase.org/json/{API_KEY}/{number}'
        self.data = self.retrieve()

        self.item_name = self.data.get('itemname').decode('ascii')
        self.description = self.data.get('description').decode('ascii')

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

        document = urllib.request.urlopen(url)

        print(document)

        self.data = json.load(document)

        self.__convert_unicode_characters()

        return self.data

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

            self.retrieve(code)

            self.save()

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

        for key, value in self.data.iteritems():

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
