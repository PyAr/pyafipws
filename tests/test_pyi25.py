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

"""Test para pyi25"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"


from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div

import os
import sys
import pytest

from pyafipws.pyi25 import PyI25, main
from PIL import Image, ImageChops

pytestmark = [pytest.mark.dontusefix]

pyi25 = PyI25()


def test_GenerarImagen():
    "Prueba de generación de imagen"
    barras = "2026756539302400161203034739042201105299"
    archivo = "prueba.png"
    pyi25.GenerarImagen(barras, archivo)

    assert os.path.exists(archivo)
    # compare the image with a reference one
    ref = Image.open("tests/images/prueba-cae-i25.png")
    test = Image.open(archivo)
    diff = ImageChops.difference(ref, test)
    assert diff.getbbox() is None


def test_DigitoVerificadorModulo10():
    "Prueba de verificación de Dígitos de Verificación Modulo 10"
    cuit = 20267565393
    tipo_cbte = 2
    punto_vta = 4001
    cae = 61203034739042
    fch_venc_cae = 20110529

    # codigo de barras de ejemplo:
    barras = "%11s%02d%04d%s%8s" % (
        cuit,
        tipo_cbte,
        punto_vta,
        cae,
        fch_venc_cae,
    )

    barras = barras + pyi25.DigitoVerificadorModulo10(barras)
    assert barras == "2026756539302400161203034739042201105299"


def test_main():
    sys.argv = []
    main()


def test_main_archivo():
    sys.argv = []
    sys.argv.append("--archivo")
    sys.argv.append("test123.png")
    main()


def test_main_mostrar(mocker):
    mocker.patch("os.system")
    sys.argv = []
    sys.argv.append("--mostrar")
    archivo = "prueba-cae-i25.png"
    main()
    if sys.platform == "linux2" or sys.platform == "linux":
        os.system.assert_called_with("eog " "%s" "" % archivo)


def test_DigitoVerificadorModulo10_edge_cases():
    assert pyi25.DigitoVerificadorModulo10("") == ""
    assert pyi25.DigitoVerificadorModulo10("123") == "6"
    assert pyi25.DigitoVerificadorModulo10("9999999999") == "0"


def test_main_custom_archivo():
    sys.argv = ["pyi25.py", "--archivo", "custom_test.jpg"]
    main()
    assert os.path.exists("custom_test.jpg")
    os.remove("custom_test.jpg")


def test_GenerarImagen_odd_length_code():
    barras = "12345"
    archivo = "odd_test.png"
    pyi25.GenerarImagen(barras, archivo)
    assert os.path.exists(archivo)
    with Image.open(archivo) as img:
        assert img.size[0] > len(barras) * 3  # Check if 0 was prepended
    os.remove(archivo)


def test_DigitoVerificadorModulo10_non_digit():
    assert pyi25.DigitoVerificadorModulo10("12A34") == ""


def test_DigitoVerificadorModulo10_large_number():
    large_number = "9" * 1000
    result = pyi25.DigitoVerificadorModulo10(large_number)
    assert len(result) == 1 and result.isdigit()


def test_GenerarImagen_with_custom_params():
    barras = "1234567890"
    archivo = "custom_params.png"
    pyi25.GenerarImagen(
        barras, archivo, basewidth=5, width=300, height=50, extension="PNG"
    )
    assert os.path.exists(archivo)
    with Image.open(archivo) as img:
        assert img.size == (300, 50)


def test_main_with_noverificador():
    sys.argv = ["pyi25.py", "--barras", "1234567890", "--noverificador"]
    main()
    assert os.path.exists("prueba-cae-i25.png")
    with open("prueba-cae-i25.png", "rb") as f:
        content = f.read()
    assert len(content) > 0
