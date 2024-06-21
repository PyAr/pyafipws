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

"""Test para formato_txt"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010-2019 Mariano Reingart"
__license__ = "GPL 3.0"


import pytest
from pyafipws.formatos import formato_txt

@pytest.mark.dontusefix
class TestFormatoTxt:

    @pytest.fixture
    def factura_line(self):
        return "0      2021080520400012345678  212Joao Da Silva                                                                                                                                                                                           8030000000007Rua 76 km 34.5 Alagoas                                                                                                                                                                                                                                                                                      PJ54482221-l                                      000000000127000000000000003000000000000100000                              000000000002000                                                            000000000001000PES0001000000Observaciones Comerciales<br/>texto libre                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Observaciones Generales<br/>linea2<br/>linea3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           30 dias                                           FOB                          20210805 20210805202108056112302292585520110320A Factura individual, DocTipo: 80, DocNro 30000000007 no se encuentra registrado en los padrones de AFIP.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 000000000000000                                                  Hurlingham                                        Buenos Aires                                                                                                                                                                                                                                                        OK                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    000000000000000                3               000000000021000                     20104000 "

    def test_leer_linea_txt_encabezado(self, factura_line):
        formato = formato_txt.ENCABEZADO
        result = formato_txt.leer_linea_txt(factura_line, formato)

        print("Encabezado result:", result)

        assert result['tipo_reg'] == 0
        assert result['fecha_cbte'] == '20210805'
        assert result['tipo_cbte'] == 201
        assert result['punto_vta'] == 4000
        assert result['cbte_nro'] == 12345678
        assert result['tipo_expo'] is None  # Changed from 2 to None
        assert result['permiso_existente'] == ''
        assert result['pais_dst_cmp'] == 212
        assert result['nombre_cliente'] == 'Joao Da Silva'
        assert result['tipo_doc'] == 80
        assert result['nro_doc'] == 30000000007
        assert result['domicilio_cliente'] == 'Rua 76 km 34.5 Alagoas'
        assert result['id_impositivo'] == 'PJ54482221-l'
        assert result['imp_total'] == 127.0
        assert result['imp_tot_conc'] == 3.0
        assert result['imp_neto'] == 100.0
        assert result['impto_liq'] is None
        assert result['impto_liq_nri'] is None
        assert result['imp_op_ex'] == 2.0
        assert result['imp_trib'] == 1.0
        assert result['moneda_id'] == 'PES'
        assert result['moneda_ctz'] == 1.0
        assert result['obs_comerciales'] == 'Observaciones Comerciales<br/>texto libre'
        assert result['obs_generales'] == 'Observaciones Generales<br/>linea2<br/>linea3'
        assert result['forma_pago'] == '30 dias'
        assert result['incoterms'] == 'FOB'
        assert result['fecha_venc_pago'] == '20210805'
        assert result['idioma_cbte'] == ''
        assert result['cae'] == '61123022925855'
        assert result['fecha_vto'] == '20110320'
        assert result['resultado'] == 'A'
        assert result['motivos_obs'] == 'Factura individual, DocTipo: 80, DocNro 30000000007 no se encuentra registrado en los padrones de AFIP.'
        assert result['localidad_cliente'] == 'Hurlingham'
        assert result['provincia_cliente'] == 'Buenos Aires'
        assert result['concepto'] == 3
        assert result['imp_iva'] == 21.0

    def test_leer_linea_txt_iva(self):
        iva_line = "400005000000000100000000000000021000                                                                                                                                                                                                                                                                                                           "
        formato = formato_txt.IVA
        result = formato_txt.leer_linea_txt(iva_line, formato)
        
        assert result['tipo_reg'] == 4
        assert result['iva_id'] == 5
        assert result['base_imp'] == 100.0
        assert result['importe'] == 21.0

    def test_leer_linea_txt_tributo(self):
        tributo_line = "500099Impuesto Municipal Matanza                                                                          000000000100000000000000000100000000000001000                                                                                                                                                                                        "
        formato = formato_txt.TRIBUTO
        result = formato_txt.leer_linea_txt(tributo_line, formato)
        
        assert result['tipo_reg'] == 5
        assert result['tributo_id'] == 99
        assert result['desc'] == 'Impuesto Municipal Matanza'
        assert result['base_imp'] == 100.0
        assert result['alic'] == 1.0
        assert result['importe'] == 1.0
