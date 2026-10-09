import math

from app.data.barraca_mock import BARRACAS

class Barraca:
    TAXA_BASE = 50.0

    def __init__(self, id, codigo, metragem):
        self._id = id
        self.alterar_codigo(codigo)
        self.alterar_metragem(metragem)

    def mostrar_id(self):
        return self._id

    def mostrar_codigo(self):
        return self._codigo

    def mostrar_metragem(self):
        return self._metragem


    def alterar_codigo(self, codigo):
        try:
            codigo_limpo = codigo.strip()
        except AttributeError as erro:
            raise ValueError("Código inválido.") from erro
        if not codigo_limpo:
            raise ValueError("Código inválido.")
        self._codigo = codigo_limpo

    def alterar_metragem(self, metragem):
        try:
            metragem_validada = float(metragem)
        except (TypeError, ValueError) as erro:
            raise ValueError("A metragem deve ser um número maior que zero.") from erro
        if not math.isfinite(metragem_validada) or metragem_validada <= 0:
            raise ValueError("A metragem deve ser maior que zero.")
        self._metragem = metragem_validada


    def calcular_taxa_diaria(self):
        return Barraca.TAXA_BASE

    def __repr__(self):
        return f"Barraca({self._codigo})"


class BarracaAlimentacao(Barraca):
    TAXA_BASE = 80.0
    TAXA_ADICIONAL_SANITARIA = 30.0

    def calcular_taxa_diaria(self):
        return super().calcular_taxa_diaria() + self.TAXA_ADICIONAL_SANITARIA


class BarracaGourmet(BarracaAlimentacao):
    TAXA_BASE = 120.0
    TAXA_ADICIONAL_INFRAESTRUTURA = 40.0

    def calcular_taxa_diaria(self):
        return super().calcular_taxa_diaria() + self.TAXA_ADICIONAL_INFRAESTRUTURA


BARRACAS_TIPOS = {
    "barraca": Barraca,
    "alimentacao": BarracaAlimentacao,
    "gourmet": BarracaGourmet
}

def carregar_barracas():
    lista = []
    for b in BARRACAS:
        classe_barraca = BARRACAS_TIPOS[b["tipo"]]
        instancia = classe_barraca(b["id"], b["codigo"], b["metragem"])
        lista.append(instancia)
    return lista
