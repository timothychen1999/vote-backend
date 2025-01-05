from flask import Blueprint,send_file
from http import HTTPStatus


metadata_routes = Blueprint('metadata_routes', __name__)

@metadata_routes.route('/contract-cat', methods=['GET'])
def get_contract_metadata():
    return send_file('Contract/cat.json')

@metadata_routes.route('/<int:tokenid>', methods=['GET'])
def get_metadata(tokenid:int):
    return 'In Progress', HTTPStatus.NOT_IMPLEMENTED