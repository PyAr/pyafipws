#!/usr/bin/python
# -*- coding: utf8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.

"Módulo para manejo de Facturas Electrónicas en tablas DBF (dBase, FoxPro, Clipper et.al.)"
from __future__ import print_function

from builtins import str

__author__ = "Mariano Reingart (reingart@gmail.com)"
__copyright__ = "Copyright (C) 2011 Mariano Reingart"
__license__ = "LGPL-3.0-or-later"

from decimal import Decimal
import os

CODEPAGE = "cp437"

try:
    import dbf
except:
    dbf = None

CHARSET = "latin1"
CODEPAGE = "cp437"
DEBUG = True

if dbf and hasattr(dbf, "encoding"):
    dbf.encoding(CODEPAGE)

# Formato de entrada/salida similar a SIAP RECE, con agregados

# definición del formato del archivo de intercambio:

from .formato_txt import (
    A,
    N,
    I,
    ENCABEZADO,
    DETALLE,
    TRIBUTO,
    IVA,
    CMP_ASOC,
    PERMISO,
    DATO,
)

# agrego identificadores unicos para relacionarlos con el encabezado
DETALLE = [("id", 15, N)] + DETALLE
TRIBUTO = [("id", 15, N)] + TRIBUTO
IVA = [("id", 15, N)] + IVA
CMP_ASOC = [("id", 15, N)] + CMP_ASOC
PERMISO = [("id", 15, N)] + PERMISO
DATO = [("id", 15, N)] + DATO


def definir_campos(formato):
    "Procesar la definición de campos para DBF según el formato txt"
    claves, campos = [], {}
    for fmt in formato:
        clave, longitud, tipo = fmt[0:3]
        if isinstance(longitud, tuple):
            longitud, decimales = longitud
        else:
            decimales = 2
        if longitud > 250:
            tipo = "M"  # memo!
        elif tipo == A:
            tipo = "C(%s)" % longitud  # character
        elif tipo == N:
            tipo = "N(%s,0)" % longitud  # numeric
        elif tipo == I:
            tipo = "N(%s,%s)" % (longitud, decimales)  # "currency"
        else:
            raise RuntimeError(
                "Tipo desconocido: %s %s %s %s" % (tipo, clave, longitud, decimales)
            )
        nombre = dar_nombre_campo(clave)
        campo = "%s %s" % (nombre, tipo)
        campos[clave] = campo
        if nombre not in claves:
            claves.append(nombre)
    return claves, list(campos.values())


CLAVES_ESPECIALES = {
    "Dato_adicional1": "datoadic01",
    "Dato_adicional2": "datoadic02",
    "Dato_adicional3": "datoadic03",
    "Dato_adicional4": "datoadic04",
}


def dar_nombre_campo(clave):
    "Reducir nombre de campo a 10 caracteres, sin espacios ni _, sin repetir"
    nombre = CLAVES_ESPECIALES.get(clave)
    if not nombre:
        nombre = clave.replace("_", "")[:10]
    return nombre.lower()


def leer(archivos=None, carpeta=None):
    "Leer las tablas dbf y devolver una lista de diccionarios con las facturas"
    if DEBUG:
        print("Leyendo DBF...")
    if archivos is None:
        archivos = {}
    regs = {}
    formatos = [
        ("Encabezado", ENCABEZADO, None),
        ("Detalle", DETALLE, "detalles"),
        ("Iva", IVA, "ivas"),
        ("Tributo", TRIBUTO, "tributos"),
        ("Permiso", PERMISO, "permisos"),
        ("Comprobante Asociado", CMP_ASOC, "cbtes_asoc"),
        ("Dato", DATO, "datos"),
    ]
    for nombre, formato, subclave in formatos:
        filename = archivos.get(nombre.lower(), "%s.dbf" % nombre[:8]).strip()
        if not filename:
            continue
        # construir ruta absoluta si se especifica carpeta
        if carpeta is not None:
            filename = os.path.join(carpeta, filename)
        
        # Added check for file existence
        # To handle missing files gracefully and continue processing other files
        if not os.path.exists(filename):
            if DEBUG:
                print(f"Warning: File {filename} not found, skipping.")
            continue

        if DEBUG:
            print("leyendo tabla", nombre, filename)
        tabla = dbf.Table(filename, codepage=CODEPAGE)
        
        # Explicitly open the table
        # To ensure the table is properly opened before reading
        tabla.open()
        
        for record in tabla:
            r = {}
            for fmt in formato:
                clave, longitud, tipo = fmt[0:3]
                nombre_campo = dar_nombre_campo(clave)
                v = record[nombre_campo]
                
                # Added explicit type handling and stripping
                # To ensure consistent data types and remove whitespace
                if isinstance(v, bytes):
                    v = v.decode("utf8", "ignore").strip()
                elif isinstance(v, str):
                    v = v.strip()
                if tipo == N:
                    v = int(v) if v else 0
                elif tipo == I:
                    v = float(v) if v else 0.0
                
                r[clave] = v
            # agrego
            if formato == ENCABEZADO:
                r.update(
                    {
                        "detalles": [],
                        "ivas": [],
                        "tributos": [],
                        "permisos": [],
                        "cbtes_asoc": [],
                        "datos": [],
                    }
                )
                regs[r["id"]] = r
            elif r["id"] in regs:
                regs[r["id"]][subclave].append(r)    
        # Explicitly close the table
        # To ensure proper resource management
        tabla.close()

    return regs


