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
import io
import re
import pytest
import unicodedata
from io import StringIO
import tempfile
from unittest.mock import patch, mock_open
from pyafipws.formatos import formato_txt

def read_facturas_txt():
    """Lee el archivo de facturas de prueba"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    facturas_path = os.path.join(current_dir, 'facturas.txt')
    with open(facturas_path, 'r', encoding='utf-8') as file:
        return file.readlines()

@pytest.mark.dontusefix
class TestLeerLineaTxt:
    """Pruebas para la función leer_linea_txt"""
     
    @pytest.fixture(scope="class")
    def facturas_lines(self):
        """Fixture que proporciona las líneas del archivo de facturas"""
        return read_facturas_txt()
    
    def test_leer_linea_txt_encabezado(self, facturas_lines):
        """Prueba la lectura de una línea de encabezado"""
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
        """Prueba la lectura de una línea de detalle"""
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
        """Prueba la lectura de una línea de IVA"""
        iva_line = next(line for line in facturas_lines if line.startswith('4'))
        result = formato_txt.leer_linea_txt(iva_line, formato_txt.IVA)

        assert result['tipo_reg'] == 4
        assert result['iva_id'] == 5
        assert result['base_imp'] == 100.0
        assert result['importe'] == 21.0

    def test_leer_linea_txt_tributo(self, facturas_lines):
        """Prueba la lectura de una línea de tributo"""
        tributo_line = next(line for line in facturas_lines if line.startswith('5'))
        result = formato_txt.leer_linea_txt(tributo_line, formato_txt.TRIBUTO)

        assert result['tipo_reg'] == 5
        assert result['tributo_id'] == 99
        assert result['desc'] == 'Impuesto Municipal Matanza'
        assert result['base_imp'] == 100.0
        assert result['alic'] == 1.0
        assert result['importe'] == 1.0

    def test_leer_linea_txt_permiso(self, facturas_lines):
        """Prueba la lectura de una línea de permiso"""
        permiso_line = next((line for line in facturas_lines if line.startswith('3')), None)
        if permiso_line:
            result = formato_txt.leer_linea_txt(permiso_line, formato_txt.PERMISO)
            assert result['tipo_reg'] == 3
            assert 'id_permiso' in result
        else:
            pytest.skip("No permiso line found in facturas.txt")

    def test_leer_linea_txt_dato(self, facturas_lines):
        """Prueba la lectura de una línea de dato adicional"""
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
        """Prueba la escritura de una línea de encabezado"""
        encabezado_line = next(line for line in facturas_lines if line.startswith('0'))
        parsed_encabezado = formato_txt.leer_linea_txt(encabezado_line, formato_txt.ENCABEZADO)
        written_line = formato_txt.escribir_linea_txt(parsed_encabezado, formato_txt.ENCABEZADO)
        assert written_line.strip() == encabezado_line.strip()

    def test_escribir_linea_txt_detalle(self, facturas_lines):
        """Prueba la escritura de una línea de detalle"""
        detalle_line = next(line for line in facturas_lines if line.startswith('1'))
        parsed_detalle = formato_txt.leer_linea_txt(detalle_line, formato_txt.DETALLE)
        written_line = formato_txt.escribir_linea_txt(parsed_detalle, formato_txt.DETALLE)
        assert written_line.strip() == detalle_line.strip()

    def test_escribir_linea_txt_iva(self, facturas_lines):
        """Prueba la escritura de una línea de IVA"""
        iva_line = next(line for line in facturas_lines if line.startswith('4'))
        parsed_iva = formato_txt.leer_linea_txt(iva_line, formato_txt.IVA)
        written_line = formato_txt.escribir_linea_txt(parsed_iva, formato_txt.IVA)
        assert written_line.strip() == iva_line.strip()

    def test_escribir_linea_txt_tributo(self, facturas_lines):
        """Prueba la escritura de una línea de tributo"""
        tributo_line = next(line for line in facturas_lines if line.startswith('5'))
        parsed_tributo = formato_txt.leer_linea_txt(tributo_line, formato_txt.TRIBUTO)
        written_line = formato_txt.escribir_linea_txt(parsed_tributo, formato_txt.TRIBUTO)
        assert written_line.strip() == tributo_line.strip()

    def test_escribir_linea_txt_permiso(self, facturas_lines):
        """Prueba la escritura de una línea de permiso"""
        permiso_line = next((line for line in facturas_lines if line.startswith('3')), None)
        if permiso_line:
            parsed_permiso = formato_txt.leer_linea_txt(permiso_line, formato_txt.PERMISO)
            written_line = formato_txt.escribir_linea_txt(parsed_permiso, formato_txt.PERMISO)
            assert written_line.strip() == permiso_line.strip()
        else:
            pytest.skip("No permiso line found in facturas.txt")

    def test_escribir_linea_txt_dato(self, facturas_lines):
        """Prueba la escritura de una línea de dato adicional"""
        dato_line = next((line for line in facturas_lines if line.startswith('9')), None)
        if dato_line:
            parsed_dato = formato_txt.leer_linea_txt(dato_line, formato_txt.DATO)
            written_line = formato_txt.escribir_linea_txt(parsed_dato, formato_txt.DATO)
            assert written_line.strip() == dato_line.strip()
        else:
            pytest.skip("No dato line found in facturas.txt")

    def test_leer_escribir_all_lines(self, facturas_lines):
        """Prueba la lectura y escritura de todas las líneas del archivo"""
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
        """Prueba la lectura de múltiples facturas en un solo archivo"""
        multiple_invoices = (''.join(facturas_lines) * 2).encode(formato_txt.CHARSET)  # Encode the input
        with patch('builtins.open', mock_open(read_data=multiple_invoices)):
            result = formato_txt.leer("dummy.txt")
        
        assert len(result) == 2
        for invoice in result:
            assert invoice['tipo_reg'] == 0
            assert len(invoice['detalles']) >= 1

    def test_leer_missing_sections(self, facturas_lines):
        """Prueba la lectura de un archivo con secciones faltantes"""
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
        """Prueba el manejo de líneas inválidas en el archivo"""
        invalid_input = (''.join(facturas_lines) + "7Invalid line\n").encode(formato_txt.CHARSET)  # Encode the input
        with patch('builtins.open', mock_open(read_data=invalid_input)):
            result = formato_txt.leer("dummy.txt")
        
        out, err = capfd.readouterr()
        assert "Tipo de registro incorrecto: 7" in out
        assert len(result) == 1  # The valid invoice should still be processed

    @pytest.mark.parametrize("encoding", ["utf-8", "iso-8859-1", "ascii"])
    def test_leer_different_encodings(self, facturas_lines, encoding):
        """Prueba la lectura de archivos con diferentes codificaciones"""
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
        """Prueba la lectura de un archivo grande"""
        large_input = (''.join(facturas_lines) * 1000).encode(formato_txt.CHARSET)  # Encode the input
        with patch('builtins.open', mock_open(read_data=large_input)):
            result = formato_txt.leer("large.txt")
        
        assert len(result) == 1000
        for invoice in result:
            assert invoice['tipo_reg'] == 0
            assert len(invoice['detalles']) >= 1

    def test_leer_compatibility_cbt_numero(self, facturas_lines):
        """Prueba la compatibilidad del campo cbt_numero"""
        mock_data = ''.join(facturas_lines).encode(formato_txt.CHARSET)  # Encode the input
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = formato_txt.leer("dummy.txt")
        
        assert result[0]['cbt_numero'] == result[0]['cbte_nro']

    def test_leer_all_sections(self, facturas_lines):
        """Prueba la lectura de todas las secciones de una factura"""
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
        """Prueba la impresión de datos durante la lectura"""
        mock_data = ''.join(facturas_lines).encode(formato_txt.CHARSET)  # Encode the input
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = formato_txt.leer("dummy.txt")
        
        out, err = capfd.readouterr()
        assert "{'tipo_reg': 9," in out  # Check if dato is printed


@pytest.mark.dontusefix
class TestEscribir:
    """Pruebas para la función escribir"""

    @pytest.fixture(scope="class")
    def facturas_lines(self):
        return read_facturas_txt()

    @pytest.fixture
    def sample_regs(self, facturas_lines):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(''.join(facturas_lines))
            temp_file.flush()
            temp_filename = temp_file.name

        try:
            return formato_txt.leer(temp_filename)
        finally:
            os.unlink(temp_filename)


    def test_escribir_basic(self, sample_regs):
        """Prueba básica de escritura de registros"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_filename = temp_file.name

        try:
            formato_txt.escribir(sample_regs, temp_filename)
            
            with open(temp_filename, 'r') as f:
                content = f.read()

            assert "0" in content  # Encabezado
            assert "1" in content  # Detalle
            assert "3" in content  # Permiso
            assert "4" in content  # IVA
            assert "5" in content  # Tributo
            assert "9" in content  # Dato
        finally:
            os.unlink(temp_filename)

    def test_escribir_empty_regs(self):
        """Prueba escribir con una lista vacía de registros"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_filename = temp_file.name

        try:
            formato_txt.escribir([], temp_filename)
            
            with open(temp_filename, 'r') as f:
                content = f.read()

            assert content == ""  # El archivo debería estar vacío
        finally:
            os.unlink(temp_filename)

    def test_escribir_multiple_regs(self, sample_regs):
        """Prueba escribir múltiples registros"""
        multiple_regs = sample_regs * 2
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            formato_txt.escribir(multiple_regs, temp_filename)
            
            with open(temp_filename, 'r') as f:
                content = f.readlines()
            
            # Count the number of lines that start with '0' (header lines)
            header_count = sum(1 for line in content if line.startswith('0'))
            
            assert header_count == 2, f"Expected 2 headers, but found {header_count}"
            
            # Count lines for each type of record
            type_counts = {str(i): sum(1 for line in content if line.startswith(str(i))) for i in range(10)}
            
            print("Line type counts:", type_counts)
            
            # Check that we have the expected number of each type of line
            assert type_counts['0'] == 2, f"Expected 2 header lines (type 0), but found {type_counts['0']}"
            assert type_counts['1'] >= 2, f"Expected at least 2 detail lines (type 1), but found {type_counts['1']}"
            
            # Print out all lines for debugging
            for i, line in enumerate(content):
                print(f"Line {i+1}: {line.strip()}")
            
            # Check total number of lines
            expected_min_lines = sum(len(reg['detalles']) + 1 for reg in multiple_regs)
            assert len(content) >= expected_min_lines, f"Expected at least {expected_min_lines} lines, but found {len(content)}"
        
        finally:
            os.unlink(temp_filename)


    def test_escribir_compatibility_cbt_numero(self, sample_regs):
        """Prueba la compatibilidad del campo cbt_numero"""
        sample_regs[0].pop("cbte_nro", None)
        sample_regs[0]["cbt_numero"] = 9876

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_filename = temp_file.name

        try:
            formato_txt.escribir(sample_regs, temp_filename)
            
            with open(temp_filename, 'r') as f:
                content = f.read()

            assert "9876" in content  # Debería usar cbt_numero en lugar de cbte_nro
        finally:
            os.unlink(temp_filename)

    @patch('pyafipws.formatos.formato_txt.escribir_linea_txt')
    def test_escribir_calls_escribir_linea_txt(self, mock_escribir_linea_txt, sample_regs):
        """Prueba que se llame a escribir_linea_txt para cada sección"""
        with patch('builtins.open', mock_open()) as mock_file:
            formato_txt.escribir(sample_regs, "dummy.txt")

        expected_calls = sum(len(reg.get(section, [])) for reg in sample_regs for section in ['detalles', 'permisos', 'cbtes_asoc', 'ivas', 'tributos', 'opcionales', 'datos']) + len(sample_regs)
        assert mock_escribir_linea_txt.call_count == expected_calls

    def test_escribir_file_permissions(self, sample_regs):
        """Prueba que el archivo se cree con los permisos correctos"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_filename = temp_file.name

        try:
            formato_txt.escribir(sample_regs, temp_filename)
            
            assert os.access(temp_filename, os.R_OK)  # Readable
            assert os.access(temp_filename, os.W_OK)  # Writable
        finally:
            os.unlink(temp_filename)

    def test_escribir_file_already_exists(self, sample_regs):
        """Prueba escribir cuando el archivo ya existe"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_filename = temp_file.name
            temp_file.write("Existing content\n")

        try:
            formato_txt.escribir(sample_regs, temp_filename)
            
            with open(temp_filename, 'r') as f:
                content = f.read()

            assert "Existing content" in content  # El contenido existente debería permanecer
            assert "0" in content  # Y el nuevo contenido debería agregarse
        finally:
            os.unlink(temp_filename)

    def test_escribir_unicode_content(self, sample_regs):
        """Prueba escribir contenido con caracteres Unicode"""
        sample_regs[0]["nombre_cliente"] = "José Martínez"

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_filename = temp_file.name

        try:
            formato_txt.escribir(sample_regs, temp_filename)

            # Read the file in binary mode
            with open(temp_filename, 'rb') as f:
                content = f.read()

            # Try to decode with different encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1']
            decoded_content = None
            used_encoding = None

            for encoding in encodings:
                try:
                    decoded_content = content.decode(encoding)
                    used_encoding = encoding
                    break
                except UnicodeDecodeError:
                    continue

            assert decoded_content is not None, f"Could not decode the file content with any of these encodings: {encodings}"
            
            print(f"File successfully decoded with {used_encoding} encoding")

            assert "José Martínez" in decoded_content, "Unicode content not found in the written file"

            # Additional checks
            lines = decoded_content.split('\n')
            assert any('José Martínez' in line for line in lines), "Unicode content not found in any line"

            # Print content for debugging
            print("File content:")
            print(decoded_content)

        finally:
            os.unlink(temp_filename)


@pytest.mark.dontusefix
class TestAyuda:
    @pytest.fixture(scope="class")
    def facturas_lines(self):
        """Fixture para proporcionar el contenido de facturas.txt"""
        return read_facturas_txt()

    def test_ayuda_output(self, facturas_lines):
        """Prueba que la función ayuda() genera la salida esperada basada en facturas.txt"""
        expected_output = "Formato:\n== Encabezado ==\n"
        
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            formato_txt.ayuda()
            output = fake_output.getvalue()
            assert output.startswith(expected_output)
            
            # Verificar que los campos del encabezado están presentes
            for line in facturas_lines:
                if line.startswith('0'):
                    encabezado = formato_txt.leer_linea_txt(line, formato_txt.ENCABEZADO)
                    for campo in encabezado.keys():
                        assert f"Campo: {campo}" in output

    def test_ayuda_all_tipos_registro(self, facturas_lines):
        """Prueba que todos los tipos de registro en facturas.txt están incluidos en la salida"""
        tipos_registro = set()
        for line in facturas_lines:
            tipos_registro.add(int(line[0]))

        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            formato_txt.ayuda()
            output = fake_output.getvalue()
            
            for tipo in tipos_registro:
                if tipo == 0:
                    assert "== Encabezado ==" in output
                elif tipo == 1:
                    assert "== Detalle Item ==" in output
                elif tipo == 2:
                    assert "== Comprobante Asociado ==" in output
                elif tipo == 3:
                    assert "== Permiso ==" in output
                elif tipo == 4:
                    assert "== Iva ==" in output
                elif tipo == 5:
                    assert "== Tributo ==" in output
                elif tipo == 9:
                    assert "== Datos Adicionales ==" in output

    def test_ayuda_campo_format(self, facturas_lines):
        """Prueba que el formato de cada campo es correcto usando datos de facturas.txt"""
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            formato_txt.ayuda()
            output = fake_output.getvalue()
            lines = output.split('\n')
            
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

                for fmt in formato:
                    campo = fmt[0]
                    campo_line = next((l for l in lines if l.startswith(f" * Campo: {campo}")), None)
                    assert campo_line is not None, f"Campo {campo} no encontrado en la salida de ayuda()"
                    parts = campo_line.split()
                    assert len(parts) >= 9, f"Formato incorrecto para el campo {campo}: {campo_line}"
                    assert parts[0] == "*"
                    assert parts[1] == "Campo:"
                    assert parts[3] == "Posición:"
                    assert parts[5] == "Longitud:"
                    assert "Tipo:" in parts
                    assert "Decimales:" in parts


    def test_ayuda_main(self):
        """Prueba que existe un bloque __main__ que llama a la función ayuda()"""
        with open(formato_txt.__file__, 'r') as file:
            content = file.read()
            assert 'if __name__ == "__main__":' in content
            assert 'ayuda()' in content
    