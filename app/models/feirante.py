from app.data.feirante_mock import FEIRANTES


class Feirante:
    LIMITE_RESERVAS = 2

    def __init__(self, id, nome, documento, telefone):
        self._id = id
        self.alterar_nome(nome)
        self.alterar_documento(documento)
        self.alterar_telefone(telefone)


    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def mostrar_documento(self):
        return self._documento

    def mostrar_telefone(self):
        return self._telefone

    
    def alterar_nome(self, novo_nome):
        try:
            nome = novo_nome.strip()
        except AttributeError as erro:
            raise ValueError("Nome do feirante deve ser um texto.") from erro
        if not nome:
            raise ValueError("Nome do feirante não pode ser vazio.")
        self._nome = nome

    def alterar_documento(self, novo_documento):
        try:
            doc_limpo = novo_documento.strip()
        except AttributeError as erro:
            raise ValueError("Documento deve ser um texto.") from erro
        if not doc_limpo.isdigit() or len(doc_limpo) not in (11, 14):
            raise ValueError("Documento deve ter exatamente 11 (CPF) ou 14 (CNPJ) dígitos numéricos.")
        self._documento = doc_limpo

    def alterar_telefone(self, novo_telefone):
        try:
            telefone = novo_telefone.strip()
        except AttributeError as erro:
            raise ValueError("Telefone do feirante deve ser um texto.") from erro
        if not telefone:
            raise ValueError("Telefone do feirante não pode ser vazio.")
        self._telefone = telefone

    def __repr__(self):
        return f"Feirante({self._nome})"


def carregar_feirantes():
    return [
        Feirante(
            f["id"],
            f["nome"],
            f["documento"],
            f["telefone"]
        )
        for f in FEIRANTES
    ]
