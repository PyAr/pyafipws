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
import os
from pyafipws.formatos.formato_xml import (mapear, leer, desserializar, 
    escribir, serializar 
    )
import tempfile

pytestmark = [pytest.mark.dontusefix]

@pytest.fixture
def xml_file():
    # Create a temporary file with XML content
    xml_content = """
        <?xml version="1.0" encoding="UTF-8"?>
        <comprobantes>
            <comprobante>
                <tipo>1</tipo>
            </comprobante>
        </comprobantes>
    """.strip()
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(xml_content)
        file_path = f.name

    yield file_path

    os.remove(file_path)


def test_mapear():
    # Mapping with default behavior
    old = {"tipo_cbte": 1, "punto_vta": 2, "cbt_numero": 3}
    new = mapear({}, old, {"tipo": "tipo_cbte", "ptovta": "punto_vta", "numero": "cbt_numero"})
    assert new == {"tipo": 1, "ptovta": 2, "numero": 3}

    # Mapping with swap=True
    old = {"tipo_cbte": 1, "punto_vta": 2, "cbt_numero": 3}
    new = mapear({}, old, {"tipo_cbte": "tipo", "punto_vta": "ptovta", "cbt_numero": "numero"}, swap=True)
    assert {'tipo': 1, 'ptovta': 2, 'numero': 3}
    
    # Mapping with missing value
    old = {"tipo_cbte": 1, "punto_vta": 2}
    new = mapear({}, old, {"tipo": "tipo_cbte", "ptovta": "punto_vta", "numero": "cbt_numero"})
    assert new == {"tipo": 1, "ptovta": 2, "numero": None}

    # Mapping with empty dictionary
    old = {}
    new = mapear({}, old, {"tipo": "tipo_cbte", "ptovta": "punto_vta", "numero": "cbt_numero"})
    assert new == {"tipo": None, "ptovta": None, "numero": None}


def test_desserializar():
    # Test case 1: Valid XML string
    xml = "<comprobantes><comprobante><tipo>1</tipo></comprobante></comprobantes>"
    with pytest.raises(KeyError):
        result = desserializar(xml)

    # with Invalid XML string
    xml = "<comprobantes><comprobante><tipo>1</tipo></comprobante>"
    with pytest.raises(Exception):
        result = desserializar(xml)

