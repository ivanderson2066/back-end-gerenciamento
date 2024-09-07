import models
from models import EstoqueItem
import config
from config import db

# Adicionar um item usando o email como ID
def adicionar_item(item: EstoqueItem, email: str):
    db.collection("users").document(email).collection("items").document(item.id).set(item.to_dict())

# Obter um item específico
def obter_item(id: str, email: str):
    doc = db.collection("users").document(email).collection("items").document(id).get()
    if doc.exists:
        return EstoqueItem.from_dict(doc.to_dict())
    else:
        return None

# Atualizar um item existente
def atualizar_item(id: str, dados_atualizados: dict, email: str):
    db.collection("users").document(email).collection("items").document(id).update(dados_atualizados)

# Remover um item
def remover_item(id: str, email: str):
    db.collection("users").document(email).collection("items").document(id).delete()

# Listar todos os itens de um usuário
def listar_itens(email: str):
    docs = db.collection("users").document(email).collection("items").stream()
    return [EstoqueItem.from_dict(doc.to_dict()) for doc in docs]
