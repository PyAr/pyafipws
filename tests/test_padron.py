# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para Módulo Padron
(Procesar y consultar el Padrón Unico de Contribuyentes AFIP).
"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"


import pytest

from pyafipws.padron import PadronAFIP

skp = pytest.mark.skip

URL = "http://www.afip.gob.ar/genericos/cInscripcion/archivos/apellidoNombreDenominacion.zip"
URL_API = "https://soa.afip.gob.ar/"
CACHE = ""
wsp = PadronAFIP()


def test_conectar():
    """Conectar con servidor."""
    conexion = wsp.Conectar(CACHE, URL_API)
    assert conexion


def test_inicializar():
    """Test inicializar variables de BaseWS."""
    wsp.inicializar()
    assert wsp.data == {}
    assert wsp.cod_postal == ''
    assert wsp.actividades == []


@skp
def test_descargar():
    """Test descargar el archivo de afip."""
    descarga = wsp.Descargar(URL)
    assert descarga == 200


@skp
def test_procesar():
    """Test procesar: analiza y crea una base de datos
    interna sqlite para consultas."""
    filename = 'aux/padron.txt'
    dato = wsp.Procesar(filename)
    assert dato


@skp
def test_buscar():
    """Test buscar."""
    nro_doc = 20001514939
    tipo_doc = 80
    resultado = wsp.Buscar(nro_doc, tipo_doc)
    assert resultado


@skp
def test_consultar_domicilios():
    """Test consultar domicilios."""
    nro_doc = 34999257706
    tipo_doc = 80
    cat_iva = 1
    resultado = wsp.ConsultarDomicilios(nro_doc, tipo_doc, cat_iva)
    assert resultado


@skp
def test_buscar_cuit():
    """Test buscar cuit."""
    denominacion = 'MUNICIPIO DE ORO VERDE'
    busqueda = wsp.BuscarCUIT(denominacion)
    assert busqueda


@skp
def test_guardar():
    """Test guardar."""
    tipo_doc = 80
    nro_doc = 20277777771
    denominacion = 'Dibag'
    cat_iva = 20
    direccion = 'los naranjos 3526'
    email = 'prueba@gmail.com'

    salvado = wsp.Guardar(tipo_doc, nro_doc, denominacion,
                          cat_iva, direccion, email)
    assert salvado


@skp
def test_consultar():
    """Test consultar."""
    nro_doc = 20278994593
    consulta = wsp.Consultar(nro_doc)
    assert consulta


@skp
def test_descargar_constancia():
    """Test descargar constancia."""
    nro_doc = 34999257706
    constancia = wsp.DescargarConstancia(nro_doc)
    assert constancia


@skp
def test_mostrar_pdf():
    """Test mostrar pdf."""
    archivo = "constancia.pdf"
    pdf = wsp.MostrarPDF(archivo)
    assert pdf


@skp
def test_obtener_tabla_parametros():
    """Test obtener tabla parametros."""
    tipo_recursos = "impuestos"
    tabla = wsp.ObtenerTablaParametros(tipo_recursos)
    assert tabla
