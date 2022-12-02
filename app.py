from flask import Flask, request, render_template, send_file, send_from_directory, redirect, url_for
import hashlib, os, io
from PIL import Image
from src.utils import str2qr, qr2vc, vc2qr, qr2str

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
        private_img = Image.open(request.files.get('iKey', ''))

        if login not in storage:
            return render_template('auth_bad.html')

        h_creds = hash(login + password)
        stored_img = Image.open(f'./static/storage/{storage[login]}.png', 'r')
        # create qr from h_creds
        qr_img1 = str2qr(h_creds)
        qr_img2 = vc2qr(private_img, stored_img, qr_img1)
        temp_qr_img_path = './temp/temp.png'
        qr_img2.save(temp_qr_img_path)
        
        # for tesing only
        # auth_ok = storage[login] == password
        restored_h_creds = qr2str(temp_qr_img_path)
        os.remove(temp_qr_img_path)
        auth_ok = restored_h_creds == h_creds
        
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
        qr_img = str2qr(h_creds)
        private_img, stored_img = qr2vc(qr_img)
        
        private_img_name = login
        private_img.save(f'./static/storage/private/{private_img_name}.png')
        
        storage[login] = login
        stored_img.save(f'./static/storage/{login}.png')

        return render_template('reg_ok.html', img_ref = f'storage/private/{private_img_name}.png')

    return render_template('reg.html')


@app.route("/")
def redirect_to_auth():
    return redirect(url_for("form_auth"))


@app.route('/iKey/<path:filename>', methods=['GET', 'POST'])
def iKey(filename):
    return_data = io.BytesIO()
    with open(filename, 'rb') as fo:
        return_data.write(fo.read())
        
    return_data.seek(0)

    os.remove(f'./{filename}')

    return send_file(return_data, mimetype='application/png', download_name='iKey.png')



def init_storage():
    with os.scandir("./static/storage/") as entries:
        for entry in entries:
            if entry.name.endswith('.png'):
                login = entry.name[:-4]
                storage[login] = login


if __name__ == "__main__":
    init_storage()
    app.run()
