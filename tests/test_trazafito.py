# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para Módulo TrazaFito
(Trazabilidad de Productos Fitosanitarios SENASA ).
"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import pytest
import time
import datetime

from pyafipws.trazafito import TrazaFito


WSDL = "https://servicios.pami.org.ar/trazaenagr.WebService?wsdl"
CACHE = ""

wstf = TrazaFito()

wstf.Username = 'testwservice'
wstf.Password = 'testwservicepsw'
usuario = 'pruebasws'
password = 'pruebasws'


def test_conectar():
    """Conectar con servidor."""
    conexion = wstf.Conectar(CACHE, WSDL)
    assert conexion


def test_inicializar():
    """Test inicializar variables de BaseWS."""
    wstf.inicializar()
    assert wstf.CantPaginas is None
    assert wstf.Resultado == ''


def test_analizar_errores():
    """Test analizar si se encuentran errores."""
    ret = {'errores': [{
        'c_error': 100,
        'd_error': 'El N° de CAI/CAE/CAEA consultado no existe'
        'en las bases del organismo.'
    }]}
    wstf._TrazaFito__analizar_errores(ret)
    # devuelve '' si no encuentra errores
    assert wstf.Errores


def test_save_transaccion():
    """Test save transaccion."""

    transaccion_dto = dict(
        gln_origen="9876543210982", gln_destino="3692581473693",
        f_operacion=datetime.datetime.now().strftime("%d/%m/%Y"),
        f_elaboracion=datetime.datetime.now().strftime("%d/%m/%Y"),
        f_vto=(datetime.datetime.now() +
               datetime.timedelta(30)).strftime("%d/%m/%Y"),
        id_evento=11,
        cod_producto="88900000000001",
        n_cantidad=1,
        n_serie=int(time.time() * 10),
        n_lote=datetime.datetime.now().strftime("%Y"),
        n_cai="123456789012345",
        n_cae="",
        id_motivo_destruccion=0,
        n_manifiesto="",
        en_transporte="N",
        n_remito="1234",
        motivo_devolucion="",
        observaciones="prueba",
        n_vale_compra="",
        apellidoNombres="Juan Peres",
        direccion="Saraza", numero="1234",
        localidad="Hurlingham", provincia="Buenos Aires",
        n_postal="1688",
        cuit="20267565393",
        codigo_transaccion=None,
    )
    transaccion = wstf.SaveTransaccion(usuario, password, transaccion_dto)

    assert transaccion


def test_send_alerta_transacc():
    """Test enviar alerta transacciones."""
    p_ids_transac_ws = 656565656565
    transaccion = wstf.SendAlertaTransacc(usuario, password, p_ids_transac_ws)
    assert transaccion


def test_send_confirma_transacc():
    """Test send confirma transaccion."""
    p_ids_transac = 545646545
    f_operacion = 6546565656
    transaccion = wstf.SendConfirmaTransacc(
        usuario, password, p_ids_transac, f_operacion, n_cantidad=None)

    assert transaccion


def test_send_cancela_transac():
    """Test send cancela transacion."""
    codigo_transaccion = 454685151564
    transaccion = wstf.SendCancelaTransac(
        usuario, password, codigo_transaccion)
    assert transaccion


def test_get_transacciones():
    """Test get transacciones."""
    transaccion = wstf.GetTransacciones(usuario, password,
                                        id_transaccion=None, id_evento=None, gln_origen=None,
                                        fecha_desde_t=None, fecha_hasta_t=None,
                                        fecha_desde_v=None, fecha_hasta_v=None,
                                        gln_informador=None, id_tipo_transaccion=None,
                                        gtin_elemento=None, n_lote=None, n_serie=None,
                                        n_remito_factura=None,
                                        )
    assert transaccion


def test_leer_transaccion():
    """Test leer transaccion."""
    lectura = wstf.LeerTransaccion()
    assert lectura is False


def test_leer_error():
    """Test leer error."""
    error = wstf.LeerError()
    assert error


def test_set_username():
    """Test set username."""
    wstf.SetUsername(usuario)
    assert wstf.Username == 'pruebasws'


def test_set_password():
    """Test set password."""
    wstf.SetPassword(password)
    assert wstf.Password == 'pruebasws'


@pytest.mark.skip
def test_get_codigo_transaccion():
    """Test getc odigo transaccion."""
    codigo = wstf.CodigoTransaccion()
    assert codigo


def test_get_resultado():
    """Test get resultado."""
    resultado = wstf.GetResultado()
    assert resultado is False
