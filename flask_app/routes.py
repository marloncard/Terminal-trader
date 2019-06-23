from flask import request, jsonify, abort, make_response
from .app import app
from model.user import User


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'User does not exist'}), 404)


@app.route("/api/account_info/<api_key>", methods=['GET'])
def get_user(api_key):
    user = User.one_where("api_key=?", (api_key,))
    if user is None:
        abort(404)
    return jsonify({"user_name":user.user_name,
                    "real_name":user.real_name,
                    "balance":user.balance})