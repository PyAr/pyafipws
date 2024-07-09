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

import json
import pytest
from decimal import Decimal
from pyafipws.formatos.formato_json import leer, escribir


@pytest.mark.dontusefix
class TestFormatoJSON:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        self.entrada_file = tmp_path / "entrada.json"
        self.salida_file = tmp_path / "salida.json"

    def test_leer_archivo_facturas(self):
        # Leer el archivo facturas.json
        with open("tests/facturas.json", "r") as f:
            expected_data = json.load(f)
        result = leer("tests/facturas.json")
        assert result == expected_data

    def test_escribir_archivo_facturas(self, tmp_path):
        # Escribir los datos de facturas.json en un nuevo archivo
        with open("tests/facturas.json", "r") as f:
            data = json.load(f)
        temp_file = tmp_path / "temp_facturas.json"
        escribir(data, str(temp_file))
        with open(temp_file, "r") as f:
            result = json.load(f)
        assert result == data

    def test_leer_archivo_facturas_modificado(self, tmp_path):
        # Leer una versión modificada del archivo facturas.json
        with open("tests/facturas.json", "r") as f:
            data = json.load(f)
        # Modificar los datos
        data[0]["cae"] = "12345678901234"
        data[0]["imp_total"] = "1500.00"
        temp_file = tmp_path / "modified_facturas.json"
        temp_file.write_text(json.dumps(data))
        result = leer(str(temp_file))
        assert result == data

    def test_leer_archivo_json_invalido(self):
        # Leer un archivo con sintaxis JSON inválida
        # Sintaxis JSON inválida
        self.entrada_file.write_text('{"key": "value",}')
        with pytest.raises(json.decoder.JSONDecodeError):
            leer(str(self.entrada_file))

    def test_leer_archivo_vacio(self):
        # Leer un archivo JSON vacío
        self.entrada_file.write_text("")
        try:
            result = leer(str(self.entrada_file))
            assert result == []
        except json.decoder.JSONDecodeError:
            # Manejar el caso cuando el archivo está vacío o no tiene
            # un formato JSON válido
            pass

    def test_leer_archivo_valido(self):
        # Leer un archivo JSON válido
        data = [{"id": 1, "nombre": "Juan"}, {"id": 2, "nombre": "María"}]
        self.entrada_file.write_text(json.dumps(data))
        result = leer(str(self.entrada_file))
        assert result == data

    def test_leer_archivo_inexistente(self):
        # Leer un archivo JSON inexistente
        with pytest.raises(FileNotFoundError):
            leer("archivo_inexistente.json")

    def test_leer_archivo_invalido(self):
        # Leer un archivo JSON inválido
        self.entrada_file.write_text("invalid JSON")
        with pytest.raises(json.JSONDecodeError):
            leer(str(self.entrada_file))

    def test_escribir_lista_comprobantes(self):
        # Escribir una lista de comprobantes (diccionarios) en un archivo JSON
        comprobantes = [
            {"numero": 1, "fecha": "2023-06-01", "total": 100.50},
            {"numero": 2, "fecha": "2023-06-02", "total": 200.75},
        ]
        escribir(comprobantes, str(self.salida_file))
        with open(self.salida_file, "r") as f:
            result = json.load(f)
        assert result == comprobantes

    def test_escribir_lista_vacia(self):
        # Escribir una lista vacía en un archivo JSON
        escribir([], str(self.salida_file))
        with open(self.salida_file, "r") as f:
            result = json.load(f)
        assert result == []

    def test_escribir_archivo_existente(self):
        # Escribir en un archivo JSON existente
        self.salida_file.write_text("existing content")
        comprobantes = [{"numero": 1, "fecha": "2023-06-01", "total": 100.50}]
        escribir(comprobantes, str(self.salida_file))
        with open(self.salida_file, "r") as f:
            result = json.load(f)
        assert result == comprobantes

    def test_escribir_datos_complejos(self):
        # Escribir estructuras de datos complejas en un archivo JSON
        datos = {
            "nombre": "Juan",
            "edad": 30,
            "direccion": {
                "calle": "Av. ejemplo",
                "numero": 123,
                "ciudad": "Buenos Aires",
            },
            "telefonos": ["1234567890", "9876543210"],
            "activo": True,
        }
        escribir(datos, str(self.salida_file))
        with open(self.salida_file, "r") as f:
            result = json.load(f)
        assert result == datos

    def test_escribir_datos_unicode(self):
        # Escribir datos con caracteres Unicode en un archivo JSON
        datos = {"nombre": "Juan", "apellido": "Pérez", "ciudad": "Córdoba"}
        escribir(datos, str(self.salida_file))
        with open(self.salida_file, "r", encoding="utf-8") as f:
            result = json.load(f)
        assert result == datos

    def test_escribir_datos_decimales(self):
        # Escribir datos con objetos Decimal en un archivo JSON
        datos = {"precio": Decimal("10.50"), "cantidad": Decimal("5")}
        escribir(datos, str(self.salida_file), default=str)
        with open(self.salida_file, "r") as f:
            result = json.load(f)
        assert result == {"precio": "10.50", "cantidad": "5"}
