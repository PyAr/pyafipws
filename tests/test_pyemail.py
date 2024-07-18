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

"""Test para pyemail"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

from pyafipws.pyemail import PyEmail, main
import pytest
import traceback
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import sys, os
import smtplib
import base64
from configparser import SafeConfigParser

pytestmark = [pytest.mark.dontusefix]

pyemail = PyEmail()
config = SafeConfigParser()
config.read("rece.ini")
conf_mail = dict(config.items("MAIL"))


def test_Connectar_Enviar(mocker):
    """Test de conexion"""
    mocker.patch("smtplib.SMTP")
    pyemail.Conectar(
        conf_mail["servidor"],
        conf_mail["usuario"],
        conf_mail["clave"],
        25,
    )
    pyemail.Enviar(conf_mail["remitente"], "prueba", "check@gmail.com", None)

    pyemail.Salir()

    smtplib.SMTP.assert_called_with(conf_mail["servidor"], 25)


def test_Crear():
    ok = pyemail.Crear()
    assert ok


def test_Agreagar_Destinatario():
    ok = pyemail.AgregarDestinatario("test@gmail.com")
    assert ok


def test_AgregarCC():
    ok = pyemail.AgregarCC("test@gmail.com")
    assert ok


def test_AgregarBCC():
    ok = pyemail.AgregarBCC("test@gmail.com")
    assert ok


def test_Adjuntar():
    ok = pyemail.Adjuntar("test@gmail.com")
    assert ok


def test_main(mocker):
    """Test de funcion main"""
    mocker.patch("smtplib.SMTP")
    sys.argv = []
    sys.argv.append("/debug")
    sys.argv.append("prueba")
    sys.argv.append("test@gmail.com")
    sys.argv.append("")
    main()

    smtplib.SMTP.assert_called_with(conf_mail["servidor"], 25)


def test_main_prueba(mocker):
    mocker.patch("smtplib.SMTP")
    sys.argv = []
    sys.argv.append("/prueba")
    sys.argv.append("user@gmail.com")
    sys.argv.append("pass123")
    main()

    smtplib.SMTP.assert_called_with("smtp.gmail.com", 587)


def test_Conectar_SSL(mocker):
    mocker.patch("smtplib.SMTP_SSL")
    pyemail.Conectar(
        conf_mail["servidor"], conf_mail["usuario"], conf_mail["clave"], 465
    )
    smtplib.SMTP_SSL.assert_called_with(conf_mail["servidor"], 465)


def test_Conectar_TLS(mocker):
    mock_smtp = mocker.patch("smtplib.SMTP")
    pyemail.Conectar(
        conf_mail["servidor"], conf_mail["usuario"], conf_mail["clave"], 587
    )
    mock_smtp.return_value.starttls.assert_called_once()


def test_Conectar_Exception(mocker):
    mocker.patch("smtplib.SMTP", side_effect=Exception("Connection error"))
    result = pyemail.Conectar(
        conf_mail["servidor"], conf_mail["usuario"], conf_mail["clave"], 25
    )
    assert result is False
    assert pyemail.Excepcion != ""
    assert pyemail.Traceback != ""


def test_Enviar_CC_BCC(mocker):
    mocker.patch("smtplib.SMTP")
    pyemail.Conectar(
        conf_mail["servidor"], conf_mail["usuario"], conf_mail["clave"], 25
    )
    pyemail.CC = []  # Clear CC list
    pyemail.BCC = []  # Clear BCC list
    pyemail.AgregarCC("cc@example.com")
    pyemail.AgregarBCC("bcc@example.com")
    pyemail.Enviar(conf_mail["remitente"], "prueba", "check@gmail.com", "Test message")
    assert len(pyemail.CC) == 1
    assert len(pyemail.BCC) == 1


def test_Salir_Exception(mocker):
    mock_smtp = mocker.patch("smtplib.SMTP")
    mock_smtp.return_value.quit.side_effect = Exception("Quit error")
    pyemail.Conectar(
        conf_mail["servidor"], conf_mail["usuario"], conf_mail["clave"], 25
    )
    result = pyemail.Salir()
    assert result is False
    assert pyemail.Excepcion != ""
    assert pyemail.Traceback != ""


def test_Enviar_HTML(mocker):
    mock_smtp = mocker.patch("smtplib.SMTP")
    pyemail.Conectar(
        conf_mail["servidor"], conf_mail["usuario"], conf_mail["clave"], 25
    )
    pyemail.MensajeHTML = "<html><body>Test HTML</body></html>"
    pyemail.MensajeTexto = "Test plain text"
    pyemail.Crear(conf_mail["remitente"], "prueba")
    pyemail.AgregarDestinatario("check@gmail.com")
    pyemail.Enviar()

    assert mock_smtp.return_value.sendmail.called
    call_args = mock_smtp.return_value.sendmail.call_args[0][2]

    assert "Content-Type: multipart/related" in call_args
    assert "Content-Type: multipart/alternative" in call_args
    assert "Content-Type: text/text" in call_args
    assert "Content-Type: text/html" in call_args
    assert "Test plain text" in call_args
    assert "<html><body>Test HTML</body></html>" in call_args

    # Reset for next tests
    pyemail.MensajeHTML = None
    pyemail.MensajeTexto = None


def test_Enviar_Con_Adjunto(mocker):
    mock_smtp = mocker.patch("smtplib.SMTP")
    pyemail.Conectar(
        conf_mail["servidor"], conf_mail["usuario"], conf_mail["clave"], 25
    )
    pyemail.Crear(conf_mail["remitente"], "prueba")
    pyemail.AgregarDestinatario("check@gmail.com")

    attachment_content = "This is a test attachment"
    with open("test_attachment.txt", "w") as f:
        f.write(attachment_content)

    pyemail.Adjuntar("test_attachment.txt")
    pyemail.MensajeTexto = "Test message"
    pyemail.Enviar()

    assert mock_smtp.return_value.sendmail.called
    call_args = mock_smtp.return_value.sendmail.call_args[0][2]

    assert (
        'Content-Disposition: attachment; filename="test_attachment.txt"' in call_args
    )
    encoded_content = base64.b64encode(attachment_content.encode()).decode()
    assert encoded_content in call_args

    os.remove("test_attachment.txt")
    pyemail.adjuntos = []
    pyemail.MensajeTexto = None
