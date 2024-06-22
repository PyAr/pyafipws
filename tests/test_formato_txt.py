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

import os
import pytest
from unittest.mock import patch, mock_open
from pyafipws.formatos import formato_txt

def read_facturas_txt():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    facturas_path = os.path.join(current_dir, 'facturas.txt')
    with open(facturas_path, 'r', encoding='utf-8') as file:
        return file.readlines()

@pytest.mark.dontusefix
class TestLeerLineaTxt:
    """Pruebas para la función leer_linea_txt"""
     
    @pytest.fixture(scope="class")
    def facturas_lines(self):
        return read_facturas_txt()
    
    def test_leer_linea_txt_encabezado(self, facturas_lines):
        
        encabezado_line = next(line for line in facturas_lines if line.startswith('0'))
        result = formato_txt.leer_linea_txt(encabezado_line, formato_txt.ENCABEZADO)

        assert result['tipo_reg'] == 0
        assert result['fecha_cbte'] == '20210805'
        assert result['tipo_cbte'] == 201
        assert result['punto_vta'] == 4000
        assert result['cbte_nro'] == 12345678
        assert result['tipo_expo'] is None
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
        assert result['imp_op_ex'] == 2.0
        assert result['imp_trib'] == 1.0
        assert result['moneda_id'] == 'PES'
        assert result['moneda_ctz'] == 1.0
        assert result['obs_comerciales'].startswith('Observaciones Comerciales')
        assert result['obs_generales'].startswith('Observaciones Generales')
        assert result['forma_pago'] == '30 dias'
        assert result['incoterms'] == 'FOB'
        assert result['cae'] == '61123022925855'
        assert result['fecha_vto'] == '20110320'
        assert result['resultado'] == 'A'
        assert result['motivos_obs'].startswith('Factura individual')
        assert result['concepto'] == 3
        assert result['imp_iva'] == 21.0

    def test_leer_linea_txt_detalle(self, facturas_lines):
        
        detalle_line = next(line for line in facturas_lines if line.startswith('1'))
        result = formato_txt.leer_linea_txt(detalle_line, formato_txt.DETALLE)

        assert result['tipo_reg'] == 1
        assert result['codigo'] == 'P0001'
        assert result['qty'] == 1.0
        assert result['umed'] == 7
        assert result['precio'] == 133.1
        assert result['importe'] == 133.1
        assert result['iva_id'] == 5
        assert result['ds'].startswith('Descripcion del producto P0001')
        assert result['despacho'] == 'Nº 123456'

    def test_leer_linea_txt_iva(self, facturas_lines):
        iva_line = next(line for line in facturas_lines if line.startswith('4'))
        result = formato_txt.leer_linea_txt(iva_line, formato_txt.IVA)

        assert result['tipo_reg'] == 4
        assert result['iva_id'] == 5
        assert result['base_imp'] == 100.0
        assert result['importe'] == 21.0

    def test_leer_linea_txt_tributo(self, facturas_lines):
        tributo_line = next(line for line in facturas_lines if line.startswith('5'))
        result = formato_txt.leer_linea_txt(tributo_line, formato_txt.TRIBUTO)

        assert result['tipo_reg'] == 5
        assert result['tributo_id'] == 99
        assert result['desc'] == 'Impuesto Municipal Matanza'
        assert result['base_imp'] == 100.0
        assert result['alic'] == 1.0
        assert result['importe'] == 1.0

    def test_leer_linea_txt_permiso(self, facturas_lines):
        permiso_line = next((line for line in facturas_lines if line.startswith('3')), None)
        if permiso_line:
            result = formato_txt.leer_linea_txt(permiso_line, formato_txt.PERMISO)
            assert result['tipo_reg'] == 3
            assert 'id_permiso' in result
        else:
            pytest.skip("No permiso line found in facturas.txt")

    def test_leer_linea_txt_dato(self, facturas_lines):
        dato_line = next((line for line in facturas_lines if line.startswith('9')), None)
        if dato_line:
            result = formato_txt.leer_linea_txt(dato_line, formato_txt.DATO)
            assert result['tipo_reg'] == 9
            assert 'campo' in result
            assert 'valor' in result
        else:
            pytest.skip("No dato line found in facturas.txt")

