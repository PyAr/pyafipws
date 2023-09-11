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

import shutil
import pytest

from pyafipws.formatos.formato_csv import leer, aplanar, desaplanar, escribir

pytestmark = [pytest.mark.dontusefix]

regs = [
    {
        "tipo_cbte": "Factura A",
        "punto_vta": 1,
        "cbt_numero": 123456,
        "cuit": "20-12345678-9",
        "fecha_cbte": "2022-01-01",
        "idioma": "Español",
        "concepto": "Productos varios",
        "moneda_id": "ARS",
        "moneda_ctz": 1.0,
        "tipo_doc": "DNI",
        "nro_doc": 12345678,
        "nombre_cliente": "Juan Perez",
        "domicilio_cliente": "Calle Falsa 123",
        "telefono_cliente": "+54 9 11 1234-5678",
        "localidad_cliente": "Buenos Aires",
        "provincia_cliente": "Buenos Aires",
        "id_impositivo": "AR-123456789-0",
        "email": "juan.perez@example.com",
        "numero_cliente": 987654321,
        "numero_orden_compra": "OC-12345",
        "condicion_frente_iva": "Responsable Inscripto",
        "numero_cotizacion": 54321,
        "numero_remito": 67890,
        "imp_total": 1000.0,
        "imp_tot_conc": 0.0,
        "imp_neto": 800.0,
        "imp_iva": 168.0,
        "imp_trib": 32.0,
        "imp_op_ex": 0.0,
        "fecha_serv_desde": "2022-01-01",
        "fecha_serv_hasta": "2022-01-31",
        "fecha_venc_pago": "2022-02-15",
        "tipo_expo": "No Exportación",
        "incoterms": "FOB",
        "incoterms_ds": "Free on Board",
        "pais_dst_cmp": "Argentina",
        "idioma_cbte": "Español",
        "permiso_existente": False,
        "obs_generales": "Sin observaciones generales",
        "obs_comerciales": "Sin observaciones comerciales",
        "resultado": "Aprobado",
        "cae": "12345678901234",
        "fecha_vto": "2022-02-28",
        "reproceso": False,
        "motivo": "",
        "id": 987654321,
        "detalles": [
            {
                "codigo": "001",
                "ds": "Producto 1",
                "umed": "unidad",
                "qty": 2,
                "precio": 200.0,
                "importe": 400.0,
                "iva_id": 21,
                "imp_iva": 84.0,
                "bonif": 0.0,
                "despacho": "",
                "dato_a": "",
                "dato_b": "",
                "dato_c": "",
                "dato_d": "",
                "dato_e": ""
            },
            {
                "codigo": "002",
                "ds": "Producto 2",
                "umed": "unidad",
                "qty": 1,
                "precio": 400.0,
                "importe": 400.0,
                "iva_id": 21,
                "imp_iva": 84.0,
                "bonif": 0.0,
                "despacho": "",
                "dato_a": "",
                "dato_b": "",
                "dato_c": "",
                "dato_d": "",
                "dato_e": ""
            }
        ],
        "ivas": [
            {
                "iva_id": 21,
                "base_imp": 800.0,
                "importe": 168.0
            }
        ],
        "tributos": [],
        "opcionales": [],
        "cbtes_asoc": []
    }
]


def test_leer_csv():
    """Test reading data from a csv file"""

    data = leer("test_data.csv", ";")

    expected_output = [
        ["Name", "Age", "City"],
        ["John", "30", "New York"],
        ["Jane", "25", "Los Angeles"],
        ["Bob", "40", "Chicago"]
    ]

    assert data == expected_output

def test_leer_xml():
    """Test reading from an excel file"""

    data = leer("test_data.xlsx")

    expected_output = [
        ["Name", "Age", "City"],
        ["John", 30, "New York"],
        ["Jane", 25, "Los Angeles"],
        ["Bob", 40, "Chicago"]
    ]

    assert data == expected_output

def test_aplanar():
    """Test the conversion of a dict to a csv ready format"""

    result = aplanar(regs)

    # Peform some sanity checks 
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], list)


def test_desaplanar():
    filas = [
        ["cbt_numero", "descripcion1", "cantidad1", "descripcion2", "cantidad2", "forma_pago"],
        [123, "Product A", 5, "Product B", 3, 111],
        [456, "Product C", 2, "Product D", 4, 222],
    ]

    result = desaplanar(filas)

    assert isinstance(result, list)
    assert len(result) == 2

    # Check the structure of the first row
    assert isinstance(result[0], dict)
    assert "cbte_nro" in result[0]
    assert "detalles" in result[0]

    # Check the structure of the second row
    assert isinstance(result[1], dict)
    assert "cbte_nro" in result[1]
    assert "detalles" in result[1]
    
    # SANITY CHECKS FOR RESULT DATA  
    assert result[0]["cbte_nro"] == 123
    assert len(result[0]["detalles"]) == 2

    # Example assertion for the second row
    assert result[1]["cbte_nro"] == 456
    assert len(result[1]["detalles"]) == 2  