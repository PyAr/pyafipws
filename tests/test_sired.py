# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para Módulo WSMTXCA de AFIP
(Factura Electrónica Mercado Interno con codificación de productos).
"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import os
import datetime

from pyafipws.wsaa import WSAA
from pyafipws.wsmtx import WSMTXCA

WSDL = "https://fwshomo.afip.gov.ar/wsmtxca/services/MTXCAService?wsdl"
CUIT = 20267565393  # os.environ['CUIT']
CERT = 'rei.crt'
PKEY = 'rei.key'
CACHE = ""

# obteniendo el TA para pruebas
wsaa = WSAA()
wsmtx = WSMTXCA()
ta = wsaa.Autenticar("wsmtxca", CERT, PKEY)
wsmtx.Cuit = CUIT
wsmtx.SetTicketAcceso(ta)
wsmtx.Conectar(CACHE, WSDL)
def test_server_status():
    """Test de estado de servidores."""
    wsmtx.Dummy()
    assert wsmtx.AppServerStatus == 'OK'
    assert wsmtx.DbServerStatus == 'OK'
    assert wsmtx.AuthServerStatus == 'OK'

def test_at_as_dict():
"""Test at_as_dict."""
    assert

def test__planilla():
"""Test _planilla."""
    assert

def test__json():
"""Test _json."""
    assert

def test_ar_json():
"""Test ar_json."""
    assert

def test_rar_encabezado():
"""Test rar_encabezado."""
    assert

def test_rar_detalle():
"""Test rar_detalle."""
    assert

def test_rar_ventas():
"""Test rar_ventas."""
    assert

def test___init__():
"""Test __init__."""
    assert

def test_crearfactura():
"""Test crearfactura."""
    assert

def test_establecerparametro():
"""Test establecerparametro."""
    assert

def test_agregardato():
"""Test agregardato."""
    assert

def test_agregardetalleitem():
"""Test agregardetalleitem."""
    assert

def test_agregarcmpasoc():
"""Test agregarcmpasoc."""
    assert

def test_agregartributo():
"""Test agregartributo."""
    assert

def test_agregariva():
"""Test agregariva."""
    assert

def test_guardarfactura():
"""Test guardarfactura."""
    assert

def test_actualizarfactura():
"""Test actualizarfactura."""
    assert

def test_obtenerfactura():
"""Test obtenerfactura."""
    assert

def test_consultar():
"""Test consultar."""
    assert

def test_    def cmp_dict():
"""Test     def cmp_dict."""
    assert

