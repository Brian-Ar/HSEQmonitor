from flask import Blueprint

gestion_bp = Blueprint("gestion",__name__)

from app.modulos.gestion import rutas