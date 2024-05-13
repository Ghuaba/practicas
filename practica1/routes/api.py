from flask import Blueprint, jsonify, make_response, request

'''
from models.usuario import Usuario
from models.producto import Producto
from models.lote import Lote
from models.factura import Factura
from models.detalle_factura import DetalleFactura
'''
api = Blueprint('api', __name__)

@api.route('/')
def home():
    return make_response(
        jsonify({"msg" : "OK", "code" : 200, 'jaja' : "Lizyta tilina"}), 
        200
    )

#esto es sin post
@api.route('/suma/<a>/<b>')
def suma(a, b):
    c = float(a) + float(b)
    return make_response(
        jsonify({"msg" : "OK", "code" : 200, "data":{"suma es: ": c}}), 
        200
    )
