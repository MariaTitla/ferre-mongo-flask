from flask import Blueprint

impre=Blueprint("impre", __name__)

@impre.route("/impresoras/todas")
def obtenerTodas():
    return "todas"