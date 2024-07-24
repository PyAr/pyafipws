from pyi25 import PyI25


class PyI25Wrapper:
    def __init__(self):
        self.pyi25 = PyI25()

    def Version(self):
        return self.pyi25.Version

    def DigitoVerificadorModulo10(self, barras):
        return self.pyi25.DigitoVerificadorModulo10(barras)

    def GenerarImagen(self, barras, archivo, **kwargs):
        return self.pyi25.GenerarImagen(barras, archivo, **kwargs)
