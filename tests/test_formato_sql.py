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
from decimal import Decimal
from unittest.mock import MagicMock, patch
from pyafipws.formatos.formato_sql import esquema_sql, configurar, ejecutar, max_id, redondear, escribir, modificar, CAE_NULL, FECHA_VTO_NULL, RESULTADO_NULL, NULL
from pyafipws.formatos.formato_txt import ENCABEZADO, DETALLE, TRIBUTO, IVA, CMP_ASOC, PERMISO, A, N, I

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
    


@pytest.mark.dontusefix
class TestConfigurar:
    def test_configurar_without_schema(self):
        # Test configuring without a custom schema
        schema = {}
        expected_tablas = {
            "encabezado": "encabezado",
            "detalle": "detalle",
            "cmp_asoc": "cmp_asoc",
            "permiso": "permiso",
            "tributo": "tributo",
            "iva": "iva",
        }
        expected_campos = {
            "encabezado": {"id": "id"},
            "detalle": {"id": "id"},
            "cmp_asoc": {"id": "id"},
            "permiso": {"id": "id"},
            "tributo": {"id": "id"},
            "iva": {"id": "id"},
        }
        expected_campos_rev = {
            "encabezado": {"id": "id"},
            "detalle": {"id": "id"},
            "cmp_asoc": {"id": "id"},
            "permiso": {"id": "id"},
            "tributo": {"id": "id"},
            "iva": {"id": "id"},
        }
        tablas, campos, campos_rev = configurar(schema)
        assert tablas == expected_tablas
        assert campos == expected_campos
        assert campos_rev == expected_campos_rev

    def test_configurar_with_custom_schema(self):
        # Test configuring with a custom schema
        schema = {
            "encabezado": {"nombre": "encabezado_nombre"},
            "detalle": {"cantidad": "detalle_cantidad"},
            "cmp_asoc": {"numero": "cmp_asoc_numero"},
            "permiso": {"destino": "permiso_destino"},
            "tributo": {"descripcion": "tributo_descripcion"},
            "iva": {"importe": "iva_importe"},
        }
        expected_tablas = {
            "encabezado": "encabezado",
            "detalle": "detalle",
            "cmp_asoc": "cmp_asoc",
            "permiso": "permiso",
            "tributo": "tributo",
            "iva": "iva",
        }
        expected_campos = {
            "encabezado": {"nombre": "encabezado_nombre", "id": "id"},
            "detalle": {"cantidad": "detalle_cantidad", "id": "id"},
            "cmp_asoc": {"numero": "cmp_asoc_numero", "id": "id"},
            "permiso": {"destino": "permiso_destino", "id": "id"},
            "tributo": {"descripcion": "tributo_descripcion", "id": "id"},
            "iva": {"importe": "iva_importe", "id": "id"},
        }
        expected_campos_rev = {
            "encabezado": {"encabezado_nombre": "nombre", "id": "id"},
            "detalle": {"detalle_cantidad": "cantidad", "id": "id"},
            "cmp_asoc": {"cmp_asoc_numero": "numero", "id": "id"},
            "permiso": {"permiso_destino": "destino", "id": "id"},
            "tributo": {"tributo_descripcion": "descripcion", "id": "id"},
            "iva": {"iva_importe": "importe", "id": "id"},
        }
        tablas, campos, campos_rev = configurar(schema)
        assert tablas == expected_tablas
        assert campos == expected_campos
        assert campos_rev == expected_campos_rev

    def test_configurar_with_partial_schema(self):
        # Test configuring with a partial schema
        schema = {
            "encabezado": {"nombre": "encabezado_nombre"},
            "detalle": {"cantidad": "detalle_cantidad"},
        }
        expected_tablas = {
            "encabezado": "encabezado",
            "detalle": "detalle",
            "cmp_asoc": "cmp_asoc",
            "permiso": "permiso",
            "tributo": "tributo",
            "iva": "iva",
        }
        expected_campos = {
            "encabezado": {"nombre": "encabezado_nombre", "id": "id"},
            "detalle": {"cantidad": "detalle_cantidad", "id": "id"},
            "cmp_asoc": {"id": "id"},
            "permiso": {"id": "id"},
            "tributo": {"id": "id"},
            "iva": {"id": "id"},
        }
        expected_campos_rev = {
            "encabezado": {"encabezado_nombre": "nombre", "id": "id"},
            "detalle": {"detalle_cantidad": "cantidad", "id": "id"},
            "cmp_asoc": {"id": "id"},
            "permiso": {"id": "id"},
            "tributo": {"id": "id"},
            "iva": {"id": "id"},
        }
        tablas, campos, campos_rev = configurar(schema)
        assert tablas == expected_tablas
        assert campos == expected_campos
        assert campos_rev == expected_campos_rev


    def test_configurar_with_empty_schema(self):
        # Test configuring with an empty schema
        schema = {}
        expected_tablas = {
            "encabezado": "encabezado",
            "detalle": "detalle",
            "cmp_asoc": "cmp_asoc",
            "permiso": "permiso",
            "tributo": "tributo",
            "iva": "iva",
        }
        expected_campos = {
            "encabezado": {"id": "id"},
            "detalle": {"id": "id"},
            "cmp_asoc": {"id": "id"},
            "permiso": {"id": "id"},
            "tributo": {"id": "id"},
            "iva": {"id": "id"},
        }
        expected_campos_rev = {
            "encabezado": {"id": "id"},
            "detalle": {"id": "id"},
            "cmp_asoc": {"id": "id"},
            "permiso": {"id": "id"},
            "tributo": {"id": "id"},
            "iva": {"id": "id"},
        }
        tablas, campos, campos_rev = configurar(schema)
        assert tablas == expected_tablas
        assert campos == expected_campos
        assert campos_rev == expected_campos_rev

    def test_configurar_with_none_schema(self):
        # Test configuring with a None schema
        schema = None
        expected_tablas = {
            "encabezado": "encabezado",
            "detalle": "detalle",
            "cmp_asoc": "cmp_asoc",
            "permiso": "permiso",
            "tributo": "tributo",
            "iva": "iva",
        }
        expected_campos = {
            "encabezado": {"id": "id"},
            "detalle": {"id": "id"},
            "cmp_asoc": {"id": "id"},
            "permiso": {"id": "id"},
            "tributo": {"id": "id"},
            "iva": {"id": "id"},
        }
        expected_campos_rev = {
            "encabezado": {"id": "id"},
            "detalle": {"id": "id"},
            "cmp_asoc": {"id": "id"},
            "permiso": {"id": "id"},
            "tributo": {"id": "id"},
            "iva": {"id": "id"},
        }
        tablas, campos, campos_rev = configurar(schema)
        assert tablas == expected_tablas
        assert campos == expected_campos
        assert campos_rev == expected_campos_rev



