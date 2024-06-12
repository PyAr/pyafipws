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

"""Test para formato_xml"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"


import os
import unittest
import pytest
from decimal import Decimal
from pyafipws.formatos import formato_xml

@pytest.mark.dontusefix
class TestFormatoXML(unittest.TestCase):
    def setUp(self):
        # Configuración inicial de los archivos de entrada y salida
        self.entrada_xml = "datos/facturas.xml"
        self.salida_xml = "tests/test_salida.xml"

    def tearDown(self):
        # Limpiar el archivo de salida después de cada prueba
        if os.path.exists(self.salida_xml):
            os.remove(self.salida_xml)

    def test_leer(self):
        # Prueba de la función leer
        regs = formato_xml.leer(self.entrada_xml)
        self.assertEqual(len(regs), 1)
        reg = regs[0]
        self.assertEqual(reg["concepto"], 1)
        self.assertEqual(reg["tipo_doc"], 80)
        self.assertEqual(reg["nro_doc"], 30500010912)
        self.assertEqual(reg["tipo_cbte"], 6)
        self.assertEqual(reg["punto_vta"], 5)
        self.assertEqual(reg["cbt_numero"], 7)
        self.assertEqual(reg["imp_total"], Decimal("1085.57"))
        self.assertEqual(reg["imp_neto"], Decimal("889.82"))
        self.assertEqual(reg["imp_iva"], Decimal("186.86"))
        self.assertEqual(reg["imp_trib"], Decimal("8.89"))
        self.assertEqual(reg["imp_op_ex"], Decimal("0.00"))
        self.assertEqual(reg["fecha_cbte"], "20110609")
        self.assertEqual(reg["fecha_venc_pago"], "")
        self.assertEqual(reg["fecha_serv_desde"], "")
        self.assertEqual(reg["fecha_serv_hasta"], "")
        self.assertEqual(reg["moneda_id"], "PES")
        self.assertEqual(reg["moneda_ctz"], Decimal("1.000000"))
        self.assertEqual(str(reg["cae"]), "61233038185853")
        self.assertEqual(reg["fecha_vto"], "20110619")
        self.assertEqual(len(reg["detalles"]), 1)
        self.assertEqual(len(reg["ivas"]), 1)
        self.assertEqual(len(reg["tributos"]), 1)
        self.assertEqual(len(reg["cbtes_asoc"]), 0)
        self.assertEqual(len(reg["opcionales"]), 0)

    def test_escribir(self):
        # Prueba de la función escribir
        regs = formato_xml.leer(self.entrada_xml)
        formato_xml.escribir(regs, self.salida_xml)
        self.assertTrue(os.path.exists(self.salida_xml))

        # Verificar si el archivo escrito contiene el contenido XML esperado
        with open(self.salida_xml, "r") as f:
            xml_content = f.read()
            self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', xml_content)
            self.assertIn("<comprobantes>", xml_content)
            self.assertIn("</comprobantes>", xml_content)

    def test_serializar(self):
        # Prueba de la función serializar
        regs = formato_xml.leer(self.entrada_xml)
        xml = formato_xml.serializar(regs)
        self.assertIsInstance(xml, str)
        self.assertTrue(xml.startswith('<?xml version="1.0" encoding="UTF-8"?>'))
        self.assertIn("<comprobantes>", xml)
        self.assertIn("<comprobante>", xml)
        self.assertIn("<detalles>", xml)
        self.assertIn("<ivas>", xml)
        self.assertIn("<tributos>", xml)

    def test_mapear(self):
        # Prueba de la función mapear
        # Mapeo con comportamiento predeterminado
        old = {"tipo_cbte": 1, "punto_vta": 2, "cbt_numero": 3}
        new = formato_xml.mapear({}, old, {"tipo": "tipo_cbte", "ptovta": "punto_vta", "numero": "cbt_numero"})
        self.assertEqual(new, {"tipo": 1, "ptovta": 2, "numero": 3})

        # Mapeo con swap=True
        old = {"tipo_cbte": 1, "punto_vta": 2, "cbt_numero": 3}
        new = formato_xml.mapear({}, old, {"tipo_cbte": "tipo", "punto_vta": "ptovta", "cbt_numero": "numero"}, swap=True)
        self.assertEqual(new, {"tipo": 1, "ptovta": 2, "numero": 3})

        # Mapeo con valor faltante
        old = {"tipo_cbte": 1, "punto_vta": 2}
        new = formato_xml.mapear({}, old, {"tipo": "tipo_cbte", "ptovta": "punto_vta", "numero": "cbt_numero"})
        self.assertEqual(new, {"tipo": 1, "ptovta": 2})

        # Mapeo con diccionario vacío
        old = {}
        new = formato_xml.mapear({}, old, {"tipo": "tipo_cbte", "ptovta": "punto_vta", "numero": "cbt_numero"})
        self.assertEqual(new, {})

    def test_desserializar(self):
        # Prueba de la función desserializar
        xml_data = open(self.entrada_xml, "rb").read()
        regs = formato_xml.desserializar(xml_data)
        self.assertEqual(len(regs), 1)
        # Agregar más aserciones para los datos deserializados

    def test_serializar_empty(self):
        # Prueba de la función serializar con una lista vacía
        regs = []
        xml = formato_xml.serializar(regs)
        self.assertIsInstance(xml, str)
        self.assertTrue(xml.startswith('<?xml version="1.0" encoding="UTF-8"?>'))
        self.assertIn("<comprobantes/>", xml)

    def test_mapear_exception(self):
        # Prueba para cubrir el manejo de excepciones en la función mapear
        old = {"a": 1, "b": 2}
        mapping = None  # Proporcionar un mapeo inválido para provocar una excepción
        with self.assertRaises(Exception):
            formato_xml.mapear({}, old, mapping)

if __name__ == "__main__":
    unittest.main()
