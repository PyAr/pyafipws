# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para Módulo TrazaMed
(Trazabilidad de Medicamentos ANMAT - PAMI - INSSJP).
"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import pytest
import time
import datetime

from pyafipws.trazamed import TrazaMed

skp = pytest.mark.skip

WSDL = "https://servicios.pami.org.ar/trazamed.WebService?wsdl"
CACHE = ""
wstm = TrazaMed()

wstm.Username = 'testwservice'
wstm.Password = 'testwservicepsw'
usuario = 'pruebasws'
password = 'pruebasws'


def test_conectar():
    """Conectar con servidor."""
    conexion = wstm.Conectar(CACHE, WSDL)
    assert conexion


def test_inicializar():
    """Test inicializar variables de BaseWS."""
    wstm.inicializar()
    assert wstm.CantPaginas is None
    assert wstm.Resultado == ''


def test_analizar_errores():
    """Test analizar si se encuentran errores."""
    ret = {'errores': [{
        '_c_error': 100,
        '_d_error': 'El N° de CAI/CAE/CAEA consultado no existe'
        'en las bases del organismo.'
    }]}
    wstm._TrazaMed__analizar_errores(ret)
    # devuelve '' si no encuentra errores
    assert wstm.Errores


def test_send_medicamentos():
    """Test send medicamentos."""
    med = dict(usuario=usuario, password=password,
               f_evento=datetime.datetime.now().strftime("%d/%m/%Y"),
               h_evento=datetime.datetime.now().strftime("%H:%M"),
               gln_origen="9999999999918", gln_destino="glnws",
               n_remito="R000100001234", n_factura="A000100001234",
               vencimiento=(datetime.datetime.now() +
                            datetime.timedelta(30)).strftime("%d/%m/%Y"),
               gtin="GTIN1", lote=datetime.datetime.now().strftime("%Y"),
               numero_serial=int(time.time() * 10),
               id_obra_social=None, id_evento=134,
               cuit_origen="20267565393", cuit_destino="20267565393",
               apellido="Reingart", nombres="Mariano",
               tipo_documento="96", n_documento="26756539", sexo="M",
               direccion="Saraza", numero="1234", piso="", depto="",
               localidad="Hurlingham", provincia="Buenos Aires",
               n_postal="1688", fecha_nacimiento="01/01/2000",
               telefono="5555-5555",
               nro_asociado="9999999999999",)
    transaccion = wstm.SendMedicamentos(**med)
    assert transaccion


def test_send_medicamentos_fraccion():
    """Test send medicamentos fraccion."""
    med_frac = dict(usuario=usuario, password=password,
                    f_evento=datetime.datetime.now().strftime("%d/%m/%Y"),
                    h_evento=datetime.datetime.now().strftime("%H:%M"),
                    gln_origen="9999999999918", gln_destino="glnws",
                    n_remito="1234", n_factura="1234",
                    vencimiento=(datetime.datetime.now() +
                                 datetime.timedelta(30)).strftime("%d/%m/%Y"),
                    gtin="GTIN1", lote=datetime.datetime.now().strftime("%Y"),
                    numero_serial=int(time.time() * 10),
                    id_obra_social=None, id_evento=134,
                    cuit_origen="20267565393", cuit_destino="20267565393",
                    apellido="Reingart", nombres="Mariano",
                    tipo_documento="96", n_documento="26756539", sexo="M",
                    direccion="Saraza", numero="1234", piso="", depto="",
                    localidad="Hurlingham", provincia="Buenos Aires",
                    n_postal="1688", fecha_nacimiento="01/01/2000",
                    telefono="5555-5555",
                    nro_asociado="9999999999999",
                    cantidad=5)
    transaccion = wstm.SendMedicamentosFraccion(**med_frac)
    assert transaccion


def test_send_medicamentos_dh_serie():
    """Test  transaccionsend medica mentos dh serie."""
    med_dh = dict(usuario=usuario, password=password,
                  f_evento=datetime.datetime.now().strftime("%d/%m/%Y"),
                  h_evento=datetime.datetime.now().strftime("%H:%M"),
                  gln_origen="9999999999918", gln_destino="glnws",
                  n_remito="1234", n_factura="1234",
                  vencimiento=(datetime.datetime.now() +
                               datetime.timedelta(30)).strftime("%d/%m/%Y"),
                  gtin="GTIN1", lote=datetime.datetime.now().strftime("%Y"),
                  desde_numero_serial=int(time.time() * 10) - 1,
                  hasta_numero_serial=int(time.time() * 10) + 1,
                  id_obra_social=None, id_evento=134,
                  nro_asociado="1234")
    transaccion = wstm.SendMedicamentosDHSerie(**med_dh)
    assert transaccion


def test_send_alerta_transacc():
    """Test send alerta transacc."""
    p_ids_transac_ws = 2545655221154
    transaccion = wstm.SendAlertaTransacc(usuario, password, p_ids_transac_ws)
    assert transaccion


def test_send_confirma_transacc():
    """Test sendc onfirma transacc."""
    p_ids_transac = 241546
    f_operacion = 21213221
    transaccion = wstm.SendConfirmaTransacc(
        usuario, password, p_ids_transac, f_operacion)
    assert transaccion


def test_send_cancela_c_transacc_parcial():
    """Test send cancela c transacc parcial."""
    codigo_transaccion = 665656565
    transaccion = wstm.SendCancelacTransaccParcial(
        usuario, password, codigo_transaccion)
    assert transaccion


def test_send_cancela_c_transacc():
    """Test send cancela c transacc."""
    codigo_transaccion = 5456465464654
    transaccion = wstm.SendCancelacTransacc(
        usuario, password, codigo_transaccion)
    assert transaccion


def test_get_transacciones_no_confirmadas():
    """Test get transacciones no confirmadas."""
    transaccion = wstm.GetTransaccionesNoConfirmadas(usuario, password)
    assert transaccion


def test_leer_transaccion():
    """Test leer transaccion."""
    transaccion = wstm.LeerTransaccion()
    assert transaccion is False


def test_leer_error():
    """Test lee rerror."""
    transaccion = wstm.LeerError()
    assert transaccion == ''


@skp
def test_get_envios_propios_alertados():
    """Test get envios propios alertados."""
    transaccion = wstm.GetEnviosPropiosAlertados(usuario, password)
    assert transaccion


@skp
def test_get_transacciones_ws():
    """Test get transacciones ws."""
    transaccion = wstm.GetTransaccionesWS(usuario, password)
    assert transaccion


@skp
def test_get_catalogo_electronico_by_gtin():
    """Test get catalogo electronico by gtin."""
    transaccion = wstm.GetCatalogoElectronicoByGTIN(usuario, password)
    assert transaccion


@skp
def test_get_consulta_stock():
    """Test get consulta stock."""
    transaccion = wstm.GetConsultaStock(usuario, password)
    assert transaccion


def test_set_username():
    """Test set username."""
    wstm.SetUsername(usuario)
    assert wstm.Username == 'pruebasws'


def test_set_password():
    """Test set password."""
    wstm.SetPassword(password)
    assert wstm.Password == 'pruebasws'


@skp
def test_get_codigo_transaccion():
    """Test getc odigo transaccion."""
    codigo = wstm.CodigoTransaccion()
    assert codigo


def test_get_resultado():
    """Test get resultado."""
    resultado = wstm.GetResultado()
    assert resultado == ''
