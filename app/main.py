import os
from flask import Flask, jsonify, request, session, redirect
from models import db, bcrypt, User

def initalize_app():
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI='sqlite:///database',
        SECRET_KEY="top secret okay"
    )
    bcrypt.init_app(app)
    db.init_app(app)
    return app

app = initalize_app()

@app.route('/', methods=['GET'])
def index():
    return redirect('static/index.html')

@app.route('/register', methods=['POST'])
def register():
    id = request.form['id']
    password = request.form['password']
    user = User(id, password)
    db.session.add(user)
    db.session.commit()
    return '', 201

@app.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    user = User.query.get_or_404(id)
    password = request.form['password']
    if user.authenticate(password):
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
