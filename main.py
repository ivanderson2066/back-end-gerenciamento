from flask import Flask, request, jsonify
from services import adicionar_item, obter_item, atualizar_item, remover_item, listar_itens
from models import EstoqueItem

app = Flask(__name__)

# Rota simples para a raiz do servidor
@app.route("/", methods=["GET"])
def home():
    return "API de gerenciamento de estoque funcionando!", 200

@app.route("/item", methods=["POST"])
def criar_item():
    dados = request.json
    item = EstoqueItem(**dados)
    adicionar_item(item)
    return jsonify({"status": "Item adicionado com sucesso!"}), 201

@app.route("/item/<id>", methods=["GET"])
def obter_item_por_id(id):
    item = obter_item(id)
    if item:
        return jsonify(item.to_dict())
    else:
        return jsonify({"error": "Item não encontrado!"}), 404

@app.route("/item/<id>", methods=["PUT"])
def atualizar_item_por_id(id):
    dados_atualizados = request.json
    atualizar_item(id, dados_atualizados)
    return jsonify({"status": "Item atualizado com sucesso!"})

@app.route("/item/<id>", methods=["DELETE"])
def remover_item_por_id(id):
    remover_item(id)
    return jsonify({"status": "Item removido com sucesso!"})

@app.route("/itens", methods=["GET"])
def listar_todos_itens():
    itens = listar_itens()
    return jsonify([item.to_dict() for item in itens])

if __name__ == "__main__":
    app.run(debug=True)
