# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Test para Módulo WSLPG
(Liquidación Primaria Electrónica de Granos.)
"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import os
import pytest

from pyafipws.wsaa import WSAA
from pyafipws.wslpg import WSLPG, escribir_archivo, leer_archivo


skip = pytest.mark.skip

WSDL = "https://fwshomo.afip.gov.ar/wslpg/LpgService?wsdl"
CUIT = os.environ['CUIT']
CERT = 'rei.crt'
PKEY = 'rei.key'
CACHE = ""

# obteniendo el TA para pruebas
wsaa = WSAA()
wslpg = WSLPG()
ta = wsaa.Autenticar("wslpg", CERT, PKEY)
wslpg.Cuit = CUIT
wslpg.SetTicketAcceso(ta)


def test_conectar():
    """Conectar con servidor."""
    conexion = wslpg.Conectar(CACHE, WSDL)
    assert conexion


def test_server_status():
    """Test de estado de servidores."""
    wslpg.Dummy()
    assert wslpg.AppServerStatus == 'OK'
    assert wslpg.DbServerStatus == 'OK'
    assert wslpg.AuthServerStatus == 'OK'


def test_inicializar():
    """Test inicializar variables de BaseWS."""
    wslpg.inicializar()
    assert wslpg.datos == {}
    assert wslpg.FechaCertificacion == ''


def test_analizar_errores():
    """Test Analizar si se encuentran errores."""
    ret = {'errores': [{'error': {
        'codigo': 1106,
        'descripcion': 'No existen puntos de venta habilitados para utilizar en el presente ws.'
    }}]}
    wslpg._WSLPG__analizar_errores(ret)
    # devuelve '' si no encuentra errores
    assert wslpg.ErrMsg


def test_crear_liquidacion():
    """Test crear liquidacion."""
    pto_emision = 99
    wslpg.ConsultarUltNroOrden(pto_emision)
    liquidacion = wslpg.CrearLiquidacion(pto_emision=pto_emision,
                                         nro_orden=wslpg.NroOrden + 1,
                                         cuit_comprador=wslpg.Cuit,
                                         nro_act_comprador=29, nro_ing_bruto_comprador=wslpg.Cuit,
                                         cod_tipo_operacion=1,
                                         es_liquidacion_propia='N', es_canje='N',
                                         cod_puerto=14, des_puerto_localidad="DETALLE PUERTO",
                                         cod_grano=31,
                                         cuit_vendedor=23000000019, nro_ing_bruto_vendedor=23000000019,
                                         actua_corredor="N", liquida_corredor="N",
                                         cuit_corredor=0,
                                         comision_corredor=0, nro_ing_bruto_corredor=0,
                                         fecha_precio_operacion="2019-02-07",
                                         precio_ref_tn=2000,
                                         cod_grado_ref="G1",
                                         cod_grado_ent="FG",
                                         factor_ent=98, val_grado_ent=1.02,
                                         precio_flete_tn=10,
                                         cont_proteico=20,
                                         alic_iva_operacion=10.5,
                                         campania_ppal=1819,
                                         cod_localidad_procedencia=5544,
                                         cod_prov_procedencia=12,
                                         datos_adicionales="DATOS ADICIONALES",
                                         peso_neto_sin_certificado=10000,
                                         cod_prov_procedencia_sin_certificado=1,
                                         cod_localidad_procedencia_sin_certificado=15124,)
    assert liquidacion


def test_agregar_certificado():
    """Test agregar certificado."""

    cert = wslpg.AgregarCertificado(tipo_certificado_deposito=5,
                                    nro_certificado_deposito=555501200802,
                                    peso_neto=10000,
                                    cod_localidad_procedencia=5,
                                    cod_prov_procedencia=1,
                                    campania=1819,
                                    fecha_cierre='2019-07-12')
    assert cert


