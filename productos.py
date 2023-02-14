from flask import request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

import datetime

from flask import Blueprint
mongo = PyMongo()

prod=Blueprint('product', __name__)



@prod.route('/subirFoto', methods=['POST'])
def subir():
    file=request.files['foto']
    print(file, file.filename)
    nombreArchivo=secure_filename(file.filename)
    file.save(os.path.join(prod.config["UPLOAD_FILE"]), nombreArchivo)
    #https://www.youtube.com/watch?v=Yyul17TBHrE
    res=jsonify({'mensage':'subido'})
    res.status_code=200
    return res

#ruta que muestra la lista de todos los Productos
@prod.route('/productos/todos', methods=['GET'])
def mostrar_prod():
	prod = mongo.db.productos.find()
	resp = dumps(prod)
	return resp


@prod.route('/productos/listaProductos', methods=['GET'])
def listar_Productos():
    query = {}
    sort = [("nombProd", 1)]
    project = {"_id":0,"nombProd": 1, 'caracteristicas':1,'categoria':1,
    "costo":1, 'paisOrigen':1}
    productos = mongo.db.productos.find(query, project).sort(sort)
    return dumps(productos)

@prod.route('/productos/unico', methods=['GET'])
def mostrarFoco():
    query = {'nombProd':'tijeras'}
    sort = [("nombProd", 1)]
    project = {"_id":0,"nombProd": 1, 'caracteristicas':1,'categoria':1,
    "costo":1, 'paisOrigen':1}
    productos = mongo.db.productos.find(query, project).sort(sort)
    return dumps(productos)
  
@prod.route('/productos/id/<id>', methods=['GET'])
def obtener_prod_por_ID(id):
    producto=mongo.db.productos.find_one({'_id':ObjectId(id)})
    return dumps(producto)


@prod.route('/productoPorNombre/<nombre>')
def obtener_PorNombre(nombre):
    #nom="tijeras"
    query={'nombProd':{'$eq':nombre}}
    sort = [("nombProd", 1)]
    project = {"_id":0,"nombProd": 1,"costo":1, 'marca':1}
    try:
        productos = mongo.db.productos.find(query, project).sort(sort)
        return list(productos)

    # TODO: Error Handling
    # Si es invalido el nombre retorna None.
    except (StopIteration) as _:
        return None

    except Exception as e:
        return {}

@prod.route('/productoPorNombreyCosto/<nombre>/<costo>')
def obtener_PorNombreyCosto(nombre,costo):
    #nom="tijeras"
    query={"$and":[{'nombProd':{'$eq':nombre}}, {"costo":{"$lt":costo}}]}
    sort = [("nombProd", 1)]
    project = {"_id":0,"nombProd": 1,"costo":1, 'marca':1}
    try:
        productos = mongo.db.productos.find(query, project).sort(sort)
        return list(productos)

    # TODO: Error Handling
    # Si es invalido el nombre retorna None.
    except (StopIteration) as _:

        return None

    except Exception as e:
        return {}


@prod.route('/productos/productoPorNombreoCosto/<nombre>/<costo>')
def obtener_PorNombreoCosto(nombre,costo):
    cost=int(costo)
    query={'$or':[{'nombProd':{'$eq':nombre}}, {'costo':{'$lt':cost}}]}
    sort = [("nombProd", 1)]
    project = {"_id":0,"nombProd": 1,"costo":1, 'marca':1}
    try:
        productos = mongo.db.productos.find(query, project).sort(sort)
        return list(productos)

    # TODO: Error Handling
    # Si es invalido el nombre retorna None.
    except (StopIteration) as _:

        return None

    except Exception as e:
        return {}



@prod.route("/productos/eliminar/<id>", methods=['DELETE'] )
def eliminar(id):
    mongo.db.productos.delete_one( { "_id": ObjectId(id) } )
    resp=jsonify({'mensaje':"Producto con "+id+" fue eliminado"})
    return resp


@prod.errorhandler(404)
def not_found(error:any=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@prod.route('/productos/actualizar/<id>', methods=['PUT'])
def actualizar_Prod(id):
    n = request.json['nombProd']
    cos = request.json['costo']
    c = request.json['caracteristicas']
    um = request.json['unidadMedida']
    po = request.json['paisOrigen']
    ce = request.json['cantidad']
    nc = request.json['categoria']['nombCat']
    dc = request.json['categoria']['descCat']
    fe = request.json['fechaAdquisicion']
    fechaActualizacion=datetime.now(),
    costo=int(cos)
    listaCarac=c.split(",")

    prodAct={'nombProd': n,  
    'caracteristicas': listaCarac, 'unidadMedida':um, 'paisOrigen':po, 
    'estatus':"activo", 'costo':costo,'precio':costo+(costo*30)/100,
    'cantidadExistente':int(ce), 'fechaActualizacion':fechaActualizacion,
    'fechaAdquisicion':fe,
    'categoria':{'nombCat':nc, 'descCat':dc}}

    try:
        mongo.db.productos.update_one({ "_id": ObjectId(id) },{'$set':prodAct})
    except(StopIteration) as _:
          return "error"
    finally:
        resp = jsonify({"resp":'actualizado'})
        resp.status_code = 200
        return resp
        



@prod.route('/productos/nuevoProd', methods=['POST'])
#@cross_o
# rigin()
def add_producto():
    
    n = request.json['nombProd']
    cos = request.json['costo']
    c = request.json['caracteristicas']
    um = request.json['unidadMedida']
    po = request.json['paisOrigen']
    ce = request.json['cantidad']
    nc = request.json['categoria']['nombCat']
    dc = request.json['categoria']['descCat']
    fe = request.json['fechaAdquisicion']
    f = request.json['foto']
    actor1=request.json['actores'][0]
    actor2=request.json['actores'][1]
    listaActores=[]
    listaActores.append(actor1)
    listaActores.append(actor2)
    fechaActual=datetime.now(),
    costo=int(cos)
    listaCarac=c.split(",")

    prod={'nombProd': n,  
        'caracteristicas': listaCarac, 'unidadMedida':um, 'paisOrigen':po, 
        'estatus':"activo", 'costo':costo,'precio':costo+(costo*30)/100,
        'cantidadExistente':int(ce), 'fechaCreacion':fechaActual, 'fechaAdquisicion':fe,
        'categoria':{'nombCat':nc, 'descCat':dc}, 'foto':"foto1.jpg", "actores":listaActores}

    mongo.db.productos.insert_one(prod)
    resp = jsonify({"resp":'agregado'})
    resp.status_code = 200
    return resp






