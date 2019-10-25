from flask import Flask, render_template, make_response, request, redirect, jsonify
import os
import random
import requests
import time 
from urllib.parse import urlencode
from functools import wraps



app=Flask(__name__)
port = int(os.getenv("PORT", 5001))

def generate_orderid():
	return random.radint(1000000000000, 9999999999999)

def gen_url(base_url, params):
    qstr = urlencode(params)
    return base_url + "?" + qstr

def verify(state):
    if 'pin' in state:
        if state['pin'] == user['pin']:
            return 'SUCCESSFUL'
        else:
            return 'FAILED'
    elif 'pin' not in state:
        return 'AUTHORIZATION_REQ'

def check_auth(username, password):
    return username == 'admin' and password == 'secret'

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth: 
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        global state
        state = request.get_json()

        order_id = state['order_id']
        # merchant_id = request.json['merchant_id']
        transaction_status = state['transaction_status']
        # time.sleep(10)
        url_ = {'transaction_status': state['transaction_status'], 'order_id':order_id}
        result = verify(state)
        state['result'] = result
        if result == 'SUCCESSFUL':
            state['return_url'] = request.json.get('URLpositive')
            url_['result'] = 'SUCCESSFUL'
            url_['transaction_status'] = 'ended'
            state['return_url'] = gen_url(state['return_url'], url_)
            r = requests.post(url=state['return_url'], json=url_)
            return jsonify(state)
        elif result == 'AUTHORIZATION_REQ':
            state['return_url'] = 'http://0.0.0.0:5001/authorize'
            return jsonify(state)

        else:
            state['return_url'] = request.json.get('URLnegative')
            url_['result'] = 'FAILED'
            state['return_url'] = gen_url(state['return_url'], url_)
            r = requests.post(url=state['return_url'], json=url_)
            return jsonify(state)
        # return make_response('success')
    if request.method == 'GET':
        # headers = {"Content-Type": "application/json"}
        # return make_response('Test worked!',
        #                  200,
        #                  headers=headers)
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="0;url={}" />
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
    
</head>


</html>'''.format(state['return_url'])
        

@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if request.method == 'POST':
        global state
        pin = request.form.get('pin')
        state['pin'] = pin
        r = requests.post(url='http://0.0.0.0:5001', json=state)
        print(r.json())
        # data = request.form.to_dict()
        return redirect('http://0.0.0.0:5001')
        # return 'Authorizing'
    if request.method == 'GET':
        card_no = state['card_no']
        return render_template('auth.html', card_no=card_no)


@app.route('/test', methods=['POST'])
def test():
    data = {}
    data['password'] = request.form.get('password')
    data['timeZone'] = request.form.get('timeZone')
    data['loginId'] = request.form.get('loginId')
    print(data)
    # data = dict(data)
    r = requests.post(url='https://aimsportal.iitbhilai.ac.in/iitbhAims/login/loginHome', json=data, verify=False)
    print(r.text)
    return redirect('https://192.168.10.98/iitbhAims/login/loginHome')


if __name__ == '__main__':
    state = {}
    tmp = {}
    user = {'card_no': '1234567890',
            'cvv': '111',
            'pin': '123'}
    app.run(host = '0.0.0.0', port = port, debug=True)
    
