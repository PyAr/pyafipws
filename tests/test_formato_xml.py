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
import pytest
from decimal import Decimal
from pyafipws.formatos import formato_xml


@pytest.mark.dontusefix
class TestFormatoXML:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        # Configuración inicial de los archivos de entrada y salida
        self.entrada_xml = "datos/facturas.xml"
        self.salida_xml = "tests/test_salida.xml"
        yield
        # Limpiar el archivo de salida después de cada prueba
        if os.path.exists(self.salida_xml):
            os.remove(self.salida_xml)

    def test_leer(self):
        # Prueba de la función leer
        regs = formato_xml.leer(self.entrada_xml)
        assert len(regs) == 1
        reg = regs[0]
        assert reg["concepto"] == 1
        assert reg["tipo_doc"] == 80
        assert reg["nro_doc"] == 30500010912
        assert reg["tipo_cbte"] == 6
        assert reg["punto_vta"] == 5
        assert reg["cbt_numero"] == 7
        assert reg["imp_total"] == Decimal("1085.57")
        assert reg["imp_neto"] == Decimal("889.82")
        assert reg["imp_iva"] == Decimal("186.86")
        assert reg["imp_trib"] == Decimal("8.89")
        assert reg["imp_op_ex"] == Decimal("0.00")
        assert reg["fecha_cbte"] == "20110609"
        assert reg["fecha_venc_pago"] == ""
        assert reg["fecha_serv_desde"] == ""
        assert reg["fecha_serv_hasta"] == ""
        assert reg["moneda_id"] == "PES"
        assert reg["moneda_ctz"] == Decimal("1.000000")
        assert str(reg["cae"]) == "61233038185853"
        assert reg["fecha_vto"] == "20110619"
        assert len(reg["detalles"]) == 1
        assert len(reg["ivas"]) == 1
        assert len(reg["tributos"]) == 1
        assert len(reg["cbtes_asoc"]) == 0
        assert len(reg["opcionales"]) == 0

    def test_escribir(self):
        # Prueba de la función escribir
        regs = formato_xml.leer(self.entrada_xml)
        formato_xml.escribir(regs, self.salida_xml)
        assert os.path.exists(self.salida_xml)

        # Verificar si el archivo escrito contiene el contenido XML esperado
        with open(self.salida_xml, "r") as f:
            xml_content = f.read()
            assert '<?xml version="1.0" encoding="UTF-8"?>' in xml_content
            assert "<comprobantes>" in xml_content
            assert "</comprobantes>" in xml_content

    def test_serializar(self):
        # Prueba de la función serializar
        regs = formato_xml.leer(self.entrada_xml)
        xml = formato_xml.serializar(regs)
        assert isinstance(xml, str)
        assert xml.startswith('<?xml version="1.0" encoding="UTF-8"?>')
        assert "<comprobantes>" in xml
        assert "<comprobante>" in xml
        assert "<detalles>" in xml
        assert "<ivas>" in xml
        assert "<tributos>" in xml

    def test_mapear(self):
        # Prueba de la función mapear
        # Mapeo con comportamiento predeterminado
        old = {"tipo_cbte": 1, "punto_vta": 2, "cbt_numero": 3}
        new = formato_xml.mapear(
            {},
            old,
            {
                "tipo": "tipo_cbte",
                "ptovta": "punto_vta",
                "numero": "cbt_numero"
            },
        )
        assert new == {"tipo": 1, "ptovta": 2, "numero": 3}

        # Mapeo con swap=True
        old = {"tipo_cbte": 1, "punto_vta": 2, "cbt_numero": 3}
        new = formato_xml.mapear(
            {},
            old,
            {   
                "tipo_cbte": "tipo",
                "punto_vta": "ptovta",
                "cbt_numero": "numero"
            },
            swap=True,
        )
        assert new == {"tipo": 1, "ptovta": 2, "numero": 3}

        # Mapeo con valor faltante
        old = {"tipo_cbte": 1, "punto_vta": 2}
        new = formato_xml.mapear(
            {},
            old,
            {   
                "tipo": "tipo_cbte",
                "ptovta": "punto_vta",
                 "numero": "cbt_numero"
            },
        )
        assert new == {"tipo": 1, "ptovta": 2}

        # Mapeo con diccionario vacío
        old = {}
        new = formato_xml.mapear(
            {},
            old,
            {
                "tipo": "tipo_cbte",
                "ptovta": "punto_vta",
                "numero": "cbt_numero"
            },
        )
        assert new == {}

    def test_desserializar(self):
        # Prueba de la función desserializar
        xml_data = open(self.entrada_xml, "rb").read()
        regs = formato_xml.desserializar(xml_data)
        assert len(regs) == 1
        # Agregar más aserciones para los datos deserializados

    def test_serializar_empty(self):
        # Prueba de la función serializar con una lista vacía
        regs = []
        xml = formato_xml.serializar(regs)
        assert isinstance(xml, str)
        assert xml.startswith('<?xml version="1.0" encoding="UTF-8"?>')
        assert "<comprobantes/>" in xml

    def test_mapear_exception(self):
        # Prueba para cubrir el manejo de excepciones en la función mapear
        old = {"a": 1, "b": 2}
        mapping = None  # Proporcionar un mapeo inválido para provocar una excepción
        with pytest.raises(Exception):
            formato_xml.mapear({}, old, mapping)


if __name__ == "__main__":
    pytest.main()
