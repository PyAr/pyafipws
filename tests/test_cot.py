# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para Módulo COT (remito electrónico automático
 Codigo de Operacion Translado o Tranporte).
"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import sys
import pytest

from pyafipws.cot import COT

# SSLError- No estaria funcionando el web service testing

pytestmark = pytest.mark.skipif()

URL = "http://cot.test.arba.gov.ar/TransporteBienes/SeguridadCliente/presentarRemitos.do"
CACHE = ""
CACERT = "conf/arba.crt"
filename = 'datos/TB_20111111112_000000_20080124_000001.txt'

wsc = COT()
wsc.Usuario = 20269265393
wsc.Password = 23456


def test_conectar():
    """Conectar con servidor."""
    conexion = wsc.Conectar(URL, trace='--trace' in sys.argv, cacert=CACERT)
    assert conexion


def test_limpiar():
    """Test limpiar."""
    wsc.remitos = ['codigo', 'articulo']
    wsc.Procesado = 'OK'
    wsc.limpiar()
    assert wsc.remitos == []
    assert wsc.Procesado == ''


def test_presentar_remito():
    """Test presentar remito."""
    filename = 'TB_20111111112_000000_20080124_000001.txt'
    result = wsc.PresentarRemito(filename)
    assert result


def test_leer_validacion_remito():
    """Test leer validacion remito."""
    validacion = wsc.LeerValidacionRemito()
    assert validacion


def test_leer_error_validacion():
    """Test leer error validacion."""
    error = wsc.LeerErrorValidacion()
    assert error


def test_analizar_xml():
    """Test analizar xml."""
    xml = way + 'datos/TB_20111111112_000000_20080124_000001.xml'
    xml_result = wsc.AnalizarXml(xml)
    assert xml_result


def test_obtener_tag_xml():
    """Test obtener tag xml."""
    tag = 'x'
    tag = wsc.ObtenerTagXml(*tag)
    assert tag
