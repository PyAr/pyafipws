#!/usr/bin/python
# -*- coding: latin-1 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Pruebas para WSFEv1 de AFIP
(Factura Electrónica Mercado Interno sin detalle)
"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import unittest
import datetime
import sys
import os

from pyafipws.wsaa import WSAA
from pyafipws.wsfev1 import WSFEv1


WSDL = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
CUIT = os.environ['CUIT']
CERT = 'rei.crt'
PRIVATEKEY = 'rei.key'
CACHE = ""

# obteniendo el TA para pruebas
ta = WSAA().Autenticar("wsfe", "rei.crt", "rei.key")


class TestFE(unittest.TestCase):

    def setUp(self):
        self.wsfev1 = wsfev1 = WSFEv1()
        wsfev1.Cuit = CUIT
        wsfev1.SetTicketAcceso(ta)
        wsfev1.Conectar(CACHE, WSDL)

    def test_dummy(self):
        wsfev1 = self.wsfev1
        print(wsfev1.client.help("FEDummy"))
        wsfev1.Dummy()
        print("AppServerStatus", wsfev1.AppServerStatus)
        print("DbServerStatus", wsfev1.DbServerStatus)
        print("AuthServerStatus", wsfev1.AuthServerStatus)
        self.assertEqual(wsfev1.AppServerStatus, 'OK')
        self.assertEqual(wsfev1.DbServerStatus, 'OK')
        self.assertEqual(wsfev1.AuthServerStatus, 'OK')


if __name__ == '__main__':
    unittest.main()
