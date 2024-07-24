from pyafipws.wsaa import WSAA
from pyafipws.wsremcarne import WSRemCarne


class RemitoElectronicoCarnicoWrapper:
    def __init__(self):
        self.wsaa = WSAA()
        self.wsremcarne = WSRemCarne()

    def autenticar(self, cert, privatekey, wsdl):
        return self.wsaa.Autenticar("wsremcarne", cert, privatekey, wsdl)

    def conectar(self, wsdl, proxy="", wrapper="", cacert=""):
        return self.wsremcarne.Conectar(wsdl, proxy, wrapper, cacert)

    def crear_remito(self, **kwargs):
        return self.wsremcarne.CrearRemito(**kwargs)

    def agregar_viaje(self, **kwargs):
        return self.wsremcarne.AgregarViaje(**kwargs)

    def agregar_vehiculo(self, dominio_vehiculo, dominio_acoplado):
        return self.wsremcarne.AgregarVehiculo(
            dominio_vehiculo, dominio_acoplado
            )

    def agregar_mercaderia(self, **kwargs):
        return self.wsremcarne.AgregarMercaderia(**kwargs)

    def generar_remito(self, id_cliente, archivo):
        return self.wsremcarne.GenerarRemito(id_cliente, archivo)

    def consultar_ultimo_remito_emitido(self, tipo_comprobante, punto_emision):
        return self.wsremcarne.ConsultarUltimoRemitoEmitido(
            tipo_comprobante, punto_emision
        )
