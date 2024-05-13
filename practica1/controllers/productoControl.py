from models.producto import Producto
from flask import current_app
import uuid
from app import db
import jwt
from datetime import datetime, timedelta

class ProductoControl:

    def listarProductos(self):
        return Producto.query.all()
    

    def saveProducto(self, data):
        producto = Producto()
        producto_existente = Producto.query.filter_by(nombre=data['nombre']).first()
        if producto_existente:
            return -1
        else:
            #fecha_caducidad = datetime.strptime(data['fecha_caducidad'], "%Y-%m-%d")

            producto.nombre=data['nombre']
            #producto.fecha_caducidad=data['fecha_caducidad']
            #producto.cantidad = data['cantidad']
            producto.external_id = uuid.uuid4()
            db.session.add(producto)
            db.session.commit()
            return producto.id
        

     

    def modify(self, external_id, data):
        # Recuperar el censo existente de la base de datos utilizando external_id
        producto = Producto.query.filter_by(external_id = external_id).first()
        
        if producto is None:
            return -4  # Código de error para indicar que no se encontró el censo
        
        # Hacer una copia del censo existente
        new_producto = producto.copy()
        
        producto_existente = Producto.query.filter_by(nombre=data['nombre']).first()
                
        if producto_existente:
            return -1
        else:
            new_producto.nombre=data['nombre']
            new_producto.external_id = uuid.uuid4()
            db.session.merge(new_producto)
            db.session.commit()
            return new_producto.id # Código de error para indicar que la fecha de fin no es posterior a la fecha de inicio