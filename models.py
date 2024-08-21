class EstoqueItem:
    def __init__(self, id, nome, quantidade, preco, categoria):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.categoria = categoria

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "quantidade": self.quantidade,
            "preco": self.preco,
            "categoria": self.categoria,
        }

    @staticmethod
    def from_dict(source):
        return EstoqueItem(
            id=source.get("id"),
            nome=source.get("nome"),
            quantidade=source.get("quantidade"),
            preco=source.get("preco"),
            categoria=source.get("categoria")
        )
