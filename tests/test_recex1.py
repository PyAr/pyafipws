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

"""Test para Módulo recex1"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import io
import sys
import time
from unittest.mock import patch, MagicMock

import pytest

from pyafipws import recex1


@pytest.fixture
def mock_ws():
    """
    Fixture que crea un mock del objeto WebService.
    """
    return MagicMock()


@pytest.fixture
def mock_config(mocker):
    """
    Fixture que mockea la función abrir_conf de recex1.
    """
    return mocker.patch("pyafipws.recex1.abrir_conf")


@pytest.fixture
def mock_escribir(mocker):
    """
    Fixture que mockea la función escribir de recex1 y retorna un valor fijo.
    """
    mock = mocker.patch("pyafipws.recex1.escribir")
    mock.return_value = "mocked_string"
    return mock


@pytest.fixture
def mock_guardar_dbf(mocker):
    """
    Fixture que mockea la función guardar_dbf de recex1.
    """
    return mocker.patch("pyafipws.recex1.guardar_dbf")


@pytest.fixture
def mock_conf_dbf(mocker):
    """
    Fixture que mockea el diccionario conf_dbf en recex1.
    """
    return mocker.patch.dict(
        "pyafipws.recex1.__dict__", {"conf_dbf": {"test": "config"}}
    )


@pytest.mark.dontusefix
def test_autorizar_with_testing_arg(mock_ws, mocker):
    """
    Prueba la función autorizar con el argumento de testing.
    """
    mock_entrada = io.StringIO(
        (
            "0,20230101,1,1,1,1,S,203,Test Client,12345678901,Test Address,"
            "Test ID,1000.00,PES,1.0,Test Obs,Test Gen Obs,Test Payment,FOB,"
            "Test Incoterms,1\n"
        )
    )
    mock_salida = io.StringIO()
    mocker.patch.object(mock_ws, "GetLastID", return_value=1)
    mocker.patch.object(mock_ws, "GetLastCMP", return_value=1)
    mocker.patch("pyafipws.recex1.escribir_factura")
    mocker.patch(
        "pyafipws.recex1.leer",
        return_value={
            "id": "",
            "tipo_cbte": "1",
            "punto_vta": "1",
            "cbte_nro": "1",
            "fecha_cbte": "20230101",
            "tipo_expo": "1",
            "permiso_existente": "S",
            "pais_dst_cmp": "203",
            "nombre_cliente": "Test Client",
            "cuit_pais_cliente": "12345678901",
            "domicilio_cliente": "Test Address",
            "id_impositivo": "Test ID",
            "imp_total": "1000.00",
            "moneda_id": "PES",
            "moneda_ctz": "1.0",
            "obs_comerciales": "Test Obs",
            "obs_generales": "Test Gen Obs",
            "forma_pago": "Test Payment",
            "incoterms": "FOB",
            "incoterms_ds": "Test Incoterms",
            "idioma_cbte": "1",
        },
    )
    mocker.patch.object(sys, "argv", ["/testing"])
    mocker.patch.dict(
        "pyafipws.recex1.__dict__",
        {"TIPOS_REG": ("0", "1", "2", "3")}
    )

    recex1.autorizar(mock_ws, mock_entrada, mock_salida)

    mock_ws.CrearFactura.assert_called_once()


@pytest.mark.dontusefix
def test_autorizar_with_full_input(mock_ws, mocker):
    """
    Prueba la función autorizar con una entrada completa.
    """
    mock_entrada = io.StringIO(
        (
            "0,20230101,1,1,1,1,S,203,Test Client,12345678901,Test Address,"
            "Test ID,1000.00,PES,1.0,Test Obs,Test Gen Obs,Test Payment,FOB,"
            "Test Incoterms,1\n"
            "1,PROD1,1,1,1000.00,1000.00,0.00,Test Product\n"
            "2,123456,203\n"
            "3,1,1,1,12345678901\n"
        )
    )
    mock_salida = io.StringIO()
    mocker.patch.object(mock_ws, "GetLastID", return_value=1)
    mocker.patch("pyafipws.recex1.escribir_factura")
    mocker.patch(
        "pyafipws.recex1.leer",
        side_effect=[
            {
                "id": "1",
                "tipo_cbte": "1",
                "punto_vta": "1",
                "cbte_nro": "1",
                "fecha_cbte": "20230101",
            },
            {
                "tipo_reg": "1",
                "codigo": "PROD1",
                "qty": "1",
                "umed": "1",
                "precio": "1000.00",
                "importe": "1000.00",
                "bonif": "0.00",
                "ds": "Test Product",
            },
            {"tipo_reg": "2", "id_permiso": "123456", "dst_merc": "203"},
            {
                "tipo_reg": "3",
                "cbte_tipo": "1",
                "cbte_punto_vta": "1",
                "cbte_nro": "1",
                "cbte_cuit": "12345678901",
            },
        ],
    )
    mocker.patch.dict(
        "pyafipws.recex1.__dict__",
        {"TIPOS_REG": ("0", "1", "2", "3")}
    )

    recex1.autorizar(mock_ws, mock_entrada, mock_salida)

    mock_ws.CrearFactura.assert_called_once()
    mock_ws.AgregarItem.assert_called_once()
    mock_ws.AgregarPermiso.assert_called_once()
    mock_ws.AgregarCmpAsoc.assert_called_once()


@pytest.mark.dontusefix
def test_autorizar_with_error(mock_ws, mocker):
    """
    Prueba la función autorizar cuando se produce un error.
    """
    mock_entrada = io.StringIO(
        (
            "0,20230101,1,1,1,1,S,203,Test Client,12345678901,Test Address,"
            "Test ID,1000.00,PES,1.0,Test Obs,Test Gen Obs,Test Payment,FOB,"
            "Test Incoterms,1\n"
        )
    )
    mock_salida = io.StringIO()
    mocker.patch.object(mock_ws, "GetLastID", return_value=1)
    mocker.patch(
        "pyafipws.recex1.leer",
        return_value={"id": "1", "cbte_nro": "1"}
    )
    mock_ws.Authorize.side_effect = Exception("Test error")
    mocker.patch.dict(
        "pyafipws.recex1.__dict__",
        {"TIPOS_REG": ("0", "1", "2", "3")}
    )

    with pytest.raises(Exception):
        recex1.autorizar(mock_ws, mock_entrada, mock_salida)


@pytest.mark.dontusefix
def test_escribir_factura_basic(mock_escribir):
    """
    Prueba la función escribir_factura con un diccionario básico.
    """
    dic = {"tipo_reg": "0", "id": "1"}
    archivo = io.StringIO()
    recex1.escribir_factura(dic, archivo)

    mock_escribir.assert_called_once_with(dic, recex1.ENCABEZADO)
    assert dic["tipo_reg"] == recex1.TIPOS_REG[0]
    assert archivo.getvalue() == "mocked_string"


@pytest.mark.dontusefix
def test_escribir_factura_with_all_fields(mock_escribir):
    """
    Prueba la función escribir_factura con todos los campos posibles.
    """
    dic = {
        "id": "1",
        "detalles": [{"codigo": "001"}],
        "permisos": [{"id_permiso": "P001"}],
        "cbtes_asoc": [{"cbte_nro": "001"}],
    }
    archivo = io.StringIO()
    recex1.escribir_factura(dic, archivo)

    assert mock_escribir.call_count == 4
    assert archivo.getvalue() == "mocked_string" * 4


@pytest.mark.dontusefix
def test_escribir_factura_with_dbf(
    mock_escribir, mock_guardar_dbf, mock_conf_dbf
):
    """
    Prueba la función escribir_factura con la opción DBF activada.
    """
    dic = {"id": "1"}
    archivo = io.StringIO()

    with patch.object(sys, "argv", ["/dbf"]):
        recex1.escribir_factura(dic, archivo)

    mock_guardar_dbf.assert_called_once()
    expected_formatos = [
        ("Encabezado", recex1.ENCABEZADO, [dic]),
        ("Permisos", recex1.PERMISO, []),
        ("Comprobante Asociado", recex1.CMP_ASOC, []),
        ("Detalles", recex1.DETALLE, []),
    ]
    assert mock_guardar_dbf.call_args[0][0] == expected_formatos
    assert archivo.getvalue() == "mocked_string"


@pytest.mark.dontusefix
def test_escribir_factura_without_dbf(mock_escribir, mock_guardar_dbf):
    """
    Prueba la función escribir_factura sin la opción DBF.
    """
    dic = {"id": "1"}
    archivo = io.StringIO()

    with patch.object(sys, "argv", []):
        recex1.escribir_factura(dic, archivo)

    mock_guardar_dbf.assert_not_called()
    assert archivo.getvalue() == "mocked_string"


@pytest.mark.dontusefix
def test_escribir_factura_agrega_true(
    mock_escribir, mock_guardar_dbf, mock_conf_dbf
):
    """
    Prueba la función escribir_factura con la opción de agregar activada.
    """
    dic = {"id": "1"}
    archivo = io.StringIO()

    with patch.object(sys, "argv", ["/dbf"]):
        recex1.escribir_factura(dic, archivo, agrega=True)

    mock_guardar_dbf.assert_called_once()
    assert mock_guardar_dbf.call_args[0][1] is True
    assert archivo.getvalue() == "mocked_string"


@pytest.mark.dontusefix
def test_escribir_factura_empty_dic(mock_escribir):
    """
    Prueba la función escribir_factura con un diccionario vacío.
    """
    dic = {}
    archivo = io.StringIO()
    recex1.escribir_factura(dic, archivo)

    mock_escribir.assert_called_once()
    assert archivo.getvalue() == "mocked_string"


@pytest.mark.dontusefix
def test_escribir_factura_multiple_items(mock_escribir):
    """
    Prueba la función escribir_factura con múltiples items en cada campo.
    """
    dic = {
        "id": "1",
        "detalles": [{"codigo": "001"}, {"codigo": "002"}],
        "permisos": [{"id_permiso": "P001"}, {"id_permiso": "P002"}],
        "cbtes_asoc": [{"cbte_nro": "001"}, {"cbte_nro": "002"}],
    }
    archivo = io.StringIO()
    recex1.escribir_factura(dic, archivo)

    # 1 (header) + 2 (detalles) + 2 (permisos) + 2 (cbtes_asoc)
    assert mock_escribir.call_count == 7
    assert archivo.getvalue() == "mocked_string" * 7


@pytest.mark.dontusefix
def test_depurar_xml(mocker):
    """
    Prueba la función depurar_xml para asegurar que escribe correctamente
    los archivos de solicitud y respuesta XML.
    """
    mock_client = mocker.Mock()
    mock_client.xml_request = "mock request"
    mock_client.xml_response = b"mock response"

    mock_time = "20230101120000"

    mocker.patch("time.strftime", return_value=mock_time)
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)

    recex1.depurar_xml(mock_client)

    # Verifica que se abren los archivos correctos
    mock_open.assert_any_call(f"request-{mock_time}.xml", "w")
    mock_open.assert_any_call(f"response-{mock_time}.xml", "w")

    # Verifica que se escribe el contenido correcto
    mock_open().write.assert_any_call("mock request")
    mock_open().write.assert_any_call("mock response")

    # Verifica que se llama a close() dos veces (una por cada archivo)
    assert mock_open().close.call_count == 2


@pytest.fixture
def mock_config(mocker):
    """
    Fixture que crea un mock de la configuración.

    Simula las respuestas de un objeto de configuración para diferentes
    secciones y claves.
    """
    config = mocker.MagicMock()
    config.get.side_effect = lambda section, key: {
        ("WSAA", "CERT"): "cert.crt",
        ("WSAA", "PRIVATEKEY"): "key.key",
        ("WSFEXv1", "CUIT"): "20111111112",
        ("WSFEXv1", "ENTRADA"): "entrada.txt",
        ("WSFEXv1", "SALIDA"): "salida.txt",
        ("WSFEXv1", "URL"): "https://test.url",
        ("WSFEXv1", "TIMEOUT"): "30",
    }.get((section, key))
    config.has_option.return_value = True
    config.has_section.return_value = True
    config.items.return_value = [("host", "localhost"), ("port", "8080")]
    return config


@pytest.fixture
def mock_ws(mocker):
    """
    Fixture que crea un mock del objeto WebService.

    Configura valores de retorno predeterminados para varios métodos del WS.
    """
    ws = mocker.MagicMock()
    ws.Dummy.return_value = True
    ws.GetLastCMP.return_value = 1
    ws.GetParamCtz.return_value = 1.0
    ws.GetParamMonConCotizacion.return_value = ["USD:1.0"]
    return ws


@pytest.fixture
def mock_wsaa(mocker):
    """
    Fixture que crea un mock del objeto WSAA.

    Configura un valor de retorno predeterminado para el método Autenticar.
    """
    wsaa = mocker.MagicMock()
    wsaa.Autenticar.return_value = "mocked_ta"
    return wsaa


@pytest.mark.dontusefix
def setup_mocks(mocker, mock_config, mock_ws, mock_wsaa):
    """
    Configura varios mocks para las pruebas.

    Esta función aplica parches a varias funciones y métodos utilizados en
    recex1.py para simular su comportamiento durante las pruebas.
    """
    mocker.patch("pyafipws.recex1.abrir_conf", return_value=mock_config)
    mocker.patch("pyafipws.recex1.wsfexv1.WSFEXv1", return_value=mock_ws)
    mocker.patch("pyafipws.recex1.WSAA", return_value=mock_wsaa)
    mocker.patch("pyafipws.recex1.autorizar")
    mocker.patch("pyafipws.recex1.depurar_xml")
    mocker.patch("pyafipws.recex1.escribir_factura")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.path.getsize", return_value=100)
    mocker.patch("os.path.getmtime", return_value=time.time())
    mocker.patch(
        "builtins.open",
        mocker.mock_open(read_data="mocked_file_content")
    )
    mocker.patch("builtins.input", side_effect=["1", "1", "1"])


@pytest.mark.parametrize(
    "args",
    [
        ["/ayuda"],
        ["/dummy"],
        ["/debug", "/xml", "/ult", "1", "1"],
        ["/get", "1", "1", "1"],
        ["/ctz", "USD"],
        ["/monctz", "20230101"],
        ["/prueba"],
        ["/dbf"],
        ["/testing"],
    ],
)
@pytest.mark.dontusefix
def test_main_comprehensive(mocker, mock_config, mock_ws, mock_wsaa, args):
    """
    Prueba comprehensiva de la función main de recex1.

    Esta prueba verifica el comportamiento de recex1.main() bajo diferentes
    escenarios de ejecución, determinados por los argumentos proporcionados.
    """
    setup_mocks(mocker, mock_config, mock_ws, mock_wsaa)
    mocker.patch.object(recex1.sys, "argv", ["recex1.py"] + args)
    mocker.patch("os.access", return_value=True)
    mocker.patch(
        "builtins.open",
        mocker.mock_open(read_data="mocked_file_content")
    )

    mocker.patch(
        "pyafipws.wsaa.open",
        mocker.mock_open(read_data="mocked_ta_content")
    )
    mocker.patch(
        "os.path.exists",
        return_value=True
    )
    mocker.patch(
        "pyafipws.wsaa.SimpleXMLElement",
        return_value=mocker.MagicMock()
    )

    recex1.main()

    if "/ayuda" in args:
        mock_ws.Conectar.assert_not_called()
        mock_wsaa.Autenticar.assert_not_called()
    else:
        mock_ws.Conectar.assert_called()

    if "/prueba" in args:
        mock_ws.CrearFactura.assert_called_once()
        mock_ws.AgregarItem.assert_called_once()
        mock_ws.AgregarPermiso.assert_called_once()
    elif "/ayuda" not in args:
        if not any(
            arg in args
            for arg in [
                "/dummy", "/ult", "/get",
                "/ctz", "/monctz", "/dbf",
                "/testing"
            ]
        ):
            mock_wsaa.Autenticar.assert_called()

    mock_ws.Cuit = mock_config.get("WSFEXv1", "CUIT")
