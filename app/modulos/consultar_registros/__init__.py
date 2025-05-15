from flask import Blueprint

consultar_registros_bp = Blueprint('consultar_registros',__name__)

from app.modulos.consultar_registros import rutas