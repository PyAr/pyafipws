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

cert = os.environ['CERT']
pkey = os.environ['PKEY']

CERT = cert.replace(r'\n', '\n')
PKEY = pkey.replace(r'\n', '\n')


with open('rei.crt', 'w', encoding='utf-8') as f:
    f.write(CERT)
    
with open('rei.key', 'w', encoding='utf-8') as f:
    f.write(PKEY)


ta = WSAA().Autenticar('wsfe', 'rei.crt', 'rei.key')

cache = '/home/travis/build/NicolasSandoval/pyafipws/cache'


def test_cache(cache=cache):
    assert os.path.exists(cache) == True


def test_acces_ticket(ta=ta):
   assert ta == 'X'

