from flask import Blueprint, jsonify, session, request
from http import HTTPStatus
from auth import require_login
from database import get_user_by_address
import userActions
import database as db

coins_routes = Blueprint('coins_routes', __name__)

@coins_routes.route('/get_coin_a', methods=['POST'])
@require_login
def get_coin_a():
    data = request.get_json()
    coin_a = float(data['coin_a'])
    coin_b = float(data['coin_b'])
    txhash = str(data['txhash'])
    user = get_user_by_address(session['address'])
    if user is None:
        return jsonify({'message': 'User not found'}), HTTPStatus.NOT_FOUND
    succ = userActions.coin_conversion(user, coin_a, coin_b, txhash)
    if succ:
        result = user
        r = db.set_user(result)
        if r:    
            return jsonify({'message': 'Item bought', 'user': result.serialize()}), HTTPStatus.OK
        else:
            return jsonify({'message': 'db failed'}), HTTPStatus.SERVICE_UNAVAILABLE
    else:
        return jsonify({'message': 'conversion failed'}), HTTPStatus.BAD_REQUEST