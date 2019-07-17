import os

UNO = os.environ['UNO']
DOS = os.environ['DOS']
CERT = os.environ['CERT']
CERT = CERT.replace(r'\n', '\n')
# PKEY = os.environ['PKEY']

print(CERT)

def test_environ(UNO=UNO, DOS=DOS):
    assert int(UNO) == 1
    assert int(DOS) == 2


def test_environ_crt(cert=CERT):
    assert cert == ('-----BEGIN CERTIFICATE-----'
    '\nMIIDTzCCAjegAwIBAgIIPo2ARJ07t6gwDQYJKoZIhvcNAQENBQAwODEaMBgGA1UEAwwRQ29tcHV0'
    '\nYWRvcmVzIFRlc3QxDTALBgNVBAoMBEFGSVAxCzAJBgNVBAYTAkFSMB4XDTE5MDcxMzE2MzgzMFoX'
    '\nDTIxMDcxMjE2MzgzMFowNTEYMBYGA1UEAwwPcmVpbmdhcnRwdWIyMDE5MRkwFwYDVQQFExBDVUlU'
    '\nIDIwMjY3NTY1MzkzMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3Mc/IZ8X3x8YhIa0'
    '\nSQ89VjSOhEdYcJnffa5QqAtqISQ3Di382B4XOHDRg3CDzt/jck3fKEV7K/wfgS33KDAv2EWW2mTJ'
    '\naJZHlLSY05CtaesHpxlBCYlzTc7z0aABOx+e9S1R80R5LZ1a+kzEcgODeHi4PKu0Z1qHvkotrZ9F'
    '\nEx2kl3bwdX4LjyxCKdeqL4tY1OOkpNq6sT5geGBsHn8yQNVz7iP2OUYO7Acs3so7GLLrZtb/zWx1'
    '\nxyWB5PVs8DGY2iK22H5k2jnvas9gzntshvRG6c+/skWOG7vtFp2qL7TvAathE5YQEp/2T1iLcgxr'
    '\nqtUV2K7LHifvJghKxgN15QIDAQABo2AwXjAMBgNVHRMBAf8EAjAAMB8GA1UdIwQYMBaAFLOy0//9'
    '\n6bre3o2vESGc1iB98k9vMB0GA1UdDgQWBBSNWsHTyranSfK1GGDUOLjPYe3Z6TAOBgNVHQ8BAf8E'
    '\nBAMCBeAwDQYJKoZIhvcNAQENBQADggEBAI/EVxvWCMawF0y1KNFanHR1IVTavQfRgloEmaoljOIS'
    '\navrwPDQ1V8iUOpAM5PLE5ES5kzCAkuvmV/98r1XwnlcldPvYdm+l3zJUuwqwb1lU3vXlBC9gNlo9'
    '\nFathfp8FlBzL5la9eH60dEhLeur+EPRN2wu/c+bFlyLBlwDxFHULnY+6Dvu9k2tiws/P8grjrDHI'
    '\npf4gp1LsEwa19YgX8W/DAUv5Z1Y5wvc8L5K6NTYSz/AZT7CkhDnHItQIKGpBZFXV2mvxBC1Evgst'
    '\n9OVrAFqYbfcp5iINH03iG6SHzXnGG2JwzVSfoBEngZ1eieEGTGF9IpPNK2jaZRsGo2/sOGs='
    '\n-----END CERTIFICATE-----')