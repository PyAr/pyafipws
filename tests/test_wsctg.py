# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para Módulo WSCTG
(Código de Trazabilidad de Granos).
"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import os
import pytest


from pyafipws.wsaa import WSAA
from pyafipws import wsctg
from pyafipws.wsctg import WSCTG


WSDL = "https://fwshomo.afip.gov.ar/wsctg/services/CTGService_v4.0?wsdl"
CUIT = os.environ['CUIT']
CERT = 'rei.crt'
PKEY = 'rei.key'
CACHE = ""

wsc = wsctg
# obteniendo el TA para pruebas
wsaa = WSAA()
wsctg = WSCTG()
ta = wsaa.Autenticar("wsctg", CERT, PKEY)
wsctg.Cuit = CUIT
wsctg.SetTicketAcceso(ta)


def test_conectar():
    """Conectar con servidor."""
    conexion = wsctg.Conectar(CACHE, WSDL)
    assert conexion


def test_server_status():
    """Test de estado de servidores."""
    wsctg.Dummy()
    assert wsctg.AppServerStatus == 'OK'
    assert wsctg.DbServerStatus == 'OK'
    assert wsctg.AuthServerStatus == 'OK'


def test_inicializar():
    """Test inicializar variables de BaseWS."""
    wsctg.inicializar()
    assert wsctg.DatosCTG is None
    assert wsctg.UsuarioReal == ''


def test_analizar_errores():
    """Test Analizar si se encuentran errores en clientes."""
    ret = {'numeroComprobante': 286}
    wsctg._WSCTG__analizar_errores(ret)
    # devuelve '' si no encuentra errores
    assert wsctg.ErrMsg == ''


def test_analizar_controles():
    """Test Analizar si se encuentran errores en clientes."""
    ret = {'numeroComprobante': 286}
    wsctg._WSCTG__analizar_controles(ret)
    assert wsctg.Controles == []


def test_anular_ctg():
    """Test anular ctg."""
    carta_porte = 7
    ctg = 2
    ret = wsctg.AnularCTG(carta_porte, ctg)

    assert ret is None


def test_rechazar_ctg():
    """Test rechazar ctg."""
    carta_porte = 11
    ctg = 25
    motivo = 5
    ret = wsctg.RechazarCTG(carta_porte, ctg, motivo)
    assert ret is None


@pytest.mark.skip
def test_solicitar_ctg_inicial():
    """Test solicitar ctg inicial."""
    numero_carta_de_porte = 512345679
    codigo_especie = 23
    cuit_canjeador = 0  # 30660685908,
    cuit_destino = 20111111112
    cuit_destinatario = 20222222223
    codigo_localidad_origen = 3058
    codigo_localidad_destino = 3059
    codigo_cosecha = '1819'
    peso_neto_carga = 1000
    km_a_recorrer = 150

    cant_horas = 1
    patente_vehiculo = 'OPE652'
    cuit_transportista = 20333333334

    ctg = wsctg.SolicitarCTGInicial(numero_carta_de_porte, codigo_especie,
                                    cuit_canjeador, cuit_destino,
                                    cuit_destinatario, codigo_localidad_origen,
                                    codigo_localidad_destino,
                                    codigo_cosecha, peso_neto_carga, km_a_recorrer,

                                    cant_horas,
                                    patente_vehiculo,
                                    cuit_transportista
                                    )
    assert ctg


@pytest.mark.skip
def test_solicitar_ctg_dato_pendiente():
    """Test solicitar ctg dato pendiente."""
    numero_carta_de_porte = 512345679
    cant_horas = 1
    patente_vehiculo = 'OPE652'
    cuit_transportista = 20333333334
    ctg = wsctg.SolicitarCTGDatoPendiente(numero_carta_de_porte, cant_horas, patente_vehiculo,
                                          cuit_transportista)
    assert ctg


