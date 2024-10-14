from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Ensure the database name is correct
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean, default=True)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'], active=data['active'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created!"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"username": user.username, "active": user.active} for user in users]), 200

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"username": user.username, "active": user.active}), 200
    return jsonify({"message": "User not found!"}), 404

@app.route('/users/<username>', methods=['PUT'])
def update_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        data = request.get_json()
        user.active = data['active']
        db.session.commit()
        return jsonify({"message": "User updated!"}), 200
    return jsonify({"message": "User not found!"}), 404

@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted!"}), 200
    return jsonify({"message": "User not found!"}), 404

if __name__ == '__main__':
    db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
