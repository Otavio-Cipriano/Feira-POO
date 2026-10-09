
from datetime import date

from app.data.reserva_mock import RESERVAS
from app.models.feirante import carregar_feirantes
from app.models.barraca import carregar_barracas


class Reserva:
    def __init__(self, id, feirante, barraca, data):
        if not isinstance(id, int) or isinstance(id, bool) or id <= 0:
            raise ValueError("O ID da reserva deve ser positivo.")

        self._id = id
        self._feirante = feirante
        self._barraca = barraca
        self.alterar_data(data)

    # Métodos de visualização
    def mostrar_id(self):
        return self._id

    def mostrar_feirante(self):
        return self._feirante

    def mostrar_barraca(self):
        return self._barraca

    def mostrar_data(self):
        return self._data

    # Métodos de validação e alteração
    def alterar_data(self, nova_data):
        if not isinstance(nova_data, str) or not nova_data.strip():
            raise ValueError("A data da reserva não pode ser vazia.")

        try:
            data_validada = date.fromisoformat(nova_data.strip())
        except ValueError:
            raise ValueError(
                "A data deve estar no formato AAAA-MM-DD."
            )

        self._data = data_validada.isoformat()

    # Representação do objeto
    def __repr__(self):
        return (
            f"Reserva(id={self._id}, "
            f"feirante={self._feirante.mostrar_nome()}, "
            f"barraca={self._barraca.mostrar_id()}, "
            f"data='{self._data}')"
        )


def carregar_reservas():
    feirantes = carregar_feirantes()
    barracas = carregar_barracas()

    feirantes_por_id = {
        feirante.mostrar_id(): feirante
        for feirante in feirantes
    }

    barracas_por_id = {
        barraca.mostrar_id(): barraca
        for barraca in barracas
    }

    reservas = []

    for registro in RESERVAS:
        feirante = feirantes_por_id.get(registro["feirante_id"])
        barraca = barracas_por_id.get(registro["barraca_id"])

        if feirante is None:
            raise ValueError(
                f"Feirante {registro['feirante_id']} não encontrado."
            )

        if barraca is None:
            raise ValueError(
                f"Barraca {registro['barraca_id']} não encontrada."
            )

        reserva = Reserva(
            registro["id"],
            feirante,
            barraca,
            registro["data"]
        )

        reservas.append(reserva)

    return reservas