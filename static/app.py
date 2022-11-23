from flask import Flask, request, render_template
import hashlib
import uuid

app = Flask(__name__)


# map[username]{stored_img}
storage = {}


def hash(str):
    return hashlib.sha256(str.encode()).hexdigest()


@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():

    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')
        # private_image = request.form.get('iKey')

        if login not in storage:
            return render_template('auth_bad.html')

        h_creds = hash(login + password)
        # create qr from h_creds
        # check equality of creds using visual_crypto
        auth_ok = storage[login] == password
        
        if auth_ok:
            return render_template('auth_ok.html')
        else:
            return render_template('auth_bad.html')

    return render_template('auth.html')


@app.route('/registration', methods=['GET', 'POST'])
def form_registration():

    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')

        h_creds = hash(login + password)
        # create qr from h_creds
        # visual_crypto(qr) -> private_img, stored_img
        # todo:
        stored_img = password

        storage[login] = stored_img

        # todo: return private_img
        return render_template('reg_ok.html')

    return render_template('reg.html')


if __name__ == "__main__":
    app.run()
