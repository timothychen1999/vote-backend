from flask import Blueprint, jsonify, session
from http import HTTPStatus
import database as db
from auth import require_login
from models import User
from chain import get_claim_cat_id,check_bcoin_balance
from models import Cat,User
from dailyUtils import daily_update

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/', methods=['GET'])
@require_login
def get_user():
    user = db.get_user_by_address(session['address'])
    if user is not None:
        daily_update(user)
        return jsonify(user.serialize()), HTTPStatus.OK
    else:
        user = User()
        user.address = session['address']
        db.create_user(user)
        return jsonify(user.serialize()), HTTPStatus.CREATED

@user_routes.route('/', methods=['POST'])
@require_login
def create_user():
    address = session['address']
    user = User()
    user.address = address
    db.set_user(user)
    return jsonify({'message': 'User created', 'user': user.serialize()}), HTTPStatus.CREATED

@user_routes.route('/claim-cat/<txhash>', methods=['POST'])
@require_login
def claim_cat(txhash:str):
    user = db.get_user_by_address(session['address'])
    if user is None:
        return jsonify({'message': 'User not found'}), HTTPStatus.NOT_FOUND
    cat_id = get_claim_cat_id(session['address'],txhash)
    cat_id = int(cat_id)
    if cat_id == -1:
        return jsonify({'message': 'Claim Failed'}), HTTPStatus.BAD_REQUEST
    user.cat_id = cat_id
    user.cat = Cat()
    user.cat.is_active = True
    user.cat.happiness = 50
    user.cat.energy = 50
    user.cat.id = cat_id
    
    
    db.set_user(user)
    return jsonify({'message': 'Cat claimed', 'user': user.serialize()}), HTTPStatus.OK
@user_routes.route('/bcoin', methods=['GET'])
@require_login
def get_bcoin():
    address = session['address']
    balance = check_bcoin_balance(address)
    if balance == -1:
        return jsonify({'message': 'Query Failed, try again later'}), HTTPStatus.SERVICE_UNAVAILABLE
    else:
        return jsonify({'message': 'Query Successful', 'balance': balance/(10**18)}), HTTPStatus.OK
    
    
    
    
