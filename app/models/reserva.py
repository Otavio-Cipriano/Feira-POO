from datetime import datetime

from app.data.reserva_mock import RESERVAS


class Reserva:
    FORMATO_DATA = "%Y-%m-%d"

    def __init__(self, id, feirante, barraca, data):
        self._id = id
        self.alterar_feirante(feirante)
        self.alterar_barraca(barraca)
        self.alterar_data(data)

    # Leitura
    def mostrar_id(self):
        return self._id

    def mostrar_feirante(self):
        return self._feirante

    def mostrar_barraca(self):
        return self._barraca

    def mostrar_data(self):
        return self._data

    # Alteração e validação
    def alterar_feirante(self, feirante):
        # Feirante é obrigatório
        if feirante is None:
            raise ValueError("Feirante inválido.")
        self._feirante = feirante

    def alterar_barraca(self, barraca):
        # Barraca é obrigatória
        if barraca is None:
            raise ValueError("Barraca inválida.")
        self._barraca = barraca

    def alterar_data(self, data):
        # Rejeita vazio, tipo errado e data fora do formato AAAA-MM-DD
        try:
            data_limpa = data.strip()
            if not data_limpa:
                raise ValueError
            datetime.strptime(data_limpa, self.FORMATO_DATA)
        except (ValueError, AttributeError):
            raise ValueError("Data inválida. Use o formato AAAA-MM-DD.")
        self._data = data_limpa

    def __repr__(self):
        return (
            f"Reserva({self._id}, {self._feirante.mostrar_nome()}, "
            f"{self._barraca.mostrar_codigo()}, {self._data})"
        )


def carregar_reservas(feirantes, barracas):
    # Indexa feirantes e barracas pelo id para ligar cada reserva aos objetos
    feirantes_por_id = {f.mostrar_id(): f for f in feirantes}
    barracas_por_id = {b.mostrar_id(): b for b in barracas}

    # Cria um objeto Reserva para cada item do mock
    return [
        Reserva(
            r["id"],
            feirantes_por_id.get(r["feirante_id"]),
            barracas_por_id.get(r["barraca_id"]),
            r["data"],
        )
        for r in RESERVAS
    ]