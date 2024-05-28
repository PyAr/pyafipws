#!/usr/bin/python
# -*- coding: utf8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

import os
import sys
import unittest
import importlib.util
import csv
import pytest
import tempfile
from io import StringIO
from openpyxl import Workbook, load_workbook
from unittest.mock import MagicMock, mock_open, patch


# Get the absolute path to the formato_csv.py file
formato_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'formatos', 'formato_csv.py'))


# Load the formato_csv module
spec = importlib.util.spec_from_file_location("formato_csv", formato_csv_path)
formato_csv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(formato_csv)


from pyafipws.formatos.formato_csv import leer


@pytest.mark.dontusefix
class TestLeerFunction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create sample CSV data
        cls.sample_csv_data = "Column1,Column2,Column3\nValue1,Value2,Value3\r\nValue4,Value5,Value6"


        # Create sample CSV data with pipe delimiter
        cls.sample_pipe_csv_data = "Column1|Column2|Column3\r\nValue1|Value2|Value3\r\nValue4|Value5|Value6"


        # Create empty CSV data
        cls.empty_csv_data = ""


    def test_leer_csv_file(self):
        """
        Test that the leer function can read a valid CSV file correctly.
        """
        expected_data = [
            ["Column1", "Column2", "Column3"],
            ["Value1", "Value2", "Value3"],
            ["Value4", "Value5", "Value6"],
        ]
        with patch('builtins.open', return_value=StringIO(self.sample_csv_data)):
            result = leer('data/sample.csv')
        self.assertEqual(result, expected_data)


    def test_leer_xlsx_file(self):
        """
        Test that the leer function can read a valid Excel file correctly.
        """
        expected_data = [
            ["Column1", "Column2", "Column3"],
            ["Value1", "Value2", "Value3"],
            ["Value4", "Value5", "Value6"],
        ]


        # Create a temporary Excel file for testing
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
            workbook = Workbook()
            worksheet = workbook.active
            worksheet['A1'] = 'Column1'
            worksheet['B1'] = 'Column2'
            worksheet['C1'] = 'Column3'
            worksheet['A2'] = 'Value1'
            worksheet['B2'] = 'Value2'
            worksheet['C2'] = 'Value3'
            worksheet['A3'] = 'Value4'
            worksheet['B3'] = 'Value5'
            worksheet['C3'] = 'Value6'
            workbook.save(temp_file.name)


            result = leer(temp_file.name)
            self.assertEqual(result, expected_data)


            # Clean up the temporary file
            os.unlink(temp_file.name)


    def test_leer_missing_file(self):
        """
        Test that the leer function raises an appropriate exception when the file is missing.
        """
        filename = os.path.join('data', 'missing.csv')
        with self.assertRaises(FileNotFoundError):
            leer(filename)


    def test_leer_empty_file(self):
        """
        Test that the leer function handles an empty file correctly.
        """
        expected_data = []
        with patch('builtins.open', return_value=StringIO(self.empty_csv_data)):
            result = leer('data/empty.csv')
        self.assertEqual(result, expected_data)


    def test_leer_custom_delimiter(self):
        """
        Test that the leer function can read a CSV file with a custom delimiter.
        """
        expected_data = [
            ["Column1", "Column2", "Column3"],
            ["Value1", "Value2", "Value3"],
            ["Value4", "Value5", "Value6"],
        ]
        with patch('builtins.open', return_value=StringIO(self.sample_pipe_csv_data)):
            result = leer('data/sample_pipe.csv', delimiter="|")
        self.assertEqual(result, expected_data)


    def test_leer_csv_missing_columns(self):
        """
        Test that the leer function handles a CSV file with missing columns correctly.
        """
        sample_csv_data = "Column1,Column2\nValue1,Value2\nValue3\nValue4,Value5,Value6"
        expected_data = [
            ["Value1", "Value2"],
            ["Value3"],
            ["Value4", "Value5", "Value6"],
        ]
        with patch('builtins.open', return_value=StringIO(sample_csv_data)):
            result = formato_csv.leer('data/sample_missing_columns.csv', delimiter=',')
        self.assertEqual(result, expected_data)

    
    def test_leer_csv_extra_columns(self):
        """
        Test that the leer function handles a CSV file with extra columns correctly.
        """
        sample_csv_data = "Column1,Column2,Column3,Column4,column5,column6\nValue1,Value2,Value3,Value4\nValue5,Value6,Value7,Value8"
        expected_data = [
            ["Value1", "Value2", "Value3", "Value4"],
            ["Value5", "Value6", "Value7", "Value8"],
        ]
        with patch('builtins.open', return_value=StringIO(sample_csv_data)):
            result = formato_csv.leer('data/sample_extra_columns.csv', delimiter=',')
        self.assertEqual(result, expected_data)

    def test_leer_csv_different_column_order(self):
        """
        Test that the leer function handles a CSV file with different column order correctly.
        """
        sample_csv_data = "Column2,Column1,Column3\nValue2,Value1,Value3\nValue5,Value4,Value6"
        expected_data = [
            ["Value2", "Value1", "Value3"],
            ["Value5", "Value4", "Value6"],
        ]
        with patch('builtins.open', return_value=StringIO(sample_csv_data)):
            result = formato_csv.leer('data/sample_different_order.csv', delimiter=',')
        self.assertEqual(result, expected_data)

    
    def test_leer_csv_special_characters(self):
        """
        Test that the leer function handles a CSV file with special characters correctly.
        """
        sample_csv_data = "Column1,Column2,Column3\nValue1,Válue2,Value3\nValue4,Value5,Válue6"
        expected_data = [
            ["Value1", "Válue2", "Value3"],
            ["Value4", "Value5", "Válue6"],
        ]
        with patch('builtins.open', return_value=StringIO(sample_csv_data)):
            result = formato_csv.leer('data/sample_special_chars.csv', delimiter=',')
        self.assertEqual(result, expected_data)


if __name__ == "__main__":
    unittest.main()
