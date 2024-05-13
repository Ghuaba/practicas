from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
#import config.config



db = SQLAlchemy()

#db.create_all()

def create_app():
    app = Flask(__name__, instance_relative_config = False)
    #TODO
    app.config.from_object('config.config.Config')
    db.init_app(app)
    with app.app_context():
        
        from routes.api import api
        from routes.api_usuario import api_usuario
        from routes.api_producto import api_producto
        from routes.api_lote import api_lote


        app.register_blueprint(api_lote)
        

        app.register_blueprint(api_producto)
        app.register_blueprint(api_usuario)
        app.register_blueprint(api)
        #crear tablas db
        db.create_all()

        
    return app
