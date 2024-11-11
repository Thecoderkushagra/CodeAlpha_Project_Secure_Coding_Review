from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'secret'  # Hard-coded secret key

# In-memory user storage
users = {}

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if username in users:
        return jsonify({'message': 'User already exists!'}), 400
    users[username] = password  # Storing password in plain text
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username not in users or users[username] != password:  # Plain text comparison
        return jsonify({'message': 'Invalid username or password!'}), 401
    session['username'] = username
    return jsonify({'message': 'Logged in successfully!'}), 200

@app.route('/profile', methods=['GET'])
def profile():
    if 'username' in session:
        return jsonify({'username': session['username']}), 200
    return jsonify({'message': 'Unauthorized'}), 401

if __name__ == '__main__':
    app.run(debug=True)