def test_crear_liq_secundaria_base():
    """Test crear liquidacion secundaria base."""
    ok = wslpg.CrearLiqSecundariaBase(pto_emision=1, nro_orden=None,
                                      nro_contrato=None,
                                      cuit_comprador=None, nro_ing_bruto_comprador=None,
                                      cod_puerto=None, des_puerto_localidad=None,
                                      cod_grano=None, cantidad_tn=None,
                                      cuit_vendedor=None, nro_act_vendedor=None,  # nuevo!!
                                      nro_ing_bruto_vendedor=None,
                                      actua_corredor=None, liquida_corredor=None, cuit_corredor=None,
                                      nro_ing_bruto_corredor=None,
                                      fecha_precio_operacion=None, precio_ref_tn=None,
                                      precio_operacion=None, alic_iva_operacion=None, campania_ppal=None,
                                      cod_localidad_procedencia=None, cod_prov_procedencia=None,
                                      datos_adicionales=None,
                                      )
    assert ok


def test_agregar_retencion():
    """Test agregar retencion."""
    ret = dict(
        codigo_concepto="RG",
        detalle_aclaratorio="DETALLE DE GANANCIAS",
        base_calculo=100,
        alicuota=15,)
    agregado = wslpg.AgregarRetencion(**ret)
    assert agregado


def test_agregar_deduccion():
    """Test agregar deduccion."""
    ded = dict(codigo_concepto="AL",
               detalle_aclaratorio="Deduc Alm",
               dias_almacenaje="1",
               precio_pkg_diario=0.01,
               comision_gastos_adm=1.0,
               base_calculo=500.0,
               alicuota=10.5, )
    agregado = wslpg.AgregarDeduccion(**ded)
    assert agregado


def test_agregar_percepcion():
    """Test agregar percepcion."""
    per = dict(codigo_concepto=None, detalle_aclaratoria=None,
               base_calculo=None, alicuota=None, importe_final=None)
    ok = wslpg.AgregarPercepcion(**per)

    assert ok


def test_agregar_opcional():
    """Test agregar opcional."""
    codigo = 1
    descripcion = 'previsto para info adic.'
    agregado = wslpg.AgregarOpcional(codigo, descripcion)
    assert agregado


def test_agregar_factura_papel():
    """Test agregar factura papel."""
    nro_cai = '1234'
    nro_factura_papel = 2
    fecha_factura = '2019-05-15'
    tipo_comprobante = 1
    agregado = wslpg.AgregarFacturaPapel(nro_cai, nro_factura_papel,
                                         fecha_factura, tipo_comprobante,
                                         )
    assert agregado


@skip
def test_autorizar_liquidacion():
    """Test autorizar liquidacion."""
    ret = wslpg.AutorizarLiquidacion()
    assert ret


def test_autorizar_liquidacion_secundaria():
    """Test autorizarliquidacionsecundaria."""
    liq_seq = wslpg.AutorizarLiquidacionSecundaria()
    assert liq_seq


@skip
def test_autorizar_anticipo():
    """Test autorizaranticipo."""
    anticipo = wslpg.AutorizarAnticipo()
    assert anticipo


def test_cancelar_anticipo():
    """Test cancelaranticipo."""
    pto_emision = 1
    nro_orden = wslpg.NroOrden
    coe = 330100000330
    anticipo = wslpg.CancelarAnticipo(pto_emision, nro_orden, coe)
    assert anticipo


@skip
def test_analizar_liquidacion():
    """Test analizarliquidacion."""
    aut = wslpg.Coe
    liquidacion = wslpg.AnalizarLiquidacion(aut, liq=None, ajuste=False)
    assert liquidacion


def test_crear_ajuste_base():
    """Test crearajustebase."""
    ajuste = wslpg.CrearAjusteBase(pto_emision=1, nro_orden=None,       # unificado, contrato, papel
                                   coe_ajustado=None,                   # unificado
                                   nro_contrato=None,                   # contrato
                                   tipo_formulario=None,                # papel
                                   nro_formulario=None,                 # papel
                                   actividad=None,                      # contrato / papel
                                   cod_grano=None,                      # contrato / papel
                                   cuit_vendedor=None,                  # contrato / papel
                                   cuit_comprador=None,                 # contrato / papel
                                   cuit_corredor=None,                  # contrato / papel
                                   nro_ing_bruto_vendedor=None,         # papel
                                   nro_ing_bruto_comprador=None,        # papel
                                   nro_ing_bruto_corredor=None,         # papel
                                   tipo_operacion=None,                 # papel
                                   precio_ref_tn=None,                  # contrato
                                   cod_grado_ent=None,                  # contrato
                                   val_grado_ent=None,                  # contrato
                                   precio_flete_tn=None,                # contrato
                                   cod_puerto=None,                     # contrato
                                   des_puerto_localidad=None,           # contrato
                                   cod_provincia=None,                  # unificado, contrato, papel
                                   cod_localidad=None,                  # unificado, contrato, papel
                                   comision_corredor=None,              # papel
                                   )
    assert ajuste


