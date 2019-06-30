from flask import request, jsonify, abort, make_response
from .app import app
from model.user import User
from model.util import get_price
from model.user import InsufficientFundsError, InsufficientSharesError



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/api/account_info/<api_key>", methods=['GET'])
def get_user(api_key):
    # curl http://localhost:5000/api/account_info/32641019545724871837
    user = User.one_where("api_key=?", (api_key,))
    if user is None:
        abort(404)
    return jsonify(user.json())

@app.route("/api/get_api_key", methods=["POST"])
# curl -i -H "Content-Type: application/json" -X POST -d '{"user_name":"mikebloom", "password":"password"}' http://localhost:5000/api/get_api_key
def web_login():
    """ accept a username and password in json data, return the user's api key """
    if request.json is None:
        abort(404)
    user_name = request.json["user_name"]
    password = request.json["password"]
    user = User.login(user_name, password)
    return jsonify({"API Key":user.api_key})

# FIXME create account cannot have pre-existing api_key
@app.route('/api/create_account/<api_key>', methods=["POST"])
def create_account(api_key):
    """ create an account with a username, realname, and password provided in
    a json POST request """
    if not request.get_json():
        abort(404)
    if "user_name" or "real_name" not in request.json():
        abort(404)
    user = User({"user_name": request.get_json().user_name,
                 "real_name": request.get_json().real_name,
                 "balance": request.get_json().balance})
    user.save()
    return jsonify(user)

@app.route('/api/price/<ticker>', methods=["GET"])
def lookup_price(ticker):
    # curl http://localhost:5000/api/price/nvda
    """ return the price of a given stock. no api authentication """
    price = get_price(ticker)
    if price is None:
        abort(404)
    return jsonify({
        "ticker": ticker,
        "price": price
    })

@app.route('/api/positions/<api_key>', methods=["GET"])
def get_positions(api_key):
    # curl http://localhost:5000/api/positions/32641019545724871837
    """ return a json list of dictionaries of the user's positions """
    user = User.api_authenticate(api_key)
    if user is None:
        abort(404)
    positions = user.all_positions()
    if positions is None:
        return {"User has no positions"}
    return jsonify([position.json() for position in positions])

@app.route('/api/position/<ticker>/<api_key>', methods=["GET"])
def get_position(ticker, api_key):
    # curl http://localhost:5000/api/position/pfe/32641019545724871837
    """ return a json object of a user's position for a given stock symbol """
    user = User.api_authenticate(api_key)
    position = user.positions_for_stock(ticker)

    return jsonify(position.json())

@app.route('/api/trades/<api_key>', methods=["GET"])
def get_trades(api_key):
    # curl http://localhost:5000/api/trades/32641019545724871837
    """ return a json list of dictionaries representing all of a user's trades """
    user = User.api_authenticate(api_key)
    trades = user.all_trades()
    return jsonify([trade.json() for trade in trades])
    

@app.route('/api/trades/<ticker>/<api_key>', methods=["GET"])
def get_trades_for(ticker, api_key):
    # curl http://localhost:5000/api/trades/tsla/32641019545724871837
    """ return a json list of dictionaries representing all trades for a given stock """
    user = User.api_authenticate(api_key)
    trades = user.trades_for(ticker)
    return jsonify([trade.json() for trade in trades])


@app.route('/api/deposit/<api_key>', methods=["POST"])
def deposit(api_key):
    if not request.json or "amount" not in request.json:
        return jsonify({"error": "deposit requires json with 'amount' key"}), 400
    amount = request.json["amount"]
    user = User.api_authenticate(api_key)
    user.balance += amount
    user.save()
    return jsonify({"deposit":amount}), 201

@app.route('/api/buy/<api_key>', methods=["POST"])
def buy(api_key):
    # curl -i -H "Content-Type: application/json" -X POST -d '{"shares":4, "ticker":"nvda"}' http://localhost:5000/api/buy/32641019545724871837
    """ buy a certain amount of a certain stock, amount & symbol provided in a json POST request """
    if not request.json:
        return jsonify({"error": "requires json with 'shares' & 'ticker' key"}), 400
    if "ticker" not in request.json or "shares" not in request.json:
        return jsonify({"error": "requires json with 'shares' & 'ticker' key"}), 400
    shares = request.json["shares"]
    ticker = request.json["ticker"]
    user = User.api_authenticate(api_key)
    try:
        buy_shares = user.buy(ticker, shares)
        return jsonify(buy_shares.json())
    except InsufficientFundsError:
        return jsonify({"error": "Insufficient Funds"})

@app.route('/api/sell/<api_key>', methods=["POST"])
def sell(api_key):
    # curl -i -H "Content-Type: application/json" -X POST -d '{"shares":2, "ticker":"nvda"}' http://localhost:5000/api/sell/32641019545724871837
    """ sell a certain amount of a certain stock, amount & symbol provided in a json POST request """
    if not request.json:
        return jsonify({"error": "requires json with 'shares' & 'ticker' key"}), 400
    if "ticker" not in request.json or "shares" not in request.json:
        return jsonify({"error": "requires json with 'shares' & 'ticker' key"}), 400
    shares = request.json["shares"]
    ticker = request.json["ticker"]
    user = User.api_authenticate(api_key)
    try:
        sell_shares = user.sell(ticker, shares)
        return jsonify(sell_shares.json())
    except InsufficientSharesError:
        return jsonify({"error": "Insufficient Shares"})