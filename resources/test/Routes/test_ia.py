from flask import Blueprint, jsonify, session, request
from http import HTTPStatus
from auth import require_login
from test.Routes.test_class_ia import IA

ia_routes = Blueprint('ia_routes', __name__)

ia=IA()

@ia_routes.route("./",methods=["POST"])
@require_login
def return_register():
    #TODO:後端拿token，後端跟前端要權限，總之就是研究google登入
    pass