import secrets
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

FLAG = 'bsides{s3ss10n5_4nd_c5rf_70k3n5_4r3_fun_9c8f}'
ADMIN_PIN = '2294'


def generate_csrf():
    '''Generates a random token and stores it in the session. Overwrites any existing token.'''
    token = secrets.token_hex(16)
    session['csrf_token'] = token
    return token


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve the expected token and invalidate it
        expected_csrf = session.get('csrf_token')
        session.pop('csrf_token', None)
        
        # Grab the one submitted by the form
        submitted_csrf = request.form.get('csrf_token')
        
        if not expected_csrf or submitted_csrf != expected_csrf:
            return render_template('login.html', error='CSRF Token Missing or Invalid.', csrf_token=generate_csrf())
            
        username = request.form.get('username')
        pin = request.form.get('pin')
        
        if not username or not pin:
            return render_template('login.html', error='Missing credentials.', csrf_token=generate_csrf())

        # Validate credentials
        if username.lower() == 'admin' and pin == ADMIN_PIN:
            return render_template('login.html', success=f'Welcome Admin! {FLAG}', csrf_token='')
        else:
            return render_template('login.html', error='Incorrect PIN for that user.', csrf_token=generate_csrf())

    # GET Request
    return render_template('login.html', csrf_token=generate_csrf())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