def test_crear_ajuste_credito():
    """Test crearajustecredito."""
    ajuste_cred = wslpg.CrearAjusteCredito(datos_adicionales=None,              # unificado, contrato, papel
                                           concepto_importe_iva_0=None,         # unificado, contrato, papel
                                           importe_ajustar_iva_0=None,          # unificado, contrato, papel
                                           concepto_importe_iva_105=None,       # unificado, contrato, papel
                                           importe_ajustar_iva_105=None,        # unificado, contrato, papel
                                           concepto_importe_iva_21=None,        # unificado, contrato, papel
                                           importe_ajustar_iva_21=None,         # unificado, contrato, papel
                                           diferencia_peso_neto=None,           # unificado
                                           diferencia_precio_operacion=None,    # unificado
                                           cod_grado=None,                      # unificado
                                           val_grado=None,                      # unificado
                                           factor=None,                         # unificado
                                           diferencia_precio_flete_tn=None,     # unificado

                                           )
    assert ajuste_cred


def test_crear_ajuste_debito():
    """Test crearajustedebito."""
    ok = wslpg.AnalizarAjusteDebito()
    assert ok


def test_agregar_fusion():
    """Test agregarfusion."""
    nro_ing_brutos = 12123244544
    nro_actividad = 25
    agregado = wslpg.AgregarFusion(
        nro_ing_brutos, nro_actividad, )
    assert agregado


@skip
def test_ajustar_liquidacion_unificado():
    """Test ajustarliquidacionunificado."""
    ok = wslpg.AjustarLiquidacionUnificado()
    assert ok


@skip
def test_ajustar_liquidacion_unificado_papel():
    """Test ajustar liquidacion unificado papel."""
    ok = wslpg.AjustarLiquidacionUnificadoPapel()
    assert ok


@skip
def test_ajustar_liquidacion_contrato():
    """Test ajustar liquidacion contrato."""
    ok = wslpg.AjustarLiquidacionContrato()

    assert ok


def test_ajustar_liquidacion_secundaria():
    """Test ajustar liquidacion secundaria."""
    ok = wslpg.AjustarLiquidacionSecundaria()
    assert ok


@skip
def test_analizar_ajuste():
    """Test analizar ajuste."""
    aut = wslpg.Coe
    ok = wslpg.AnalizarAjuste(aut, base=True)
    assert ok


def test_analizar_ajuste_debito():
    """Test analizar ajuste debito."""
    ok = wslpg.AnalizarAjusteDebito()
    assert ok


def test_analizar_ajuste_credito():
    """Test analizar ajuste credito."""
    ok = wslpg.AnalizarAjusteCredito()
    assert ok


def test_crear_certificacion_cabecera():
    """Test crear certificacion cabecera."""
    ok = wslpg.CrearCertificacionCabecera(pto_emision=1, nro_orden=None,
                                          tipo_certificado=None, nro_planta=None,
                                          nro_ing_bruto_depositario=None, titular_grano=None,
                                          cuit_depositante=None, nro_ing_bruto_depositante=None,
                                          cuit_corredor=None, cod_grano=None, campania=None,
                                          datos_adicionales=None,
                                          )
    assert ok


