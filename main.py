from flask import Flask, jsonify, request, redirect, url_for, render_template, flash
import os

app = Flask(__name__)


USERNAME = 'admin'
PASSWORD = 'password'

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('upload_file'))
        else:
            flash('Invalid Credentials. Please try again.')
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # Here you would normally process the file
            flash(f'File "{file.filename}" successfully uploaded.')
            return redirect(request.url)
    return render_template('upload.html')

if __name__ == '__main__':
    port = int(os.getenv("PORT", default=5000))
    app.run(debug=True, host='0.0.0.0', port=port)
