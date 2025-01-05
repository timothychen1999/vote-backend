import sys
from test.Routes.test_class_va import VA, modinv, extended_gcd, Beacon
from flask import Blueprint, jsonify, session, request
from http import HTTPStatus
from auth import require_login

sys.setrecursionlimit(10**6)
padding : bytes = bytes.fromhex("003031300D060960864801650304020105000420")

va=VA()

va_routes=Blueprint("va_routes",__name__)

@va_routes.route("./get_pairs",methods=["GET"])
@require_login
def return_pairs():
    # Done
    try:
        # 使用 VA 類別生成加密對
        enc_pairs = va.generate_enc_pair()
        return jsonify({'encrypted_pairs': enc_pairs}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST


@va_routes.route("./get_proof",methods=["GET"])
@require_login
def return_proof():
    # Done
    try:
        # 使用 VA 類別生成交互證明
        if va.ep==None:
            return jsonify({'message': "Please generate an encryption pair first."}), HTTPStatus.BAD_REQUEST
        b = Beacon()
        proof = va.get_interactive_proof(b, va.ep)
        return jsonify({
            'seed': proof[0],
            'proof': proof[1]
        }), HTTPStatus.OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST

@va_routes.route("./get_commitment",methods=["GET"])
@require_login
def return_commitment():
    #Done
    try:
        # 使用 VA 類別返回加密對的承諾
        if va.ep==None:
            return jsonify({'message': "Please generate an encryption pair first."}), HTTPStatus.BAD_REQUEST
        commitment = va.get_commitment(va.ep)
        return jsonify({'commitment': commitment}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST


@va_routes.route("./get_results",methods=["GET"])
@require_login
def return_results():
    #TODO: ?
    pass
    try:
        results = "Here are the election results."  # 假設這裡會獲取結果
        return jsonify({'results': results}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST

@va_routes.route("./get_encryptedresult",methods=["GET"])
@require_login
def return_encryptedresult():
    #TODO: ?
    pass
    try:
        encrypted_result = "Encrypted result."  # 假設這裡會返回加密的結果
        return jsonify({'encrypted_result': encrypted_result}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST

@va_routes.route("./set_result",methods=["POST"])
@require_login
def return_pairs():
    #TODO: ?
    pass
    data = request.get_json()
    result = data.get("result", None)
    
    if not result:
        return jsonify({'message': 'Result is required'}), HTTPStatus.BAD_REQUEST
    
    try:
        # 假設會設置並處理投票結果
        # 這裡可以做具體的結果處理邏輯
        return jsonify({'message': 'Result set successfully'}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST