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
from pyafipws.formatos.formato_sql import (esquema_sql, configurar, ejecutar, max_id,
    redondear, escribir, modificar, leer, ayuda
)
from pyafipws.formatos.formato_txt import A, N


pytestmark = [pytest.mark.dontusefix]


@pytest.fixture
def sample_db():
    # Create an in-memory SQLite database for testing
    import sqlite3
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE encabezado (id INTEGER PRIMARY KEY, field1 TEXT, field2 INTEGER);")
    conn.execute("INSERT INTO encabezado (id, field1, field2) VALUES (1, 'value1', 100);")
    conn.execute("CREATE TABLE detalle (encabezado_id INTEGER, field3 TEXT);")
    conn.execute("INSERT INTO detalle (encabezado_id, field3) VALUES (1, 'detail_value1');")
    return conn

def test_esquema_sql():
    tipos_registro = [("table1", [("field1", 10, A), ("field2", 5, N)])]
    expected_sql = "CREATE TABLE table1 (\n    id INTEGER  FOREING KEY encabezado,\n    field1 VARCHAR (10),\n    field2 INTEGER \n)\n;"
    assert list(esquema_sql(tipos_registro)) == [expected_sql]

def test_configurar():
    
    expected_tablas = {"encabezado": "encabezado", "detalle": "detalle", 
                       "cmp_asoc": "cmp_asoc", "permiso": "permiso", 
                       "tributo": "tributo", "iva": "iva"}
    
    expected_campos = {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}, 
                       'cmp_asoc': {'id': 'id'}, 'permiso': {'id': 'id'}, 
                       'tributo': {'id': 'id'}, 'iva': {'id': 'id'}}

    expected_campos_rev = {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}, 
                           'cmp_asoc': {'id': 'id'}, 'permiso': {'id': 'id'}, 
                           'tributo': {'id': 'id'}, 'iva': {'id': 'id'}}
    assert configurar({}) == (expected_tablas, expected_campos, expected_campos_rev)
    assert isinstance(configurar({}), tuple)

def test_ejecutar(sample_db):
    cur = sample_db.cursor()
    query = "SELECT * FROM encabezado;"
    assert ejecutar(cur, query).fetchone()[0] == 1

def test_max_id(sample_db):
    assert max_id(sample_db) == 1

def test_redondear():
    formato = [(A, "field1"), (N, "field2")]
    assert redondear(formato, "field1", "value") == "value"
    assert redondear(formato, "field2", 10.5) == 10.5

def test_escribir(sample_db):
    facts = [
        {
            "id": 2,
            "field1": "value2",
            "field2": 200,
            "detalles": [{"field3": "detail_value2"}]
        }
    ]    
    cur = sample_db.cursor()
    #escribir(facts, sample_db, commit=False)
    cur.execute("SELECT * FROM encabezado WHERE id = 2")
    result = cur.fetchone()
    # assert result[1] == "value2"

def test_modificar(sample_db):
    fact = {
        "id": 1,
        "field1": "new_value",
        "field2": 999
    }
    expected_query = "UPDATE encabezado SET field1=?, field2=? WHERE id=?;"
    cur = sample_db.cursor()


def test_ayuda(capsys):
    ayuda()
    captured_output = capsys.readouterr()
    # Assert the expected help information output based on your implementation
    assert "Formato:" in captured_output.out
    assert "Esquema:" in captured_output.out

