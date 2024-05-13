schemaUsuario = {
    'type' : 'object',
    'propierties' : {
        'username': {'type' : 'string'},
        'clave': {'type' : 'string'}
    },
    'required' : ['username','clave']
}

#++++++++++++++++++++++++++++++++++++++++++++++++++

schemaProducto = {
    'type' : 'object',
    'propierties' : {
        'nombre': {'type' : 'string'}
    },
    'required' : ['nombre']
}
#++++++++++++++++++++++++++++++++++++++++++++++++++


schemaLote = {
    'type': 'object',
    'properties': {
        'codigo': {'type': 'string'},
        'fecha_emision': {"type": "string", "format": "date-time"},
        'fecha_caducidad': {"type": "string", "format": "date-time"},
        'cantidad': {'type': 'integer'},  # Cambiado a tipo 'integer' si representa una cantidad entera
        'precio': {'type': 'number'},  # Cambiado a tipo 'number' para permitir valores decimales
        'producto_id' : {'type' : 'integer'}
    },
    'required': ['codigo', 'fecha_emision', 'fecha_caducidad', 'cantidad', 'precio', 'producto_id']
}

schemaProductoLote = {
    'type': 'object',
    'properties': {
        'nombre': {'type': 'string'},
        'estadoProducto': {'type': 'string'},  # Campo opcional
        'codigo': {'type': 'string'},
        'fecha_emision': {'type': 'string', 'format': 'date-time'},
        'fecha_caducidad': {'type': 'string', 'format': 'date-time'},
        'cantidad': {'type': 'integer'},
        'precio': {'type': 'number'}
    },
    'required': ['nombre', 'codigo', 'fecha_emision', 'fecha_caducidad', 'cantidad', 'precio']
}

schemaProductoLoteModify = {
    'type': 'object',
    'properties': {
        'estadoProducto': {'type': 'string'},  # Campo opcional
        'codigo': {'type': 'string'},
        'fecha_emision': {'type': 'string', 'format': 'date-time'},
        'fecha_caducidad': {'type': 'string', 'format': 'date-time'},
        'cantidad': {'type': 'integer'},
        'precio': {'type': 'number'}
    },
}

schemaProductoLoteModifyEs = {
    'type': 'object',
    'properties': {
        'estadoLote': {'type': 'string'}  # Campo opcional
    },
}
#++++++++++++++++++++++++++++++++++++++++++++++++++
schema_sesion = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'clave': {'type': 'string'}
    },
    'required': ['username', 'clave']
}