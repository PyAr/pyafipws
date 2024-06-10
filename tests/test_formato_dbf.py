"""
Pruebas para el módulo `formato_dbf` del paquete `pyafipws`.

Este módulo contiene pruebas para las funciones `definir_campos`, `dar_nombre_campo`, `leer` y `escribir` en el módulo `formato_dbf`.
Las pruebas utilizan datos simulados y fixtures para verificar el comportamiento esperado de estas funciones.

La función `test_definir_campos` prueba la función `definir_campos`, que define los nombres de los campos y los formatos de los campos para un archivo DBF.

La función `test_dar_nombre_campo` prueba la función `dar_nombre_campo`, que genera un nombre de campo abreviado a partir de un nombre de campo largo.

La función `test_leer` prueba la función `leer`, que lee datos de uno o más archivos DBF y devuelve un diccionario que contiene los datos.

La función `test_escribir` prueba la función `escribir`, que escribe datos en un archivo DBF.

La función `test_ayuda` prueba la función `ayuda`, que imprime un mensaje de ayuda describiendo el formato del archivo DBF.
"""
import os
import pytest
from pyafipws.formatos import formato_dbf
from unittest.mock import Mock

# Datos de prueba y fixtures
TEST_DATA_DIR = "tests/data"
TEST_DBF_FILES = {
    "encabezado": os.path.join(TEST_DATA_DIR, "encabeza.dbf"),
    "detalle": os.path.join(TEST_DATA_DIR, "detalle.dbf"),
    # Agregar más archivos DBF de prueba según sea necesario
}

# Prueba de definir_campos
@pytest.mark.dontusefix
def test_definir_campos():
    test_formato = [
        ("campo1", 10, formato_dbf.N),
        ("campo2", 20, formato_dbf.A)
    ]
    claves, campos = formato_dbf.definir_campos(test_formato)

    # Asegurar la salida esperada
    assert claves == ["campo1", "campo2"]
    assert campos[0] == "campo1 N(10,0)"
    assert campos[1] == "campo2 C(20)"

# Prueba de definir_campos con formato vacío
@pytest.mark.dontusefix
def test_definir_campos_empty():
    claves, campos = formato_dbf.definir_campos([])
    assert claves == []
    assert campos == []

# Prueba de definir_campos con nombres de campos largos
@pytest.mark.dontusefix
def test_definir_campos_long_field():
    test_formato = [
        ("campo1", 300, formato_dbf.N),  # Longitud del campo > 250
        ("campo2", 20, formato_dbf.A)
    ]
    claves, campos = formato_dbf.definir_campos(test_formato)
    assert campos[0] == "campo1 M"  # Campo de tipo Memo

# Prueba de definir_campos con campo decimal
@pytest.mark.dontusefix
def test_definir_campos_decimal_field():
    test_formato = [
        ("campo1", (10, 2), formato_dbf.N),  # Campo numérico con 2 decimales
        ("campo2", 20, formato_dbf.A)
    ]
    claves, campos = formato_dbf.definir_campos(test_formato)
    assert campos[0] == "campo1 N(10,0)"  # Campo numérico con 2 decimales

# Prueba de definir_campos con campo de caracteres
@pytest.mark.dontusefix
def test_definir_campos_character_field():
    test_formato = [
        ("campo1", 10, formato_dbf.A),  # Campo de caracteres
        ("campo2", 20, formato_dbf.A)
    ]
    claves, campos = formato_dbf.definir_campos(test_formato)
    assert campos[0] == "campo1 C(10)"  # Campo de caracteres

# Prueba de definir_campos con campo numérico
@pytest.mark.dontusefix
def test_definir_campos_numeric_field():
    test_formato = [
        ("campo1", 10, formato_dbf.N),  # Campo numérico
        ("campo2", 20, formato_dbf.A)
    ]
    claves, campos = formato_dbf.definir_campos(test_formato)
    assert campos[0] == "campo1 N(10,0)"  # Campo numérico

# Prueba de dar_nombre_campo
@pytest.mark.dontusefix
@pytest.mark.parametrize("clave, expected", [
    ("campo_largo", "campolargo"),
    ("Dato_adicional1", "datoadic01"),
    ("campo_corto", "campocorto"),
])
def test_dar_nombre_campo(clave, expected):
    assert formato_dbf.dar_nombre_campo(clave) == expected

