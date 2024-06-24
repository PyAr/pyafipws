import pytest
import os
import tempfile
import dbf
from pyafipws.formatos import formato_dbf
import time
import shutil

@pytest.fixture(scope="module")
def temp_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after tests
    for attempt in range(5):  # Try up to 5 times
        try:
            time.sleep(0.5)  # Add a small delay
            shutil.rmtree(temp_dir, ignore_errors=True)
            break
        except OSError:
            if attempt == 4:  # Last attempt
                raise
            time.sleep(0.5)  # Wait for 0.5 seconds before retrying


@pytest.fixture(scope="module")
def sample_dbf_files(temp_dir):
    # Create Encabezado.dbf
    encabezado_def = formato_dbf.definir_campos(formato_dbf.ENCABEZADO)[1]
    encabezado_table = dbf.Table(os.path.join(temp_dir, 'Encabeza.dbf'), encabezado_def)
    encabezado_table.open(mode=dbf.READ_WRITE)
    encabezado_table.append({
        'tiporeg': 0,
        'webservice': 'wsfev1',
        'fechacbte': '20230601',
        'tipocbte': 1,
        'puntovta': 4000,
        'cbtenro': 12345,
        'tipoexpo': 1,
        'permisoexi': 'S',
        'paisdstcmp': 203,
        'nombreclie': 'Test Client',
        'tipodoc': 80,
        'nrodoc': '30500010912',
        'domicilioc': 'Test Address 123',
        'idimpositi': 'PJ12345678',
        'imptotal': 1000.00,
        'imptotconc': 0.00,
        'impneto': 826.45,
        'imptoliq': 173.55,
        'imptoliqnr': 0.00,
        'impopex': 0.00,
        'imptoperc': 0.00,
        'impiibb': 0.00,
        'imptopercm': 0.00,
        'impinterno': 0.00,
        'imptrib': 0.00,
        'monedaid': 'PES',
        'monedactz': 1.000000,
        'formapago': 'Contado',
        'cae': '12345678901234',
        'fechavto': '20230611',
        'resultado': 'A',
        'reproceso': 'N',
        'id': 1,
    })
    encabezado_table.close()

    # Create Detalle.dbf
    detalle_def = formato_dbf.definir_campos(formato_dbf.DETALLE)[1]
    detalle_table = dbf.Table(os.path.join(temp_dir, 'Detalle.dbf'), detalle_def)
    detalle_table.open(mode=dbf.READ_WRITE)
    detalle_table.append({
        'tiporeg': 1,
        'codigo': 'PROD001',
        'qty': 1.00,
        'umed': 7,
        'precio': 826.45,
        'importe': 826.45,
        'ivaid': 5,
        'ds': 'Test Product',
        'ncm': '',
        'sec': '',
        'bonif': 0.00,
        'impiva': 173.55,
        'despacho': '',
        'id': 1,
    })
    detalle_table.close()

    # Create IVA.dbf
    iva_def = formato_dbf.definir_campos(formato_dbf.IVA)[1]
    iva_table = dbf.Table(os.path.join(temp_dir, 'Iva.dbf'), iva_def)
    iva_table.open(mode=dbf.READ_WRITE)
    iva_table.append({
        'tiporeg': 4,
        'ivaid': 5,
        'baseimp': 826.45,
        'importe': 173.55,
        'id': 1,
    })
    iva_table.close()

    # Create empty Tributo.dbf, Permiso.dbf, CmpAsoc.dbf, and Dato.dbf
    for name, format_def in [
        ('Tributo.dbf', formato_dbf.TRIBUTO),
        ('Permiso.dbf', formato_dbf.PERMISO),
        ('CmpAsoc.dbf', formato_dbf.CMP_ASOC),
        ('Dato.dbf', formato_dbf.DATO),
    ]:
        table_def = formato_dbf.definir_campos(format_def)[1]
        table = dbf.Table(os.path.join(temp_dir, name), table_def)
        table.open(mode=dbf.READ_WRITE)
        table.close()

    return temp_dir



