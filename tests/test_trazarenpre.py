# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para Módulo TrazaRenPre
(Trazabilidad de Precursores Químicos RENPRE).
"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"


import pytest

from pyafipws.trazarenpre import TrazaRenpre


WSDL = "https://servicios.pami.org.ar/trazamed.WebServiceSDRN?wsdl"
CACHE = ""

wstr = TrazaRenpre()

wstr.Username = 'testwservice'
wstr.Password = 'testwservicepsw'
usuario = 'pruebasws'
password = 'pruebasws'


def test_conectar():
    """Conectar con servidor."""
    conexion = wstr.Conectar(CACHE, WSDL)
    assert conexion


def test_inicializar():
    """Test inicializar variables de BaseWS."""
    wstr.inicializar()
    assert wstr.CodigoTransaccion is None
    assert wstr.Resultado is None


def test_analizar_errores():
    """Test analizar si se encuentran errores."""
    ret = {'errores': [{
        'c_error': 100,
        'd_error': 'El N° de CAI/CAE/CAEA consultado no existe'
        'en las bases del organismo.'
    }]}
    wstr._TrazaRenpre__analizar_errores(ret)
    # devuelve '' si no encuentra errores
    assert wstr.Errores


def test_save_transacciones():
    """Test save transacciones."""
    transaccion = wstr.SaveTransacciones(
        usuario, password,
        gln_origen=8888888888888,
        gln_destino=8888888888888,
        f_operacion="20/05/2019",
        id_evento=44,
        cod_producto=88800000000035,  # acido sulfúrico
        n_cantidad=1,
        n_documento_operacion=1,
        # m_entrega_parcial="",
        n_remito=124,
        n_serie=113
    )
    assert transaccion
    print(wstr.CodigoTransaccion, 'resultado')


def test_send_cancela_transacc():
    """Test send cancela transacc."""
    codigo_transaccion = 65456468424
    transaccion = wstr.SendCancelacTransacc(
        usuario, password, codigo_transaccion)
    assert transaccion


@pytest.mark.skip
def test_send_confirma_transacc():
    """Test sendconfirmatransacc."""
    p_ids_transac = 2121212121
    f_operacion = 2121212121
    transaccion = wstr.SendConfirmaTransacc(
        usuario, password, p_ids_transac, f_operacion)
    assert transaccion


@pytest.mark.skip
def test_send_alerta_transacc():
    """Test send alerta transacc."""
    p_ids_transac_ws = 33542156445
    transaccion = wstr.SendAlertaTransacc(usuario, password, p_ids_transac_ws)
    assert transaccion


def test_get_transacciones_ws():
    """Test get transacciones ws."""
    transaccion = wstr.GetTransaccionesWS(usuario, password,
                                          p_id_transaccion_global=None,
                                          id_agente_origen=None, id_agente_destino=None,
                                          id_agente_informador=None,
                                          gtin=None, id_evento=None, cant_analitica=None,
                                          fecha_desde_op=None, fecha_hasta_op=None,
                                          fecha_desde_t=None, fecha_hasta_t=None,
                                          id_tipo=None,
                                          id_estado=None, nro_pag=1, cant_reg=100,)
    assert transaccion


def test_set_username():
    """Test set username."""
    wstr.SetUsername(usuario)
    assert wstr.Username == 'pruebasws'
    print(wstr.Username)


def test_set_password():
    """Test set password."""
    wstr.SetPassword(password)
    assert wstr.Password == 'pruebasws'


def test_get_codigo_transaccion():
    """Test get codigo transaccion."""
    codigo = wstr.GetCodigoTransaccion()
    assert codigo is None


def test_get_resultado():
    """Test get resultado."""
    resultado = wstr.GetResultado()
    assert resultado is None
