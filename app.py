from flask import Flask, request, render_template, send_file, send_from_directory
import hashlib, os
from PIL import Image

app = Flask(__name__)


# map[username]{stored_img}
storage = {}


def hash(str):
    return hashlib.sha256(str.encode()).hexdigest()


@app.route('/auth', methods=['GET', 'POST'])
def form_auth():

    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')
        private_img = request.files.get('iKey', '')

        if login not in storage:
            return render_template('auth_bad.html')

        h_creds = hash(login + password)
        stored_img = Image.open(f'./static/storage/{storage[login]}.jpg', 'r')
        # create qr from h_creds
        # check equality of creds using visual_crypto_check(private_image, stored_img, generated_from_creds_qr)
        
        # for tesing only
        auth_ok = storage[login] == password
        
        if auth_ok:
            return render_template('auth_ok.html')
        else:
            return render_template('auth_bad.html')

    return render_template('auth.html')


@app.route('/reg', methods=['GET', 'POST'])
def form_reg():

    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')

        if login in storage:
            return render_template('reg_bad.html')

        h_creds = hash(login + password)
        # create qr from h_creds
        # visual_crypto(qr) -> private_img, stored_img
        
        private_img_name = login
        # private_img.save(f'./static/storage/private/{private_img_name}.jpg')
        
        # todo: uncomment
        # storage[login] = login
        # stored_img.save(f'./static/storage/{login}.jpg')

        return render_template('reg_ok.html', img_ref = f'storage/private/{private_img_name}.jpg')

    return render_template('reg.html')


@app.route('/iKey/<path:filename>', methods=['GET', 'POST'])
def iKey(filename):
    return send_file(filename, as_attachment=True), os.remove(f'./{filename}')


if __name__ == "__main__":
    app.run()
