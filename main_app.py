from flask import Flask, make_response, render_template, request, abort, redirect, url_for
import random
import string
import requests
import hmac
import hashlib

app = Flask(__name__)

APP_ID = "xxx"
ACCOUNT_KIT_APP_SECRET = "xxx"
ACCOUNT_KIT_VERSION = 'v1.1'


@app.route('/')
def index():
    csrf_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
    resp = make_response(render_template('index.html',
                                         app_id=APP_ID,
                                         csrf=csrf_token,
                                         accountkit_version=ACCOUNT_KIT_VERSION))
    resp.set_cookie('csrf', csrf_token)
    return resp


@app.route('/success', methods=['POST'])
def success():
    code = request.form.get('code')
    csrf = request.form.get('csrf')

    cookie_csrf = request.cookies.get('csrf')

    if csrf != cookie_csrf:
        abort(401, 'CSRF Token Mismatch')

    token_url = 'https://graph.accountkit.com/' + ACCOUNT_KIT_VERSION + '/access_token'
    token_params = {'grant_type': 'authorization_code',
                    'code': code,
                    'access_token': 'AA|%s|%s' % (APP_ID, ACCOUNT_KIT_APP_SECRET)
                    }

    r = requests.get(token_url, params=token_params)
    token_response = r.json()

    user_id = token_response.get('id')
    user_access_token = token_response.get('access_token')
    refresh_interval = token_response.get('token_refresh_interval_sec')

    identity_url = 'https://graph.accountkit.com/' + ACCOUNT_KIT_VERSION + '/me'

    app_secret_proof = hmac.new(ACCOUNT_KIT_APP_SECRET, user_access_token, hashlib.sha256)

    identity_params = {'access_token': user_access_token,
                       'appsecret_proof': app_secret_proof.hexdigest()}

    r = requests.get(identity_url, params=identity_params)
    identity_response = r.json()

    phone_number = identity_response.get('phone', {}).get('number', 'N/A')
    email_address = identity_response.get('email', {}).get('address', 'N/A')

    return render_template('response.html',
                           user_id=user_id,
                           phone_number=phone_number,
                           email_address=email_address,
                           user_access_token=user_access_token,
                           refresh_interval=refresh_interval)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = 8080
    app.run(host='127.0.0.1', port=port)
