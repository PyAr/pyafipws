import base64
import sys
from wsaa import WSAA, sign_tra_openssl, sign_tra_new


# KEY='reingart.key'
# CERT='reingart.crt'
# key_and_cert = [KEY,CERT]

import pytest
from unittest.mock import mock_open, patch
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


@pytest.fixture
def test_data():
    tra = b"test_transaction_data"
    cert = b"test_certificate_data"
    privatekey = b"test_privatekey_data"
    passphrase = "test_passphrase"

    return tra, cert, privatekey, passphrase


def test_sign_tra_new(test_data):
    tra, cert, privatekey, passphrase = test_data

    # Mocking file read operations
    with patch("builtins.open", mock_open(read_data=cert)) as mock_cert, \
         patch("builtins.open", mock_open(read_data=privatekey)) as mock_pk, \
         patch.object(serialization, "load_pem_private_key") as mock_load_key, \
         patch("cryptography.x509.load_pem_x509_certificate") as mock_load_cert, \
         patch("cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey.decrypt") as mock_decrypt, \
         patch("cryptography.hazmat.primitives.serialization.Encoding.SMIME") as mock_encoding, \
         patch("cryptography.hazmat.primitives.serialization.pkcs7.PKCS7Options.Binary") as mock_pkcs7_options, \
         patch("email.message_from_string") as mock_message_from_string:

        # Mocking return values for mocked functions
        mock_decrypt.return_value = b"test_decrypted_data"
        mock_load_key.return_value = "test_private_key"
        mock_load_cert.return_value = "test_certificate"
        mock_encoding.return_value = "test_SMIME_encoding"
        mock_pkcs7_options.return_value = "test_PKCS7_options"
        mock_message_from_string.return_value = "test_message"

        result = sign_tra_new(tra, cert, privatekey, passphrase)

        # Asserting the mocked function calls and return values
        mock_cert.assert_called_once_with(cert)
        mock_pk.assert_called_once_with(privatekey)
        mock_load_key.assert_called_once_with(mock_pk.return_value, passphrase.encode(), default_backend())
        mock_load_cert.assert_called_once_with(mock_cert.return_value)
        mock_decrypt.assert_called_once_with(tra, mock_load_key.return_value)
        pkcs7_builder = pkcs7.PKCS7SignatureBuilder()
        pkcs7_builder.set_data.assert_called_once_with(mock_decrypt.return_value)
        pkcs7_builder.add_signer.assert_called_once_with(
            mock_load_cert.return_value, mock_load_key.return_value, hashes.SHA256()
        )
        pkcs7_builder.sign.assert_called_once_with(
            "test_SMIME_encoding", ["test_PKCS7_options"]
        )
        mock_message_from_string.assert_called_once_with(pkcs7_builder.sign.return_value.decode("utf8"))
        assert result == mock_message_from_string.return_value.get_payload.return_value


def test_sign_tra_new_file_read(test_data):
    tra, cert, privatekey, passphrase = test_data

    # Mocking file read operations
    with patch("builtins.open", mock_open(read_data=cert)) as mock_cert, \
         patch("builtins.open", mock_open(read_data=privatekey)) as mock_pk, \
         patch.object(serialization, "load_pem_private_key") as mock_load_key, \
         patch("cryptography.x509.load_pem_x509_certificate") as mock_load_cert, \
         patch("cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey.decrypt") as mock_decrypt, \
         patch("cryptography.hazmat.primitives.serialization.Encoding.SMIME") as mock_encoding, \
         patch("cryptography.hazmat.primitives.serialization.pkcs7.PKCS7Options.Binary") as mock_pkcs7_options, \
         patch("email.message_from_string") as mock_message_from_string:

        # Mocking return values for mocked functions
        mock_decrypt.return_value = b"test_decrypted_data"
        mock_load_key.return_value = "test_private_key"
        mock_load_cert.return_value = "test_certificate"
        mock_encoding.return_value = "test_SMIME_encoding"
        mock_pkcs7_options.return_value = "test_PKCS7_options"
        mock_message_from_string.return_value = "test_message"

        # Calling the function with file paths instead of bytes
        cert_path = "/path/to/cert.pem"
        pk_path = "/path/to/privatekey.pem"
        result = sign_tra_new(tra, cert_path, pk_path, passphrase)

        # Asserting the mocked function calls and return values
        mock_cert.assert_called_once_with(cert_path)
        mock_pk.assert_called_once_with(pk_path)
        mock_load_key.assert_called_once_with(mock_pk.return_value, passphrase.encode(), default_backend())
        mock_load_cert.assert_called_once_with(mock_cert.return_value)
        mock_decrypt.assert_called_once_with(tra, mock_load_key.return_value)
        pkcs7_builder = pkcs7.PKCS7SignatureBuilder()
        pkcs7_builder.set_data.assert_called_once_with(mock_decrypt.return_value)
        pkcs7_builder.add_signer.assert_called_once_with(
            mock_load_cert.return_value, mock_load_key.return_value, hashes.SHA256()
        )
        pkcs7_builder.sign.assert_called_once_with(
            "test_SMIME_encoding", ["test_PKCS7_options"]
        )
        mock_message_from_string.assert_called_once_with(pkcs7_builder.sign.return_value.decode("utf8"))
        assert result == mock_message_from_string.return_value.get_payload.return_value