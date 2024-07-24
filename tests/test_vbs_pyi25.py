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

"""Test para pyi25.vbs"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"


"""
This module contains tests for the PyI25Wrapper class,
which is a wrapper around a library for generating barcodes
in the Interleaved 2 of 5 (I25) format.
The tests cover the following functionality:
- Retrieving the version information of the PyI25Wrapper
- Generating a barcode string with a valid check digit
- Generating a barcode image file from a barcode string
The tests use the pytest framework and include fixtures
and markers to manage the test setup and execution.
"""
import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ejemplos.pyi25.pyi25_wrapper import PyI25Wrapper


@pytest.fixture(scope="module")
def pyi25():
    return PyI25Wrapper()


@pytest.mark.dontusefix
def test_pyi25_version(pyi25):
    version = pyi25.Version()
    assert version, "Version information not found"
    print(f"Version: {version}")


@pytest.mark.dontusefix
def test_pyi25_barcode_generation(pyi25):
    barras = "202675653930240016120303473904220110529"
    barras_with_verifier = barras + pyi25.DigitoVerificadorModulo10(barras)
    assert (
        len(barras_with_verifier) == 40
    ), f"Barcode length is {len(barras_with_verifier)}, expected 40"
    print(f"Barras: {barras_with_verifier}")


@pytest.mark.dontusefix
def test_pyi25_image_generation(pyi25):
    barras = "202675653930240016120303473904220110529"
    barras_with_verifier = barras + pyi25.DigitoVerificadorModulo10(barras)
    output_file = "test_barcode.png"
    pyi25.GenerarImagen(barras_with_verifier, output_file)
    assert os.path.exists(
        output_file
    ), f"Generated image file not found at {output_file}"
    print(f"Listo! {output_file}")