from datetime import datetime

from app.data.reserva_mock import RESERVAS


class Reserva:
    FORMATO_DATA = "%Y-%m-%d"

    def __init__(self, id, feirante, barraca, data):
        self._id = id
        self.alterar_feirante(feirante)
        self.alterar_barraca(barraca)
        self.alterar_data(data)

    
    def mostrar_id(self):
        return self._id

    def mostrar_feirante(self):
        return self._feirante

    def mostrar_barraca(self):
        return self._barraca

    def mostrar_data(self):
        return self._data

    
    def alterar_feirante(self, feirante):
        if feirante is None:
            raise ValueError("Feirante inválido.")
        self._feirante = feirante

    def alterar_barraca(self, barraca):
        if barraca is None:
            raise ValueError("Barraca inválida.")
        self._barraca = barraca

    def alterar_data(self, data):
        try:
            data_limpa = data.strip()
            if not data_limpa:
                raise ValueError
            data_validada = datetime.strptime(data_limpa, self.FORMATO_DATA)
        except (ValueError, AttributeError) as erro:
            raise ValueError("Data inválida. Use o formato AAAA-MM-DD.") from erro
        if data_validada.strftime(self.FORMATO_DATA) != data_limpa:
            raise ValueError("Data inválida. Use o formato AAAA-MM-DD.")
        self._data = data_limpa

    def __repr__(self):
        return (
            f"Reserva({self._id}, {self._feirante.mostrar_nome()}, "
            f"{self._barraca.mostrar_codigo()}, {self._data})"
        )


def carregar_reservas(feirantes, barracas):
    feirantes_por_id = {f.mostrar_id(): f for f in feirantes}
    barracas_por_id = {b.mostrar_id(): b for b in barracas}
    reservas = []
    for registro in RESERVAS:
        feirante = feirantes_por_id.get(registro["feirante_id"])
        barraca = barracas_por_id.get(registro["barraca_id"])
        if feirante is None or barraca is None:
            raise ValueError("Mock de reserva referencia recurso inexistente.")
        reservas.append(
            Reserva(
                registro["id"],
                feirante,
                barraca,
                registro["data"],
            )
        )
    return reservas