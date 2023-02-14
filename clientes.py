from flask import Blueprint

clientes=Blueprint("clientes",__name__)

@clientes.route("/clientes/todos")
def obt_clientes():
    return "clientes"
