from flask import Flask, render_template, make_response, request, redirect, jsonify
import os
import random
import requests
import time
from urllib.parse import urlencode


app=Flask(__name__)
port = int(os.getenv("PORT", 5000))

def generate_orderid():
	return random.randint(1000000000000, 9999999999999)

def gen_url(base_url, params):
    qstr = urlencode(params)
    return base_url + "?" + qstr

@app.route('/')
def index():
    return "Hello world!!"

@app.route('/<merchant_id>/redirect', methods=['GET', 'POST'])
def get_data(merchant_id):
    # order_id = 'al'
    if request.method == 'GET':
        # time.sleep(2)
        # order_id = state['order_id']
        order_id = request.args.get('order_id')

        state['transaction_id'] = generate_orderid()
        api_url = bank_redirects['1']['url']
        state['order_id'] = order_id
        state['api_url'] = api_url
        state['URLpositive'] = merchant_urls[merchant_id]['URLpositive']
        state['URLnegative'] = merchant_urls[merchant_id]['URLnegative']
        # transaction = {'order_id': order_id, 'api_url': api_url,
        #                'transaction_status': 'waiting', 
        #                'transaction_id': state['transaction_id'],
        #                'URLpositive': merchant_urls[merchant_id]['URLpositive'],
        #                'URLnegative': merchant_urls[merchant_id]['URLnegative'],
        #                'card_no' : state['card_no'] }
        # print(transaction)
        url_ = {'transaction_id': state['transaction_id'], 'id':bank_redirects['1']['id']}
        post_url = gen_url(api_url, url_)
        r = requests.post(url=post_url, json=state)
        # print(r.json())
        return render_template('payment_gateway.html')
        # return jsonify(r.json())

    if request.method == 'POST':
        global state
        state = request.get_json()
        print()
        print(state)
        print('\n\n\n\n\n')

        order_id = request.args.get('order_id')
        print(order_id, merchant_id)
        state['order_id'] = order_id
        state['merchant_id'] = merchant_id
        
        return jsonify({'order_id': order_id, 'status': 'received'})

if __name__ == '__main__':
    state = {}
    bank_redirects = {'1': {'url': 'http://0.0.0.0:5001', 'id': 'asdfghjkl'}}
    merchant_urls = {'qwertyuiop':{'URLpositive': 'http://0.0.0.0:8000/payment_success', 'URLnegative': 'http://0.0.0.0:8000/payment_failed'}}
    app.run(host = '0.0.0.0', port = port, debug=True)
