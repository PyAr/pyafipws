# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para WSAA"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"


import sys
import os

from pyafipws.wsaa import WSAA
from pyafipws.wsbfev1 import WSBFEv1

cert = os.environ['CERT']
pkey = os.environ['PKEY']

CERT = cert.replace(r'\n', '\n')
PKEY = pkey.replace(r'\n', '\n')


with open('rei.crt', 'w', encoding='utf-8') as f:
    f.write(CERT)
    
with open('rei.key', 'w', encoding='utf-8') as f:
    f.write(PKEY)

cuit = os.environ['CUIT']
CACHE = ''
WSDL = "https://wswhomo.afip.gov.ar/wsbfev1/service.asmx?WSDL"


wsbfev1 = WSBFEv1()
wsaa = WSAA()
tax = wsaa.Autenticar('wsfe', 'rei.crt', 'rei.key')

wsbfev1.Cuit = cuit
wsbfev1.SetTicketAcceso(tax)
wsbfev1.Conectar(CACHE, WSDL)
wsbfev1.Dummy()


def test_autenticar(sign=tax):
    assert isinstance(tax, str)


def test_app_server_status():
    assert wsbfev1.AppServerStatus == 'OK'


def test_db_server_status():
    assert wsbfev1.DbServerStatus == 'OK'


def test_Auth_server_status():
    assert wsbfev1.AppServerStatus == 'OK'
