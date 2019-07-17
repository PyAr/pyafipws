import os

UNO = os.environ['UNO']
DOS = os.environ['DOS']
CERT = os.environ['CERT']
CERT = CERT.replace(r'\n', '\n')
PKEY = os.environ['PKEY']
PKEY = PKEY.replace(r'\n', '\n')

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


def test_environ_key(pkey=PKEY):
    assert pkey == ('-----BEGIN RSA PRIVATE KEY-----'
    '\nMIIEpQIBAAKCAQEA3Mc/IZ8X3x8YhIa0SQ89VjSOhEdYcJnffa5QqAtqISQ3Di38'
    '\n2B4XOHDRg3CDzt/jck3fKEV7K/wfgS33KDAv2EWW2mTJaJZHlLSY05CtaesHpxlB'
    '\nCYlzTc7z0aABOx+e9S1R80R5LZ1a+kzEcgODeHi4PKu0Z1qHvkotrZ9FEx2kl3bw'
    '\ndX4LjyxCKdeqL4tY1OOkpNq6sT5geGBsHn8yQNVz7iP2OUYO7Acs3so7GLLrZtb/'
    '\nzWx1xyWB5PVs8DGY2iK22H5k2jnvas9gzntshvRG6c+/skWOG7vtFp2qL7TvAath'
    '\nE5YQEp/2T1iLcgxrqtUV2K7LHifvJghKxgN15QIDAQABAoIBAFLwVvsedS1Q1TkU'
    '\nEa5Ql05HODLhSowigh8I2SwH/bqtjDE7fX0C8N43I74pCpsw6JUMRAUw9PC1KnCw'
    '\n/+SNFaw9mEo7Cp7LteBbZ/4yn7LmpF1V02Ttye81C8t4PH4lhuW8PMkStCM6te7J'
    '\n4BKk10Lutuez6XXaQJxv6XEMIDrpeUC34huyLEeld7SekoO2YvBHEob24O8ZD7oD'
    '\nti1m6GFHDCRzose9dJ63CmFQExsToOYDBpqrFvhZ3tc//bEvMiIxIb91KPFk//L5'
    '\n+QnuDMuvuJMAU4A7Xmool9yiz7/WsFxQceQC0OPmj+btc+BK54+LhQo+pXwy5Zb4'
    '\nmCND1BECgYEA8hbfQwY4rvcjdKfJzU8ypPDgTK2kSmEZS2jQhKl2W+6a8Amc20CC'
    '\nS1qMXKTEFccpZjJxvR3nywcQZ1n5atVUAeHP3VEhmNkLpOYDD2WEsjgfmDYWbuo4'
    '\n4fRENAa7PPJzv1EnBxzMFZowUGKMfGYP/0jhtAhTkBAfpKQO45QKrasCgYEA6Xbj'
    '\nwwZ/TMUaJ0iswQcEk2EkoTreWPWT8A2nnBSczcBUPvrIKd5EnOLBImi/hJLO+sTN'
    '\n8RBpEwcc+RdUId6BjaOQ/TVv7NX86DyS9lL4kjHrOQJoL0s+OQ17nI8BCNmIY9tD'
    '\n8Zq8818ctyDwjC36wt5yG4E1rPzkdij8XYwaOq8CgYEAzj5QHJC7T8w6h5K+qMvV'
    '\nEJIp9Qll0vwgCY+VPcAFltKTavY1jNDLcBkHRZIVf5w6F9fX8E7+/4fYIMSVab+u'
    '\nnx/a7+jDn60hb22Jo99QCmkn+Yvy1rFynoV0aYJml8jSdWZUwol1EN5YVNNwbjah'
    '\nYFKd/rutPSmPW7ts99NSuZsCgYEAldiJN5PkARJBRxWOTBaFCVNAf3uZWt/EpD8f'
    '\nZT6Vpjnb2NB9yOGwiEHCVKOGyUCxOKM4y5EM3/mgzv/6MALwhEiHtv2laQ2v1h+K'
    '\n9C8s/CiuIVk6JaDVvyi4PjRLJbL5p54Ebf4zaMGTXLb3rgGVAZ5k/uJf4TgwKucD'
    '\nk8dozmECgYEAtoKnCF8cQaJGKgr2bJt3JQb2gn2xO+tNW7LQStKBSpzYY8S1AuYB'
    '\nJNrYl5eGXfT22zOsETPlO/xy2d6l4+9h7g3sn21FSVC0Ivgf6Utq40aI1rG5BbF6'
    '\nkFjXA2mIhgAUpIZYDdu7tQq8ysN/odAOANtBz8f3MbPzRuCn26/Xm0Y='
    '\n-----END RSA PRIVATE KEY-----')
