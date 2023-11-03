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

"""Test Formatos"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"


import pytest
from pyafipws.formatos.formato_txt import leer_linea_txt, escribir_linea_txt, leer, escribir

pytestmark = [pytest.mark.dontusefix]


# test different data types against each function
def test_leer_linea_txt_numeric_field():
    line = "1234567890"
    format_spec = [("field", 10, "Numerico")]
    result = leer_linea_txt(line, format_spec)
    assert result == {"field": 1234567890}

def test_leer_linea_txt_alphanumeric_field():
    line = "Hello World"
    format_spec = [("field", 12, "Alfanumerico")]
    result = leer_linea_txt(line, format_spec)
    assert result == {"field": "Hello World"}

def test_leer_linea_txt_import_field():
    line = "12.34       "
    format_spec = [("field", 12, "Importe")]
    result = leer_linea_txt(line, format_spec)
    assert result == {"field": 12.34}

def test_escribir_linea_txt_numeric_field():
    data = {"field": 1234567890}
    format_spec = [("field", 10, "Numerico")]
    result = escribir_linea_txt(data, format_spec)
    assert result.strip() == "1234567890"

def test_escribir_linea_txt_alphanumeric_field():
    data = {"field": "Hello World"}
    format_spec = [("field", 12, "Alfanumerico")]
    result = escribir_linea_txt(data, format_spec)
    assert result.strip() == "Hello World"

def test_escribir_linea_txt_import_field():
    data = {"field": 12.34}
    format_spec = [("field", 12, "Importe")]
    result = escribir_linea_txt(data, format_spec)
    assert result.strip() == "000000001234"
