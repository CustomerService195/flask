from flask import Flask, jsonify, request, redirect, url_for, render_template, flash
import os
import boto3

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')  # Use a secure secret key from env

# Hardcoded credentials for simplicity (in a real app, use a proper authentication mechanism)
USERNAME = 'admin'
PASSWORD = 'password'

# AWS S3 Configuration
S3_BUCKET = os.getenv('S3_BUCKET')
S3_KEY = os.getenv('AWS_ACCESS_KEY_ID')
S3_SECRET = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_LOCATION = f'http://{S3_BUCKET}.s3.amazonaws.com/'

s3 = boto3.client(
    's3',
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)

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
            s3.upload_fileobj(
                file,
                S3_BUCKET,
                file.filename,
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )
            flash('File successfully uploaded to S3')
            return redirect(request.url)
    return render_template('upload.html')

if __name__ == '__main__':
    port = int(os.getenv("PORT", default=5000))
    app.run(debug=True, host='0.0.0.0', port=port)

