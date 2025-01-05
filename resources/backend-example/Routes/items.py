from flask import Blueprint, jsonify, session, request
from http import HTTPStatus
from auth import require_login
from models import User
from database import get_user_by_address
import itemUtils
import userActions
import database as db

items_routes = Blueprint('items_routes', __name__)

@items_routes.route('/use/<int:item_id>', methods=['GET'])
@require_login
def use_item(item_id:int):
    user = get_user_by_address(session['address'])
    if user is None:
        return jsonify({'message': 'User not found'}), HTTPStatus.NOT_FOUND
    if user.cat is None:
        return jsonify({'message': 'Cat not found'}), HTTPStatus.NOT_FOUND
    succ = itemUtils.use_item(user, item_id)
    if succ:
        result = user
        db_suc = db.set_user(result)
        if db_suc:
            return jsonify({'message': 'Item used', 'user': result.serialize()}), HTTPStatus.OK
        else:
            return jsonify({'message': 'db failed'}), HTTPStatus.SERVICE_UNAVAILABLE
    else:
        return jsonify({'message': 'Item use failed'}), HTTPStatus.BAD_REQUEST

@items_routes.route('/buy_item_coin_a', methods=['POST'])
@require_login
def buy_item():
    data = request.get_json()
    shopping_list = data['shopping_list']
    user = get_user_by_address(session['address'])
    if user is None:
        return jsonify({'message': 'User not found'}), HTTPStatus.NOT_FOUND
    succ = userActions.acoin_buy_item(user, shopping_list)
    if succ:
        result = user
        db.set_user(result)
        return jsonify({'message': 'Item bought', 'user': result.serialize()}), HTTPStatus.OK


