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

"""Test para formato_csv"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import os
import sys
import unittest
import importlib.util
import csv
import pytest
import tempfile
from io import StringIO
from openpyxl import Workbook
from unittest.mock import patch

# Add the 'formatos' directory to the Python module search path
formatos_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'formatos'))
sys.path.insert(0, formatos_dir)

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
        cls.sample_csv_data = "Column1,Column2,Column3\nValue1,Value2,Value3\nValue4,Value5,Value6"

        # Create sample CSV data with pipe delimiter
        cls.sample_pipe_csv_data = "Column1|Column2|Column3\nValue1|Value2|Value3\nValue4|Value5|Value6"

        # Create empty CSV data
        cls.empty_csv_data = ""


    def test_leer_csv_file(self):
        """
        Test that the leer function can read a valid CSV file correctly.
        """
        expected_data = [
            ["Value1", "Value2", "Value3"],
            ["Value4", "Value5", "Value6"],
        ]
        with patch('builtins.open', return_value=StringIO(self.sample_csv_data)):
            result = formato_csv.leer('data/sample.csv')
        self.assertEqual(result, expected_data)


    def test_leer_xlsx_file(self):
        """
        Test that the leer function can read a valid Excel file correctly.
        """
        expected_data = [
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

            result = formato_csv.leer(temp_file.name)
        self.assertEqual(result, expected_data)

        # Clean up the temporary file
        os.unlink(temp_file.name)


    def test_leer_missing_file(self):
        """
        Test that the leer function raises an appropriate exception when the file is missing.
        """
        filename = os.path.join('data', 'missing.csv')
        with self.assertRaises(FileNotFoundError):
            formato_csv.leer(filename)

    def test_leer_empty_file(self):
        """
        Test that the leer function handles an empty file correctly.
        """
        expected_data = []
        with patch('builtins.open', return_value=StringIO(self.empty_csv_data)):
            result = formato_csv.leer('data/empty.csv')
        self.assertEqual(result, expected_data)


    def test_leer_custom_delimiter(self):
        """
        Test that the leer function can read a CSV file with a custom delimiter.
        """
        expected_data = [
            ["Value1", "Value2", "Value3"],
            ["Value4", "Value5", "Value6"],
        ]
        with patch('builtins.open', return_value=StringIO(self.sample_pipe_csv_data)):
            result = formato_csv.leer('data/sample_pipe.csv', delimiter="|")
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
        sample_csv_data = "Column1,Column2,Column3,Column4\nValue1,Value2,Value3,Value4\nValue5,Value6,Value7,Value8"
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

@pytest.mark.dontusefix
class TestAplanarFunction(unittest.TestCase):
    def test_aplanar_single_record(self):
        """
        Test that the aplanar function correctly flattens a single record.
        """
        reg = {
            "id": 1,
            "tipo_cbte": 1,
            "punto_vta": 1,
            "cbte_nro": 1,
            "fecha_cbte": "2023-06-08",
            "tipo_doc": 80,
            "nro_doc": "20123456789",
            "imp_total": 126,
            "detalles": [
                {
                    "codigo": "P1",
                    "ds": "Producto 1",
                    "qty": 2,
                    "umed": 7,
                    "precio": 50,
                    "importe": 100,
                }
            ],
            "ivas": [
                {
                    "iva_id": 5,
                    "base_imp": 100,
                    "importe": 21,
                }
            ],
            "tributos": [
                {
                    "tributo_id": 1,
                    "base_imp": 100,
                    "desc": "Tributo 1",
                    "alic": 5,
                    "importe": 5,
                }
            ],
            "forma_pago": "Contado",
        }

        expected_data = [
            [
                'id',
                'tipo_cbte',
                'punto_vta',
                'cbt_numero',
                'fecha_cbte',
                'tipo_doc',
                'nro_doc',
                'imp_total',
                'forma_pago',
                'pdf',
                'codigo1',
                'descripcion1',
                'umed1',
                'cantidad1',
                'precio1',
                'importe1',
                'iva_id_1',
                'iva_base_imp_1',
                'iva_importe_1',
                'tributo_id_1',
                'tributo_base_imp_1',
                'tributo_desc_1',
                'tributo_alic_1',
                'tributo_importe_1',
                'cbte_nro',
                'moneda_id',
                'moneda_ctz',
                'imp_neto',
                'imp_iva',
                'imp_trib',
                'imp_op_ex',
                'imp_tot_conc'
            ],
            [
                1,
                1,
                1,
                1,
                '2023-06-08',
                80,
                '20123456789',
                126,
                'Contado',
                '',
                'P1',
                'Producto 1',
                7,
                2,
                50,
                100,
                5,
                100,
                21,
                1,
                100,
                'Tributo 1',
                5,
                5,
                1,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ]
        ]

        result = formato_csv.aplanar([reg])
        self.assertEqual(result, expected_data)






    def test_aplanar_multiple_records(self):
        """
        Test that the aplanar function correctly flattens multiple records.
        """
        regs = [
            {
                "id": 1,
                "tipo_cbte": 1,
                "punto_vta": 1,
                "cbte_nro": 1,
                "fecha_cbte": "2023-06-08",
                "tipo_doc": 80,
                "nro_doc": "20123456789",
                "moneda_id": "PES",
                "moneda_ctz": 1,
                "imp_neto": 100,
                "imp_iva": 21,
                "imp_trib": 5,
                "imp_op_ex": 0,
                "imp_tot_conc": 0,
                "imp_total": 126,
                "concepto": 1,
                "fecha_venc_pago": "2023-06-08",
                "fecha_serv_desde": "2023-06-08",
                "fecha_serv_hasta": "2023-06-08",
                "cae": "1234567890",
                "fecha_vto": "2023-06-18",
                "resultado": "A",
                "motivo": "",
                "reproceso": "",
                "nombre": "John Doe",
                "domicilio": "123 Main St",
                "localidad": "City",
                "telefono": "1234567890",
                "categoria": "A",
                "email": "john@example.com",
                "numero_cliente": "ABC123",
                "numero_orden_compra": "OC123",
                "condicion_frente_iva": "Responsable Inscripto",
                "numero_cotizacion": "COT123",
                "numero_remito": "REM123",
                "obs_generales": "Observaciones generales",
                "obs_comerciales": "Observaciones comerciales",
                "detalles": [
                    {
                        "codigo": "P1",
                        "ds": "Producto 1",
                        "qty": 2,
                        "umed": 7,
                        "precio": 50,
                        "importe": 100,
                        "iva_id": 5,
                        "imp_iva": 21,
                        "bonif": 0,
                        "despacho": "",
                        "dato_a": "",
                        "dato_b": "",
                        "dato_c": "",
                        "dato_d": "",
                        "dato_e": "",
                    }
                ],
                "ivas": [
                    {
                        "iva_id": 5,
                        "base_imp": 100,
                        "importe": 21,
                    }
                ],
                "tributos": [
                    {
                        "tributo_id": 1,
                        "base_imp": 100,
                        "desc": "Tributo 1",
                        "alic": 5,
                        "importe": 5,
                    }
                ],
                "opcionales": [
                    {
                        "opcional_id": 1,
                        "valor": "Valor opcional 1",
                    }
                ],
                "cbtes_asoc": [
                    {
                        "cbte_tipo": 1,
                        "cbte_punto_vta": 1,
                        "cbte_nro": 0,
                        "cbte_cuit": "20123456789",
                        "cbte_fecha": "2023-06-07",
                    }
                ],
                "forma_pago": "Contado",
            },
            {
                "id": 2,
                "tipo_cbte": 1,
                "punto_vta": 1,
                "cbte_nro": 2,
                "fecha_cbte": "2023-06-09",
                "tipo_doc": 80,
                "nro_doc": "20987654321",
                "moneda_id": "PES",
                "moneda_ctz": 1,
                "imp_neto": 200,
                "imp_iva": 42,
                "imp_trib": 10,
                "imp_op_ex": 0,
                "imp_tot_conc": 0,
                "imp_total": 252,
                "concepto": 1,
                "fecha_venc_pago": "2023-06-09",
                "fecha_serv_desde": "2023-06-09",
                "fecha_serv_hasta": "2023-06-09",
                "cae": "0987654321",
                "fecha_vto": "2023-06-19",
                "resultado": "A",
                "motivo": "",
                "reproceso": "",
                "nombre": "Jane Smith",
                "domicilio": "456 Elm St",
                "localidad": "Town",
                "telefono": "0987654321",
                "categoria": "B",
                "email": "jane@example.com",
                "numero_cliente": "XYZ789",
                "numero_orden_compra": "OC456",
                "condicion_frente_iva": "Responsable Inscripto",
                "numero_cotizacion": "COT456",
                "numero_remito": "REM456",
                "obs_generales": "Observaciones generales",
                "obs_comerciales": "Observaciones comerciales",
                "detalles": [
                    {
                        "codigo": "P2",
                        "ds": "Producto 2",
                        "qty": 1,
                        "umed": 7,
                        "precio": 200,
                        "importe": 200,
                        "iva_id": 5,
                        "imp_iva": 42,
                        "bonif": 0,
                        "despacho": "",
                        "dato_a": "",
                        "dato_b": "",
                        "dato_c": "",
                        "dato_d": "",
                        "dato_e": "",
                    }
                ],
                "ivas": [
                    {
                        "iva_id": 5,
                        "base_imp": 200,
                        "importe": 42,
                    }
                ],
                "tributos": [
                    {
                        "tributo_id": 2,
                        "base_imp": 200,
                        "desc": "Tributo 2",
                        "alic": 5,
                        "importe": 10,
                    }
                ],
                "opcionales": [
                    {
                        "opcional_id": 2,
                        "valor": "Valor opcional 2",
                    }
                ],
                "cbtes_asoc": [
                    {
                        "cbte_tipo": 1,
                        "cbte_punto_vta": 1,
                        "cbte_nro": 1,
                        "cbte_cuit": "20123456789",
                        "cbte_fecha": "2023-06-08",
                    }
                ],
                "forma_pago": "Tarjeta de Crédito",
            },
        ]

        expected_data = [
            [
                "id",
                "tipo_cbte",
                "punto_vta",
                "cbt_numero",
                "fecha_cbte",
                "tipo_doc",
                "nro_doc",
                "moneda_id",
                "moneda_ctz",
                "imp_neto",
                "imp_iva",
                "imp_trib",
                "imp_op_ex",
                "imp_tot_conc",
                "imp_total",
                "concepto",
                "fecha_venc_pago",
                "fecha_serv_desde",
                "fecha_serv_hasta",
                "cae",
                "fecha_vto",
                "resultado",
                "motivo",
                "reproceso",
                "nombre",
                "domicilio",
                "localidad",
                "telefono",
                "categoria",
                "email",
                "numero_cliente",
                "numero_orden_compra",
                "condicion_frente_iva",
                "numero_cotizacion",
                "numero_remito",
                "obs_generales",
                "obs_comerciales",
                "forma_pago",
                "pdf",
                "codigo1",
                "descripcion1",
                "umed1",
                "cantidad1",
                "precio1",
                "importe1",
                "iva_id1",
                "imp_iva1",
                "bonif1",
                "numero_despacho1",
                "dato_a1",
                "dato_b1",
                "dato_c1",
                "dato_d1",
                "dato_e1",
                "iva_id_1",
                "iva_base_imp_1",
                "iva_importe_1",
                "tributo_id_1",
                "tributo_base_imp_1",
                "tributo_desc_1",
                "tributo_alic_1",
                "tributo_importe_1",
                "opcional_id_1",
                "opcional_valor_1",
                "cbte_asoc_tipo_1",
                "cbte_asoc_pto_vta_1",
                "cbte_asoc_nro_1",
                "cbte_asoc_cuit_1",
                "cbte_asoc_fecha_1",
                "codigo2",
                "descripcion2",
                "umed2",
                "cantidad2",
                "precio2",
                "importe2",
                "iva_id2",
                "imp_iva2",
                "bonif2",
                "numero_despacho2",
                "dato_a2",
                "dato_b2",
                "dato_c2",
                "dato_d2",
                "dato_e2",
                "iva_id_2",
                "iva_base_imp_2",
                "iva_importe_2",
                "tributo_id_2",
                "tributo_base_imp_2",
                "tributo_desc_2",
                "tributo_alic_2",
                "tributo_importe_2",
                "opcional_id_2",
                "opcional_valor_2",
                "cbte_asoc_tipo_2",
                "cbte_asoc_pto_vta_2",
                "cbte_asoc_nro_2",
                "cbte_asoc_cuit_2",
                "cbte_asoc_fecha_2",
            ],
            [
                1,
                1,
                1,
                1,
                "2023-06-08",
                80,
                "20123456789",
                "PES",
                1,
                100,
                21,
                5,
                0,
                0,
                126,
                1,
                "2023-06-08",
                "2023-06-08",
                "2023-06-08",
                "1234567890",
                "2023-06-18",
                "A",
                "",
                "",
                "John Doe",
                "123 Main St",
                "City",
                "1234567890",
                "A",
                "john@example.com",
                "ABC123",
                "OC123",
                "Responsable Inscripto",
                "COT123",
                "REM123",
                "Observaciones generales",
                "Observaciones comerciales",
                "Contado",
                "",
                "P1",
                "Producto 1",
                7,
                2,
                50,
                100,
                5,
                21,
                0,
                "",
                "",
                "",
                "",
                "",
                "",
                5,
                100,
                21,
                1,
                100,
                "Tributo 1",
                5,
                5,
                1,
                "Valor opcional 1",
                1,
                1,
                0,
                "20123456789",
                "2023-06-07",
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            [
                2,
                1,
                1,
                2,
                "2023-06-09",
                80,
                "20987654321",
                "PES",
                1,
                200,
                42,
                10,
                0,
                0,
                252,
                1,
                "2023-06-09",
                "2023-06-09",
                "2023-06-09",
                "0987654321",
                "2023-06-19",
                "A",
                "",
                "",
                "Jane Smith",
                "456 Elm St",
                "Town",
                "0987654321",
                "B",
                "jane@example.com",
                "XYZ789",
                "OC456",
                "Responsable Inscripto",
                "COT456",
                "REM456",
                "Observaciones generales",
                "Observaciones comerciales",
                "Tarjeta de Crédito",
                "",
                "P2",
                "Producto 2",
                7,
                1,
                200,
                200,
                5,
                42,
                0,
                "",
                "",
                "",
                "",
                "",
                "",
                5,
                200,
                42,
                2,
                200,
                "Tributo 2",
                5,
                10,
                2,
                "Valor opcional 2",
                1,
                1,
                1,
                "20123456789",
                "2023-06-08",
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
        ]

        result = formato_csv.aplanar(regs)
        self.assertEqual(result, expected_data)

    def test_aplanar_empty_records(self):
        """
        Test that the aplanar function handles empty records correctly.
        """
        regs = []
        expected_data = [
            [
                "id",
                "tipo_cbte",
                "punto_vta",
                "cbt_numero",
                "fecha_cbte",
                "tipo_doc",
                "nro_doc",
                "moneda_id",
                "moneda_ctz",
                "imp_neto",
                "imp_iva",
                "imp_trib",
                "imp_op_ex",
                "imp_tot_conc",
                "imp_total",
                "concepto",
                "fecha_venc_pago",
                "fecha_serv_desde",
                "fecha_serv_hasta",
                "cae",
                "fecha_vto",
                "resultado",
                "motivo",
                "reproceso",
                "nombre",
                "domicilio",
                "localidad",
                "telefono",
                "categoria",
                "email",
                "numero_cliente",
                "numero_orden_compra",
                "condicion_frente_iva",
                "numero_cotizacion",
                "numero_remito",
                "obs_generales",
                "obs_comerciales",
            ],
        ]
        result = formato_csv.aplanar(regs)
        self.assertEqual(result, expected_data)





    def test_aplanar_missing_fields(self):
        """
        Test that the aplanar function handles records with missing fields correctly.
        """
        regs = [
            {
                "id": 1,
                "tipo_cbte": 1,
                "punto_vta": 1,
                "cbte_nro": 1,
                "fecha_cbte": "2023-06-08",
                "tipo_doc": 80,
                "nro_doc": "20123456789",
                "moneda_id": "PES",
                "moneda_ctz": 1,
                "imp_neto": 100,
                "imp_iva": 21,
                "imp_trib": 5,
                "imp_op_ex": 0,
                "imp_tot_conc": 0,
                "imp_total": 126,
                "concepto": 1,
                "fecha_venc_pago": "2023-06-08",
                "fecha_serv_desde": "2023-06-08",
                "fecha_serv_hasta": "2023-06-08",
                "cae": "1234567890",
                "fecha_vto": "2023-06-18",
                "resultado": "A",
                "motivo": "",
                "reproceso": "",
                "nombre": "John Doe",
                "domicilio": "123 Main St",
                "localidad": "City",
                "telefono": "1234567890",
                "categoria": "A",
                "email": "john@example.com",
                "numero_cliente": "ABC123",
                "numero_orden_compra": "OC123",
                "condicion_frente_iva": "Responsable Inscripto",
                "numero_cotizacion": "COT123",
                "numero_remito": "REM123",
                "obs_generales": "Observaciones generales",
                "obs_comerciales": "Observaciones comerciales",
                "detalles": [],
                "ivas": [],
                "tributos": [],
                "opcionales": [],
                "cbtes_asoc": [],
                "forma_pago": "Contado",
            },
        ]

        expected_data = [
            [
                "id",
                "tipo_cbte",
                "punto_vta",
                "cbt_numero",
                "fecha_cbte",
                "tipo_doc",
                "nro_doc",
                "moneda_id",
                "moneda_ctz",
                "imp_neto",
                "imp_iva",
                "imp_trib",
                "imp_op_ex",
                "imp_tot_conc",
                "imp_total",
                "concepto",
                "fecha_venc_pago",
                "fecha_serv_desde",
                "fecha_serv_hasta",
                "cae",
                "fecha_vto",
                "resultado",
                "motivo",
                "reproceso",
                "nombre",
                "domicilio",
                "localidad",
                "telefono",
                "categoria",
                "email",
                "numero_cliente",
                "numero_orden_compra",
                "condicion_frente_iva",
                "numero_cotizacion",
                "numero_remito",
                "obs_generales",
                "obs_comerciales",
                "provincia_cliente",
                "forma_pago",
                "pais_dst_cmp",
                "id_impositivo",
                "moneda",
                "tipo_cambio",
                "incoterms",
                "idioma_cbte",
                "motivos_obs",
                "cae_cbte",
                "fch_venc_cae",
                "pais_dst_cliente",
                "pdf",
            ],
            [
                1,
                1,
                1,
                1,
                "2023-06-08",
                80,
                "20123456789",
                "PES",
                1,
                100,
                21,
                5,
                0,
                0,
                126,
                1,
                "2023-06-08",
                "2023-06-08",
                "2023-06-08",
                "1234567890",
                "2023-06-18",
                "A",
                "",
                "",
                "John Doe",
                "123 Main St",
                "City",
                "1234567890",
                "A",
                "john@example.com",
                "ABC123",
                "OC123",
                "Responsable Inscripto",
                "COT123",
                "REM123",
                "Observaciones generales",
                "Observaciones comerciales",
                None,
                "Contado",
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                "",
            ],
        ]

        result = formato_csv.aplanar(regs)
        self.assertEqual(result, expected_data)

# @pytest.mark.dontusefix
# class TestEscribir(unittest.TestCase):
#     def test_escribir_csv_file(self):
#         data = [
#             ["Column1", "Column2", "Column3"],
#             ["Value1", "Value2", "Value3"],
#             ["Value4", "Value5", "Value6"],
#         ]
#         expected_csv_content = "Column1,Column2,Column3\nValue1,Value2,Value3\nValue4,Value5,Value6\n"
#         with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
#             formato_csv.escribir(data, temp_file.name)
#             with open(temp_file.name, "r") as file:
#                 csv_content = file.read()
#             self.assertEqual(csv_content, expected_csv_content)
#         os.unlink(temp_file.name)

#     def test_escribir_xlsx_file(self):
#         data = [
#             ["Column1", "Column2", "Column3"],
#             ["Value1", "Value2", "Value3"],
#             ["Value4", "Value5", "Value6"],
#         ]
#         with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
#             formato_csv.escribir(data, temp_file.name)
#             workbook = load_workbook(temp_file.name)
#             sheet = workbook.active
#             self.assertEqual(sheet["A1"].value, "Column1")
#             self.assertEqual(sheet["B1"].value, "Column2")
#             self.assertEqual(sheet["C1"].value, "Column3")
#             self.assertEqual(sheet["A2"].value, "Value1")
#             self.assertEqual(sheet["B2"].value, "Value2")
#             self.assertEqual(sheet["C2"].value, "Value3")
#             self.assertEqual(sheet["A3"].value, "Value4")
#             self.assertEqual(sheet["B3"].value, "Value5")
#             self.assertEqual(sheet["C3"].value, "Value6")
#         os.unlink(temp_file.name)

# @pytest.mark.dontusefix
# class TestDescribir(unittest.TestCase):
#     def test_desaplanar_single_record(self):
#         data = [
#             [
#                 "id",
#                 "tipo_cbte",
#                 "punto_vta",
#                 "cbt_numero",
#                 "fecha_cbte",
#                 "tipo_doc",
#                 "nro_doc",
#                 "moneda_id",
#                 "moneda_ctz",
#                 "imp_neto",
#                 "imp_iva",
#                 "imp_trib",
#                 "imp_op_ex",
#                 "imp_tot_conc",
#                 "imp_total",
#                 "concepto",
#                 "fecha_venc_pago",
#                 "fecha_serv_desde",
#                 "fecha_serv_hasta",
#                 "cae",
#                 "fecha_vto",
#                 "resultado",
#                 "motivo",
#                 "reproceso",
#                 "nombre",
#                 "domicilio",
#                 "localidad",
#                 "telefono",
#                 "categoria",
#                 "email",
#                 "numero_cliente",
#                 "numero_orden_compra",
#                 "condicion_frente_iva",
#                 "numero_cotizacion",
#                 "numero_remito",
#                 "obs_generales",
#                 "obs_comerciales",
#                 "forma_pago",
#                 "pdf",
#                 "codigo1",
#                 "descripcion1",
#                 "umed1",
#                 "cantidad1",
#                 "precio1",
#                 "importe1",
#                 "iva_id1",
#                 "imp_iva1",
#                 "bonif1",
#                 "numero_despacho1",
#                 "dato_a1",
#                 "dato_b1",
#                 "dato_c1",
#                 "dato_d1",
#                 "dato_e1",
#                 "iva_id_1",
#                 "iva_base_imp_1",
#                 "iva_importe_1",
#                 "tributo_id_1",
#                 "tributo_base_imp_1",
#                 "tributo_desc_1",
#                 "tributo_alic_1",
#                 "tributo_importe_1",
#                 "opcional_id_1",
#                 "opcional_valor_1",
#                 "cbte_asoc_tipo_1",
#                 "cbte_asoc_pto_vta_1",
#                 "cbte_asoc_nro_1",
#                 "cbte_asoc_cuit_1",
#                 "cbte_asoc_fecha_1",
#             ],
#             [
#                 1,
#                 1,
#                 1,
#                 1,
#                 "2023-06-08",
#                 80,
#                 "20123456789",
#                 "PES",
#                 1,
#                 100,
#                 21,
#                 5,
#                 0,
#                 0,
#                 126,
#                 1,
#                 "2023-06-08",
#                 "2023-06-08",
#                 "2023-06-08",
#                 "1234567890",
#                 "2023-06-18",
#                 "A",
#                 "",
#                 "",
#                 "John Doe",
#                 "123 Main St",
#                 "City",
#                 "1234567890",
#                 "A",
#                 "john@example.com",
#                 "ABC123",
#                 "OC123",
#                 "Responsable Inscripto",
#                 "COT123",
#                 "REM123",
#                 "Observaciones generales",
#                 "Observaciones comerciales",
#                 "Contado",
#                 "",
#                 "P1",
#                 "Producto 1",
#                 7,
#                 2,
#                 50,
#                 100,
#                 5,
#                 21,
#                 0,
#                 "",
#                 "",
#                 "",
#                 "",
#                 "",
#                 "",
#                 5,
#                 100,
#                 21,
#                 1,
#                 100,
#                 "Tributo 1",
#                 5,
#                 5,
#                 1,
#                 "Valor opcional 1",
#                 1,
#                 1,
#                 0,
#                 "20123456789",
#                 "2023-06-07",
#             ],
#         ]
#         expected_result = [
#             {
#                 "id": 1,
#                 "tipo_cbte": 1,
#                 "punto_vta": 1,
#                 "cbte_nro": 1,
#                 "fecha_cbte": "2023-06-08",
#                 "tipo_doc": 80,
#                 "nro_doc": "20123456789",
#                 "moneda_id": "PES",
#                 "moneda_ctz": 1,
#                 "imp_neto": 100,
#                 "imp_iva": 21,
#                 "imp_trib": 5,
#                 "imp_op_ex": 0,
#                 "imp_tot_conc": 0,
#                 "imp_total": 126,
#                 "concepto": 1,
#                 "fecha_venc_pago": "2023-06-08",
#                 "fecha_serv_desde": "2023-06-08",
#                 "fecha_serv_hasta": "2023-06-08",
#                 "cae": "1234567890",
#                 "fecha_vto": "2023-06-18",
#                 "resultado": "A",
#                 "motivo": "",
#                 "reproceso": "",
#                 "nombre": "John Doe",
#                 "domicilio": "123 Main St",
#                 "localidad": "City",
#                 "telefono": "1234567890",
#                 "categoria": "A",
#                 "email": "john@example.com",
#                 "numero_cliente": "ABC123",
#                 "numero_orden_compra": "OC123",
#                 "condicion_frente_iva": "Responsable Inscripto",
#                 "numero_cotizacion": "COT123",
#                 "numero_remito": "REM123",
#                 "obs_generales": "Observaciones generales",
#                 "obs_comerciales": "Observaciones comerciales",
#                 "forma_pago": "Contado",
#                 "detalles": [
#                     {
#                         "codigo": "P1",
#                         "ds": "Producto 1",
#                         "umed": 7,
#                         "qty": 2,
#                         "precio": 50,
#                         "importe": 100,
#                         "iva_id": 5,
#                         "imp_iva": 21,
#                         "bonif": 0,
#                         "despacho": None,
#                         "dato_a": None,
#                         "dato_b": None,
#                         "dato_c": None,
#                         "dato_d": None,
#                         "dato_e": None,
#                     }
#                 ],
#                 "tributos": [
#                     {
#                         "tributo_id": 1,
#                         "desc": "Tributo 1",
#                         "base_imp": 100,
#                         "alic": 5,
#                         "importe": 5,
#                     }
#                 ],
#                 "ivas": [
#                     {
#                         "iva_id": 5,
#                         "base_imp": 100,
#                         "importe": 21,
#                     }
#                 ],
#                 "permisos": [],
#                 "opcionales": [
#                     {
#                         "opcional_id": 1,
#                         "valor": "Valor opcional 1",
#                     }
#                 ],
#                 "cbtes_asoc": [
#                     {
#                         "cbte_tipo": 1,
#                         "cbte_punto_vta": 1,
#                         "cbte_nro": 0,
#                         "cbte_cuit": "20123456789",
#                         "cbte_fecha": "2023-06-07",
#                     }
#                 ],
#                 "datos": [],
#             }
#         ]
#         result = formato_csv.desaplanar(data)
#         self.assertEqual(result, expected_result)

#     def test_desaplanar_multiple_records(self):
#         data = [
#             [
#                 "id",
#                 "tipo_cbte",
#                 "punto_vta",
#                 "cbt_numero",
#                 "fecha_cbte",
#                 "tipo_doc",
#                 "nro_doc",
#                 "moneda_id",
#                 "moneda_ctz",
#                 "imp_neto",
#                 "imp_iva",
#                 "imp_trib",
#                 "imp_op_ex",
#                 "imp_tot_conc",
#                 "imp_total",
#                 "concepto",
#                 "fecha_venc_pago",
#                 "fecha_serv_desde",
#                 "fecha_serv_hasta",
#                 "cae",
#                 "fecha_vto",
#                 "resultado",
#                 "motivo",
#                 "reproceso",
#                 "nombre",
#                 "domicilio",
#                 "localidad",
#                 "telefono",
#                 "categoria",
#                 "email",
#                 "numero_cliente",
#                 "numero_orden_compra",
#                 "condicion_frente_iva",
#                 "numero_cotizacion",
#                 "numero_remito",
#                 "obs_generales",
#                 "obs_comerciales",
#                 "forma_pago",
#                 "pdf",
#                 "codigo1",
#                 "descripcion1",
#                 "umed1",
#                 "cantidad1",
#                 "precio1",
#                 "importe1",
#                 "iva_id1",
#                 "imp_iva1",
#                 "bonif1",
#                 "numero_despacho1",
#                 "dato_a1",
#                 "dato_b1",
#                 "dato_c1",
#                 "dato_d1",
#                 "dato_e1",
#                 "iva_id_1",
#                 "iva_base_imp_1",
#                 "iva_importe_1",
#                 "tributo_id_1",
#                 "tributo_base_imp_1",
#                 "tributo_desc_1",
#                 "tributo_alic_1",
#                 "tributo_importe_1",
#                 "opcional_id_1",
#                 "opcional_valor_1",
#                 "cbte_asoc_tipo_1",
#                 "cbte_asoc_pto_vta_1",
#                 "cbte_asoc_nro_1",
#                 "cbte_asoc_cuit_1",
#                 "cbte_asoc_fecha_1",
#                 "codigo2",
#                 "descripcion2",
#                 "umed2",
#                 "cantidad2",
#                 "precio2",
#                 "importe2",
#                 "iva_id2",
#                 "imp_iva2",
#                 "bonif2",
#                 "numero_despacho2",
#                 "dato_a2",
#                 "dato_b2",
#                 "dato_c2",
#                 "dato_d2",
#                 "dato_e2",
#                 "iva_id_2",
#                 "iva_base_imp_2",
#                 "iva_importe_2",
#                 "tributo_id_2",
#                 "tributo_base_imp_2",
#                 "tributo_desc_2",
#                 "tributo_alic_2",
#                 "tributo_importe_2",
#                 "opcional_id_2",
#                 "opcional_valor_2",
#                 "cbte_asoc_tipo_2",
#                 "cbte_asoc_pto_vta_2",
#                 "cbte_asoc_nro_2",
#                 "cbte_asoc_cuit_2",
#                 "cbte_asoc_fecha_2",
#             ],
#             [
#                 1,
#                 1,
#                 1,
#                 1,
#                 "2023-06-08",
#                 80,
#                 "20123456789",
#                 "PES",
#                 1,
#                 100,
#                 21,
#                 5,
#                 0,
#                 0,
#                 126,
#                 1,
#                 "2023-06-08",
#                 "2023-06-08",
#                 "2023-06-08",
#                 "1234567890",
#                 "2023-06-18",
#                 "A",
#                 "",
#                 "",
#                 "John Doe",
#                 "123 Main St",
#                 "City",
#                 "1234567890",
#                 "A",
#                 "john@example.com",
#                 "ABC123",
#                 "OC123",
#                 "Responsable Inscripto",
#                 "COT123",
#                 "REM123",
#                 "Observaciones generales",
#                 "Observaciones comerciales",
#                 "Contado",
#                 "",
#                 "P1",
#                 "Producto 1",
#                 7,
#                 2,
#                 50,
#                 100,
#                 5,
#                 21,
#                 0,
#                 "",
#                 "",
#                 "",
#                 "",
#                 "",
#                 "",
#                 5,
#                 100,
#                 21,
#                 1,
#                 100,
#                 "Tributo 1",
#                 5,
#                 5,
#                 1,
#                 "Valor opcional 1",
#                 1,
#                 1,
#                 0,
#                 "20123456789",
#                 "2023-06-07",
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#             ],
#             [
#                 2,
#                 1,
#                 1,
#                 2,
#                 "2023-06-09",
#                 80,
#                 "20987654321",
#                 "PES",
#                 1,
#                 200,
#                 42,
#                 10,
#                 0,
#                 0,
#                 252,
#                 1,
#                 "2023-06-09",
#                 "2023-06-09",
#                 "2023-06-09",
#                 "0987654321",
#                 "2023-06-19",
#                 "A",
#                 "",
#                 "",
#                 "Jane Smith",
#                 "456 Elm St",
#                 "Town",
#                 "0987654321",
#                 "B",
#                 "jane@example.com",
#                 "XYZ789",
#                 "OC456",
#                 "Responsable Inscripto",
#                 "COT456",
#                 "REM456",
#                 "Observaciones generales",
#                 "Observaciones comerciales",
#                 "Tarjeta de Crédito",
#                 "",
#                 "P2",
#                 "Producto 2",
#                 7,
#                 1,
#                 200,
#                 200,
#                 5,
#                 42,
#                 0,
#                 "",
#                 "",
#                 "",
#                 "",
#                 "",
#                 "",
#                 5,
#                 200,
#                 42,
#                 2,
#                 200,
#                 "Tributo 2",
#                 5,
#                 10,
#                 2,
#                 "Valor opcional 2",
#                 1,
#                 1,
#                 1,
#                 "20123456789",
#                 "2023-06-08",
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#             ],
#         ]
#         expected_result = [
#             {
#                 "id": 1,
#                 "tipo_cbte": 1,
#                 "punto_vta": 1,
#                 "cbte_nro": 1,
#                 "fecha_cbte": "2023-06-08",
#                 "tipo_doc": 80,
#                 "nro_doc": "20123456789",
#                 "moneda_id": "PES",
#                 "moneda_ctz": 1,
#                 "imp_neto": 100,
#                 "imp_iva": 21,
#                 "imp_trib": 5,
#                 "imp_op_ex": 0,
#                 "imp_tot_conc": 0,
#                 "imp_total": 126,
#                 "concepto": 1,
#                 "fecha_venc_pago": "2023-06-08",
#                 "fecha_serv_desde": "2023-06-08",
#                 "fecha_serv_hasta": "2023-06-08",
#                 "cae": "1234567890",
#                 "fecha_vto": "2023-06-18",
#                 "resultado": "A",
#                 "motivo": "",
#                 "reproceso": "",
#                 "nombre": "John Doe",
#                 "domicilio": "123 Main St",
#                 "localidad": "City",
#                 "telefono": "1234567890",
#                 "categoria": "A",
#                 "email": "john@example.com",
#                 "numero_cliente": "ABC123",
#                 "numero_orden_compra": "OC123",
#                 "condicion_frente_iva": "Responsable Inscripto",
#                 "numero_cotizacion": "COT123",
#                 "numero_remito": "REM123",
#                 "obs_generales": "Observaciones generales",
#                 "obs_comerciales": "Observaciones comerciales",
#                 "forma_pago": "Contado",
#                 "detalles": [
#                     {
#                         "codigo": "P1",
#                         "ds": "Producto 1",
#                         "umed": 7,
#                         "qty": 2,
#                         "precio": 50,
#                         "importe": 100,
#                         "iva_id": 5,
#                         "imp_iva": 21,
#                         "bonif": 0,
#                         "despacho": None,
#                         "dato_a": None,
#                         "dato_b": None,
#                         "dato_c": None,
#                         "dato_d": None,
#                         "dato_e": None,
#                     }
#                 ],
#                 "tributos": [
#                     {
#                         "tributo_id": 1,
#                         "desc": "Tributo 1",
#                         "base_imp": 100,
#                         "alic": 5,
#                         "importe": 5,
#                     }
#                 ],
#                 "ivas": [
#                     {
#                         "iva_id": 5,
#                         "base_imp": 100,
#                         "importe": 21,
#                     }
#                 ],
#                 "permisos": [],
#                 "opcionales": [
#                     {
#                         "opcional_id": 1,
#                         "valor": "Valor opcional 1",
#                     }
#                 ],
#                 "cbtes_asoc": [
#                     {
#                         "cbte_tipo": 1,
#                         "cbte_punto_vta": 1,
#                         "cbte_nro": 0,
#                         "cbte_cuit": "20123456789",
#                         "cbte_fecha": "2023-06-07",
#                     }
#                 ],
#                 "datos": [],
#             },
#             {
#                 "id": 2,
#                 "tipo_cbte": 1,
#                 "punto_vta": 1,
#                 "cbte_nro": 2,
#                 "fecha_cbte": "2023-06-09",
#                 "tipo_doc": 80,
#                 "nro_doc": "20987654321",
#                 "moneda_id": "PES",
#                 "moneda_ctz": 1,
#                 "imp_neto": 200,
#                 "imp_iva": 42,
#                 "imp_trib": 10,
#                 "imp_op_ex": 0,
#                 "imp_tot_conc": 0,
#                 "imp_total": 252,
#                 "concepto": 1,
#                 "fecha_venc_pago": "2023-06-09",
#                 "fecha_serv_desde": "2023-06-09",
#                 "fecha_serv_hasta": "2023-06-09",
#                 "cae": "0987654321",
#                 "fecha_vto": "2023-06-19",
#                 "resultado": "A",
#                 "motivo": "",
#                 "reproceso": "",
#                 "nombre": "Jane Smith",
#                 "domicilio": "456 Elm St",
#                 "localidad": "Town",
#                 "telefono": "0987654321",
#                 "categoria": "B",
#                 "email": "jane@example.com",
#                 "numero_cliente": "XYZ789",
#                 "numero_orden_compra": "OC456",
#                 "condicion_frente_iva": "Responsable Inscripto",
#                 "numero_cotizacion": "COT456",
#                 "numero_remito": "REM456",
#                 "obs_generales": "Observaciones generales",
#                 "obs_comerciales": "Observaciones comerciales",
#                 "forma_pago": "Tarjeta de Crédito",
#                 "detalles": [
#                     {
#                         "codigo": "P2",
#                         "ds": "Producto 2",
#                         "umed": 7,
#                         "qty": 1,
#                         "precio": 200,
#                         "importe": 200,
#                         "iva_id": 5,
#                         "imp_iva": 42,
#                         "bonif": 0,
#                         "despacho": None,
#                         "dato_a": None,
#                         "dato_b": None,
#                         "dato_c": None,
#                         "dato_d": None,
#                         "dato_e": None,
#                     }
#                 ],
#                 "tributos": [
#                     {
#                         "tributo_id": 2,
#                         "desc": "Tributo 2",
#                         "base_imp": 200,
#                         "alic": 5,
#                         "importe": 10,
#                     }
#                 ],
#                 "ivas": [
#                     {
#                         "iva_id": 5,
#                         "base_imp": 200,
#                         "importe": 42,
#                     }
#                 ],
#                 "permisos": [],
#                 "opcionales": [
#                     {
#                         "opcional_id": 2,
#                         "valor": "Valor opcional 2",
#                     }
#                 ],
#                 "cbtes_asoc": [
#                     {
#                         "cbte_tipo": 1,
#                         "cbte_punto_vta": 1,
#                         "cbte_nro": 1,
#                         "cbte_cuit": "20123456789",
#                         "cbte_fecha": "2023-06-08",
#                     }
#                 ],
#                 "datos": [],
#             },
#         ]
#         result = formato_csv.desaplanar(data)
#         self.assertEqual(result, expected_result)
    
#     def test_desaplanar_empty_data(self):
#         data = [
#             [
#                 "id",
#                 "tipo_cbte",
#                 "punto_vta",
#                 "cbt_numero",
#                 "fecha_cbte",
#                 "tipo_doc",
#                 "nro_doc",
#                 "moneda_id",
#                 "moneda_ctz",
#                 "imp_neto",
#                 "imp_iva",
#                 "imp_trib",
#                 "imp_op_ex",
#                 "imp_tot_conc",
#                 "imp_total",
#                 "concepto",
#                 "fecha_venc_pago",
#                 "fecha_serv_desde",
#                 "fecha_serv_hasta",
#                 "cae",
#                 "fecha_vto",
#                 "resultado",
#                 "motivo",
#                 "reproceso",
#                 "nombre",
#                 "domicilio",
#                 "localidad",
#                 "telefono",
#                 "categoria",
#                 "email",
#                 "numero_cliente",
#                 "numero_orden_compra",
#                 "condicion_frente_iva",
#                 "numero_cotizacion",
#                 "numero_remito",
#                 "obs_generales",
#                 "obs_comerciales",
#                 "forma_pago",
#                 "pdf",
#             ],
#         ]
#         expected_result = []
#         result = formato_csv.desaplanar(data)
#         self.assertEqual(result, expected_result)

#     def test_desaplanar_missing_fields(self):
#         data = [
#             [
#                 "id",
#                 "tipo_cbte",
#                 "punto_vta",
#                 "cbt_numero",
#                 "fecha_cbte",
#                 "tipo_doc",
#                 "nro_doc",
#                 "moneda_id",
#                 "moneda_ctz",
#                 "imp_neto",
#                 "imp_iva",
#                 "imp_trib",
#                 "imp_op_ex",
#                 "imp_tot_conc",
#                 "imp_total",
#                 "concepto",
#                 "fecha_venc_pago",
#                 "fecha_serv_desde",
#                 "fecha_serv_hasta",
#                 "cae",
#                 "fecha_vto",
#                 "resultado",
#                 "motivo",
#                 "reproceso",
#                 "nombre",
#                 "domicilio",
#                 "localidad",
#                 "telefono",
#                 "categoria",
#                 "email",
#                 "numero_cliente",
#                 "numero_orden_compra",
#                 "condicion_frente_iva",
#                 "numero_cotizacion",
#                 "numero_remito",
#                 "obs_generales",
#                 "obs_comerciales",
#                 "forma_pago",
#                 "pdf",
#             ],
#             [
#                 1,
#                 1,
#                 1,
#                 1,
#                 "2023-06-08",
#                 80,
#                 "20123456789",
#                 "PES",
#                 1,
#                 100,
#                 21,
#                 5,
#                 0,
#                 0,
#                 126,
#                 1,
#                 "2023-06-08",
#                 "2023-06-08",
#                 "2023-06-08",
#                 "1234567890",
#                 "2023-06-18",
#                 "A",
#                 "",
#                 "",
#                 "John Doe",
#                 "123 Main St",
#                 "City",
#                 "1234567890",
#                 "A",
#                 "john@example.com",
#                 "ABC123",
#                 "OC123",
#                 "Responsable Inscripto",
#                 "COT123",
#                 "REM123",
#                 "Observaciones generales",
#                 "Observaciones comerciales",
#                 "Contado",
#                 "",
#             ],
#         ]
#         expected_result = [
#             {
#                 "id": 1,
#                 "tipo_cbte": 1,
#                 "punto_vta": 1,
#                 "cbte_nro": 1,
#                 "fecha_cbte": "2023-06-08",
#                 "tipo_doc": 80,
#                 "nro_doc": "20123456789",
#                 "moneda_id": "PES",
#                 "moneda_ctz": 1,
#                 "imp_neto": 100,
#                 "imp_iva": 21,
#                 "imp_trib": 5,
#                 "imp_op_ex": 0,
#                 "imp_tot_conc": 0,
#                 "imp_total": 126,
#                 "concepto": 1,
#                 "fecha_venc_pago": "2023-06-08",
#                 "fecha_serv_desde": "2023-06-08",
#                 "fecha_serv_hasta": "2023-06-08",
#                 "cae": "1234567890",
#                 "fecha_vto": "2023-06-18",
#                 "resultado": "A",
#                 "motivo": "",
#                 "reproceso": "",
#                 "nombre": "John Doe",
#                 "domicilio": "123 Main St",
#                 "localidad": "City",
#                 "telefono": "1234567890",
#                 "categoria": "A",
#                 "email": "john@example.com",
#                 "numero_cliente": "ABC123",
#                 "numero_orden_compra": "OC123",
#                 "condicion_frente_iva": "Responsable Inscripto",
#                 "numero_cotizacion": "COT123",
#                 "numero_remito": "REM123",
#                 "obs_generales": "Observaciones generales",
#                 "obs_comerciales": "Observaciones comerciales",
#                 "forma_pago": "Contado",
#                 "detalles": [],
#                 "tributos": [],
#                 "ivas": [],
#                 "permisos": [],
#                 "opcionales": [],
#                 "cbtes_asoc": [],
#                 "datos": [],
#             }
#         ]
#         result = formato_csv.desaplanar(data)
#         self.assertEqual(result, expected_result)

#     def test_desaplanar_extra_fields(self):
#         data = [
#             [
#                 "id",
#                 "tipo_cbte",
#                 "punto_vta",
#                 "cbt_numero",
#                 "fecha_cbte",
#                 "tipo_doc",
#                 "nro_doc",
#                 "moneda_id",
#                 "moneda_ctz",
#                 "imp_neto",
#                 "imp_iva",
#                 "imp_trib",
#                 "imp_op_ex",
#                 "imp_tot_conc",
#                 "imp_total",
#                 "concepto",
#                 "fecha_venc_pago",
#                 "fecha_serv_desde",
#                 "fecha_serv_hasta",
#                 "cae",
#                 "fecha_vto",
#                 "resultado",
#                 "motivo",
#                 "reproceso",
#                 "nombre",
#                 "domicilio",
#                 "localidad",
#                 "telefono",
#                 "categoria",
#                 "email",
#                 "numero_cliente",
#                 "numero_orden_compra",
#                 "condicion_frente_iva",
#                 "numero_cotizacion",
#                 "numero_remito",
#                 "obs_generales",
#                 "obs_comerciales",
#                 "forma_pago",
#                 "pdf",
#                 "extra_field1",
#                 "extra_field2",
#             ],
#             [
#                 1,
#                 1,
#                 1,
#                 1,
#                 "2023-06-08",
#                 80,
#                 "20123456789",
#                 "PES",
#                 1,
#                 100,
#                 21,
#                 5,
#                 0,
#                 0,
#                 126,
#                 1,
#                 "2023-06-08",
#                 "2023-06-08",
#                 "2023-06-08",
#                 "1234567890",
#                 "2023-06-18",
#                 "A",
#                 "",
#                 "",
#                 "John Doe",
#                 "123 Main St",
#                 "City",
#                 "1234567890",
#                 "A",
#                 "john@example.com",
#                 "ABC123",
#                 "OC123",
#                 "Responsable Inscripto",
#                 "COT123",
#                 "REM123",
#                 "Observaciones generales",
#                 "Observaciones comerciales",
#                 "Contado",
#                 "",
#                 "Extra Value 1",
#                 "Extra Value 2",
#             ],
#         ]
#         expected_result = [
#             {
#                 "id": 1,
#                 "tipo_cbte": 1,
#                 "punto_vta": 1,
#                 "cbte_nro": 1,
#                 "fecha_cbte": "2023-06-08",
#                 "tipo_doc": 80,
#                 "nro_doc": "20123456789",
#                 "moneda_id": "PES",
#                 "moneda_ctz": 1,
#                 "imp_neto": 100,
#                 "imp_iva": 21,
#                 "imp_trib": 5,
#                 "imp_op_ex": 0,
#                 "imp_tot_conc": 0,
#                 "imp_total": 126,
#                 "concepto": 1,
#                 "fecha_venc_pago": "2023-06-08",
#                 "fecha_serv_desde": "2023-06-08",
#                 "fecha_serv_hasta": "2023-06-08",
#                 "cae": "1234567890",
#                 "fecha_vto": "2023-06-18",
#                 "resultado": "A",
#                 "motivo": "",
#                 "reproceso": "",
#                 "nombre": "John Doe",
#                 "domicilio": "123 Main St",
#                 "localidad": "City",
#                 "telefono": "1234567890",
#                 "categoria": "A",
#                 "email": "john@example.com",
#                 "numero_cliente": "ABC123",
#                 "numero_orden_compra": "OC123",
#                 "condicion_frente_iva": "Responsable Inscripto",
#                 "numero_cotizacion": "COT123",
#                 "numero_remito": "REM123",
#                 "obs_generales": "Observaciones generales",
#                 "obs_comerciales": "Observaciones comerciales",
#                 "forma_pago": "Contado",
#                 "detalles": [],
#                 "tributos": [],
#                 "ivas": [],
#                 "permisos": [],
#                 "opcionales": [],
#                 "cbtes_asoc": [],
#                 "datos": [
#                     {
#                         "campo": "extra_field1",
#                         "valor": "Extra Value 1",
#                         "pagina": "",
#                     },
#                     {
#                         "campo": "extra_field2",
#                         "valor": "Extra Value 2",
#                         "pagina": "",
#                     },
#                 ],
#             }
#         ]
#         result = formato_csv.desaplanar(data)
#         self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
