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

"""Test para pyemail"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"


import os
import unittest
import json
import stat
import pytest
from decimal import Decimal
from pyafipws.formatos.formato_json import leer, escribir
import tempfile

@pytest.mark.dontusefix
class TestFormatoJSON(unittest.TestCase):
    def setUp(self):
        self.entrada_file = tempfile.NamedTemporaryFile(delete=False).name
        self.salida_file = tempfile.NamedTemporaryFile(delete=False).name

    def tearDown(self):
        try:
            os.unlink(self.entrada_file)
        except PermissionError:
            pass
        try:
            os.unlink(self.salida_file)
        except PermissionError:
            pass
       
    def test_leer_archivo_facturas(self):
        # Caso de prueba: Leer el archivo facturas.json
        with open("tests/facturas.json", "r") as f:
            expected_data = json.load(f)
        result = leer("tests/facturas.json")
        self.assertEqual(result, expected_data)

    def test_escribir_archivo_facturas(self):
        # Caso de prueba: Escribir los datos de facturas.json en un nuevo archivo
        with open("tests/facturas.json", "r") as f:
            data = json.load(f)
        temp_file = tempfile.NamedTemporaryFile(delete=False).name
        escribir(data, temp_file)
        with open(temp_file, "r") as f:
            result = json.load(f)
        self.assertEqual(result, data)
        os.unlink(temp_file)

    def test_leer_archivo_facturas_modificado(self):
        # Caso de prueba: Leer una versión modificada del archivo facturas.json
        with open("tests/facturas.json", "r") as f:
            data = json.load(f)
        # Modificar los datos
        data[0]["cae"] = "12345678901234"
        data[0]["imp_total"] = "1500.00"
        temp_file = tempfile.NamedTemporaryFile(delete=False).name
        with open(temp_file, "w") as f:
            json.dump(data, f)
        result = leer(temp_file)
        self.assertEqual(result, data)
        os.unlink(temp_file)
   
    def test_leer_archivo_json_invalido(self):
        # Caso de prueba: Leer un archivo con sintaxis JSON inválida
        with open(self.entrada_file, "w") as f:
            f.write('{"key": "value",}')  # Sintaxis JSON inválida
        with self.assertRaises(json.decoder.JSONDecodeError):
            leer(self.entrada_file)
   
    def test_leer_archivo_vacio(self):
        # Caso de prueba: Leer un archivo JSON vacío
        with open(self.entrada_file, "w") as f:
            f.write("")
        try:
            result = leer(self.entrada_file)
            self.assertEqual(result, [])
        except json.decoder.JSONDecodeError:
            # Manejar el caso cuando el archivo está vacío o no tiene un formato JSON válido
            pass

    def test_leer_archivo_valido(self):
        # Caso de prueba: Leer un archivo JSON válido
        data = [{"id": 1, "nombre": "Juan"}, {"id": 2, "nombre": "María"}]
        with open(self.entrada_file, "w") as f:
            json.dump(data, f)
        result = leer(self.entrada_file)
        self.assertEqual(result, data)
       
    def test_leer_archivo_inexistente(self):
        # Caso de prueba: Leer un archivo JSON inexistente
        with self.assertRaises(FileNotFoundError):
            leer("archivo_inexistente.json")

    def test_leer_archivo_invalido(self):
        # Caso de prueba: Leer un archivo JSON inválido
        with open(self.entrada_file, "w") as f:
            f.write("invalid JSON")
        with self.assertRaises(json.JSONDecodeError):
            leer(self.entrada_file)

    def test_escribir_lista_comprobantes(self):
        # Caso de prueba: Escribir una lista de comprobantes (diccionarios) en un archivo JSON
        comprobantes = [
            {"numero": 1, "fecha": "2023-06-01", "total": 100.50},
            {"numero": 2, "fecha": "2023-06-02", "total": 200.75},
        ]
        escribir(comprobantes, self.salida_file)
        with open(self.salida_file, "r") as f:
            result = json.load(f)
        self.assertEqual(result, comprobantes)

    def test_escribir_lista_vacia(self):
        # Caso de prueba: Escribir una lista vacía en un archivo JSON
        escribir([], self.salida_file)
        with open(self.salida_file, "r") as f:
            result = json.load(f)
        self.assertEqual(result, [])

    def test_escribir_archivo_existente(self):
        # Caso de prueba: Escribir en un archivo JSON existente
        with open(self.salida_file, "w") as f:
            f.write("existing content")
        comprobantes = [{"numero": 1, "fecha": "2023-06-01", "total": 100.50}]
        escribir(comprobantes, self.salida_file)
        with open(self.salida_file, "r") as f:
            result = json.load(f)
        self.assertEqual(result, comprobantes)

    def test_escribir_datos_complejos(self):
        # Caso de prueba: Escribir estructuras de datos complejas en un archivo JSON
        datos = {
            "nombre": "Juan",
            "edad": 30,
            "direccion": {
                "calle": "Av. ejemplo",
                "numero": 123,
                "ciudad": "Buenos Aires"
            },
            "telefonos": ["1234567890", "9876543210"],
            "activo": True
        }
        escribir(datos, self.salida_file)
        with open(self.salida_file, "r") as f:
            result = json.load(f)
        self.assertEqual(result, datos)

    def test_escribir_datos_unicode(self):
        # Caso de prueba: Escribir datos con caracteres Unicode en un archivo JSON
        datos = {"nombre": "Juan", "apellido": "Pérez", "ciudad": "Córdoba"}
        escribir(datos, self.salida_file)
        with open(self.salida_file, "r", encoding="utf-8") as f:
            result = json.load(f)
        self.assertEqual(result, datos)

    def test_escribir_datos_decimales(self):
        # Caso de prueba: Escribir datos con objetos Decimal en un archivo JSON
        datos = {"precio": Decimal("10.50"), "cantidad": Decimal("5")}
        escribir(datos, self.salida_file, default=str)
        with open(self.salida_file, "r") as f:
            result = json.load(f)
        self.assertEqual(result, {"precio": "10.50", "cantidad": "5"})

if __name__ == "__main__":
    unittest.main()
