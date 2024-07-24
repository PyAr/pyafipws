from pyafipws.wsaa import WSAA
from pyafipws.wsfev1 import WSFEv1


class FacturaElectronicaWrapper:
    def __init__(self):
        self.wsaa = WSAA()
        self.wsfev1 = WSFEv1()

    def autenticar(self, cert, privatekey, wsdl):
        return self.wsaa.Autenticar("wsfe", cert, privatekey, wsdl)

    def conectar(self, wsdl, proxy="", wrapper="", cacert=""):
        return self.wsfev1.Conectar(wsdl, proxy, wrapper, cacert)

    def crear_factura(self, **kwargs):
        return self.wsfev1.CrearFactura(**kwargs)

    def agregar_tributo(self, id, desc, base_imp, alic, importe):
        return self.wsfev1.AgregarTributo(id, desc, base_imp, alic, importe)

    def agregar_iva(self, id, base_imp, importe):
        return self.wsfev1.AgregarIva(id, base_imp, importe)

    def solicitar_cae(self):
        return self.wsfev1.CAESolicitar()

    def comp_ultimo_autorizado(self, tipo_cbte, punto_vta):
        return self.wsfev1.CompUltimoAutorizado(tipo_cbte, punto_vta)
