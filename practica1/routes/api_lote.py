from flask import Blueprint, jsonify, make_response, request
from controllers.loteControl import LoteControl
from controllers.productoControl import ProductoControl

from controllers.utils.errors import Errors
from flask_expects_json import expects_json
#ppppoooool ochoaaaa prueba
from .schemas import schemaLote,schemaProductoLote, schemaProductoLoteModifyEs,schemaProductoLoteModify
from controllers.authenticate import token_required
from models.lote import Lote

api_lote = Blueprint('api_lote', __name__)

loteC = LoteControl()



@api_lote.route('/lote/listar', methods=["GET"])
@token_required
def listar_lote():
    return jsonify({"msg": "OK", "code": 200, "datos": ([i.serialize for i in loteC.listarLote()])})

@api_lote.route('/lote/listarBueno', methods=["GET"])
@token_required
def listar_loteBueno():
    return jsonify({"msg": "OK", "code": 200, "datos": ([i.serialize for i in loteC.listarLoteBueno()])})

@api_lote.route('/lote/listarPorCaducar', methods=["GET"])
@token_required
def listar_lotePorCaducar():
    return jsonify({"msg": "OK", "code": 200, "datos": ([i.serialize for i in loteC.listarLotePorCaducar()])})

@api_lote.route('/lote/listarCaducado', methods=["GET"])
@token_required
def listar_loteCaducado():
    return jsonify({"msg": "OK", "code": 200, "datos": ([i.serialize for i in loteC.listarLoteCaducado()])})



#-----------------------------------------------------------------
@api_lote.route('/lote/guardar', methods = ["POST"])
@token_required
@expects_json(schemaProductoLote)
def guardar_producto():
    data = request.json  
    id = loteC.saveProductoLote(data)
    if(id >= 0):
        return make_response(
                jsonify({"msg" : "OK", "code" : 200, "datos" : {"tag" : "datos guardados"}}), 
                200
        )
    else:
        return make_response(
                jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Errors.error[str(id)]}}), 
                400
    )


@api_lote.route('/lote/modificarEstado/<external_id>', methods=["POST"])
@token_required
@expects_json(schemaProductoLoteModifyEs)
def modify_loteEstado(external_id):
    data = request.json  # Supongamos que recibes los datos en formato JSON
    result = loteC.modifyEstado(external_id=external_id, data=data)
    
    if result >= 0:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": {"external_id": external_id}}),
            200
        )
    else:
        error_message = Errors.error.get(str(result))
        return make_response(
            jsonify({"msg": "ERROR", "code": 400, "datos": {"error": error_message}}),
            400
    )

@api_lote.route('/lote/modificar/<external_id>', methods=["POST"])
@token_required
@expects_json(schemaProductoLoteModify)
def modify_lote(external_id):
    data = request.json  # Supongamos que recibes los datos en formato JSON
    result = loteC.modify(external_id=external_id, data=data)
    
    if result >= 0:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": {"external_id": external_id}}),
            200
        )
    else:
        error_message = Errors.error.get(str(result))
        return make_response(
            jsonify({"msg": "ERROR", "code": 400, "datos": {"error": error_message}}),
            400
    )