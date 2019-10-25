from flask import Flask, render_template, request, redirect, jsonify
import os
import random
import requests
from urllib.parse import urlencode

app=Flask(__name__)
port = int(os.getenv("PORT", 8000))

def generate_orderid():
	return random.randint(1000000000000, 9999999999999)

def gen_url(base_url, params):
	qstr = urlencode(params)
	return base_url + "?" + qstr

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cart')
def cart():
	order_id = generate_orderid()
	return render_template('cart.html', order_id=order_id)

@app.route('/new_payment', methods=['POST'])
def new_payment():
	# Take more user info
    order = request.form.to_dict()

    api_url = payment_gateway_redirect['card'].format(merchant_id)
    url_ = {'order_id': order['order_id'], 'merchant_id': merchant_id}
    post_url = gen_url(api_url, url_)

    order['api_url'] = post_url
    order['transaction_status'] = 'new'
    print(order)
    print('\n\n\n\n\n\n\n\n')
    r = requests.post(url=post_url, json=order)
    print(r.json())

    return redirect(post_url)

@app.route('/payment_success', methods=['GET', 'POST'])
def success():
	params = request.args.to_dict()
	print(params)
	# return jsonify(params)
	return render_template('success.html', params=params)

@app.route('/payment_failed', methods=['GET', 'POST'])
def failure():
	params = request.args.to_dict()
	print(params)
	# return jsonify(params)
	return render_template('failure.html', params=params)


if __name__ == '__main__':
     merchant_id = "qwertyuiop"
     payment_gateway_redirect = {'card': 'http://0.0.0.0:5000/{}/redirect'}
     app.run(host = '0.0.0.0', port = port, debug=True)
