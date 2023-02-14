# importing Flask class from flask module
from flask import Flask,jsonify, request
from productos import mongo
from productos import prod
from proveedores import prove
from clientes import clientes
from empleados import emple

import os
from werkzeug.utils import secure_filename

# creacion del objecto de la clase Flask
app = Flask(__name__)

#registro del blueprint llamado prod
app.register_blueprint(prod)
app.register_blueprint(prove)
app.register_blueprint(emple)
app.register_blueprint(clientes)

#configuración de la cadena de conexion a mongo Atlas
app.config["MONGO_URI"] = "mongodb+srv://rosa:rosa123@clustermongodbnube.iiqmhwc.mongodb.net/dbferre?retryWrites=true&w=majority"
mongo.init_app(app)

from flask_cors import CORS

CORS(app)


UPLOAD_FOLDER = 'fotos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/subir', methods=['POST'])
def subirA():
    file = request.files('foto')
    print (file)
    if file and allowed_file(file.filename):
        file = request.files('foto')
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify({'message' : 'Files successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Error'})
        resp.status_code = 400
        return resp
  
@app.route('/upload', methods=['POST'])
def upload_file():
    #https://www.youtube.com/watch?v=BNBjJ5AvTG0&t=2s
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
 
    files = request.files.getlist('files[]')
     
    errors = {}
    success = False
     
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message' : 'Files successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


#Running our Flask application using app.run method
if __name__=='__main__':
    #app.run(host="0.0.0.0", port=4000, debug=True)
    app.run()