def escribir(regs, archivos=None, carpeta=None):
    "Grabar en talbas dbf la lista de diccionarios con la factura"
    if DEBUG:
        print("Creando DBF...")
        
    # Initialize archivos as an empty dict if it's None
    # To avoid potential NoneType errors
    if archivos is None:
        archivos = {}

    for reg in regs:
        formatos = [
            ("Encabezado", ENCABEZADO, [reg]),
            ("Detalle", DETALLE, reg.get("detalles", [])),
            ("Iva", IVA, reg.get("ivas", [])),
            ("Tributo", TRIBUTO, reg.get("tributos", [])),
            ("Permiso", PERMISO, reg.get("permisos", [])),
            ("Comprobante Asociado", CMP_ASOC, reg.get("cbtes_asoc", [])),
            ("Dato", DATO, reg.get("datos", [])),
        ]
        for nombre, formato, l in formatos:
            claves, campos = definir_campos(formato)
            
            # Special handling for Encabezado filename
            # To maintain consistency with the original implementation
            if nombre == "Encabezado":
                filename = "Encabeza.dbf"
            else:
                filename = archivos.get(nombre.lower(), "%s.dbf" % nombre[:8])
            # construir ruta absoluta si se especifica carpeta
            if carpeta is not None:
                filename = os.path.join(carpeta, filename)
            if DEBUG:
                print("escribiendo tabla", nombre, filename)
            tabla = dbf.Table(filename, campos)
            
            # Explicitly open the table in READ_WRITE mode
            # To ensure proper table access for writing
            tabla.open(dbf.READ_WRITE)
            try:
                for d in l:
                    r = {}
                    for fmt in formato:
                        clave, longitud, tipo = fmt[0:3]
                        if clave == "id":
                            v = reg["id"]
                        else:
                            v = d.get(clave, None)
                        if DEBUG:
                            print(clave, v, tipo)
                        if v is None and tipo == A:
                            v = ""
                        if (v is None or v == "") and tipo in (I, N):
                            v = 0
                        
                        # Explicit type casting
                        # To ensure correct data types are written to the DBF
                        if tipo == N:
                            v = int(v)
                        elif tipo == I: # For import (float) fields, convert to float
                            v = float(v)
                        if tipo == A:
                            if isinstance(v, bytes):
                                # If v is bytes, decode it to a UTF-8 string
                                v = v.decode("utf8", "ignore")
                                # Convert to string and remove leading/trailing whitespace
                            v = str(v).strip()
                        
                        r[dar_nombre_campo(clave)] = v
                    tabla.append(r)
            finally:
                # Ensure table is closed even if an exception occurs
                # To guarantee proper resource management
                tabla.close()


def ayuda():
    "Imprimir ayuda con las tablas DBF y definición de campos"
    print("=== Formato DBF: ===")
    tipos_registro = [
        ("Encabezado", ENCABEZADO),
        ("Detalle Item", DETALLE),
        ("Iva", IVA),
        ("Tributo", TRIBUTO),
        ("Comprobante Asociado", CMP_ASOC),
        ("Permisos", PERMISO),
        ("Datos", DATO),
    ]
    for msg, formato in tipos_registro:
        filename = "%s.dbf" % msg.lower()[:8]
        print("==== %s (%s) ====" % (msg, filename))
        claves, campos = definir_campos(formato)
        for campo in campos:
            print(" * Campo: %s" % (campo,))


if __name__ == "__main__":
    ayuda()