@pytest.mark.dontusefix
class TestEjecutar:
    
    def test_ejecutar_without_params(self, mocker):
        # Test executing a query without parameters
        cur = MagicMock()
        sql = "SELECT * FROM tabla"
        mocker.patch('pyafipws.formatos.formato_sql.ejecutar', return_value=None)
        ejecutar(cur, sql)
        cur.execute.assert_called_once_with(sql)

    def test_ejecutar_with_params(self, mocker):
        # Test executing a query with parameters
        cur = MagicMock()
        sql = "SELECT * FROM tabla WHERE id = ?"
        params = (1,)
        mocker.patch('pyafipws.formatos.formato_sql.ejecutar', return_value=None)
        ejecutar(cur, sql, params)
        cur.execute.assert_called_once_with(sql, params)

    def test_ejecutar_returns_cursor_execute_result(self, mocker):
        # Test that ejecutar returns the result of cursor.execute
        cur = MagicMock()
        sql = "SELECT * FROM tabla"
        expected_result = MagicMock()
        cur.execute.return_value = expected_result
        result = ejecutar(cur, sql)
        assert result == expected_result

    def test_ejecutar_prints_sql_and_params_when_debug_true(self, mocker, capsys):
        # Test that ejecutar prints the SQL query and parameters when DEBUG is True
        cur = MagicMock()
        sql = "SELECT * FROM tabla WHERE id = ?"
        params = (1,)
        mocker.patch('pyafipws.formatos.formato_sql.DEBUG', True)
        ejecutar(cur, sql, params)
        captured = capsys.readouterr()
        assert captured.out == "SELECT * FROM tabla WHERE id = ? (1,)\n"

    def test_ejecutar_does_not_print_when_debug_false(self, mocker, capsys):
        # Test that ejecutar does not print anything when DEBUG is False
        cur = MagicMock()
        sql = "SELECT * FROM tabla"
        mocker.patch('pyafipws.formatos.formato_sql.DEBUG', False)
        ejecutar(cur, sql)
        captured = capsys.readouterr()
        assert captured.out == ""
        
