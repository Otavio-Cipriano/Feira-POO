from app.data.barraca_mock import BARRACAS

class Barraca:
    TAXA_BASE = 50.0

    def __init__(self, id, codigo, metragem):
        self._id = id
        self.alterar_codigo(codigo)
        self.alterar_metragem(metragem)

    # --- Leitura ---
    def mostrar_id(self):
        return self._id

    def mostrar_codigo(self):
        return self._codigo

    def mostrar_metragem(self):
        return self._metragem

    # --- Alteração ---
    def alterar_codigo(self, codigo):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("Código inválido.")
        self._codigo = codigo.strip()

    def alterar_metragem(self, metragem):
        if not isinstance(metragem, (int, float)) or metragem <= 0:
            raise ValueError("A metragem deve ser maior que zero.")
        self._metragem = float(metragem)

    # --- Negócio ---
    def calcular_taxa_diaria(self):
        return self.TAXA_BASE

    def __repr__(self):
        return f"Barraca({self._codigo})"


class BarracaAlimentacao(Barraca):
    TAXA_BASE = 80.0

    def calcular_taxa_diaria(self):
        return self.TAXA_BASE


class BarracaGourmet(BarracaAlimentacao):
    TAXA_BASE = 120.0

    def calcular_taxa_diaria(self):
        # Utiliza obrigatoriamente super() como pedido na especificação
        return super().calcular_taxa_diaria()

# Mapeamento para evitar o uso de 'if'
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
