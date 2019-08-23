# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para Módulo WSCOC
(Consulta de Operaciones Cambiarias).
"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import os
import pytest

from pyafipws.wsaa import WSAA
from pyafipws.wscoc import WSCOC

pytestmark = pytest.mark.skipif()
# No se puede establecer conexion


WSDL = "https://fwshomo.afip.gov.ar/wscoc/COCService?wsdl"
CUIT = 20267565393  # os.environ['CUIT']
CERT = 'rei.crt'
PKEY = 'rei.key'
CACHE = ""

# obteniendo el TA para pruebas
wsaa = WSAA()
wscoc = WSCOC()
ta = wsaa.Autenticar("wscoc", CERT, PKEY)
wscoc.Cuit = CUIT
# wscoc.SetTicketAcceso(ta)
# wscoc.Conectar(CACHE, WSDL)


def test_conectar():
    """Conectar con servidor."""
    conexion = wscoc.Conectar(CACHE, WSDL)
    assert conexion


def test_server_status():
    """Test de estado de servidores."""
    wscoc.Dummy()
    assert wscoc.AppServerStatus == 'OK'
    assert wscoc.DbServerStatus == 'OK'
    assert wscoc.AuthServerStatus == 'OK'


def test_analizar_errores():
    """Test analizar errores."""
    ret = {'arrayErrores': [{'codigoDescripcion': {
        'codigo': 1106,
        'descripcion': 'No existen puntos de venta habilitados para utilizar en el presente wscoc.'
    }}]}
    wscoc._WSCOC__analizar_errores(ret)
    # devuelve '' si no encuentra errores
    assert wscoc.Errores


def test_analizar_solicitud():
    """Test analizar solicitud."""
    ret = {'detalleSolicitud': [{"DetalleCUITRepresentante": {
        'cuit': 20206562553,
    }}]}
    wscoc._WSCOC__analizar_solicitud(ret)
    assert wscoc.CUITRepresentante


def test_analizar_inconsistencias():
    """Test analizar inconsistencias."""
    ret = {'arrayInconsistencias': [{'codigoDescripcion': {
        'codigo': 1106,
        'descripcion': 'No existen puntos de venta.'
    }}]}
    wscoc._WSCOC__analizar_inconsistencias(ret)
    assert wscoc.Inconsistencias


def test_generar_solicitud_compra_divisa_tur_ext():
    """Test generar solicitud compra divisa turista extranjero."""
    tipo_doc = 91
    numero_doc = 1234567
    apellido_nombre = "Nombre y Apellido del turista extranjero"
    codigo_destino = 985
    codigo_moneda = 1
    cotizacion_moneda = 4.26
    monto_pesos = 100
    cuit_representante = None
    solicitud = wscoc.GenerarSolicitudCompraDivisaTurExt(
        tipo_doc, numero_doc, apellido_nombre,
        codigo_moneda, cotizacion_moneda, monto_pesos,
        cuit_representante, codigo_destino,
    )
    assert solicitud


def test_generar_solicitud_compra_divisa():
    """Test generar solicitud compra divisa."""
    cuit_comprador = 20267565393
    codigo_moneda = 1
    cotizacion_moneda = 4.26
    monto_pesos = 100
    cuit_representante = None
    codigo_destino = 625

    djai = None
    djas = None
    cod_excepcion_djai = "--no-djai" and 3 or None
    cod_excepcion_djas = "--no-djas" and 1 or None
    tipo = None
    codigo = None
    solicitud = wscoc.GenerarSolicitudCompraDivisa(cuit_comprador, codigo_moneda,
                                                   cotizacion_moneda, monto_pesos,
                                                   cuit_representante, codigo_destino,
                                                   djai, codigo_excepcion_djai,
                                                   djas, codigo_excepcion_djas,
                                                   tipo, codigo)

    assert solicitud


def test_informar_solicitud_compra_divisa():
    """Test informar solicitud compra divisa."""
    codigo_solicitud = wscoc.CodigoSolicitud
    # CO: confirmar, o 'DC' (desistio cliente) 'DB' (desistio banco)
    nuevo_estado = 'CO'
    solicitud = wscoc.InformarSolicitudCompraDivisa(
        codigo_solicitud, nuevo_estado)
    assert solicitud


def test_consultar_cuit():
    """Test consultar cuit."""
    nro_doc = 26756539
    tipo_doc = 96
    consulta = wscoc.ConsultarCUIT(nro_doc, tipo_doc)
    assert consulta


