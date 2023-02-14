from flask import Blueprint

emple=Blueprint("emple", __name__)

@emple.route('/empleados/todos')
def obtener_todos():
    return "empleados"