@pytest.fixture
def db_mock():
    return MagicMock()

@pytest.fixture
def cur_mock(db_mock):
    cur_mock = MagicMock()
    db_mock.cursor.return_value = cur_mock
    return cur_mock

@pytest.mark.dontusefix
class TestMaxId:
    def test_max_id_with_existing_id(self, db_mock, cur_mock, mocker):
        schema = {}
        expected_max_id = 42
        cur_mock.fetchone.return_value = (expected_max_id,)
        configurar_mock = mocker.patch('pyafipws.formatos.formato_sql.configurar', return_value=({'encabezado': 'encabezado'}, {'encabezado': {'id': 'id'}}, {}))
        ejecutar_mock = mocker.patch('pyafipws.formatos.formato_sql.ejecutar')

        result = max_id(db_mock, schema)

        assert result == expected_max_id
        db_mock.cursor.assert_called_once()
        configurar_mock.assert_called_once_with(schema)
        ejecutar_mock.assert_called_once()
        cur_mock.fetchone.assert_called_once()
        cur_mock.close.assert_called_once()

    def test_max_id_with_no_existing_id(self, db_mock, cur_mock, mocker):
        schema = {}
        cur_mock.fetchone.return_value = (None,)
        configurar_mock = mocker.patch('pyafipws.formatos.formato_sql.configurar', return_value=({'encabezado': 'encabezado'}, {'encabezado': {'id': 'id'}}, {}))
        ejecutar_mock = mocker.patch('pyafipws.formatos.formato_sql.ejecutar')

        result = max_id(db_mock, schema)

        assert result == 0
        db_mock.cursor.assert_called_once()
        configurar_mock.assert_called_once_with(schema)
        ejecutar_mock.assert_called_once()
        cur_mock.fetchone.assert_called_once()
        cur_mock.close.assert_called_once()

    def test_max_id_with_custom_schema(self, db_mock, cur_mock, mocker):
        schema = {'encabezado': {'custom_id': 'id'}}
        expected_max_id = 42
        cur_mock.fetchone.return_value = (expected_max_id,)
        configurar_mock = mocker.patch('pyafipws.formatos.formato_sql.configurar', return_value=({'encabezado': 'custom_encabezado'}, {'encabezado': {'id': 'custom_id'}}, {}))
        ejecutar_mock = mocker.patch('pyafipws.formatos.formato_sql.ejecutar')

        result = max_id(db_mock, schema)

        assert result == expected_max_id
        db_mock.cursor.assert_called_once()
        configurar_mock.assert_called_once_with(schema)
        ejecutar_mock.assert_called_once()
        cur_mock.fetchone.assert_called_once()
        cur_mock.close.assert_called_once()

    def test_max_id_with_empty_result(self, db_mock, cur_mock, mocker):
        schema = {}
        cur_mock.fetchone.return_value = None
        configurar_mock = mocker.patch('pyafipws.formatos.formato_sql.configurar', return_value=({'encabezado': 'encabezado'}, {'encabezado': {'id': 'id'}}, {}))
        ejecutar_mock = mocker.patch('pyafipws.formatos.formato_sql.ejecutar')

        result = max_id(db_mock, schema)

        assert result == 0
        db_mock.cursor.assert_called_once()
        configurar_mock.assert_called_once_with(schema)
        ejecutar_mock.assert_called_once()
        cur_mock.fetchone.assert_called_once()
        cur_mock.close.assert_called_once()

    def test_max_id_with_exception(self, db_mock, cur_mock, mocker):
        schema = {}
        configurar_mock = mocker.patch('pyafipws.formatos.formato_sql.configurar', return_value=({'encabezado': 'encabezado'}, {'encabezado': {'id': 'id'}}, {}))
        ejecutar_mock = mocker.patch('pyafipws.formatos.formato_sql.ejecutar', side_effect=Exception('Database error'))

        with pytest.raises(Exception) as exc_info:
            max_id(db_mock, schema)

        assert str(exc_info.value) == 'Database error'
        db_mock.cursor.assert_called_once()
        configurar_mock.assert_called_once_with(schema)
        ejecutar_mock.assert_called_once()
        cur_mock.fetchone.assert_not_called()
        cur_mock.close.assert_called_once()
        
        

