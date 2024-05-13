from flask import Blueprint, jsonify, make_response, request
from controllers.usuarioControl import UsuarioControl
from controllers.utils.errors import Errors
from flask_expects_json import expects_json
#ppppoooool ochoaaaa prueba
from .schemas import schemaUsuario,schema_sesion
from controllers.authenticate import token_required

api_usuario = Blueprint('api_usuario', __name__)

usuarioC = UsuarioControl()


@api_usuario.route('/usuario/listar', methods=["GET"])
@token_required
def listar_usuarios():
    usuarioC = UsuarioControl()  # Instancia de la clase UsuarioControl
    return jsonify({"msg": "OK", "code": 200, "datos": [i.serialize for i in usuarioC.listarUsuarios()]})


#-----------------------------------------------------------------
@api_usuario.route('/usuario/guardar', methods = ["POST"])
@expects_json(schemaUsuario)
def guardar_usuario():
    data = request.json  # Supongamos que recibes los datos en formato JSON
    #print(data)

    id = usuarioC.saveUsuario(data)
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
        
        
@api_usuario.route('/sesion', methods = ["POST"])
@expects_json(schema_sesion)
def sesion():
    data = request.json  # Supongamos que recibes los datos en formato JSON
    id = usuarioC.login(data)
    if type(id) == int:
        return make_response(
                jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Errors.error[str(id)]}}), 
                400
        )
    else:
        return make_response(
                jsonify({"msg" : "OK", "code" : 200, "datos" : id}), 
                200
    )