@pytest.mark.dontusefix
class TestDefinirCampos:
    def test_definir_campos(self):
        # Test that definir_campos returns valid lists for a non-empty format
        claves, campos = formato_dbf.definir_campos(formato_dbf.ENCABEZADO)
        assert isinstance(claves, list)
        assert isinstance(campos, list)
        assert len(claves) > 0
        assert len(campos) > 0
        assert len(claves) == len(campos)

    def test_definir_campos_empty_format(self):
        # Test that definir_campos handles empty format correctly
        claves, campos = formato_dbf.definir_campos([])
        assert len(claves) == 0
        assert len(campos) == 0
   
@pytest.mark.dontusefix
class TestDarNombreCampo:
    def test_dar_nombre_campo(self):
        # Test normal cases for dar_nombre_campo
        assert formato_dbf.dar_nombre_campo('tipo_cbte') == 'tipocbte'
        assert formato_dbf.dar_nombre_campo('punto_vta') == 'puntovta'
        assert formato_dbf.dar_nombre_campo('Dato_adicional1') == 'datoadic01'
       
    def test_dar_nombre_campo_edge_cases(self):
        # Test edge cases for dar_nombre_campo
        assert formato_dbf.dar_nombre_campo('') == ''
        assert formato_dbf.dar_nombre_campo('a' * 20) == 'a' * 10
        assert formato_dbf.dar_nombre_campo('123_abc') == '123abc'

@pytest.mark.dontusefix
class TestLeer:
    def test_leer(self, sample_dbf_files):
        # Test reading from sample DBF files
        regs = formato_dbf.leer(carpeta=sample_dbf_files)
        assert isinstance(regs, dict)
        assert len(regs) == 1  # We created one record in Encabeza.dbf

        reg = regs[1]  # Get the record with id=1
        # Verify various fields in the main record
        assert reg['tipo_cbte'] == 1
        assert reg['punto_vta'] == 4000
        assert reg['cbte_nro'] == 12345
        assert reg['nombre_cliente'] == 'Test Client'
        assert reg['imp_total'] == 1000.00
        assert reg['moneda_id'] == 'PES'
        assert reg['cae'] == '12345678901234'

        # Verify details
        assert 'detalles' in reg
        assert len(reg['detalles']) == 1
        detalle = reg['detalles'][0]
        assert detalle['codigo'] == 'PROD001'
        assert detalle['ds'] == 'Test Product'
        assert detalle['qty'] == 1.00
        assert detalle['precio'] == 826.45
        assert detalle['imp_iva'] == 173.55

        # Verify IVA
        assert 'ivas' in reg
        assert len(reg['ivas']) == 1
        iva = reg['ivas'][0]
        assert iva['iva_id'] == 5
        assert iva['base_imp'] == 826.45
        assert iva['importe'] == 173.55

    def test_leer_missing_files(self, temp_dir):
        # Test reading when some files are missing
        # Create only one file
        encabezado_def = formato_dbf.definir_campos(formato_dbf.ENCABEZADO)[1]
        encabezado_table = dbf.Table(os.path.join(temp_dir, 'Encabeza.dbf'), encabezado_def)
        encabezado_table.open(mode=dbf.READ_WRITE)
        encabezado_table.append({
            'tiporeg': 0,
            'id': 1,
            'tipocbte': 1,
            'puntovta': 4000,
            'cbtenro': 12345,
            'nombreclie': 'Test Client',
        })
        encabezado_table.close()

        regs = formato_dbf.leer(carpeta=temp_dir)
        assert len(regs) == 1

    def test_leer_empty_files(self, temp_dir):
        # Test reading from empty DBF files
        # Create empty files
        for name, format_def in [
            ('Encabeza.dbf', formato_dbf.ENCABEZADO),
            ('Detalle.dbf', formato_dbf.DETALLE),
            ('Iva.dbf', formato_dbf.IVA),
        ]:
            table_def = formato_dbf.definir_campos(format_def)[1]
            table = dbf.Table(os.path.join(temp_dir, name), table_def)
            table.open(mode=dbf.READ_WRITE)
            table.close()

        regs = formato_dbf.leer(carpeta=temp_dir)
        assert len(regs) == 0

