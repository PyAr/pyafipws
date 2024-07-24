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

"""Test para remito electronico carnico.vbs"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"


"""
This module contains tests for the RemitoElectronicoCarnicoWrapper class, which is used to interact with the AFIP's Remito Electrónico Cárnico web service.
The tests cover the following functionality:
- Authenticating with the WSAA service
- Connecting to the WSREMCARNE service
- Creating a new remito (electronic shipping document)
- Adding a trip to the remito
- Adding a vehicle to the remito
- Adding merchandise to the remito
- Generating the remito
- Retrieving the last generated remito number
Each test uses the `monkeypatch` fixture to mock the behavior of the underlying WSAA and WSREMCARNE services, allowing the tests to run without actually making external service calls.
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ejemplos.remito_electronico_carnico_wrapper import RemitoElectronicoCarnicoWrapper

@pytest.fixture
def remito_electronico():
    return RemitoElectronicoCarnicoWrapper()

@pytest.mark.dontusefix
def test_autenticar(monkeypatch, remito_electronico):
    monkeypatch.setattr(remito_electronico.wsaa, 'Autenticar', lambda *args: True)
    assert remito_electronico.autenticar("cert.crt", "key.key", "https://wsaahomo.afip.gov.ar/ws/services/LoginCms")

@pytest.mark.dontusefix
def test_conectar(monkeypatch, remito_electronico):
    monkeypatch.setattr(remito_electronico.wsremcarne, 'Conectar', lambda *args: True)
    assert remito_electronico.conectar("https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL")

@pytest.mark.dontusefix
def test_crear_remito(monkeypatch, remito_electronico):
    monkeypatch.setattr(remito_electronico.wsremcarne, 'CrearRemito', lambda **kwargs: True)
    remito_data = {
        'tipo_comprobante': 995,
        'punto_emision': 1,
        'tipo_movimiento': "ENV",
        'categoria_emisor': 1,
        'cuit_titular_mercaderia': "20222222223",
        'cod_dom_origen': 1,
        'tipo_receptor': "EM",
        'caracter_receptor': 1,
        'cuit_receptor': "20111111112",
        'cuit_depositario': None,
        'cod_dom_destino': 1,
        'cod_rem_redestinar': None,
        'cod_remito': None,
        'estado': None
    }
    assert remito_electronico.crear_remito(**remito_data)

@pytest.mark.dontusefix
def test_agregar_viaje(monkeypatch, remito_electronico):
    monkeypatch.setattr(remito_electronico.wsremcarne, 'AgregarViaje', lambda **kwargs: True)
    viaje_data = {
        'cuit_transportista': "20333333334",
        'cuit_conductor': "20333333334",
        'fecha_inicio_viaje': "2023-01-01",
        'distancia_km': 999
    }
    assert remito_electronico.agregar_viaje(**viaje_data)

@pytest.mark.dontusefix
def test_agregar_vehiculo(monkeypatch, remito_electronico):
    monkeypatch.setattr(remito_electronico.wsremcarne, 'AgregarVehiculo', lambda *args: True)
    assert remito_electronico.agregar_vehiculo("AAA000", "ZZZ000")

@pytest.mark.dontusefix
def test_agregar_mercaderia(monkeypatch, remito_electronico):
    monkeypatch.setattr(remito_electronico.wsremcarne, 'AgregarMercaderia', lambda **kwargs: True)
    mercaderia_data = {
        'orden': 1,
        'tropa': 1,
        'cod_tipo_prod': "2.13",
        'cantidad': 10,
        'unidades': 1
    }
    assert remito_electronico.agregar_mercaderia(**mercaderia_data)

@pytest.mark.dontusefix
def test_generar_remito(monkeypatch, remito_electronico):
    monkeypatch.setattr(remito_electronico.wsremcarne, 'GenerarRemito', lambda *args: True)
    assert remito_electronico.generar_remito(12345, "qr.png")

@pytest.mark.dontusefix
def test_consultar_ultimo_remito_emitido(monkeypatch, remito_electronico):
    monkeypatch.setattr(remito_electronico.wsremcarne, 'ConsultarUltimoRemitoEmitido', lambda *args: 1234)
    assert remito_electronico.consultar_ultimo_remito_emitido(995, 1) == 1234

if __name__ == "__main__":
    pytest.main([__file__, "-v"])