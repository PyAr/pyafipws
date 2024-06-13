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

"""Test para formato_sql"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"

import pytest
from pyafipws.formatos.formato_sql import esquema_sql
from pyafipws.formatos.formato_txt import ENCABEZADO, DETALLE, TRIBUTO, IVA, CMP_ASOC, PERMISO

@pytest.mark.dontusefix
class TestFormatoSQL:
    def test_esquema_sql_encabezado(self, auth):
        # Prueba para generar el esquema SQL de la tabla "encabezado"
        tipos_registro = [("encabezado", ENCABEZADO)]
        conf = {}
        expected_output = [
            "CREATE TABLE encabezado (\n"
            "    tipo_reg INTEGER ,\n"
            "    webservice VARCHAR (6),\n"
            "    fecha_cbte VARCHAR (8),\n"
            "    tipo_cbte INTEGER ,\n"
            "    punto_vta INTEGER ,\n"
            "    cbte_nro INTEGER ,\n"
            "    tipo_expo INTEGER ,\n"
            "    permiso_existente VARCHAR (1),\n"
            "    pais_dst_cmp INTEGER ,\n"
            "    nombre_cliente VARCHAR (200),\n"
            "    tipo_doc INTEGER ,\n"
            "    nro_doc INTEGER ,\n"
            "    domicilio_cliente VARCHAR (300),\n"
            "    id_impositivo VARCHAR (50),\n"
            "    imp_total NUMERIC (15, 3),\n"
            "    imp_tot_conc NUMERIC (15, 3),\n"
            "    imp_neto NUMERIC (15, 3),\n"
            "    impto_liq NUMERIC (15, 3),\n"
            "    impto_liq_nri NUMERIC (15, 3),\n"
            "    imp_op_ex NUMERIC (15, 3),\n"
            "    impto_perc NUMERIC (15, 2),\n"
            "    imp_iibb NUMERIC (15, 3),\n"
            "    impto_perc_mun NUMERIC (15, 3),\n"
            "    imp_internos NUMERIC (15, 3),\n"
            "    imp_trib NUMERIC (15, 3),\n"
            "    moneda_id VARCHAR (3),\n"
            "    moneda_ctz NUMERIC (10, 6),\n"
            "    obs_comerciales VARCHAR (1000),\n"
            "    obs_generales VARCHAR (1000),\n"
            "    forma_pago VARCHAR (50),\n"
            "    incoterms VARCHAR (3),\n"
            "    incoterms_ds VARCHAR (20),\n"
            "    idioma_cbte VARCHAR (1),\n"
            "    zona VARCHAR (5),\n"
            "    fecha_venc_pago VARCHAR (8),\n"
            "    presta_serv INTEGER ,\n"
            "    fecha_serv_desde VARCHAR (8),\n"
            "    fecha_serv_hasta VARCHAR (8),\n"
            "    cae VARCHAR (14),\n"
            "    fecha_vto VARCHAR (8),\n"
            "    resultado VARCHAR (1),\n"
            "    reproceso VARCHAR (1),\n"
            "    motivos_obs VARCHAR (1000),\n"
            "    id INTEGER  PRIMARY KEY,\n"
            "    telefono_cliente VARCHAR (50),\n"
            "    localidad_cliente VARCHAR (50),\n"
            "    provincia_cliente VARCHAR (50),\n"
            "    formato_id INTEGER ,\n"
            "    email VARCHAR (100),\n"
            "    pdf VARCHAR (100),\n"
            "    err_code VARCHAR (6),\n"
            "    err_msg VARCHAR (1000),\n"
            "    Dato_adicional1 VARCHAR (30),\n"
            "    Dato_adicional2 VARCHAR (30),\n"
            "    Dato_adicional3 VARCHAR (30),\n"
            "    Dato_adicional4 VARCHAR (30),\n"
            "    descuento NUMERIC (15, 3),\n"
            "    cbt_desde INTEGER ,\n"
            "    cbt_hasta INTEGER ,\n"
            "    concepto INTEGER ,\n"
            "    no_usar NUMERIC (15, 3),\n"
            "    imp_iva NUMERIC (15, 3),\n"
            "    emision_tipo VARCHAR (4),\n"
            "    imp_subtotal NUMERIC (15, 3),\n"
            "    cat_iva INTEGER ,\n"
            "    tipo_cbte INTEGER ,\n"
            "    punto_vta INTEGER ,\n"
            "    tipo_cod_aut VARCHAR (1)\n"
            ")\n;"
        ]
        assert list(esquema_sql(tipos_registro, conf)) == expected_output

    def test_esquema_sql_detalle(self, auth):
        # Prueba para generar el esquema SQL de la tabla "detalle"
        tipos_registro = [("detalle", DETALLE)]
        conf = {}
        expected_output = [
            "CREATE TABLE detalle (\n"
            "    id INTEGER  FOREING KEY encabezado,\n"
            "    tipo_reg INTEGER ,\n"
            "    codigo VARCHAR (30),\n"
            "    qty NUMERIC (12, 2),\n"
            "    umed INTEGER ,\n"
            "    precio NUMERIC (12, 3),\n"
            "    importe NUMERIC (14, 3),\n"
            "    iva_id INTEGER ,\n"
            "    ds VARCHAR (4000),\n"
            "    ncm VARCHAR (15),\n"
            "    sec VARCHAR (15),\n"
            "    bonif NUMERIC (15, 2),\n"
            "    imp_iva NUMERIC (15, 2),\n"
            "    despacho VARCHAR (20),\n"
            "    u_mtx INTEGER ,\n"
            "    cod_mtx INTEGER ,\n"
            "    dato_a VARCHAR (15),\n"
            "    dato_b VARCHAR (15),\n"
            "    dato_c VARCHAR (15),\n"
            "    dato_d VARCHAR (15),\n"
            "    dato_e VARCHAR (15)\n"
            ")\n;"
        ]
        assert list(esquema_sql(tipos_registro, conf)) == expected_output

    def test_esquema_sql_tributo(self, auth):
        # Prueba para generar el esquema SQL de la tabla "tributo"
        tipos_registro = [("tributo", TRIBUTO)]
        conf = {}
        expected_output = [
            "CREATE TABLE tributo (\n"
            "    id INTEGER  FOREING KEY encabezado,\n"
            "    tipo_reg INTEGER ,\n"
            "    tributo_id INTEGER ,\n"
            "    desc VARCHAR (100),\n"
            "    base_imp NUMERIC (15, 3),\n"
            "    alic NUMERIC (15, 2),\n"
            "    importe NUMERIC (15, 3)\n"
            ")\n;"
        ]
        assert list(esquema_sql(tipos_registro, conf)) == expected_output

    def test_esquema_sql_iva(self, auth):
        # Prueba para generar el esquema SQL de la tabla "iva"
        tipos_registro = [("iva", IVA)]
        conf = {}
        expected_output = [
            "CREATE TABLE iva (\n"
            "    id INTEGER  FOREING KEY encabezado,\n"
            "    tipo_reg INTEGER ,\n"
            "    iva_id INTEGER ,\n"
            "    base_imp NUMERIC (15, 3),\n"
            "    importe NUMERIC (15, 3)\n"
            ")\n;"
        ]
        assert list(esquema_sql(tipos_registro, conf)) == expected_output

    def test_esquema_sql_cmp_asoc(self, auth):
        # Prueba para generar el esquema SQL de la tabla "cmp_asoc"
        tipos_registro = [("cmp_asoc", CMP_ASOC)]
        conf = {}
        expected_output = [
            "CREATE TABLE cmp_asoc (\n"
            "    id INTEGER  FOREING KEY encabezado,\n"
            "    tipo_reg INTEGER ,\n"
            "    cbte_tipo INTEGER ,\n"
            "    cbte_punto_vta INTEGER ,\n"
            "    cbte_nro INTEGER ,\n"
            "    cbte_fecha INTEGER ,\n"
            "    cbte_cuit INTEGER \n"
            ")\n;"
        ]
        assert list(esquema_sql(tipos_registro, conf)) == expected_output

    def test_esquema_sql_permiso(self, auth):
        # Prueba para generar el esquema SQL de la tabla "permiso"
        tipos_registro = [("permiso", PERMISO)]
        conf = {}
        expected_output = [
            "CREATE TABLE permiso (\n"
            "    id INTEGER  FOREING KEY encabezado,\n"
            "    tipo_reg INTEGER ,\n"
            "    id_permiso VARCHAR (16),\n"
            "    dst_merc INTEGER \n"
            ")\n;"
        ]
        assert list(esquema_sql(tipos_registro, conf)) == expected_output

    def test_esquema_sql_detalle_with_conf(self, auth):
        # Prueba para generar el esquema SQL de la tabla "detalle" con configuración personalizada
        tipos_registro = [("detalle", DETALLE)]
        conf = {"detalle": {"qty": "cantidad"}}
        expected_output = [
            "CREATE TABLE detalle (\n"
            "    id INTEGER  FOREING KEY encabezado,\n"
            "    tipo_reg INTEGER ,\n"
            "    codigo VARCHAR (30),\n"
            "    cantidad NUMERIC (12, 2),\n"
            "    umed INTEGER ,\n"
            "    precio NUMERIC (12, 3),\n"
            "    importe NUMERIC (14, 3),\n"
            "    iva_id INTEGER ,\n"
            "    ds VARCHAR (4000),\n"
            "    ncm VARCHAR (15),\n"
            "    sec VARCHAR (15),\n"
            "    bonif NUMERIC (15, 2),\n"
            "    imp_iva NUMERIC (15, 2),\n"
            "    despacho VARCHAR (20),\n"
            "    u_mtx INTEGER ,\n"
            "    cod_mtx INTEGER ,\n"
            "    dato_a VARCHAR (15),\n"
            "    dato_b VARCHAR (15),\n"
            "    dato_c VARCHAR (15),\n"
            "    dato_d VARCHAR (15),\n"
            "    dato_e VARCHAR (15)\n"
            ")\n;"
        ]
        assert list(esquema_sql(tipos_registro, conf)) == expected_output

    def test_esquema_sql_tributo_with_conf(self, auth):
        # Prueba para generar el esquema SQL de la tabla "tributo" con configuración personalizada
        tipos_registro = [("tributo", TRIBUTO)]
        conf = {"tributo": {"desc": "descripcion"}}
        expected_output = [
            "CREATE TABLE tributo (\n"
            "    id INTEGER  FOREING KEY encabezado,\n"
            "    tipo_reg INTEGER ,\n"
            "    tributo_id INTEGER ,\n"
            "    descripcion VARCHAR (100),\n"
            "    base_imp NUMERIC (15, 3),\n"
            "    alic NUMERIC (15, 2),\n"
            "    importe NUMERIC (15, 3)\n"
            ")\n;"
        ]
        assert list(esquema_sql(tipos_registro, conf)) == expected_output

    def test_esquema_sql_iva_with_conf(self, auth):
        # Prueba para generar el esquema SQL de la tabla "iva" con configuración personalizada
        tipos_registro = [("iva", IVA)]
        conf = {"iva": {"importe": "imp_iva"}}
        expected_output = [
            "CREATE TABLE iva (\n"
            "    id INTEGER  FOREING KEY encabezado,\n"
            "    tipo_reg INTEGER ,\n"
            "    iva_id INTEGER ,\n"
            "    base_imp NUMERIC (15, 3),\n"
            "    imp_iva NUMERIC (15, 3)\n"
            ")\n;"
        ]
        assert list(esquema_sql(tipos_registro, conf)) == expected_output

    def test_esquema_sql_cmp_asoc_with_conf(self, auth):
        # Prueba para generar el esquema SQL de la tabla "cmp_asoc" con configuración personalizada
        tipos_registro = [("cmp_asoc", CMP_ASOC)]
        conf = {"cmp_asoc": {"cbte_nro": "numero"}}
        expected_output = [
            "CREATE TABLE cmp_asoc (\n"
            "    id INTEGER  FOREING KEY encabezado,\n"
            "    tipo_reg INTEGER ,\n"
            "    cbte_tipo INTEGER ,\n"
            "    cbte_punto_vta INTEGER ,\n"
            "    numero INTEGER ,\n"
            "    cbte_fecha INTEGER ,\n"
            "    cbte_cuit INTEGER \n"
            ")\n;"
        ]
        assert list(esquema_sql(tipos_registro, conf)) == expected_output

    def test_esquema_sql_permiso_with_conf(self, auth):
        # Prueba para generar el esquema SQL de la tabla "permiso" con configuración personalizada
        tipos_registro = [("permiso", PERMISO)]
        conf = {"permiso": {"dst_merc": "destino"}}
        expected_output = [
            "CREATE TABLE permiso (\n"
            "    id INTEGER  FOREING KEY encabezado,\n"
            "    tipo_reg INTEGER ,\n"
            "    id_permiso VARCHAR (16),\n"
            "    destino INTEGER \n"
            ")\n;"
        ]
        assert list(esquema_sql(tipos_registro, conf)) == expected_output
