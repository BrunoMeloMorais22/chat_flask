from flask import Flask, render_template, redirect, request, jsonify, session, url_for
from datetime import timedelta
from db import db
from flask_cors import CORS
import os
from flask_socketio import SocketIO, send
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


app.secret_key = "corinthians"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(hours=2)

db.init_app(app)

CORS(app)

from models import User

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")
    
    try:
        if request.method == "POST":
            data = request.get_json()

            if not data:
                return jsonify({"mensagem": "Erro: dados inválidos"}), 400
            
            novoUsername = data.get("novoUsername")
            novaSenha = data.get("novaSenha")

            if not novoUsername or not novaSenha:
                return jsonify({"mensagem": "Por favor, preencha todos os espaços"})
            
            user_exists = User.query.filter_by(novoUsername=novoUsername).first()

            if user_exists:
                return jsonify({"mensagem": "Usuário já existe"}), 400
            
            hashed_senha = generate_password_hash(novaSenha)

            new_user = User(novoUsername=novoUsername, novaSenha=hashed_senha)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"mensagem": "Usuário cadastrado com sucesso"})
    except Exception as e:
        print("Erro no backend", e)
        return jsonify({"mensagem": "Erro interno no servidor"}), 500

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"mensagem": "Preencha todos os campos"})
        
        user = User.query.filter_by(novoUsername=username).first()

        if user and check_password_hash(user.novaSenha, password):
            session['username'] = username
            return jsonify({"mensagem": "Login feito com sucesso"}), 200
        else:
            return jsonify({"mensagem": "Credenciais Inválidas"}), 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return jsonify({"mensagem": "Logout Feito com sucesso"}), 200

@app.route("/chat")
def chat():
    if 'username' not in session:
        return redirect(url_for("login"))
    return render_template("chat.html", username=session['username'])

@socketio.on("message")
def handle_message(data):
    print(f"Mensagem recebida de  {data['username']}: {data['message']}")
    send(data, broadcast=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))