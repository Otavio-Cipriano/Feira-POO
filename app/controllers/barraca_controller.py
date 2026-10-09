from app.models.barraca import carregar_barracas

barracas = carregar_barracas()

def _reservas():
    from app.controllers.reserva_controller import reservas
    return reservas


def _esta_reservada(barraca):
    return any(
        r.mostrar_barraca().mostrar_id() == barraca.mostrar_id()
        for r in _reservas()
    )


def _para_dicionario(barraca):
    return {
        "id": barraca.mostrar_id(),
        "codigo": barraca.mostrar_codigo(),
        "metragem": barraca.mostrar_metragem(),
        "taxa_diaria": barraca.calcular_taxa_diaria(),
        "disponivel": not _esta_reservada(barraca),
    }


def listar_barracas():
    return [_para_dicionario(b) for b in barracas]


def buscar_barraca_por_id(barraca_id):
    for barraca in barracas:
        if barraca.mostrar_id() == barraca_id:
            return _para_dicionario(barraca)
    return None


def listar_barracas_disponiveis():
    return [_para_dicionario(b) for b in barracas if not _esta_reservada(b)]