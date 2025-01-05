from flask import Blueprint, jsonify, session, request
from http import HTTPStatus
from auth import require_login
from Routes.class_ia import IA
from google.oauth2 import id_token
from google.auth.transport import requests

ia_routes = Blueprint('ia_routes', __name__)
GOOGLE_OAUTH2_CLIENT_ID = 'your_oauth2_client_id'##這裡需要自己申請一個id
##參考:https://www.maxlist.xyz/2019/06/29/flask-google-login/
ia = IA()


@ia_routes.route("./", methods=["POST"])
def return_sign_ballot():
    """
    這是google登入的後端程式碼，是子芹register這個function需要call的
    """
    # TODO: 研究database要存啥

    try:
        # Specify the GOOGLE_OAUTH2_CLIENT_ID of the app that accesses the backend:
        token = request.json['id_token']
        ballot= request.json['ballot']
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_OAUTH2_CLIENT_ID
        )
        

        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return jsonify({'message': "Failed to login with Google account"}), HTTPStatus.BAD_REQUEST
        else:
            session['token'] = token
            sign_ballot=ia.sign_ballot(ballot=ballot)
            return jsonify({"sign_ballot":sign_ballot}), HTTPStatus.OK
        # ID token is valid. Get the user's Google Account ID from the decoded token.
        # user_id = id_info['sub']
        # reference: https://developers.google.com/identity/sign-in/web/backend-auth
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST
