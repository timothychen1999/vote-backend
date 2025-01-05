import logging
import web3
from flask import Blueprint, request, session, jsonify
from eth_account.messages import encode_defunct
from http import HTTPStatus

login_routes = Blueprint('login_routes', __name__)

@login_routes.route('/login', methods=['POST'])
def login():
    if request.is_json:
        content = request.get_json()
        message = content['message']
        signature = content['signature']
        address = content['address']
        
        message = encode_defunct(text=message)
        w3 = web3.Web3(web3.HTTPProvider(""))
        
        address = w3.to_checksum_address(address)
        if w3.eth.account.recover_message(message, signature=signature) == address:
            session['address'] = address
            return jsonify({'message': 'Login Successful', 'address': address}),HTTPStatus.OK 
        else:
            logging.info('Login Failed')
            logging.info('Address: %s', address)
            logging.info('Signature: %s', signature)
            logging.info('Message: %s', message)
            logging.info('Recovered Address: %s', w3.eth.account.recover_message(message, signature=signature))
            return jsonify({'message': 'Login Failed, Wrong Address'}), HTTPStatus.UNAUTHORIZED
    else:
        return jsonify({'message': 'Login Failed, Wrong Format'}), HTTPStatus.BAD_REQUEST
@login_routes.route('/logout', methods=['POST'])
def logout():
    session.pop('address', None)
    return jsonify({'message': 'Logout Successful'}), HTTPStatus.OK
@login_routes.route('/check', methods=['GET'])
def check():
    if 'address' in session:
        return jsonify({'message': 'Logged In', 'address': session['address']}), HTTPStatus.OK
    else:
        return jsonify({'message': 'Not Logged In'}), HTTPStatus.UNAUTHORIZED