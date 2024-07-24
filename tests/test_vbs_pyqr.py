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

"""Test para pyqr.vbs"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"


"""
This module contains tests for the PyQRWrapper class,
which is used to generate QR codes for Argentine electronic invoices.
The tests cover the following functionality:
- `test_pyqr_crear_archivo`: Verifies that the `CrearArchivo` method
returns a non-empty value.
- `test_pyqr_generar_imagen`: Verifies that the `GenerarImagen` method
returns a valid URL for the generated QR code image.
"""


import pytest
import sys
import os
from urllib.parse import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ejemplos.pyqr.pyqr_wrapper import PyQRWrapper


@pytest.fixture(scope="module")
def pyqr():
    return PyQRWrapper()


@pytest.mark.dontusefix
def test_pyqr_crear_archivo(pyqr):
    archivo = pyqr.CrearArchivo()
    assert archivo, "CrearArchivo should return a non-empty value"
    print(f"Archivo: {archivo}")


@pytest.mark.dontusefix
def test_pyqr_generar_imagen(pyqr):
    ver = 1
    fecha = "2020-10-13"
    cuit = 30000000007
    pto_vta = 10
    tipo_cmp = 1
    nro_cmp = 94
    importe = 12100
    moneda = "DOL"
    ctz = 65
    tipo_doc_rec = 80
    nro_doc_rec = 20000000001
    tipo_cod_aut = "E"
    cod_aut = 70417054367476

    url = pyqr.GenerarImagen(
        ver,
        fecha,
        cuit,
        pto_vta,
        tipo_cmp,
        nro_cmp,
        importe,
        moneda,
        ctz,
        tipo_doc_rec,
        nro_doc_rec,
        tipo_cod_aut,
        cod_aut,
    )

    assert url, "GenerarImagen should return a non-empty URL"
    parsed_url = urlparse(url)
    assert parsed_url.scheme and parsed_url.netloc, f"Invalid URL format: {url}"
    assert parsed_url.path.endswith(
        "/qr/"
    ), f"URL does not end with expected path: {url}"
    print(f"URL: {url}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])