@pytest.mark.dontusefix
class TestEscribirLineaTxt:
    
    @pytest.fixture(scope="class")
    def facturas_lines(self):
        return read_facturas_txt()
    
    def test_escribir_linea_txt_encabezado(self, facturas_lines):
        encabezado_line = next(line for line in facturas_lines if line.startswith('0'))
        parsed_encabezado = formato_txt.leer_linea_txt(encabezado_line, formato_txt.ENCABEZADO)
        written_line = formato_txt.escribir_linea_txt(parsed_encabezado, formato_txt.ENCABEZADO)
        assert written_line.strip() == encabezado_line.strip()

    def test_escribir_linea_txt_detalle(self, facturas_lines):
        detalle_line = next(line for line in facturas_lines if line.startswith('1'))
        parsed_detalle = formato_txt.leer_linea_txt(detalle_line, formato_txt.DETALLE)
        written_line = formato_txt.escribir_linea_txt(parsed_detalle, formato_txt.DETALLE)
        assert written_line.strip() == detalle_line.strip()

    def test_escribir_linea_txt_iva(self, facturas_lines):
        iva_line = next(line for line in facturas_lines if line.startswith('4'))
        parsed_iva = formato_txt.leer_linea_txt(iva_line, formato_txt.IVA)
        written_line = formato_txt.escribir_linea_txt(parsed_iva, formato_txt.IVA)
        assert written_line.strip() == iva_line.strip()

    def test_escribir_linea_txt_tributo(self, facturas_lines):
        tributo_line = next(line for line in facturas_lines if line.startswith('5'))
        parsed_tributo = formato_txt.leer_linea_txt(tributo_line, formato_txt.TRIBUTO)
        written_line = formato_txt.escribir_linea_txt(parsed_tributo, formato_txt.TRIBUTO)
        assert written_line.strip() == tributo_line.strip()

    def test_escribir_linea_txt_permiso(self, facturas_lines):
        permiso_line = next((line for line in facturas_lines if line.startswith('3')), None)
        if permiso_line:
            parsed_permiso = formato_txt.leer_linea_txt(permiso_line, formato_txt.PERMISO)
            written_line = formato_txt.escribir_linea_txt(parsed_permiso, formato_txt.PERMISO)
            assert written_line.strip() == permiso_line.strip()
        else:
            pytest.skip("No permiso line found in facturas.txt")

    def test_escribir_linea_txt_dato(self, facturas_lines):
        dato_line = next((line for line in facturas_lines if line.startswith('9')), None)
        if dato_line:
            parsed_dato = formato_txt.leer_linea_txt(dato_line, formato_txt.DATO)
            written_line = formato_txt.escribir_linea_txt(parsed_dato, formato_txt.DATO)
            assert written_line.strip() == dato_line.strip()
        else:
            pytest.skip("No dato line found in facturas.txt")

    def test_leer_escribir_all_lines(self, facturas_lines):
        for line in facturas_lines:
            tipo_reg = int(line[0])
            if tipo_reg == 0:
                formato = formato_txt.ENCABEZADO
            elif tipo_reg == 1:
                formato = formato_txt.DETALLE
            elif tipo_reg == 2:
                formato = formato_txt.CMP_ASOC
            elif tipo_reg == 3:
                formato = formato_txt.PERMISO
            elif tipo_reg == 4:
                formato = formato_txt.IVA
            elif tipo_reg == 5:
                formato = formato_txt.TRIBUTO
            elif tipo_reg == 9:
                formato = formato_txt.DATO
            else:
                continue

            parsed_data = formato_txt.leer_linea_txt(line, formato)
            written_line = formato_txt.escribir_linea_txt(parsed_data, formato)
            assert written_line.strip() == line.strip()    