@pytest.mark.dontusefix
class TestRedondear:
    def test_redondear_with_invalid_key(self):
        formato = [("campo1", 10, A), ("campo2", 15, N)]
        clave = "campo3"
        valor = "123"

        result = redondear(formato, clave, valor)

        assert result == "123"

    def test_redondear_with_none_value(self):
        formato = [("campo1", 10, A), ("campo2", 15, N)]
        clave = "campo1"
        valor = None

        result = redondear(formato, clave, valor)

        assert result is None

    def test_redondear_with_empty_string_value(self):
        formato = [("campo1", 10, A), ("campo2", 15, N)]
        clave = "campo1"
        valor = ""

        result = redondear(formato, clave, valor)

        assert result == ""

    def test_redondear_with_tipo_a(self):
        formato = [("campo1", 10, A), ("campo2", 15, N)]
        clave = "campo1"
        valor = "ABC123"

        result = redondear(formato, clave, valor)

        assert result == "ABC123"

    def test_redondear_with_tipo_n(self):
        formato = [("campo1", 10, A), ("campo2", 15, N)]
        clave = "campo2"
        valor = "123"

        result = redondear(formato, clave, valor)

        assert result == 123

    def test_redondear_with_int_value(self):
        formato = [("campo1", 10, A), ("campo2", (15, 2), I)]
        clave = "campo2"
        valor = 123

        result = redondear(formato, clave, valor)

        assert result == Decimal("123.00")

    def test_redondear_with_float_value(self):
        formato = [("campo1", 10, A), ("campo2", (15, 2), I)]
        clave = "campo2"
        valor = 123.456

        result = redondear(formato, clave, valor)

        assert result == Decimal("123.45")

    def test_redondear_with_string_value(self):
        formato = [("campo1", 10, A), ("campo2", (15, 2), I)]
        clave = "campo2"
        valor = "123.456"

        result = redondear(formato, clave, valor)

        assert result == Decimal("123.45")

    def test_redondear_with_custom_decimals(self):
        formato = [("campo1", 10, A), ("campo2", (15, 3), I)]
        clave = "campo2"
        valor = "123.4567"

        result = redondear(formato, clave, valor)

        assert result == Decimal("123.456")

    def test_redondear_with_exception(self, mocker):
        formato = [("campo1", 10, A), ("campo2", (15, 2), I)]
        clave = "campo2"
        valor = "invalid"

        mocker.patch("builtins.print")

        result = redondear(formato, clave, valor)

        assert result is None
        print.assert_called_once_with("IMPOSIBLE REDONDEAR:", clave, valor, mocker.ANY)
        
        
        
        
@pytest.fixture
def db_mock():
    return MagicMock()

@pytest.fixture
def cur_mock(db_mock):
    cur_mock = MagicMock()
    db_mock.cursor.return_value = cur_mock
    return cur_mock  
   
     