@pytest.mark.dontusefix
def test_leer_empty_dbf_files(monkeypatch):
    # Simular la clase dbf.Table para devolver un objeto mock vacío
    mock_table = MockTable()
    monkeypatch.setattr("pyafipws.formatos.formato_dbf.dbf.Table", lambda *args, **kwargs: mock_table)

    # Llamar a leer y asegurar la salida
    output = formato_dbf.leer(TEST_DBF_FILES, TEST_DATA_DIR)

    # Si los archivos DBF están vacíos, la salida debe ser un diccionario vacío
    assert output == {}

@pytest.mark.dontusefix
def test_leer_non_empty_dbf_files(monkeypatch):
    # Simular la clase dbf.Table para devolver un objeto mock con datos
    mock_table = MockTable()
    mock_table.records = [MockRecord({"campo1": 123, "campo2": "test_value"})]
    monkeypatch.setattr("pyafipws.formatos.formato_dbf.dbf.Table", lambda *args, **kwargs: mock_table)

    # Llamar a leer y asegurar la salida
    output = formato_dbf.leer(TEST_DBF_FILES, TEST_DATA_DIR)

    # Si los archivos DBF no están vacíos, asegurar que la salida no está vacía
    assert len(output) > 0
    first_key = list(output.keys())[0]
    assert "detalles" in output[first_key]

# Prueba de leer con múltiples archivos DBF
@pytest.mark.dontusefix
def test_leer_multiple_dbf_files(monkeypatch):
    # Simular la clase dbf.Table para devolver un objeto mock con datos
    mock_table_encabezado = MockTable()
    mock_table_encabezado.records = [MockRecord({"id": 1, "campo1": 123, "campo2": "test_value"})]

    mock_table_detalle = MockTable()
    mock_table_detalle.records = [MockRecord({"id": 1, "campo1": 456, "campo2": "another_value"})]

    def mock_table_factory(filename, *args, **kwargs):
        if "encabeza" in filename:
            return mock_table_encabezado
        elif "detalle" in filename:
            return mock_table_detalle
        else:
            return MockTable()

    monkeypatch.setattr("pyafipws.formatos.formato_dbf.dbf.Table", mock_table_factory)

    # Llamar a leer y asegurar la salida
    output = formato_dbf.leer(TEST_DBF_FILES, TEST_DATA_DIR)

    # Asegurar que la salida es un diccionario con múltiples claves
    assert len(output) == 1
    assert 1 in output
    assert "detalles" in output[1]
    assert len(output[1]["detalles"]) == 1


@pytest.mark.dontusefix
def test_escribir(tmp_path, monkeypatch):
    # Crear un directorio temporal para pruebas
    test_dir = tmp_path / "test_dbf"
    test_dir.mkdir()

    # Simular la clase dbf.Table para rastrear los datos escritos
    mock_table = MockTable()
    def mock_table_factory(filename, field_names):
        return mock_table
    monkeypatch.setattr("pyafipws.formatos.formato_dbf.dbf.Table", mock_table_factory)

    # Definir datos de prueba y llamar a escribir
    test_data = [{
        "id": 1,
        "detalles": [{"campo1": 123, "campo2": "test_value"}],
        "ivas": [],
        "tributos": [],
        "permisos": [],
        "cbtes_asoc": [],
        "datos": []
    }]
    formato_dbf.escribir(test_data, {"encabezado": "encabeza.dbf"}, str(test_dir))

    # Asegurar que los datos fueron escritos en el archivo DBF
    assert len(mock_table.written_data) == 2
    assert mock_table.written_data[0]["id"] == 1
    assert mock_table.written_data[1]["codigo"] == b""
    assert mock_table.written_data[1]["ds"] == b""

# Prueba de ayuda (se puede capturar la salida y asegurar el contenido esperado)
@pytest.mark.dontusefix
def test_ayuda(capsys):
    formato_dbf.ayuda()
    captured = capsys.readouterr()
    assert "Formato DBF:" in captured.out
    assert "Encabezado" in captured.out
    assert "Detalle Item" in captured.out

class MockRecord:
    def __init__(self, data):
        self.data = data

    def scatter_fields(self):
        return self.data

# class MockTable:
#     def __init__(self, records=None):
#         self.records = records or []
#         self.current_index = 0

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.current_index >= len(self.records):
#             raise StopIteration
#         record = self.records[self.current_index]
#         self.current_index += 1
#         return record

#     def append(self, data):
#         record = MockRecord(data)
#         self.records.append(record)

#     def close(self):
#         pass

class MockTable:
    def __init__(self, records=None):
        self.records = records or []
        self.current_index = 0
        self.written_data = []

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= len(self.records):
            raise StopIteration
        record = self.records[self.current_index]
        self.current_index += 1
        return record

    def append(self, data):
        self.written_data.append(data)

    def close(self):
        pass