@pytest.mark.dontusefix
class TestLeer:
    
    @pytest.fixture(scope="class")
    def facturas_lines(self):
        return read_facturas_txt()
    
    def test_leer_multiple_invoices(self, facturas_lines):
        multiple_invoices = (''.join(facturas_lines) * 2).encode(formato_txt.CHARSET)  # Encode the input
        with patch('builtins.open', mock_open(read_data=multiple_invoices)):
            result = formato_txt.leer("dummy.txt")
        
        assert len(result) == 2
        for invoice in result:
            assert invoice['tipo_reg'] == 0
            assert len(invoice['detalles']) >= 1

    def test_leer_missing_sections(self, facturas_lines):
        incomplete_input = ''.join(line for line in facturas_lines if not line.startswith(('2', '3', '6')))
        incomplete_input = incomplete_input.encode(formato_txt.CHARSET)  # Encode the input
        with patch('builtins.open', mock_open(read_data=incomplete_input)):
            result = formato_txt.leer("dummy.txt")
        
        assert len(result) == 1
        assert result[0]['tipo_reg'] == 0
        assert len(result[0]['detalles']) >= 1
        assert len(result[0]['cbtes_asoc']) == 0
        assert len(result[0]['permisos']) == 0
        assert len(result[0]['opcionales']) == 0

    def test_leer_invalid_line(self, facturas_lines, capfd):
        invalid_input = (''.join(facturas_lines) + "7Invalid line\n").encode(formato_txt.CHARSET)  # Encode the input
        with patch('builtins.open', mock_open(read_data=invalid_input)):
            result = formato_txt.leer("dummy.txt")
        
        out, err = capfd.readouterr()
        assert "Tipo de registro incorrecto: 7" in out
        assert len(result) == 1  # The valid invoice should still be processed

    @pytest.mark.parametrize("encoding", ["utf-8", "iso-8859-1", "ascii"])
    def test_leer_different_encodings(self, facturas_lines, encoding):
        try:
            mock_data = ''.join(facturas_lines).encode(encoding)
        except UnicodeEncodeError:
            pytest.skip(f"Cannot encode test data in {encoding}")
        
        with patch('builtins.open', mock_open(read_data=mock_data)):
            with patch.object(formato_txt, 'CHARSET', encoding):
                result = formato_txt.leer("dummy.txt")
        
        assert len(result) == 1
        assert result[0]['tipo_reg'] == 0

    def test_leer_large_file(self, facturas_lines):
        large_input = (''.join(facturas_lines) * 1000).encode(formato_txt.CHARSET)  # Encode the input
        with patch('builtins.open', mock_open(read_data=large_input)):
            result = formato_txt.leer("large.txt")
        
        assert len(result) == 1000
        for invoice in result:
            assert invoice['tipo_reg'] == 0
            assert len(invoice['detalles']) >= 1

    def test_leer_compatibility_cbt_numero(self, facturas_lines):
        mock_data = ''.join(facturas_lines).encode(formato_txt.CHARSET)  # Encode the input
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = formato_txt.leer("dummy.txt")
        
        assert result[0]['cbt_numero'] == result[0]['cbte_nro']

    def test_leer_all_sections(self, facturas_lines):
        mock_data = ''.join(facturas_lines).encode(formato_txt.CHARSET)  # Encode the input
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = formato_txt.leer("dummy.txt")
        
        assert len(result) == 1
        invoice = result[0]
        assert 'cbtes_asoc' in invoice
        assert 'tributos' in invoice
        assert 'ivas' in invoice
        assert 'permisos' in invoice
        assert 'detalles' in invoice
        assert 'opcionales' in invoice
        assert 'datos' in invoice

    def test_leer_print_dato(self, facturas_lines, capfd):
        mock_data = ''.join(facturas_lines).encode(formato_txt.CHARSET)  # Encode the input
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = formato_txt.leer("dummy.txt")
        
        out, err = capfd.readouterr()
        assert "{'tipo_reg': 9," in out  # Check if dato is printed
