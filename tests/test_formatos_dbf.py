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


from pyafipws.formatos.formato_dbf import (definir_campos, dar_nombre_campo, leer,
    escribir, ayuda
)

import pytest
import os


pytestmark = [pytest.mark.dontusefix]


def test_definir_campos():
    
    formato = [
        ("pdf", 100, "Alfanumerico"),
        ("email", 100, "Alfanumerico"),
    ]

    field_keys, field_definitions = definir_campos(formato)

    assert field_keys == ["pdf", "email"]
    assert field_definitions == ["pdf C(100)", "email C(100)"]


def test_dar_nombre_campo():
    key = "Dato_adicional1"

    assert dar_nombre_campo(key) == "datoadic01"
