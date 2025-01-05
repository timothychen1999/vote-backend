from flask import Blueprint, request, jsonify
from http import HTTPStatus
from database import users_db,cats_db


utils_routes = Blueprint('utils_routes', __name__)
@utils_routes.route('/calculate-b-coin', methods=['POST'])
def calculate_b_coin():
    if request.is_json:
        val = request.get_json()['value']
        eth_val = (10**18)
        eth_val *= val
        pp_val = eth_val*1000
        return jsonify({'amount':str(pp_val),'value':str(eth_val)}),HTTPStatus.OK
        
