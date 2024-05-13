from flask import Blueprint, jsonify, make_response, current_app, request
from flask_sqlalchemy import SQLAlchemy
import uuid
import jwt
from controllers.utils.errors import Errors
from datetime import datetime, timedelta
from functools import wraps
from models.usuario import Usuario

#los token solo viajan por la cabece, sin post ni data
#estamos haci8edo un componente, que es los arrobas @override etc
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Access-Token')
        if not token:
            return make_response(
                jsonify({"msg": "ERROR", "code": 401, "datos": {"error": Errors.error[str(-14)]}}),
                401
            )
        try:
            data = jwt.decode(token, algorithms=["HS512"], key=current_app.config['SECRET_KEY'], verify=True)
            user = Usuario.query.filter_by(external_id=data["external"]).first()
            if not user:
                return make_response(
                    jsonify({"msg": "ERROR", "code": 401, "datos": {"error": Errors.error[str(-13)]}}),
                    401
                )
        except jwt.ExpiredSignatureError:
            return make_response(
                jsonify({"msg": "ERROR", "code": 401, "datos": {"error": Errors.error[str(-15)]}}),
                401
            )
        except jwt.InvalidTokenError:
            return make_response(
                jsonify({"msg": "ERROR", "code": 401, "datos": {"error": Errors.error[str(-15)]}}),
                401
            )
        return f(*args, **kwargs)
    return decorated