@pytest.mark.dontusefix 
class Test_escribir:  
    def test_escribir_without_id(self, db_mock, cur_mock, mocker):
            facts = [{"campo1": "valor1", "campo2": "valor2", "detalles": []}]
            schema = {}
            mocker.patch('pyafipws.formatos.formato_sql.max_id', return_value=1)
            mocker.patch('pyafipws.formatos.formato_sql.configurar', return_value=({'encabezado': 'encabezado', 'detalle': 'detalle'}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}}))
            ejecutar_mock = mocker.patch('pyafipws.formatos.formato_sql.ejecutar')

            escribir(facts, db_mock, schema)

            assert ejecutar_mock.call_count == 1
            db_mock.commit.assert_called_once()

    def test_escribir_with_id(self, db_mock, cur_mock, mocker):
            facts = [{"id": 1, "campo1": "valor1", "campo2": "valor2", "detalles": []}]
            schema = {}
            mocker.patch('pyafipws.formatos.formato_sql.configurar', return_value=({'encabezado': 'encabezado', 'detalle': 'detalle'}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}}))
            ejecutar_mock = mocker.patch('pyafipws.formatos.formato_sql.ejecutar')

            escribir(facts, db_mock, schema)

            assert ejecutar_mock.call_count == 1
            db_mock.commit.assert_called_once()

    def test_escribir_with_detalles(self, db_mock, cur_mock, mocker):
            facts = [{"id": 1, "campo1": "valor1", "campo2": "valor2", "detalles": [{"detalle1": "valor1"}, {"detalle2": "valor2"}]}]
            schema = {}
            mocker.patch('pyafipws.formatos.formato_sql.configurar', return_value=({'encabezado': 'encabezado', 'detalle': 'detalle'}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}}))
            ejecutar_mock = mocker.patch('pyafipws.formatos.formato_sql.ejecutar')

            escribir(facts, db_mock, schema)

            assert ejecutar_mock.call_count == 3
            db_mock.commit.assert_called_once()

    def test_escribir_with_cbtes_asoc(self, db_mock, cur_mock, mocker):
            facts = [{"id": 1, "campo1": "valor1", "campo2": "valor2", "detalles": [], "cbtes_asoc": [{"cbte_asoc1": "valor1"}, {"cbte_asoc2": "valor2"}]}]
            schema = {}
            mocker.patch('pyafipws.formatos.formato_sql.configurar', return_value=({'encabezado': 'encabezado', 'detalle': 'detalle', 'cmp_asoc': 'cmp_asoc'}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}, 'cmp_asoc': {'id': 'id'}}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}, 'cmp_asoc': {'id': 'id'}}))
            ejecutar_mock = mocker.patch('pyafipws.formatos.formato_sql.ejecutar')

            escribir(facts, db_mock, schema)

            assert ejecutar_mock.call_count == 3
            db_mock.commit.assert_called_once()

    def test_escribir_with_permisos(self, db_mock, cur_mock, mocker):
            facts = [{"id": 1, "campo1": "valor1", "campo2": "valor2", "detalles": [], "permisos": [{"permiso1": "valor1"}, {"permiso2": "valor2"}]}]
            schema = {}
            mocker.patch('pyafipws.formatos.formato_sql.configurar', return_value=({'encabezado': 'encabezado', 'detalle': 'detalle', 'permiso': 'permiso'}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}, 'permiso': {'id': 'id'}}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}, 'permiso': {'id': 'id'}}))
            ejecutar_mock = mocker.patch('pyafipws.formatos.formato_sql.ejecutar')

            escribir(facts, db_mock, schema)

            assert ejecutar_mock.call_count == 3
            db_mock.commit.assert_called_once()

    def test_escribir_with_tributos(self, db_mock, cur_mock, mocker):
            facts = [{"id": 1, "campo1": "valor1", "campo2": "valor2", "detalles": [], "tributos": [{"tributo1": "valor1"}, {"tributo2": "valor2"}]}]
            schema = {}
            mocker.patch('pyafipws.formatos.formato_sql.configurar', return_value=({'encabezado': 'encabezado', 'detalle': 'detalle', 'tributo': 'tributo'}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}, 'tributo': {'id': 'id'}}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}, 'tributo': {'id': 'id'}}))
            ejecutar_mock = mocker.patch('pyafipws.formatos.formato_sql.ejecutar')

            escribir(facts, db_mock, schema)

            assert ejecutar_mock.call_count == 3
            db_mock.commit.assert_called_once()

    def test_escribir_with_ivas(self, db_mock, cur_mock, mocker):
            facts = [{"id": 1, "campo1": "valor1", "campo2": "valor2", "detalles": [], "ivas": [{"iva1": "valor1"}, {"iva2": "valor2"}]}]
            schema = {}
            mocker.patch('pyafipws.formatos.formato_sql.configurar', return_value=({'encabezado': 'encabezado', 'detalle': 'detalle', 'iva': 'iva'}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}, 'iva': {'id': 'id'}}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}, 'iva': {'id': 'id'}}))
            ejecutar_mock = mocker.patch('pyafipws.formatos.formato_sql.ejecutar')

            escribir(facts, db_mock, schema)

            assert ejecutar_mock.call_count == 3
            db_mock.commit.assert_called_once()

    def test_escribir_without_commit(self, db_mock, cur_mock, mocker):
            facts = [{"id": 1, "campo1": "valor1", "campo2": "valor2", "detalles": []}]
            schema = {}
            mocker.patch('pyafipws.formatos.formato_sql.configurar', return_value=({'encabezado': 'encabezado', 'detalle': 'detalle'}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}}, {'encabezado': {'id': 'id'}, 'detalle': {'id': 'id'}}))
            ejecutar_mock = mocker.patch('pyafipws.formatos.formato_sql.ejecutar')

            escribir(facts, db_mock, schema, commit=False)

            assert ejecutar_mock.call_count == 1
            db_mock.commit.assert_not_called()  
            
            
            
            
            
