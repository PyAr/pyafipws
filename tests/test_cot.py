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

"""Test para cot"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

"""Test the COT (Comprobante de Operaciones en Tránsito) module.

This module contains tests for the COT class, which is used to interact with the
AFIP COT web service. The tests cover various scenarios, including connecting
to the service, presenting remitos, reading validation responses, and handling
errors.
"""

import pytest
from pyafipws.cot import COT, INSTALL_DIR, __version__, HOMO
from pysimplesoap.simplexml import SimpleXMLElement


@pytest.fixture
def cot_instance():
    """Fixture to create a COT instance for testing."""
    return COT()


@pytest.mark.dontusefix
def test_conectar_with_error(cot_instance):
    """
    Test the Conectar method with invalid parameters.
    Expects an exception to be raised.
    """
    with pytest.raises(Exception):
        cot_instance.Conectar(url="invalid_url", proxy="invalid_proxy")


@pytest.mark.dontusefix
def test_presentar_remito_with_file_not_found(cot_instance, monkeypatch):
    """
    Test PresentarRemito method when the file is not found.
    Expects the method to return False and set an appropriate error message.
    """
    monkeypatch.setattr("os.path.exists", lambda x: False)
    result = cot_instance.PresentarRemito("non_existent_file.txt")
    assert result is False
    assert "Archivo no encontrado" in cot_instance.Excepcion


@pytest.mark.dontusefix
def test_leer_validacion_remito(cot_instance):
    """
    Test LeerValidacionRemito method.
    Checks if the method correctly reads and sets remito validation data.
    """
    cot_instance.remitos = [
        {
            "NumeroUnico": "123",
            "Procesado": "SI",
            "COT": "COT123",
            "Errores": [("E001", "Error 1")],
        }
    ]
    assert cot_instance.LeerValidacionRemito() is True
    assert cot_instance.NumeroUnico == "123"
    assert cot_instance.Procesado == "SI"
    assert cot_instance.COT == "COT123"
    assert cot_instance.LeerValidacionRemito() is False


@pytest.mark.dontusefix
def test_leer_error_validacion(cot_instance):
    """
    Test LeerErrorValidacion method.
    Verifies if the method correctly reads and sets error validation data.
    """
    cot_instance.errores = [("E001", "Error 1"), ("E002", "Error 2")]
    assert cot_instance.LeerErrorValidacion() is True
    assert cot_instance.CodigoError == "E002"
    assert cot_instance.MensajeError == "Error 2"
    assert cot_instance.LeerErrorValidacion() is True
    assert cot_instance.CodigoError == "E001"
    assert cot_instance.MensajeError == "Error 1"
    assert cot_instance.LeerErrorValidacion() is False


@pytest.mark.dontusefix
def test_analizar_xml_with_invalid_xml(cot_instance):
    """
    Test AnalizarXml method with invalid XML.
    Expects the method to return False and set an appropriate error message.
    """
    assert cot_instance.AnalizarXml("<invalid>") is False
    assert "no element found" in cot_instance.Excepcion


@pytest.mark.dontusefix
def test_main_function(monkeypatch):
    """
    Test the main function of the COT module.
    Mocks necessary dependencies and checks if
    the function runs without errors.
    """
    monkeypatch.setattr(
        "sys.argv", ["cot.py", "test_file.txt", "test_user", "test_password"]
    )
    monkeypatch.setattr(
        "pyafipws.cot.COT.PresentarRemito",
        lambda self, filename, testing="": True
    )
    from pyafipws.cot import main

    main()


@pytest.mark.dontusefix
def test_cot_initialization(monkeypatch):
    """
    Test the initialization and basic functionality of the COT class.
    Mocks WebClient and file operations,
    then checks various attributes and methods.
    """

    def mock_webclient(*args, **kwargs):
        return lambda *a, **k: "<dummy_response></dummy_response>"

    monkeypatch.setattr("pyafipws.cot.WebClient", mock_webclient)
    monkeypatch.setattr("builtins.open", lambda *args: None)
    monkeypatch.setattr("os.path.exists", lambda x: True)

    cot = COT()
    cot.Usuario = "test_user"
    cot.Password = "test_password"

    cot.Conectar()
    assert cot.client is not None

    result = cot.PresentarRemito("test_file.txt")
    assert result is True
    assert cot.XmlResponse == "<dummy_response></dummy_response>"

    assert cot.LeerErrorValidacion() is False
    assert cot.LeerValidacionRemito() is False
    assert cot.AnalizarXml("<test></test>") is True
    assert cot.ObtenerTagXml("test") is None

    assert cot.InstallDir == INSTALL_DIR
    expected_version = (
        f"{__version__} {'Homologación' if HOMO else ''}".strip()
    )
    assert cot.Version.strip() == expected_version
    assert set(cot._public_methods_) == {
        "Conectar",
        "PresentarRemito",
        "LeerErrorValidacion",
        "LeerValidacionRemito",
        "AnalizarXml",
        "ObtenerTagXml",
    }
    assert cot._reg_progid_ == "COT"
    assert cot._reg_clsid_ == "{7518B2CF-23E9-4821-BC55-D15966E15620}"


@pytest.mark.dontusefix
def test_presentar_remito_with_different_responses(cot_instance, monkeypatch):
    """
    Test PresentarRemito method with various XML responses.
    Checks if the method correctly handles different response structures.
    """
    responses = [
        "<cot><tipoError>0</tipoError></cot>",
        (
            "<cot><tipoError>1</tipoError><codigoError>E001</codigoError>"
            "<mensajeError>Test Error</mensajeError></cot>"
        ),
        (
            "<cot><cuitEmpresa>123456789</cuitEmpresa>"
            "<numeroComprobante>12345</numeroComprobante></cot>"
        ),
        (
            "<cot><validacionesRemitos><remito><numeroUnico>123</numeroUnico>"
            "<procesado>SI</procesado><cot>COT123</cot></remito>"
            "</validacionesRemitos></cot>"
        ),
    ]

    for response in responses:
        monkeypatch.setattr(
            "pyafipws.cot.WebClient",
            lambda *args, **kwargs: lambda *a, **k: response
        )
        monkeypatch.setattr("builtins.open", lambda *args: None)
        monkeypatch.setattr("os.path.exists", lambda x: True)

        result = cot_instance.PresentarRemito("test.txt")
        assert result is False
        cot_instance.AnalizarXml(response)


@pytest.mark.dontusefix
def test_presentar_remito_error_handling(cot_instance, monkeypatch):
    """
    Test error handling in PresentarRemito method.
    Simulates an exception and checks if it's properly handled.
    """

    def raise_exception(*args, **kwargs):
        raise Exception("Test exception")

    monkeypatch.setattr(
        "pyafipws.cot.WebClient", lambda *args, **kwargs: raise_exception
    )
    monkeypatch.setattr("builtins.open", lambda *args: None)
    monkeypatch.setattr("os.path.exists", lambda x: True)

    result = cot_instance.PresentarRemito("test.txt")
    assert result is False
    assert cot_instance.Excepcion != ""


@pytest.mark.dontusefix
def test_obtener_tag_xml(cot_instance):
    """
    Test ObtenerTagXml method.
    Checks if the method correctly retrieves values from XML tags.
    """
    xml = (
        "<root><tag1>value1</tag1><tag2><subtag>value2</subtag></tag2></root>"
    )
    cot_instance.xml = SimpleXMLElement(xml)
    assert cot_instance.ObtenerTagXml("tag1") == "value1"
    assert cot_instance.ObtenerTagXml("tag2", "subtag") == "value2"
    assert cot_instance.ObtenerTagXml("nonexistent") is None


@pytest.mark.dontusefix
def test_analizar_xml_error_handling(cot_instance):
    """
    Test error handling in AnalizarXml method.
    Checks if the method properly handles invalid XML input.
    """
    assert cot_instance.AnalizarXml("") is False
    assert "no element found" in cot_instance.Excepcion


@pytest.mark.dontusefix
def test_limpiar(cot_instance):
    """
    Test limpiar method.
    Verifies if the method correctly resets instance attributes.
    """
    cot_instance.XmlResponse = "test"
    cot_instance.Excepcion = "test"
    cot_instance.TipoError = "test"
    cot_instance.limpiar()
    assert cot_instance.XmlResponse == ""
    assert cot_instance.Excepcion == ""
    assert cot_instance.TipoError == ""
