import os

UNO = os.environ['UNO']
DOS = os.environ['DOS']

def test_environ(UNO=UNO, DOS=DOS):
    assert int(UNO) == 1
    assert int(DOS) == 2
