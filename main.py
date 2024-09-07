from flask import Flask, request, jsonify, g
from functools import wraps
from config import db  # Importa a instância do Firestore do módulo config
from firebase_admin import auth  # Importa o módulo auth para autenticação


app = Flask(__name__)

# Middleware para verificar se o email foi passado no cabeçalho
def email_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        email = request.headers.get('Email')
        if not email:
            return jsonify({'error': 'Email is missing!'}), 403

        g.user_email = email  # Associando o email ao contexto global (g)
        return f(*args, **kwargs)
    return decorated

# Rota simples para a raiz do servidor
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

# Rota para login do usuário (Note que o login é tratado no lado do cliente via Firebase SDK)
@app.route('/login', methods=['POST'])
def login():
    return jsonify({'status': 'Use client-side Firebase SDK to handle login'}), 200

# Rota para criar um novo item no estoque (usando o email do usuário)
@app.route("/item", methods=["POST"])
@email_required
def criar_item():
    dados = request.json
    if not dados:
        return jsonify({"error": "Dados do item são obrigatórios!"}), 400

    try:
        # Usa o email como identificador do usuário no banco de dados
        item_ref = db.collection('users').document(g.user_email).collection('items').document()
        item_ref.set(dados)
        return jsonify({"status": "Item adicionado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para obter um item específico pelo ID (usando o email do usuário)
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

# Rota para atualizar um item específico pelo ID (usando o email do usuário)
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

# Rota para remover um item específico pelo ID (usando o email do usuário)
@app.route("/item/<id>", methods=["DELETE"])
@email_required
def remover_item_por_id(id):
    try:
        item_ref = db.collection('users').document(g.user_email).collection('items').document(id)
        item_ref.delete()
        return jsonify({"status": "Item removido com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para listar todos os itens do usuário autenticado (usando o email)
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