def test_agregar_certificacion_primaria():
    """Test agregarcertificacionprimaria."""
    ok = wslpg.AgregarCertificacionPrimaria(nro_act_depositario=None,
                                            descripcion_tipo_grano=None,
                                            monto_almacenaje=None, monto_acarreo=None,
                                            monto_gastos_generales=None, monto_zarandeo=None,
                                            porcentaje_secado_de=None, porcentaje_secado_a=None,
                                            monto_secado=None, monto_por_cada_punto_exceso=None,
                                            monto_otros=None,
                                            porcentaje_merma_volatil=None, peso_neto_merma_volatil=None,
                                            porcentaje_merma_secado=None, peso_neto_merma_secado=None,
                                            porcentaje_merma_zarandeo=None, peso_neto_merma_zarandeo=None,
                                            peso_neto_certificado=None, servicios_secado=None,
                                            servicios_zarandeo=None, servicios_otros=None,
                                            servicios_forma_de_pago=None)
    assert ok


def test_agregar_certificacion_retiro_transferencia():
    """Test agregar certificacion retiro transferencia."""
    ok = wslpg.AgregarCertificacionRetiroTransferencia(nro_act_depositario=None,
                                                       cuit_receptor=None,
                                                       fecha=None,
                                                       nro_carta_porte_a_utilizar=None,
                                                       cee_carta_porte_a_utilizar=None,
                                                       )
    assert ok


def test_agregar_certificacion_preexistente():
    """Test agregar certificacion preexistente."""
    ok = wslpg.AgregarCertificacionPreexistente(tipo_certificado_deposito_preexistente=None,
                                                nro_certificado_deposito_preexistente=None,
                                                cac_certificado_deposito_preexistente=None,
                                                fecha_emision_certificado_deposito_preexistente=None,
                                                peso_neto=None, nro_planta=None,
                                                )
    assert ok


def test_agregar_calidad():
    """Test agregar calidad."""
    ok = wslpg.AgregarCalidad(analisis_muestra=None, nro_boletin=None,
                              cod_grado=None, valor_grado=None,
                              valor_contenido_proteico=None, valor_factor=None,
                              )
    assert ok


def test_agregar_detalle_muestra_analisis():
    """Test agregar detalle muestra analisis."""
    ok = wslpg.AgregarDetalleMuestraAnalisis(descripcion_rubro=None,
                                             tipo_rubro=None, porcentaje=None,
                                             valor=None,
                                             )
    assert ok


def test_buscar_ctg():
    """Test buscar ctg."""
    ok = wslpg.BuscarCTG(tipo_certificado="P", cuit_depositante=None,
                         nro_planta=None, cod_grano=2, campania=1314,
                         nro_ctg=None, tipo_ctg=None, nro_carta_porte=None,
                         fecha_confirmacion_ctg_des=None,
                         fecha_confirmacion_ctg_has=None,
                         )
    assert ok


def test_agregar_ctg():
    """Test agregar ctg."""
    ok = wslpg.AgregarCTG(nro_ctg=None, nro_carta_porte=None,
                          porcentaje_secado_humedad=None, importe_secado=None,
                          peso_neto_merma_secado=None, tarifa_secado=None,
                          importe_zarandeo=None, peso_neto_merma_zarandeo=None,
                          tarifa_zarandeo=None,
                          peso_neto_confirmado_definitivo=None,
                          )
    assert ok


def test_buscar_cert_con_saldo_disponible():
    """Test buscar cert con saldo disponible."""
    ok = wslpg.BuscarCertConSaldoDisponible(cuit_depositante=None,
                                            cod_grano=2, campania=1314, coe=None,
                                            fecha_emision_des=None,
                                            fecha_emision_has=None,
                                            )
    assert ok


def test_autorizar_certificacion():
    """Test autorizar certificacion."""
    ok = wslpg.AutorizarCertificacion()
    assert ok


@pytest.mark.skip
def test_analizar_autorizar_certificado_resp():
    """Test analizar autorizar certificado resp."""
    "Utilizado para analizar los resultados"
    ok = wslpg.AnalizarAutorizarCertificadoResp(ret)
    assert ok


@skip
def test_informar_calidad_certificacion():
    """Test informar calidad certificacion."""
    coe = wslpg.Coe
    ok = wslpg.InformarCalidadCertificacion(coe)
    assert ok


