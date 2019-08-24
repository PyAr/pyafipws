# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para Módulo TrazaProdMed
(Trazabilidad de Productos Médicos ANMAT).
"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import time
import datetime
import pytest

from pyafipws.trazaprodmed import TrazaProdMed

WSDL = "https://servicios.pami.org.ar/trazaenprodmed.WebService?wsdl"
CACHE = ""
wstp = TrazaProdMed()
wstp.Username = 'testwservice'
wstp.Password = 'testwservicepsw'
usuario = 'pruebasws'
password = 'pruebasws'

skp = pytest.mark.skip


def test_conectar():
    """Conectar con servidor."""
    conexion = wstp.Conectar(CACHE, WSDL)
    assert conexion


def test_inicializar():
    """Test inicializar variables de BaseWS."""
    wstp.inicializar()
    assert wstp.CantPaginas is None
    assert wstp.Resultado == ''


def test_analizar_errores():
    """Test analizar si se encuentran errores."""
    ret = {'errores': [{
        'c_error': 100,
        'd_error': 'El N° de CAI/CAE/CAEA consultado no existe'
        'en las bases del organismo.'
    }]}
    wstp._TrazaProdMed__analizar_errores(ret)
    # devuelve '' si no encuentra errores
    assert wstp.Errores


def test_crear_transaccion():
    """Test crear transaccion."""
    transaccion = wstp.CrearTransaccion(
        f_evento=datetime.datetime.now().strftime("%d/%m/%Y"),
        h_evento=datetime.datetime.now().strftime("%H:%M"),
        gln_origen="7791234567801", gln_destino="7791234567801",
        n_remito="R0001-12341234", n_factura="A0001-12341234",
        vencimiento=(datetime.datetime.now() +
                     datetime.timedelta(30)).strftime("%d/%m/%Y"),
        gtin="07791234567810", lote=datetime.datetime.now().strftime("%Y"),  # R4556567
        numero_serial=int(time.time() * 10),  # A23434
        id_evento=1,
        cuit_medico="30711622507", id_obra_social=465667,
        apellido="Reingart", nombres="Mariano",
        tipo_documento="96", n_documento="28510785", sexo="M",
        calle="San Martin", numero="5656", piso="", depto="1",
        localidad="Berazategui", provincia="Buenos Aires",
        n_postal="1700", fecha_nacimiento="20/12/1972",
        telefono="5555-5555",
        nro_afiliado="9999999999999",
        cod_diagnostico="B30",
        cod_hiv="NOAP31121970",
        id_motivo_devolucion=1,
        otro_motivo_devolucion="producto fallado",
    )
    assert transaccion


@skp
def test_informar_producto():
    """Test informar producto."""
    transaccion = wstp.InformarProducto(usuario, password)

    assert transaccion


@skp
def test_send_cancela_c_transacc():
    """Test send cancela c transacc."""
    codigo_transaccion = 11111111111
    transaccion = wstp.SendCancelacTransacc(
        usuario, password, codigo_transaccion)
    assert transaccion


@skp
def test_send_cancela_c_transacc_parcial():
    """Test send cancela c transacc parcial."""
    codigo_transaccion = 11111111111
    gtin = "07791234567810"
    numero_serial = int(time.time() * 10)
    transaccion = wstp.SendCancelacTransaccParcial(usuario, password, codigo_transaccion,
                                                   gtin, numero_serial)

    assert transaccion


def test_leer_transaccion():
    """Test leer transaccion."""
    transaccion = wstp.LeerTransaccion()
    assert transaccion


@skp
def test_leer_error():
    """Test leer error."""
    transaccion = wstp.LeerError()
    assert transaccion


@skp
def test_get_transacciones_ws():
    """Test get transacciones wstp."""
    transaccion = wstp.GetTransaccionesWS(usuario, password,
                                          id_transaccion=None,
                                          gln_agente_origen=None, gln_agente_destino=None,
                                          gtin=None, lote=None, serie=None, id_evento=None,
                                          fecha_desde_op=None, fecha_hasta_op=None,
                                          fecha_desde_t=None, fecha_hasta_t=None,
                                          fecha_desde_v=None, fecha_hasta_v=None,
                                          n_remito=None, n_factura=None,
                                          id_provincia=None, id_estado=None, nro_pag=1, offset=100,)
    assert transaccion


@skp
def test_get_catalogo_electronico_by_gtin():
    """Test get catalogo electronico by gtin."""
    catalogo = wstp.GetCatalogoElectronicoByGTIN(usuario, password,
                                                 gtin=None, gln=None, marca=None, modelo=None,
                                                 cuit=None, id_nombre_generico=None, nro_pag=1, offset=100,)
    assert catalogo


def test_set_username():
    """Test set username."""
    wstp.SetUsername(usuario)
    assert wstp.Username == 'pruebasws'
    print(wstp.Username)


def test_set_password():
    """Test set password."""
    wstp.SetPassword(password)
    assert wstp.Password == 'pruebasws'


@skp
def test_get_codigo_transaccion():
    """Test getc odigo transaccion."""
    codigo = wstp.CodigoTransaccion()
    assert codigo


def test_get_resultado():
    """Test get resultado."""
    resultado = wstp.GetResultado()
    assert resultado == ''
