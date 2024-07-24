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

"""Test para factura electronica.vbs"""


__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"


"""
Tests for the FacturaElectronicaWrapper class,
which provides a wrapper around the AFIP web services for electronic invoicing.
The tests cover the following functionality:
- Authenticating with the WSAA web service
- Connecting to the WSFEV1 web service
- Creating a new invoice
- Adding a tax to the invoice
- Adding IVA (VAT) to the invoice
- Requesting a CAE (Electronic Authorization Code) for the invoice
- Retrieving the last authorized invoice number
These tests use the `monkeypatch` fixture to mock the behavior of the web
service calls, allowing the tests to run without actually making
the web service calls.
"""

import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ejemplos.factura_electronica_wrapper import FacturaElectronicaWrapper


@pytest.fixture
def factura_electronica():
    return FacturaElectronicaWrapper()


@pytest.mark.dontusefix
def test_autenticar(monkeypatch, factura_electronica):
    monkeypatch.setattr(
        factura_electronica.wsaa,
        "Autenticar",
        lambda *args: True
    )
    assert factura_electronica.autenticar(
        "cert.crt",
        "key.key",
        "https://wsaahomo.afip.gov.ar/ws/services/LoginCms"
    )


@pytest.mark.dontusefix
def test_conectar(monkeypatch, factura_electronica):
    monkeypatch.setattr(
        factura_electronica.wsfev1, "Conectar",
        lambda *args: True
    )
    assert factura_electronica.conectar(
        "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
    )


@pytest.mark.dontusefix
def test_crear_factura(factura_electronica):
    factura_data = {
        "concepto": 1,
        "tipo_doc": 80,
        "nro_doc": "33693450239",
        "tipo_cbte": 1,
        "punto_vta": 4002,
        "cbt_desde": 1,
        "cbt_hasta": 1,
        "imp_total": "124.00",
        "imp_tot_conc": "2.00",
        "imp_neto": "100.00",
        "imp_iva": "21.00",
        "imp_trib": "1.00",
        "imp_op_ex": "0.00",
        "fecha_cbte": "20230101",
        "moneda_id": "PES",
        "moneda_ctz": "1.000",
    }
    assert factura_electronica.crear_factura(**factura_data)


@pytest.mark.dontusefix
def test_agregar_tributo(monkeypatch, factura_electronica):
    monkeypatch.setattr(
        factura_electronica.wsfev1, "AgregarTributo", lambda *args: True
    )
    assert factura_electronica.agregar_tributo(
        99, "Impuesto Municipal Matanza", "100.00", "1.00", "1.00"
    )


@pytest.mark.dontusefix
def test_agregar_iva(monkeypatch, factura_electronica):
    monkeypatch.setattr(
        factura_electronica.wsfev1, "AgregarIva",
        lambda *args: True
    )
    assert factura_electronica.agregar_iva(5, "100.00", "21.00")


@pytest.mark.dontusefix
def test_solicitar_cae(monkeypatch, factura_electronica):
    monkeypatch.setattr(
        factura_electronica.wsfev1, "CAESolicitar",
        lambda: "12345678"
    )
    assert factura_electronica.solicitar_cae() == "12345678"


@pytest.mark.dontusefix
def test_comp_ultimo_autorizado(monkeypatch, factura_electronica):
    monkeypatch.setattr(
        factura_electronica.wsfev1, "CompUltimoAutorizado", lambda *args: 1234
    )
    assert factura_electronica.comp_ultimo_autorizado(1, 4002) == 1234


if __name__ == "__main__":
    pytest.main([__file__, "-v"])