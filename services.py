
import models 
from models import EstoqueItem
import config
from config import db
def adicionar_item(item: EstoqueItem):
    db.collection("estoque").document(item.id).set(item.to_dict())

def obter_item(id: str):
    doc = db.collection("estoque").document(id).get()
    if doc.exists:
        return EstoqueItem.from_dict(doc.to_dict())
    else:
        return None

def atualizar_item(id: str, dados_atualizados: dict):
    db.collection("estoque").document(id).update(dados_atualizados)

def remover_item(id: str):
    db.collection("estoque").document(id).delete()

def listar_itens():
    docs = db.collection("estoque").stream()
    return [EstoqueItem.from_dict(doc.to_dict()) for doc in docs]