@pytest.mark.dontusefix
class TestEscribir:
    def test_escribir(self, temp_dir):
        # Test writing a single record
        test_data = {
            'id': 2,
            'tipo_cbte': 2,
            'punto_vta': 5000,
            'cbt_desde': 67890,
            'cbt_hasta': 67890,
            'fecha_cbte': '20230602',
            'tipo_doc': 80,
            'nro_doc': '30600010912',
            'nombre_cliente': 'Test Client 2',
            'imp_total': 2000.00,
            'imp_tot_conc': 0.00,
            'imp_neto': 1652.90,
            'imp_iva': 347.10,
            'imp_trib': 0.00,
            'moneda_id': 'PES',
            'moneda_ctz': 1.000,
            'webservice': 'wsfev1',
            'detalles': [{
                'id': 2,
                'tipo_cbte': 2,
                'punto_vta': 5000,
                'cbt_desde': 67890,
                'cbt_hasta': 67890,
                'fecha_cbte': '20230602',
                'codigo': 'PROD002',
                'ds': 'Test Product 2',
                'qty': 2,
                'umed': 7,
                'precio': 826.45,
                'importe': 1652.90,
                'iva_id': 5,
                'imp_iva': 347.10,
            }]
        }

        formato_dbf.escribir([test_data], carpeta=temp_dir)

        # Verify that the files were created and contain the correct data
        encabezado_table = dbf.Table(os.path.join(temp_dir, 'Encabeza.dbf'))
        encabezado_table.open()
        record = encabezado_table[-1]  # Get the last record
        assert record.id == 2
        assert record.tipocbte == 2
        assert record.puntovta == 5000
        assert record.nombreclie.strip() == 'Test Client 2'
        encabezado_table.close()

        detalle_table = dbf.Table(os.path.join(temp_dir, 'Detalle.dbf'))
        detalle_table.open()
        record = detalle_table[-1]  # Get the last record
        assert record.id == 2
        assert record.codigo.strip() == 'PROD002'
        assert record.ds.strip() == 'Test Product 2'
        assert record.qty == 2
        detalle_table.close()
   
    def test_escribir_multiple_records(self, temp_dir):
        # Test writing multiple records
        test_data = [
            {
                'id': 2,
                'tipo_cbte': 2,
                'punto_vta': 5000,
                'nombre_cliente': 'Test Client 2',
                'imp_total': 2000.00,
                'detalles': [{
                    'id': 2,
                    'codigo': 'PROD002',
                    'ds': 'Test Product 2',
                    'qty': 2,
                }]
            },
            {
                'id': 3,
                'tipo_cbte': 3,
                'punto_vta': 6000,
                'nombre_cliente': 'Test Client 3',
                'imp_total': 3000.00,
                'detalles': [{
                    'id': 3,
                    'codigo': 'PROD003',
                    'ds': 'Test Product 3',
                    'qty': 3,
                }]
            }
        ]

        formato_dbf.escribir(test_data, carpeta=temp_dir)

        # Verify the content of the written files
        encabezado_table = dbf.Table(os.path.join(temp_dir, 'Encabeza.dbf'))
        encabezado_table.open()
        assert len(encabezado_table) == 1
        assert encabezado_table[-1].id == 3
        assert encabezado_table[-1].tipocbte == 3
        assert encabezado_table[-1].puntovta == 6000
        encabezado_table.close()

        detalle_table = dbf.Table(os.path.join(temp_dir, 'Detalle.dbf'))
        detalle_table.open()
        assert len(detalle_table) == 1
        assert detalle_table[-1].id == 3
        assert detalle_table[-1].codigo.strip() == 'PROD003'
        assert detalle_table[-1].qty == 3
        detalle_table.close()

    def test_escribir_edge_cases(self, temp_dir):
        # Test writing edge cases (max lengths, small/large values)
        test_data = {
            'id': 4,
            'tipo_cbte': 4,
            'punto_vta': 7000,
            'nombre_cliente': 'A' * 200,  # Test max length
            'imp_total': 0.01,  # Test small amount
            'detalles': [{
                'id': 4,
                'codigo': 'P' * 30,  # Test max length
                'ds': 'D' * 4000,  # Test max length
                'qty': 9999999.99,  # Test large quantity
            }]
        }

        formato_dbf.escribir([test_data], carpeta=temp_dir)

        # Verify the content of the written files
        encabezado_table = dbf.Table(os.path.join(temp_dir, 'Encabeza.dbf'))
        encabezado_table.open()
        record = encabezado_table[-1]
        assert record.id == 4
        assert record.nombreclie.strip() == 'A' * 200
        assert record.imptotal == 0.01
        encabezado_table.close()

        detalle_table = dbf.Table(os.path.join(temp_dir, 'Detalle.dbf'))
        detalle_table.open()
        record = detalle_table[-1]
        assert record.id == 4
        assert record.codigo.strip() == 'P' * 30
        assert record.ds.strip() == 'D' * 4000
        assert record.qty == 9999999.99
        detalle_table.close()
   
