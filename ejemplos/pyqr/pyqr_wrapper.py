from pyqr import PyQR


class PyQRWrapper:
    def __init__(self):
        self.pyqr = PyQR()

    def CrearArchivo(self):
        return self.pyqr.CrearArchivo()

    def GenerarImagen(
        self,
        ver,
        fecha,
        cuit,
        pto_vta,
        tipo_cmp,
        nro_cmp,
        importe,
        moneda,
        ctz,
        tipo_doc_rec,
        nro_doc_rec,
        tipo_cod_aut,
        cod_aut,
    ):
        return self.pyqr.GenerarImagen(
            ver,
            fecha,
            cuit,
            pto_vta,
            tipo_cmp,
            nro_cmp,
            importe,
            moneda,
            ctz,
            tipo_doc_rec,
            nro_doc_rec,
            tipo_cod_aut,
            cod_aut,
        )