def test_leer_cuit_consultado():
    """Test leer cuit consultado."""
    while wscoc.LeerCUITConsultado():
        assert wscoc.CUITConsultada
        assert wscoc.DenominacionConsultada


def test_consultar_coc():
    """Test consultar coc."""
    coc = coc = wscoc.COC
    consulta = wscoc.ConsultarCOC(coc)
    assert consulta


def test_anular_coc():
    """Test anular coc."""
    coc = wscoc.COC
    cuit_comprador = None
    anulado = wscoc.AnularCOC(coc, cuit_comprador)
    assert anulado


def test_consultar_solicitud_compra_divisa():
    """Test consultar solicitud compra divisa."""
    codigo_solicitud = wscoc.CodigoSolicitud
    solicitud = wscoc.ConsultarSolicitudCompraDivisa(codigo_solicitud)
    assert solicitud


def test_consultar_solicitudes_compra_divisas():
    """Test consultar solicitudes compra divisas."""
    cuit_comprador = None
    estado_solicitud = None
    fecha_emision_desde = '2019-01-01'
    fecha_emision_hasta = '2019-02-30'
    solicitud = wscoc.ConsultarSolicitudesCompraDivisas(cuit_comprador,
                                                        estado_solicitud,
                                                        fecha_emision_desde,
                                                        fecha_emision_hasta,)
    assert solicitud


def test_leer_solicitud_consultada():
    """Test leer solicitud consultada."""
    solicitud = wscoc.LeerSolicitudConsultada()
    assert solicitud


def test_consultar_djai():
    """Test consultar djai."""
    djai = "12345DJAI000001N"
    cuit = 20267565393
    consulta = wscoc.ConsultarDJAI(djai, cuit)
    assert consulta


def test_consultar_djas():
    """Test consultar djas."""
    djas = "12001DJAS000901N"
    cuit = 20267565393
    consulta = wscoc.ConsultarDJAS(djas, cuit)
    assert consulta


def test_consultar_referencia():
    """Test consultar referencia."""
    codigo = "12345DJAI000067C"
    cuit = 20267565393
    consulta = wscoc.ConsultarReferencia(1, codigo)
    assert consulta


def test_consultar_monedas():
    """Test consultar monedas."""
    consulta = wscoc.ConsultarMonedas()
    assert consulta


def test_consultar_destinos_compra():
    """Test consultar destinos compra."""
    consulta = wscoc.ConsultarDestinosCompra()
    assert consulta


def test_consultar_tipos_documento():
    """Test consultar tipos documento."""
    consulta = wscoc.ConsultarTiposDocumento()
    assert consulta


def test_consultar_tipos_estado_solicitud():
    """Test consultar tipos estado solicitud."""
    consulta = wscoc.ConsultarTiposEstadoSolicitud()
    assert consulta


def test_consultar_motivos_excepcion_djai():
    """Test consultar motivos excepcion djai."""
    consulta = wscoc.ConsultarMotivosExcepcionDJAI()
    assert consulta


def test_consultar_destinos_compra_djai():
    """Test consultar destinos compra djai."""
    consulta = wscoc.ConsultarDestinosCompraDJAI()
    assert consulta


def test_consultar_motivos_excepcion_djas():
    """Test consultar motivos excepcion djas."""
    consulta = wscoc.ConsultarMotivosExcepcionDJAS(sep="||")
    assert consulta


def test_consultar_destinos_compra_djas():
    """Test consultar destinos compra djas."""
    consulta = wscoc.ConsultarDestinosCompraDJAS(sep="||")
    assert consulta


def test_consultar_tipos_referencia():
    """Test consultar tipos referencia."""
    consulta = wscoc.ConsultarTipoReferencia()
    assert consulta


def test_consultar_destinos_compra_tipo_referencia():
    """Test consultar destinos compra tipo referencia."""
    consulta = wscoc.ConsultarDestinosCompraTipoReferencia()
    assert consulta


def test_leer_error():
    """Test leer error."""
    lectura = wscoc.LeerError()
    assert lectura


def test_leer_error_formato():
    """Test leer error de formato."""
    formato = wscoc.LeerErrorFormato()
    assert formato


def test_leer_inconsistencia():
    """Test leer inconsistencia."""
    lectura = wscoc.LeerInconsistencia()
    assert lectura
