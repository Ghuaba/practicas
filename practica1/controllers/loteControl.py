from models.lote import Lote
from models.producto import Producto
from flask import current_app
import uuid
from app import db
import jwt
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, date
from models.estadoLote import EstadoLote


class LoteControl:

    def listarLote(self):
        self.actualizarEstadoLote()
        return Lote.query.all()
     
    def listarLoteBueno(self):
        # Filtrar los lotes por estadoLote 'CADUCADO'
        self.actualizarEstadoLote()
        lotes_caducados = Lote.query.filter_by(estadoLote=EstadoLote.BUENO).all()
        return lotes_caducados

    def listarLotePorCaducar(self):
        self.actualizarEstadoLote()
        # Filtrar los lotes por estadoLote 'CADUCADO'
        lotes_caducados = Lote.query.filter_by(estadoLote=EstadoLote.PORCADUCAR).all()
        # Devolver la lista de lotes caducados
        return lotes_caducados

    def listarLoteCaducado(self):
        self.actualizarEstadoLote()
        # Filtrar los lotes por estadoLote 'CADUCADO'
        lotes_caducados = Lote.query.filter_by(estadoLote=EstadoLote.CADUCADO).all()
        
        # Devolver la lista de lotes caducados
        return lotes_caducados



#------------------------------------------------------
    def actualizarEstadoLote(self):
        # Obtener la fecha actual
        fecha_actual = date.today()

        # Obtener todos los lotes
        lotes = Lote.query.all()

        for lote in lotes:
            # Convertir lote.fecha_caducidad a un objeto date
            fecha_caducidad = lote.fecha_caducidad.date()

            # Calcular la diferencia de días entre la fecha de caducidad y la fecha actual
            dias_para_caducar = (fecha_caducidad - fecha_actual).days

            if dias_para_caducar == 5:
                lote.estadoLote = EstadoLote.PORCADUCAR
            elif dias_para_caducar <= 0:
                lote.estadoLote = EstadoLote.CADUCADO
        db.session.commit()

#----------------------------------------------------------------

    def saveLote(self, data):
        # Validar si se proporcionan todos los datos necesarios
        if 'codigo' not in data or 'fecha_emision' not in data or 'fecha_caducidad' not in data or 'cantidad' not in data or 'precio' not in data:
            return -2  # Código de error para indicar datos faltantes
        
        # Validar el formato de las fechas
        try:
            fecha_emision = datetime.strptime(data['fecha_emision'], "%Y-%m-%d")
            fecha_caducidad = datetime.strptime(data['fecha_caducidad'], "%Y-%m-%d")
        except ValueError:
            return -3  # Código de error para indicar formato incorrecto de fecha
        
        existing_lote = Lote.query.filter_by(codigo=data['codigo']).first()
        if existing_lote:
            return -4  # Código de error para indicar que el código del lote ya existe
    
        # Crear un nuevo lote y asignar los datos
        lote = Lote()
        lote.codigo = data['codigo']
        lote.fecha_emision = fecha_emision
        lote.fecha_caducidad = fecha_caducidad
        lote.cantidad = data['cantidad']
        lote.precio = data['precio']
        lote.producto_id = data['producto_id']  # Asegúrate de proporcionar un producto_id válido
        
        # Generar un nuevo external_id
        lote.external_id = uuid.uuid4()
        
        # Guardar el lote en la base de datos
        db.session.add(lote)
        db.session.commit()
        
        self.actualizarEstadoLote()

        return lote.id  # Devolver el ID del lote guardado




    def saveProductoLote(self, data):
        # Validar si se proporcionan todos los datos necesarios para el producto
        if 'nombre' not in data:
            return -2  # Código de error para indicar datos faltantes
        
        # Validar si se proporcionan todos los datos necesarios para el lote
        if 'codigo' not in data or 'fecha_emision' not in data or 'fecha_caducidad' not in data or 'cantidad' not in data or 'precio' not in data:
            return -3  # Código de error para indicar datos faltantes
        
        # Validar el formato de las fechas para el lote
        try:
            fecha_emision = datetime.strptime(data['fecha_emision'], "%Y-%m-%d")
            fecha_caducidad = datetime.strptime(data['fecha_caducidad'], "%Y-%m-%d")
        except ValueError:
            return -8  # Código de error para indicar formato incorrecto de fecha
        
        existing_lote = Lote.query.filter_by(codigo=data['codigo']).first()
        if existing_lote:
            return -6  
        
        # Crear un nuevo producto y asignar los datos
        producto = Producto()
        producto_existente = Producto.query.filter_by(nombre=data['nombre']).first()
        if producto_existente:
            return -1  # Código de error para indicar que ya existe un producto con el mismo nombre
        producto.nombre = data['nombre']
        producto.external_id = uuid.uuid4()
        db.session.add(producto)
        db.session.commit()

        # Crear un nuevo lote y asignar los datos
        lote = Lote()
        lote.codigo = data['codigo']
        lote.estadoLote = data.get('estadoLote', 'BUENO')  # Establecer 'BUENO' por defecto si no se proporciona
        lote.fecha_emision = fecha_emision
        lote.fecha_caducidad = fecha_caducidad
        lote.cantidad = data['cantidad']
        lote.precio = data['precio']
        lote.producto_id = producto.id  # Asignar el ID del producto al lote
        # Generar un nuevo external_id para el lote
        lote.external_id = uuid.uuid4()
        # Guardar el producto y el lote en la base de datos
        db.session.add(lote)
        db.session.commit()
        return lote.id  # Devolver los IDs del producto y del lote guardados

    def modify(self, external_id, data):
        # Recuperar el lote existente de la base de datos utilizando external_id
        lote = Lote.query.filter_by(external_id=external_id).first()

        if lote is None:
            return -4  # Código de error para indicar que no se encontró el lote

        # Hacer una copia del lote existente
        new_lote = lote.copy()

        # Asignar los datos del lote existente a la nueva instancia
        new_lote.codigo = lote.codigo
        new_lote.fecha_emision = lote.fecha_emision
        new_lote.fecha_caducidad = lote.fecha_caducidad
        new_lote.cantidad = lote.cantidad
        new_lote.precio = lote.precio
        new_lote.producto_id = lote.producto_id

        # Actualizar los datos del lote con los proporcionados en 'data'
        new_lote.estadoLote = data.get('estadoLote', lote.estadoLote)

        # Utilizar un nuevo external_id para la nueva instancia
        new_lote.external_id = uuid.uuid4()

        # Fusionar los cambios en la base de datos
        db.session.merge(new_lote)
        db.session.commit()

        # Llamar a la función actualizarEstadoLote
        self.actualizarEstadoLote()

        return new_lote.id


    def modifyEstado(self, external_id, data):
        # Recuperar el censo existente de la base de datos utilizando external_id
        lote = Lote.query.filter_by(external_id = external_id).first()
        
        if lote is None:
            return -4  # Código de error para indicar que no se encontró el censo
        
        # Hacer una copia del censo existente
        new_lote = lote.copy()
        
        new_lote.estadoLote = data.get('estadoLote', new_lote.estadoLote)  # Establecer 'BUENO' por defecto si no se proporciona
        new_lote.external_id = uuid.uuid4()
        db.session.merge(new_lote)
        db.session.commit()
        self.actualizarEstadoLote()
        return new_lote.id # Código de error para indicar que la fecha de fin no es posterior a la fecha de inicio
        
        