@pytest.mark.skip
def test_confirmar_arribo():
    """Test confirmar arribo."""
    numero_carta_de_porte = 512345679
    numero_ctg = 5465464654
    cuit_transportista = 20333333334
    peso_neto_carga = 1000
    consumo_propio = 'S'
    establecimiento = 1
    cuit_chofer = None
    confirmado = wsctg.ConfirmarArribo(numero_carta_de_porte, numero_ctg,
                                       cuit_transportista, peso_neto_carga,
                                       consumo_propio, establecimiento, cuit_chofer)
    assert confirmado


@pytest.mark.skip
def test_confirmar_definitivo():
    """Test confirmar definitivo."""
    numero_carta_de_porte = 512345679
    numero_ctg = 5465464654
    transaccion = wsctg.ConfirmarDefinitivo(numero_carta_de_porte, numero_ctg)
    assert transaccion


@pytest.mark.skip
def test_regresar_a_origen_ctg_rechazado():
    """Test regresar a origen ctg rechazado."""
    numero_carta_de_porte = 512345679
    numero_ctg = 5465464654
    transaccion = wsctg.RegresarAOrigenCTGRechazado(
        numero_carta_de_porte, numero_ctg)
    assert transaccion


@pytest.mark.skip
def test_cambiar_destino_destinatario_ctg_rechazado():
    """Test cambiar destino destinatario ctg rechazado."""
    numero_carta_de_porte = 512345679
    numero_ctg = 5465464654
    transaccion = wsctg.CambiarDestinoDestinatarioCTGRechazado(
        numero_carta_de_porte, numero_ctg)
    assert transaccion


def test_consultar_ctg():
    """Test consultar ctg."""
    ctg = 542
    ok = wsctg.ConsultarDetalleCTG(ctg)
    assert ok


def test_consultar_ctg_rechazados():
    """Test consultar ctg rechazados."""
    consulta = wsctg.ConsultarCTGRechazados()
    assert consulta is False


def test_consultar_ctg_activos_por_patente():
    """Test consultar ctg activos por patente."""
    patente = 'WWW192'
    consulta = wsctg.ConsultarCTGActivosPorPatente(patente)
    assert consulta is False


def test_ctgs_pendientes_resolucion():
    """Test ctgs pendientes resolucion."""
    pendiente = wsctg.CTGsPendientesResolucion()
    assert pendiente


@pytest.mark.skip
def test_consultar_ctg_excel():
    """Test consultar ctg excel."""

    consulta = wsctg.ConsultarCTGExcel()
    assert consulta


def test_consultar_detalle_ctg():
    """Test consultar detalle ctg."""
    ctg = 15448875
    ok = wsctg.ConsultarDetalleCTG(ctg)
    assert ok


def test_consultar_constancia_ctg_pdf():
    """Test consultar constancia ctg pdf."""
    ctg = 1234
    archivo = 'arch'
    consulta = wsctg.ConsultarConstanciaCTGPDF(ctg, archivo)
    assert consulta


def test_consultar_provincias():
    """Test consultar provincias."""
    consulta = wsctg.ConsultarProvincias()
    assert consulta


def test_consultar_localidades_por_provincia():
    """Test consultar localidades por provincia."""
    consulta = wsctg.ConsultarLocalidadesPorProvincia(1)
    assert consulta


def test_consultar_establecimientos():
    """Test consultar establecimientos."""
    consulta = wsctg.ConsultarEstablecimientos()
    assert consulta


def test_consultar_especies():
    """Test consultar especies."""
    consulta = wsctg.ConsultarEspecies()
    assert consulta


def test_consultar_cosechas():
    """Test consultar cosechas."""
    consulta = wsctg.ConsultarCosechas()
    assert consulta


@pytest.mark.skip
def test_escribir_archivo():
    """Test ibir_archivo."""
    cols = 5
    items = {'tipo_reg': 0}
    nombre_archivo = 'arch.txt'
    archivo = wsc.escribir_archivo(cols, items, nombre_archivo)
    assert archivo


@pytest.mark.skip
def test_leer_archivo():
    """Test _archivo."""
    nombre_archivo = 'arch.txt'
    archivo = wsc.leer_archivo(nombre_archivo)
    assert archivo