@skip
def test_anular_certificacion():
    """Test anular certificacion."""
    coe = wslpg.Coe
    ok = wslpg.AnularCertificacion(coe)
    assert ok


def test_asociar_liquidacion_a_contrato():
    """Test asociar liquidacion a contrato."""
    coe = 330100000357
    nro_contrato = 27
    ok = wslpg.AsociarLiquidacionAContrato(coe=coe,
                                           nro_contrato=nro_contrato,
                                           cuit_comprador="20400000000",
                                           cuit_vendedor="23000000019",
                                           cuit_corredor="20267565393",
                                           cod_grano=31)
    assert ok


def test_consultar_liquidaciones_por_contrato():
    """Test consultar liquidaciones por contrato."""
    ok = wslpg.ConsultarLiquidacionesPorContrato(nro_contrato=None,
                                                 cuit_comprador=None,
                                                 cuit_vendedor=None,
                                                 cuit_corredor=None,
                                                 cod_grano=None,
                                                 )
    assert ok


def test_consultar_liquidacion():
    """Test consultar liquidacion."""
    ok = wslpg.ConsultarLiquidacion(pto_emision=None, nro_orden=None, coe=None,
                                    pdf=None)
    assert ok


@skip
def test_consultar_liquidacion_secundaria():
    """Test consultar liquidacion secundaria."""
    ok = wslpg.ConsultarLiquidacionSecundaria(pto_emision=None, nro_orden=None,
                                              coe=None, pdf=None)
    assert ok


def test_consultar_liquidaciones_secundarias_por_contrato():
    """Test consultar liquidaciones secundarias por contrato."""
    ok = wslpg.ConsultarLiquidacionesSecundariasPorContrato(nro_contrato=None,
                                                            cuit_comprador=None,
                                                            cuit_vendedor=None,
                                                            cuit_corredor=None,
                                                            cod_grano=None,
                                                            )

    assert ok


def test_asociar_liquidacion_secundaria_a_contrato():
    """Test asociar liquidacion secundaria a contrato."""
    ok = wslpg.AsociarLiquidacionSecundariaAContrato(coe=None, nro_contrato=None,
                                                     cuit_comprador=None,
                                                     cuit_vendedor=None,
                                                     cuit_corredor=None,
                                                     cod_grano=None,
                                                     )
    assert ok


def test_consultar_certificacion():
    """Test consultar certificacion."""
    ok = wslpg.ConsultarCertificacion(pto_emision=None, nro_orden=None,
                                      coe=None, pdf=None)
    assert ok


def test_consultar_ajuste():
    """Test consultar ajuste."""
    pto_emision = 55
    nro_orden = 78
    # consulto el ajuste:
    ok = wslpg.ConsultarAjuste(pto_emision, nro_orden)
    assert ok


def test_consultar_ult_nro_orden():
    """Test consultar ult nro orden."""
    pto_emision = 99
    ok = wslpg.ConsultarUltNroOrden(pto_emision)
    assert ok


def test_consultar_liquidacion_secundaria_ult_nro_orden():
    """Test consultar liquidacion secundaria ult nro orden."""
    ok = wslpg.ConsultarLiquidacionSecundariaUltNroOrden(pto_emision=1)

    assert ok


def test_consultar_certificacion_ult_nro_orden():
    """Test consultar certificacion ult nro orden."""
    ok = wslpg.ConsultarCertificacionUltNroOrden(pto_emision=1)
    assert ok


@skip
def test_leer_datos_liquidacion():
    """Test leer  datosliquidacion."""
    ok = wslpg.LeerDatosLiquidacion()
    assert ok


@skip
def test_anular_liquidacion():
    """Test anular liquidacion."""
    coe = 330100000357
    ok = wslpg.AnularLiquidacion(coe)
    assert ok


@skip
def test_anular_liquidacion_secundaria():
    """Test anular liquidacion secundaria."""
    coe = 330100000358
    ok = wslpg.AnularLiquidacionSecundaria(coe)
    assert ok


def test_consultar_campanias():
    """Test consultar campanias."""
    ok = wslpg.ConsultarCampanias()
    assert ok