@pytest.mark.dontusefix
class TestAyuda:
    def test_ayuda(self, capsys):
        # Test that ayuda() function outputs expected information
        formato_dbf.ayuda()
        captured = capsys.readouterr()
        assert "=== Formato DBF: ===" in captured.out
        assert "Encabezado (encabeza.dbf)" in captured.out
        assert "Detalle Item (detalle .dbf)" in captured.out  # Note the space before .dbf
 
    def test_ayuda_output_structure(self, capsys):
        # Test the structure of ayuda() output
        formato_dbf.ayuda()
        captured = capsys.readouterr()
        output_lines = captured.out.split('\n')
       
        # Check that each table type is mentioned
        table_types = ['Encabezado', 'Detalle', 'Iva', 'Tributo', 'Permiso', 'Comprobante Asociado', 'Dato']
        for table_type in table_types:
            assert any(table_type in line for line in output_lines)
       
        # Check that some basic information is provided
        assert any('=== Formato DBF: ===' in line for line in output_lines)
        assert len(output_lines) > len(table_types)  # Ensure there's more output than just table names

@pytest.mark.dontusefix
class TestIntegration:
    def test_write_and_read(self, temp_dir):
        # Integration test: Write data, then read it back and verify
        # Write data
        test_data = {
            'id': 5,
            'tipo_cbte': 5,
            'punto_vta': 8000,
            'nombre_cliente': 'Integration Test Client',
            'imp_total': 5000.00,
            'detalles': [{
                'id': 5,
                'codigo': 'INT001',
                'ds': 'Integration Product',
                'qty': 5,
            }],
            'ivas': [{
                'id': 5,
                'iva_id': 5,
                'base_imp': 4132.23,
                'importe': 867.77,
            }]
        }
        formato_dbf.escribir([test_data], carpeta=temp_dir)

        # Read data
        regs = formato_dbf.leer(carpeta=temp_dir)

        # Verify
        assert len(regs) == 1
        reg = regs[5]
        assert reg['tipo_cbte'] == 5
        assert reg['punto_vta'] == 8000
        assert reg['nombre_cliente'] == 'Integration Test Client'
        assert reg['imp_total'] == 5000.00
        assert len(reg['detalles']) == 1
        assert reg['detalles'][0]['codigo'] == 'INT001'
        assert len(reg['ivas']) == 1
        assert reg['ivas'][0]['iva_id'] == 5
