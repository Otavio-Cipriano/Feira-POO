from app.models.feirante import Feirante
from app.models.reserva import Reserva, carregar_reservas
from app.controllers.barraca_controller import barracas
from app.controllers.feirante_controller import feirantes


class ConflitoReservaError(ValueError):
    """Indica conflito com as regras de capacidade de reservas."""


# Estado em memória do módulo, carregado do mock
reservas = carregar_reservas(feirantes, barracas)


def _para_dicionario(reserva):
    # Converte a reserva em dicionário
    return {
        "id": reserva.mostrar_id(),
        "barraca_id": reserva.mostrar_barraca().mostrar_id(),
        "feirante_id": reserva.mostrar_feirante().mostrar_id(),
        "data": reserva.mostrar_data(),
        "taxa_diaria": reserva.mostrar_barraca().calcular_taxa_diaria(),
    }


def _buscar_barraca(barraca_id):
    # Retorna o objeto barraca ou None
    return next((b for b in barracas if b.mostrar_id() == barraca_id), None)


def _buscar_feirante(feirante_id):
    # Retorna o objeto feirante ou None
    return next((f for f in feirantes if f.mostrar_id() == feirante_id), None)


def _proximo_id():
    # Gera o próximo id sem repetir ids existentes
    return max((r.mostrar_id() for r in reservas), default=0) + 1


def listar_reservas():
    # Retorna todas as reservas
    return [_para_dicionario(r) for r in reservas]


def registrar_reserva(barraca_id, feirante_id, data):
    # Retorna None se barraca ou feirante não existem
    barraca = _buscar_barraca(barraca_id)
    feirante = _buscar_feirante(feirante_id)
    if barraca is None or feirante is None:
        return None

    nova = Reserva(_proximo_id(), feirante, barraca, data)

    if any(
        r.mostrar_barraca().mostrar_id() == barraca_id
        and r.mostrar_data() == nova.mostrar_data()
        for r in reservas
    ):
        raise ConflitoReservaError("Barraca já reservada nesta data.")

    total_feirante = sum(
        r.mostrar_feirante().mostrar_id() == feirante_id for r in reservas
    )
    if total_feirante >= Feirante.LIMITE_RESERVAS:
        raise ConflitoReservaError(
            f"Feirante atingiu o limite de {Feirante.LIMITE_RESERVAS} reservas."
        )

    # Salva a reserva e retorna os dados
    reservas.append(nova)
    return _para_dicionario(nova)


def calcular_faturamento_total():
    # Soma a taxa diária de todas as reservas ativas
    return sum(r.mostrar_barraca().calcular_taxa_diaria() for r in reservas)