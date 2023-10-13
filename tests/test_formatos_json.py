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
import json

from pyafipws.formatos.formato_json import leer, escribir


pytestmark = [pytest.mark.dontusefix]


# Create a sample Json file 
data = [
    {"id": 1, "name": "John", "age": 25},
    {"id": 2, "name": "Jane", "age": 30},
]

def test_leer(tmpdir):

    json_file = tmpdir.join("entrada.json")
    json_file.write(json.dumps(data))

    fn_result = leer(str(json_file))
    
    assert data == fn_result
    assert isinstance(fn_result, list)


def test_escribir(tmpdir):
    
    json_file = tmpdir.join("salida.json")
    json_file.write(json.dumps(data))

    escribir(data, fn=str(json_file))

    # read json file and check contents
    with open(json_file, "r") as fs:
        fn_result = json.load(fs)

    assert fn_result == data


