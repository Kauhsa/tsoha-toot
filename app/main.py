import os
from flask import Flask, jsonify, request, session, redirect
from models import db, bcrypt, User

def initalize_app():
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///database'),
        SECRET_KEY="top secret okay"
    )
    bcrypt.init_app(app)
    db.init_app(app)
    return app

app = initalize_app()

@app.route('/', methods=['GET'])
def index():
    return redirect('static/index.html')

@app.route('/login', methods=['POST'])
def login():
    user = User.query.get_or_404(request.form['id'])
    if user.authenticate(request.form['password']):
        session['logged_user_id'] = user.id
        return jsonify()
    else:
        return jsonify(error='Incorrect username or password'), 400

@app.route('/logout', methods=['POST'])
def logout():
    del session['logged_user_id']
    return jsonify()

@app.route('/logged_user', methods=['GET'])
def logged_user():
    if 'logged_user_id' not in session:
        return jsonify()
    else:
        return jsonify(logged_user=session['logged_user_id'])

@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def users(id):
    if request.method == 'GET':
        return jsonify(user=User.query.get_or_404(id).dict())

@app.route('/users', methods=['POST'])
def user_add():
    json = request.json['user']
    user = User(json['id'], json['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user=user.dict()), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