@pytest.mark.dontusefix
@pytest.mark.parametrize("cae, fecha_vto, resultado, reproceso, motivo_obs, err_code, err_msg, cbte_nro", [
    ("12345678901234", "20230101", "A", "S", "Observación", "00", "Error mensaje", "1"),
    ("NULL", None, None, None, None, None, None, "2"),
    ("", None, "", "", "", "", "", "3"),
])
def test_modificar(db_mock, cur_mock, mocker, cae, fecha_vto, resultado, reproceso, motivo_obs, err_code, err_msg, cbte_nro):
    fact = {
        "id": 1,
        "cae": cae,
        "fecha_vto": fecha_vto,
        "resultado": resultado,
        "reproceso": reproceso,
        "motivo_obs": motivo_obs,
        "err_code": err_code,
        "err_msg": err_msg,
        "cbte_nro": cbte_nro,
    }
    schema = {}
    webservice = "wsfev1"
    ids = None
    conf_db = {"null": True}

    mocker.patch("pyafipws.formatos.formato_sql.configurar", return_value=({'encabezado': 'encabezado'}, {"encabezado": {"id": "id"}}, {}))

    modificar(fact, db_mock, schema, webservice, ids, conf_db)

    if cae == "NULL" or cae == "" or cae is None:
        assert fact["cae"] == CAE_NULL
        assert fact["fecha_vto"] == FECHA_VTO_NULL

    if "null" in conf_db and (resultado is None or resultado == ""):
        assert fact["resultado"] == RESULTADO_NULL

    for k in ["reproceso", "motivo_obs", "err_code", "err_msg"]:
        if "null" in conf_db and (k in fact and fact[k] is None or fact[k] == ""):
            assert fact[k] == NULL

    cur_mock.execute.assert_called_once()

@pytest.mark.dontusefix
def test_modificar_exception(db_mock, cur_mock, mocker):
    fact = {
        "id": 1,
        "cae": "12345678901234",
        "fecha_vto": "20230101",
        "resultado": "A",
        "reproceso": "S",
        "motivo_obs": "Observación",
        "err_code": "00",
        "err_msg": "Error mensaje",
        "cbte_nro": "1",
    }
    schema = {}
    webservice = "wsfev1"
    ids = None
    conf_db = {"null": True}

    mocker.patch("pyafipws.formatos.formato_sql.configurar", return_value=({'encabezado': 'encabezado'}, {"encabezado": {"id": "id"}}, {}))
    mocker.patch("pyafipws.formatos.formato_sql.ejecutar", side_effect=Exception("Database error"))

    with pytest.raises(Exception) as exc_info:
        modificar(fact, db_mock, schema, webservice, ids, conf_db)

    assert str(exc_info.value) == "Database error"