from flask import Flask, request, jsonify, g
from functools import wraps
from firebase_admin import auth, credentials
import firebase_admin
from config import db
app = Flask(__name__)

# Inicializa o Firebase Admin SDK com as credenciais do serviço
cred = credentials.Certificate('vicios-44d19-firebase-adminsdk-tm7ef-71f5ae5d66.json')

# Middleware para verificar se o e-mail está no cabeçalho e é válido
def email_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        email = request.headers.get('Email')
        if not email:
            return jsonify({'error': 'Email is missing!'}), 403

        try:
            # Verifica se o e-mail está registrado
            user = auth.get_user_by_email(email)
            g.user_email = email
            g.user_uid = user.uid
        except Exception as e:
            return jsonify({'error': 'Invalid email or user not found'}), 403

        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=["GET"])
def home():
    return "API de gerenciamento de estoque funcionando!", 200

# Rota para registro de um novo usuário
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        user = auth.create_user(
            email=data['email'],
            password=data['password']
        )
        return jsonify({'status': 'User registered successfully', 'uid': user.uid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para login do usuário (simplesmente retorna uma resposta positiva)
@app.route('/login', methods=['POST'])
def login():
    return jsonify({'status': 'Login successful. Use email in headers for authenticated requests.'}), 200

# Rota para criar um novo item no estoque (usando o e-mail do usuário)
@app.route("/item", methods=["POST"])
@email_required
def criar_item():
    dados = request.json
    if not dados:
        return jsonify({"error": "Dados do item são obrigatórios!"}), 400

    try:
        item_ref = db.collection('users').document(g.user_email).collection('items').document()
        item_ref.set(dados)
        return jsonify({"status": "Item adicionado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para obter um item específico pelo ID (usando o e-mail do usuário)
@app.route("/item/<id>", methods=["GET"])
@email_required
def obter_item_por_id(id):
    try:
        item_ref = db.collection('users').document(g.user_email).collection('items').document(id)
        item = item_ref.get()
        if item.exists:
            return jsonify(item.to_dict())
        else:
            return jsonify({"error": "Item não encontrado!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para atualizar um item específico pelo ID (usando o e-mail do usuário)
@app.route("/item/<id>", methods=["PUT"])
@email_required
def atualizar_item_por_id(id):
    dados_atualizados = request.json
    try:
        item_ref = db.collection('users').document(g.user_email).collection('items').document(id)
        item_ref.update(dados_atualizados)
        return jsonify({"status": "Item atualizado com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para remover um item específico pelo ID (usando o e-mail do usuário)
@app.route("/item/<id>", methods=["DELETE"])
@email_required
def remover_item_por_id(id):
    try:
        item_ref = db.collection('users').document(g.user_email).collection('items').document(id)
        item_ref.delete()
        return jsonify({"status": "Item removido com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para listar todos os itens do usuário autenticado (usando o e-mail)
@app.route("/itens", methods=["GET"])
@email_required
def listar_todos_itens():
    try:
        items_ref = db.collection('users').document(g.user_email).collection('items').stream()
        items = [item.to_dict() for item in items_ref]
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
