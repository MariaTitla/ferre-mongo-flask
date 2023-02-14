from flask import Blueprint

prove=Blueprint("prove", __name__)

@prove.route("/proveedores/todos")
def obtenerTodos():
    return "todos los proveedores"


