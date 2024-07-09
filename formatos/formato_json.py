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

"Módulo para manejo de archivos JSON"
from __future__ import print_function

__author__ = "Mariano Reingart (reingart@gmail.com)"
__copyright__ = "Copyright (C) 2011 Mariano Reingart"
__license__ = "LGPL-3.0-or-later"

from decimal import Decimal

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except:
        print("para soporte de JSON debe instalar simplejson")


def leer(archivo):
    "Leer un archivo JSON y devolver una lista de diccionarios"
    try:
        with open(archivo, "r") as jsonfile:
            content = jsonfile.read().strip()
            if not content:
                return []  # Return an empty list if the file is empty or contains only whitespace
            regs = json.loads(content)
            return regs
    except json.decoder.JSONDecodeError as e:
        raise json.decoder.JSONDecodeError("Error al leer archivo JSON: {}".format(str(e)), e.doc, e.pos)
    except FileNotFoundError as e:
        raise FileNotFoundError("Error al leer archivo JSON: {}".format(str(e)))



def escribir(filas, fn="salida.json", **kwargs):
    "Dado una lista de comprobantes (diccionarios), escribe JSON"
    import codecs

    jsonfile = codecs.open(fn, "w")
    json.dump(
        filas,
        jsonfile,
        sort_keys=True,
        indent=4,
        **kwargs
    )
    jsonfile.close()
