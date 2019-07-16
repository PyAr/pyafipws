# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para WSBFEv1"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import unittest
import sys
import os
from datetime import datetime, timedelta

from pyafipws.wsaa import WSAA
from pyafipws.wsbfev1 import WSBFEv1

if not os.path.exists('rei.crt'):
    with open('rei.crt', 'w', encoding='utf-8') as f:
        f.write(os.environ['CERT'])

if not os.path.exists('rei.key'):    
    with open('rei.key', 'w', encoding='utf-8') as f:
        f.write(os.environ['PKEY'])


WSDL = "https://wswhomo.afip.gov.ar/wsbfev1/service.asmx?WSDL"
CUIT = 20267565393
CERT = 'rei.crt'
PRIVATEKEY = 'rei.key'
CACHE = "/home/travis/build/pyafipws/cache"

# Debido a que Python solicita una opción de diseño, hay una advertencia
# sobre una conexión no cerrada al ejecutar las pruebas.
# https://github.com/kennethreitz/requests/issues/3912
# Esto puede ser molesto al ejecutar las pruebas, por lo tanto,
# suprimir la advertencia como se discute en
# https://github.com/kennethreitz/requests/issues/1882

# obteniendo el TA para pruebas

ta = WSAA().Autenticar("wsbfe", CERT, PRIVATEKEY)
print(ta)


class TestBFE(unittest.TestCase):
    """Test para WSBFEv1 de AFIP(Bonos Fiscales electronicos v1.1)"""

    def setUp(self):
        #sys.argv.append('--trace')
        self.wsbfev1 = wsbfev1 = WSBFEv1()
        wsbfev1.Cuit = CUIT
        wsbfev1.SetTicketAcceso(ta)
        wsbfev1.Conectar(CACHE, WSDL)
        print(';)')

    def test_dummy(self):
        """Test de estado del servidor."""
        wsbfev1 = self.wsbfev1
        print(wsbfev1.client.help('BFEDummy'))
        wsbfev1.Dummy()
        print("AppServerStatus", wsbfev1.AppServerStatus)
        print("DbServerStatus", wsbfev1.DbServerStatus)
        print("AuthServerStatus", wsbfev1.AuthServerStatus)
        self.assertEqual(wsbfev1.AppServerStatus, 'OK')
        self.assertEqual(wsbfev1.DbServerStatus, 'OK')
        self.assertEqual(wsbfev1.AuthServerStatus, 'OK')


if __name__ == '__main__':
    unittest.main()
