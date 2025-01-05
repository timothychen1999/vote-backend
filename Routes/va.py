import sys
from Routes.class_va import VA, modinv, extended_gcd, Beacon
from flask import Blueprint, jsonify, session, request
from http import HTTPStatus
from auth import require_login  # 以下函式上面有@require_login代表前端call後端這個網址時需要先登入

sys.setrecursionlimit(10**6)
padding: bytes = bytes.fromhex("003031300D060960864801650304020105000420")

va = VA() ## TODO: 一個candidate一個VA

# 票軌是計票的箱子，可以存在VA裡面

va_routes = Blueprint("va_routes", __name__)


@va_routes.route("./get_pairs", methods=["GET"])
def return_pairs():
    # Done
    """
    這是回傳encrypted pairs的程式碼，是子芹askEncryptedPair這個function所需要的
    
    """

    try:
        # 使用 VA 類別生成加密對
        enc_pairs = va.generate_enc_pair()
        return jsonify({'encrypted_pairs': enc_pairs}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST


@va_routes.route("./get_proof", methods=["GET"])
@require_login
def return_proof():
    # Done
    """
    這是回傳interactive proof的程式碼，是子芹getProof這個function所需要的

    """
    try:
        # 使用 VA 類別生成交互證明
        if va.ep == None:
            return jsonify({'message': "Please generate an encryption pair first."}), HTTPStatus.BAD_REQUEST
        b = Beacon()
        proof = va.get_interactive_proof(b, va.ep)
        return jsonify({
            'seed': proof[0],
            'proof': proof[1]
        }), HTTPStatus.OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST


@va_routes.route("./get_commitment", methods=["GET"])
@require_login
def return_commitment():
    # Done
    """
    這是回傳commitment的程式碼，是子芹getCommitment這個function所需要的

    """
    try:
        # 使用 VA 類別返回加密對的承諾
        if va.ep == None:
            return jsonify({'message': "Please generate an encryption pair first."}), HTTPStatus.BAD_REQUEST
        commitment = va.get_commitment(va.ep)
        return jsonify({'commitment': commitment}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST


@va_routes.route("./get_results", methods=["GET"])
@require_login
def return_results():
    # TODO: ?
    """
    這是回傳results的程式碼，是凱淇getResults這個function所需要的

    """
    try:
        results = "Here are the election results."  # 假設這裡會獲取結果
        return jsonify({'results': results}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST


@va_routes.route("./get_encryptedresult", methods=["GET"])
@require_login
def return_encryptedresult():
    # TODO: pyteozs
    pass
    try:
        encrypted_result = "Encrypted result."  # 假設這裡會返回加密的結果
        return jsonify({'encrypted_result': encrypted_result}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST


@va_routes.route("./set_result", methods=["POST"])
@require_login
def set_results():
    # TODO: ?
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