def test_consultar_tipo_grano():
    """Test consultar tipo grano."""
    ok = wslpg.ConsultarTipoGrano()
    assert ok


def test_consultar_codigo_grado_referencia():
    """Test consultar codigo grado referencia."""
    ok = wslpg.ConsultarCodigoGradoReferencia()
    assert ok


def test_consultar_grado_entregado_x_tipo_grano():
    """Test consultar grado entregado x tipo grano."""
    cod_grano = '05'
    ok = wslpg.ConsultarGradoEntregadoXTipoGrano(cod_grano)
    assert ok


def test_consultar_tipo_certificado_deposito():
    """Test consultar tipo certificado deposito."""
    ok = wslpg.ConsultarTipoCertificadoDeposito()
    assert ok


def test_consultar_tipo_deduccion():
    """Test consultar tipo deduccion."""
    ok = wslpg.ConsultarTipoDeduccion()
    assert ok


def test_consultar_tipo_retencion():
    """Test consultar tipo retencion."""
    ok = wslpg.ConsultarTipoRetencion()
    assert ok


def test_consultar_puerto():
    """Test consultar puerto."""
    ok = wslpg.ConsultarPuerto()
    assert ok


def test_consultar_tipo_actividad():
    """Test consultar tipo actividad."""
    ok = wslpg.ConsultarTipoActividad()
    assert ok


def test_consultar_tipo_actividad_representado():
    """Test consultar tipo actividad representado."""
    ok = wslpg.ConsultarTipoActividadRepresentado()
    assert ok


def test_consultar_provincias():
    """Test consultar provincias."""
    ok = wslpg.ConsultarProvincias()
    assert ok


def test_consultar_localidades_por_provincia():
    """Test consultar localidades por provincia."""
    cod_provincia = 18
    ok = wslpg.ConsultarLocalidadesPorProvincia(cod_provincia)

    assert ok


@skip
def test_buscar_localidades():
    """Test buscar localidades."""
    cod_provincia = 15
    cod_localidad = 356
    ok = wslpg.BuscarLocalidades(cod_provincia, cod_localidad)
    assert ok


def test_consultar_tipos_operacion():
    """Test consultar tipos operacion."""
    ok = wslpg.ConsultarTiposOperacion()
    assert ok


@skip
def test_cargar_formato_pdf():
    """Test cargar formato pdf."""
    ok = wslpg.CargarFormatoPDF()
    assert ok


@skip
def test_agregar_campo_pdf():
    """Test agregar campo pdf."""
    nombre = 'Lomas verdes'
    tipo = 'Rincon'
    x1 = '5'
    y1 = '10'
    x2 = '15'
    y2 = '20'
    ok = wslpg.AgregarCampoPDF(nombre, tipo, x1, y1, x2, y2,
                               font="Arial", size=12,
                               bold=False, italic=False, underline=False,
                               foreground=0x000000, background=0xFFFFFF,
                               align="L", text="", priority=0, )

    assert ok


def test_crear_plantilla_pdf():
    """Test crear plantilla pdf."""
    ok = wslpg.CrearPlantillaPDF()
    assert ok


@skip
def test_agregar_dato_pdf():
    """Test agregar dato pdf."""
    campo = 'Prueba'
    valor = '110'
    ok = wslpg.AgregarDatoPdf(campo, valor)
    assert ok


@skip
def test_procesar_plantilla_pdf():
    """Test procesar plantilla pdf."""
    ok = wslpg.ProcesarPlantillaPDF()
    assert ok


def test_pdf_formatear():
    """Test def formatear."""
    pass


def test_buscar_localidad_provincia():
    """Test def buscar_localidad_provincia."""
    pass


@skip
def test_generar_pdf():
    """Test generar pdf."""
    archivo = 'Campo'
    ok = wslpg.GenerarPDF(archivo)
    assert ok


@skip
def test_mostrar_pdf():
    """Test mostrar pdf."""
    archivo = 'Campo'
    ok = wslpg.MostrarPDF(archivo)
    assert ok


def test_escribir_archivo():
    """Test escribir archivo."""
    # assert
    pass


def test_archivo():
    """Test leer archivo."""
    # assert
    pass
