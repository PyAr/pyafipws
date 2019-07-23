import os

"""Tests de prueba de existencia de archivos"""


def test_certs_files():
    assert os.path.exists('rei.crt')
    assert os.path.exists('rei.key')
