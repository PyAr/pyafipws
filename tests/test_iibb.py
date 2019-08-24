# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para Módulo IIBB
(consultar percepciones / retenciones ARBA).
"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"


import sys
import pytest

from pyafipws.iibb import IIBB

# SSLError- No estaria funcionando el web service testing

pytestmark = pytest.mark.skipif()

URL = "https://dfe.test.arba.gov.ar/DomicilioElectronico/SeguridadCliente/dfeServicioConsulta.do"
CACHE = ""
CACERT = 'conf/arba.crt'

wsiibb = IIBB()
wsiibb.Usuario = 20269265393
wsiibb.Password = 23456
test_response = ""


def test_conectar():
    """Conectar con servidor."""
    conexion = wsiibb.Conectar(
        URL, trace='--trace' in sys.argv, cacert=CACERT, testing=test_response)
    assert conexion


def test_limpiar():
    """Test limpiar."""
    wsiibb.remitos = ['codigo', 'articulo']
    wsiibb.Procesado = 'OK'
    wsiibb.limpiar()
    assert wsiibb.remitos == []
    assert wsiibb.Procesado == ''


def test_consultar_contribuyentes():
    """Test consultar contribuyentes."""
    fecha_desde = 20190701
    fecha_hasta = 20190731
    cuit_contribuyente = 30123456780
    contribuyente = wsiibb.ConsultarContribuyentes(
        fecha_desde, fecha_hasta, cuit_contribuyente)
    assert contribuyente


def test_leer_contribuyente():
    """Test leer contribuyente."""
    datos = wsiibb.LeerContribuyente()
    assert datos


def test_leer_error_validacion():
    """Test leer error validacion."""
    error = wsiibb.LeerErrorValidacion()
    assert error


def test_analizar_xml():
    """Test analizar xml."""
    xml = 'TB_20111111112_000000_20080124_000001.xml'
    xml_result = wsiibb.AnalizarXml(xml)
    assert xml_result


def test_obtener_tag_xml():
    """Test obtener tag xml."""
    tag = 'x'
    tag = wsiibb.ObtenerTagXml(tag)
    assert tag
