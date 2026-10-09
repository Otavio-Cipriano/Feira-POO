from app.models.barraca import carregar_barracas

# Estado em memória do módulo
barracas = carregar_barracas()


def _reservas():
    # Import local evita importação circular
    from app.controllers.reserva_controller import reservas
    return reservas


def _esta_reservada(barraca):
    # Verdadeiro se existe alguma reserva para a barraca
    return any(
        r.mostrar_barraca().mostrar_id() == barraca.mostrar_id()
        for r in _reservas()
    )


def _para_dicionario(barraca):
    # Converte o objeto barraca em dicionário
    return {
        "id": barraca.mostrar_id(),
        "codigo": barraca.mostrar_codigo(),
        "metragem": barraca.mostrar_metragem(),
        "taxa_diaria": barraca.calcular_taxa_diaria(),
        "disponivel": not _esta_reservada(barraca),
    }


def listar_barracas():
    # Retorna todas as barracas
    return [_para_dicionario(b) for b in barracas]


def buscar_barraca_por_id(barraca_id):
    # Retorna a barraca pelo id ou None se não existir
    for barraca in barracas:
        if barraca.mostrar_id() == barraca_id:
            return _para_dicionario(barraca)
    return None


def listar_barracas_disponiveis():
    # Retorna apenas barracas sem reserva, usando list comprehension
    return [_para_dicionario(b) for b in barracas if not _esta_reservada(b)]