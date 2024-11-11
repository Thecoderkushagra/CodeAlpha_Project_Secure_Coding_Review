from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret')  # Use environment variable

users = {}

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    # Basic validation
    if not username or not password or len(password) < 6:
        return jsonify({'message': 'Invalid input!'}), 400
    
    if username in users:
        return jsonify({'message': 'User already exists!'}), 400
    
    hashed_password = generate_password_hash(password)  # Securely hash password
    users[username] = hashed_password
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username not in users or not check_password_hash(users[username], password):  # Secure password check
        return jsonify({'message': 'Invalid username or password!'}), 401
    
    session['username'] = username
    return jsonify({'message': 'Logged in successfully!'}), 200

@app.route('/profile', methods=['GET'])
def profile():
    if 'username' in session:
        return jsonify({'username': session['username']}), 200
    return jsonify({'message': 'Unauthorized'}), 401

if __name__ == '__main__':
    app.run(debug=False)