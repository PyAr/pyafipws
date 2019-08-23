# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para Módulo WDigDepFiel
(Interfaz Depositario Fiel).
"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import os
import datetime
import pytest

from pyafipws.wsaa import WSAA
from pyafipws.wdigdepfiel import dummy, aviso_recep_acept, aviso_digit
from pyafipws import utils
from pyafipws.utils import date, SimpleXMLElement, SoapClient, SoapFault


pytestmark = pytest.mark.skipif()

# Se cambia gov -> gob
WSDL = "https://testdia.afip.gob.ar/Dia/Ws/wDigDepFiel/wDigDepFiel.asmx"
CUIT = os.environ['CUIT']
CERT = 'rei.crt'
PKEY = 'rei.key'
CACHE = ""
SOAP_ACTION = 'ar.gov.afip.dia.serviciosWeb.wDigDepFiel/'
SOAP_NS = 'ar.gov.afip.dia.serviciosWeb.wDigDepFiel'

# obteniendo el TA para pruebas
wsaa = WSAA()
# Afip no devuelve el ticket de acceso para wDigDepFiel
ta_string = wsaa.Autenticar("wDigDepFiel", CERT, PKEY)
print(ta_string, 'NULL')
cuit = CUIT
# utils.BaseWS.SetTicketAcceso(ta)
#utils.BaseWS.Conectar(CACHE, WSDL)

#~ta_string = open(TA).read()
#ta = SimpleXMLElement(ta_string)
# print(ta)
#token = str(ta.credentials.token)
#sign = str(ta.credentials.sign)

# fin TA
# cliente soap del web service
client = SoapClient(WSDL,
                    action=SOAP_ACTION,
                    namespace=SOAP_NS, exceptions=True,
                    trace=True, ns='ar', soap_ns='soap')


def test_server_status():
    """Test de estado de servidores."""
    ret = dummy(client)
    assert ret['appserver'] == 'OK'
    assert ret['dbserver'] == 'OK'
    assert ret['authserver'] == 'OK'


def test_aviso_recep_acept():
    """Test aviso de recepcion aceptada."""
    cuit = 20267565393
    tipo_agente = 'DESP'  # 'DESP'
    rol = 'EXTE'
    nro_legajo = '0' * 16  # '1234567890123456'
    cuit_declarante = cuit_psad = cuit_ie = cuit
    codigo = '000'  # carpeta completa, '0001' carpeta adicional
    fecha_hora_acept = datetime.datetime.now().isoformat()
    ticket = '1234'
    aceptado = aviso_recep_acept(client, token, sign, cuit, tipo_agente, rol,
                                 nro_legajo, cuit_declarante, cuit_psad, cuit_ie,
                                 codigo, fecha_hora_acept, ticket)
    assert aceptado


def test_aviso_digit():
    """Test aviso de digitalizacion."""
    cuit = 20267565393
    tipo_agente = 'DESP'  # 'DESP'
    rol = 'EXTE'
    nro_legajo = '0' * 16  # '1234567890123456'
    cuit_declarante = cuit_psad = cuit_ie = cuit_ata = cuit
    codigo = '000'  # carpeta completa, '0001' carpeta adicional
    ticket = '1234'
    url = 'http://www.example.com'
    hashing = 'db1491eda47d78532cdfca19c62875aade941dc2'
    familias = [{'Familia': {'codigo': '02', 'cantidad': 1}},
                {'Familia': {'codigo': '03', 'cantidad': 3}}, ]
    cantidad_total = 4
    digital = aviso_digit(client, token, sign, cuit, tipo_agente, rol,
                          nro_legajo, cuit_declarante, cuit_psad, cuit_ie, cuit_ata,
                          codigo, url, familias, ticket, hashing, cantidad_total)
    assert digital
