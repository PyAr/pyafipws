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

"""Test para WSAA"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import pytest
import io
import os
import sys
import base64
import time
import datetime
from pyafipws.wsaa import WSAA, call_wsaa, sign_tra_openssl, DEFAULT_TTL
from pyafipws.wsaa import main
from past.builtins import basestring
from builtins import str
from pyafipws.utils import SimpleXMLElement, date

WSDL = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms"
CACERT = "conf/afip_ca_info.crt"

pytestmark = [pytest.mark.dontusefix]


@pytest.fixture
def key_and_cert():
    """Fixture for key and certificate"""
    KEY = "reingart.key"
    CERT = "reingart.crt"
    return [KEY, CERT]


@pytest.fixture
def wsaa_instance():
    """Fixture que devuelve una nueva instancia de WSAA para cada prueba."""
    return WSAA()


@pytest.fixture
def mock_dependencies(monkeypatch):
    """
    Fixture que simula varias dependencias y métodos de WSAA para las pruebas.
    Configura un entorno controlado para las operaciones de WSAA.
    """
    monkeypatch.setattr("pyafipws.wsaa.DEBUG", True)
    monkeypatch.setattr("os.path.exists", lambda x: False)
    monkeypatch.setattr("os.path.getsize", lambda x: 0)
    monkeypatch.setattr("os.path.getmtime", lambda x: 0)
    monkeypatch.setattr("time.time", lambda: DEFAULT_TTL + 1)
    monkeypatch.setattr(WSAA, "CreateTRA", lambda self, service, ttl: "mock_tra")
    monkeypatch.setattr(WSAA, "SignTRA", lambda self, tra, crt, key: "mock_cms")
    monkeypatch.setattr(WSAA, "Conectar", lambda self, *args, **kwargs: True)
    monkeypatch.setattr(WSAA, "LoginCMS", lambda self, cms: "mock_ta")
    monkeypatch.setattr(WSAA, "AnalizarXml", lambda self, xml: None)
    monkeypatch.setattr(
        WSAA,
        "ObtenerTagXml",
        lambda self, tag: "mock_token" if tag == "token" else "mock_sign",
    )


@pytest.fixture
def mock_imports(monkeypatch):
    """
    Fixture para simular el fallo de importación de cryptography y la
    información de excepción.
    """

    def mock_exception_info():
        return {
            "msg": "ModuleNotFoundError: import of cryptography halted;"
            " None in sys.modules"
        }

    monkeypatch.setitem(sys.modules, "cryptography", None)
    monkeypatch.setattr("pyafipws.wsaa.exception_info", mock_exception_info)
    yield
    if "cryptography" in sys.modules:
        del sys.modules["cryptography"]


def test_analizar_certificado(key_and_cert):
    """Test analizar datos en certificado."""
    wsaa = WSAA()
    wsaa.AnalizarCertificado(key_and_cert[1])
    assert wsaa.Identidad
    assert wsaa.Caducidad
    assert wsaa.Emisor


def test_crear_clave_privada():
    """Test crear clave RSA."""
    wsaa = WSAA()
    chk = wsaa.CrearClavePrivada()
    assert chk is True


def test_crear_pedido_certificado():
    """Crea CSM para solicitar certificado."""
    wsaa = WSAA()
    chk1 = wsaa.CrearClavePrivada()
    chk2 = wsaa.CrearPedidoCertificado()
    assert chk1 is True
    assert chk2 is True


def test_expirado():
    """Revisar si el TA se encuentra vencido."""
    wsaa = WSAA()
    # checking for expired certificate
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "xml/expired_ta.xml")
    chk = wsaa.AnalizarXml(xml=open(file_path, "r").read())
    chk2 = wsaa.Expirado()

    # checking for a valid certificate,i.e. which will
    # have expiration time 12 hrs(43200 secs) from generation
    fec = str(date("c", date("U") + 43200))
    chk3 = wsaa.Expirado(fecha=fec)

    assert chk is True
    assert chk2 is True
    assert not chk3


@pytest.mark.vcr
def test_login_cms(key_and_cert):
    """comprobando si LoginCMS está funcionando correctamente"""
    wsaa = WSAA()

    tra = wsaa.CreateTRA(service="wsfe", ttl=DEFAULT_TTL)
    cms = wsaa.SignTRA(tra, key_and_cert[1], key_and_cert[0])
    chk = wsaa.Conectar(cache=None, wsdl=WSDL, cacert=CACERT, proxy=None)
    ta_xml = wsaa.LoginCMS(cms)

    ta = SimpleXMLElement(ta_xml)

    if not isinstance(cms, str):
        cms = cms.decode("utf-8")

    assert isinstance(cms, str)

    assert cms.startswith("MII")

    assert chk is True
    assert ta_xml.startswith(
        '<?xml version="1.0" encoding="UTF-8" ' 'standalone="yes"?>'
    )
    assert ta.credentials.token
    assert ta.credentials.sign

    assert "<source>" in ta_xml
    assert "<destination>" in ta_xml
    assert "<uniqueId>" in ta_xml
    assert "<expirationTime>" in ta_xml
    assert "<generationTime>" in ta_xml
    assert "<credentials>" in ta_xml
    assert "<token>" in ta_xml
    assert "<sign>" in ta_xml
    assert ta_xml.endswith("</loginTicketResponse>\n")


def test_wsaa_create_tra():
    wsaa = WSAA()
    tra = wsaa.CreateTRA(service="wsfe")

    # sanity checks:
    assert isinstance(tra, basestring)
    assert tra.startswith(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<loginTicketRequest version="1.0">'
    )
    assert "<uniqueId>" in tra
    assert "<expirationTime>" in tra
    assert "<generationTime>" in tra
    assert tra.endswith("<service>wsfe</service></loginTicketRequest>")


def test_wsaa_sign():
    wsaa = WSAA()
    tra = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<loginTicketRequest version="1.0"/>'
    )
    # TODO: use certificate and private key as fixture / PEM text (not files)
    cms = wsaa.SignTRA(tra, "reingart.crt", "reingart.key")
    # TODO: return string
    if not isinstance(cms, str):
        cms = cms.decode("utf8")
    # sanity checks:
    assert isinstance(cms, str)
    out = base64.b64decode(cms)
    assert tra.encode("utf8") in out


def test_wsaa_sign_tra(key_and_cert):
    wsaa = WSAA()

    tra = wsaa.CreateTRA("wsfe")
    sign = wsaa.SignTRA(tra, key_and_cert[1], key_and_cert[0])

    if not isinstance(sign, str):
        sign = sign.decode("utf-8")

    assert isinstance(sign, str)
    assert sign.startswith("MII")


def test_wsaa_sign_openssl(key_and_cert, monkeypatch):
    """
    Prueba de la función sign_tra_openssl:
    1. Verificar la firma exitosa
    2. Comprobar el comportamiento cuando OpenSSL no está en la RUTA (PATH)
    3. Verificar el manejo de otros errores del sistema operativo (OSErrors)
    """

    wsaa = WSAA()
    tra = wsaa.CreateTRA("wsfe").encode()

    # Test successful signing
    sign = sign_tra_openssl(tra, key_and_cert[1], key_and_cert[0])

    # check if the commanmd line input is a byte data
    assert isinstance(sign, bytes)
    assert sign.decode("utf8").startswith("MII")

    # Test OpenSSL not in PATH
    def mock_popen_not_found(*args, **kwargs):
        raise OSError(2, "File not found")

    monkeypatch.setattr("pyafipws.wsaa.Popen", mock_popen_not_found)
    with pytest.warns(
        UserWarning,
        match="El ejecutable de OpenSSL no esta disponible en el PATH"
    ):
        with pytest.raises(OSError):
            sign_tra_openssl(tra, key_and_cert[1], key_and_cert[0])

    # Test other OSError
    def mock_popen_other_error(*args, **kwargs):
        raise OSError(1, "Operation not permitted")

    monkeypatch.setattr("pyafipws.wsaa.Popen", mock_popen_other_error)
    with pytest.raises(OSError):
        sign_tra_openssl(tra, key_and_cert[1], key_and_cert[0])


def test_wsaa_sign_tra_inline(key_and_cert):
    wsaa = WSAA()

    tra = wsaa.CreateTRA("wsfe")
    sign = wsaa.SignTRA(tra, key_and_cert[1], key_and_cert[0])

    sign_2 = wsaa.SignTRA(
        tra, open(key_and_cert[1]).read(), open(key_and_cert[0]).read()
    )

    if not isinstance(sign, str):
        sign = sign.decode("utf-8")

    if not isinstance(sign_2, str):
        sign_2 = sign_2.decode("utf-8")

    assert isinstance(sign, str)
    assert sign.startswith("MII")

    assert isinstance(sign_2, str)
    assert sign_2.startswith("MII")


@pytest.mark.vcr
def test_main():
    sys.argv = []
    sys.argv.append("--debug")
    main()


@pytest.mark.vcr
def test_main_crear_pedido_cert():
    sys.argv = []
    sys.argv.append("--crear_pedido_cert")
    sys.argv.append("20267565393")
    sys.argv.append("PyAfipWs")
    sys.argv.append("54654654")
    sys.argv.append(" ")
    main()


@pytest.mark.vcr
def test_main_analizar():
    sys.argv = []
    sys.argv.append("--analizar")
    main()


@pytest.mark.vcr
def test_CallWSAA(key_and_cert):
    wsaa = WSAA()
    tra = wsaa.CreateTRA(service="wsfe", ttl=DEFAULT_TTL)
    cms = wsaa.SignTRA(tra, key_and_cert[1], key_and_cert[0])
    assert wsaa.CallWSAA(cms, WSDL)


@pytest.mark.vcr
def test_call_wsaa(key_and_cert):
    wsaa = WSAA()
    tra = wsaa.CreateTRA(service="wsfe", ttl=DEFAULT_TTL)
    cms = wsaa.SignTRA(tra, key_and_cert[1], key_and_cert[0])
    assert call_wsaa(cms, WSDL)


def test_import_error_handling(mock_imports):
    """
    Caso de prueba para verificar el manejo de errores cuando falla la importación del módulo cryptography.
    Verifica advertencias correctas, presencia de atributos y contenido del mensaje de error.
    """

    with pytest.warns(UserWarning) as w:
        import importlib

        importlib.reload(pytest.importorskip("pyafipws.wsaa"))

    wsaa = pytest.importorskip("pyafipws.wsaa")
    assert wsaa.Binding is None
    assert all(hasattr(wsaa, attr) for attr in ["Popen", "PIPE", "b64encode"])
    assert len(w) == 2
    assert str(w[0].message) == "No es posible importar cryptography (OpenSSL)"
    assert (
        str(w[1].message).strip() ==
        "ModuleNotFoundError: import of cryptography halted; None in sys.modules"
    )


def test_autenticar_full_flow(wsaa_instance, mock_dependencies, tmp_path, capsys, monkeypatch, mocker):
    """
    Prueba el flujo completo de autenticación de WSAA.
    Esto incluye crear un nuevo TA, leer un TA existente y manejar fallos de conexión.
    Verifica el comportamiento correcto en cada escenario y comprueba el manejo adecuado de errores.
    """
    # Create mock certificate and key files
    mock_cert = tmp_path / "test.crt"
    mock_key = tmp_path / "test.key"
    mock_cert.write_text("Mock certificate content")
    mock_key.write_text("Mock key content")

    # Mock os.access to always return True for our mock files
    def mock_access(path, mode):
        return str(path) in (str(mock_cert), str(mock_key))

    monkeypatch.setattr(os, "access", mock_access)

    # Test new TA creation
    result = wsaa_instance.Autenticar(
        "test_service", str(mock_cert), str(mock_key), cache=str(tmp_path)
    )

    assert result == "mock_ta"
    assert wsaa_instance.Token == "mock_token"
    assert wsaa_instance.Sign == "mock_sign"

    captured = capsys.readouterr()
    assert "Creando TRA..." in captured.out
    assert "Firmando TRA..." in captured.out
    assert "Conectando a WSAA..." in captured.out
    assert "Llamando WSAA..." in captured.out
    assert "Grabando TA en" in captured.out

    # Test existing TA
    ta_file = tmp_path / "TA-test.xml"
    ta_file.write_text("existing_ta")

    monkeypatch.setattr("os.path.exists", lambda x: True)
    monkeypatch.setattr("os.path.getsize", lambda x: 100)
    monkeypatch.setattr("os.path.getmtime", lambda x: time.time())

    # Mock open to return our mock TA content
    monkeypatch.setattr(
        "builtins.open", lambda *args, **kwargs: io.StringIO("existing_ta")
    )

    # Ensure LoginCMS is not called when TA exists
    monkeypatch.setattr(
        WSAA, "LoginCMS", lambda self, cms: pytest.fail("LoginCMS should not be called")
    )

    result = wsaa_instance.Autenticar(
        "test_service", str(mock_cert), str(mock_key), cache=str(tmp_path)
    )
    assert result == "existing_ta"

    captured = capsys.readouterr()
    assert "Leyendo TA de" in captured.out

    # Test connection failure
    monkeypatch.setattr(
        "os.path.getmtime", lambda x: time.time() - 36000
    )  # Make TA appear 10 hours old
    mock_conectar = mocker.patch.object(WSAA, "Conectar", return_value=False)
    mock_create_tra = mocker.patch.object(WSAA, "CreateTRA", return_value="mock_tra")
    mock_sign_tra = mocker.patch.object(WSAA, "SignTRA", return_value="mock_cms")

    with pytest.raises(RuntimeError) as excinfo:
        wsaa_instance.Autenticar(
            "test_service", str(mock_cert), str(mock_key), cache=str(tmp_path)
        )

    assert "Fallo la conexión:" in str(excinfo.value)
    assert mock_conectar.called
    assert mock_create_tra.called
    assert mock_sign_tra.called

    # Check that Excepcion contains the expected error message
    assert "Fallo la conexión:" in wsaa_instance.Excepcion


def test_autenticar_error_handling(mocker):
    """
    Prueba el método AnalizarCertificado con una entrada de certificado binario.
    Verifica que el método analice correctamente el certificado y establezca los atributos apropiados.
    """
    wsaa = WSAA()
    mocker.patch("os.access", return_value=False)

    with pytest.raises(RuntimeError, match="Imposible abrir"):
        wsaa.Autenticar("test_service", "nonexistent.crt", "nonexistent.key")


def test_expirado_with_custom_date():
    """
    Prueba el método Expirado con fechas personalizadas futuras y pasadas.
    """
    wsaa = WSAA()

    future_date = datetime.datetime.now() + datetime.timedelta(days=1)
    assert not wsaa.Expirado(future_date.strftime("%Y-%m-%dT%H:%M:%S"))

    past_date = datetime.datetime.now() - datetime.timedelta(days=1)
    assert wsaa.Expirado(past_date.strftime("%Y-%m-%dT%H:%M:%S"))


def test_analizar_certificado_binary(mocker):
    """
    Prueba el método Expirado con fechas personalizadas futuras y pasadas.
    """
    wsaa = WSAA()
    mock_cert = mocker.Mock()
    mocker.patch("pyafipws.wsaa.x509.load_pem_x509_certificate", return_value=mock_cert)

    binary_cert = b"-----BEGIN CERTIFICATE-----\nMIID...\n" b"-----END CERTIFICATE-----"
    result = wsaa.AnalizarCertificado(binary_cert, binary=True)

    assert result is True
    assert wsaa.Identidad == mock_cert.subject
    assert wsaa.Caducidad == mock_cert.not_valid_after
    assert wsaa.Emisor == mock_cert.issuer
    assert wsaa.CertX509 == mock_cert
