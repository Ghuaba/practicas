from flask import Blueprint, jsonify, make_response, request
from controllers.productoControl import ProductoControl
from controllers.utils.errors import Errors
from flask_expects_json import expects_json
#ppppoooool ochoaaaa prueba
from .schemas import schemaProducto
from controllers.authenticate import token_required

api_producto = Blueprint('api_producto', __name__)

productoC = ProductoControl()


@api_producto.route('/producto/listar', methods=["GET"])
@token_required
def listar_productos():
    productoC = ProductoControl()
    return jsonify({"msg": "OK", "code": 200, "datos": [i.serialize for i in productoC.listarProducto()]})


#-----------------------------------------------------------------

@api_producto.route('/producto/guardar', methods = ["POST"])
@token_required
@expects_json(schemaProducto)
def guardar_producto():
    data = request.json  # Supongamos que recibes los datos en formato JSON
    #print(data)

    id = productoC.saveProducto(data)
    print("el id es : " +str(id)) #esto no va solo es para ver errores el trazado
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


@api_producto.route('/producto/modify/<external_id>', methods=["POST"])
@token_required
@expects_json(schemaProducto)
def modify_producto(external_id):
    data = request.json  # Supongamos que recibes los datos en formato JSON
    result = productoC.modify(external_id=external_id, data=data)
    
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



