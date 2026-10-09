from app.models.feirante import carregar_feirantes

# Estado em memória do módulo
feirantes = carregar_feirantes()


def _para_dicionario(feirante):
    # Converte o objeto feirante em dicionário
    return {
        "id": feirante.mostrar_id(),
        "nome": feirante.mostrar_nome(),
        "documento": feirante.mostrar_documento(),
        "telefone": feirante.mostrar_telefone(),
    }


def _reserva_para_dicionario(reserva):
    # Converte a reserva em dicionário para o histórico
    return {
        "id": reserva.mostrar_id(),
        "barraca_id": reserva.mostrar_barraca().mostrar_id(),
        "feirante_id": reserva.mostrar_feirante().mostrar_id(),
        "data": reserva.mostrar_data(),
    }


def listar_feirantes():
    # Retorna todos os feirantes
    return [_para_dicionario(f) for f in feirantes]


def buscar_feirante_por_id(feirante_id):
    # Retorna o feirante pelo id ou None se não existir
    for feirante in feirantes:
        if feirante.mostrar_id() == feirante_id:
            return _para_dicionario(feirante)
    return None


def historico_reservas(feirante_id):
    # Retorna None se o feirante não existe
    if buscar_feirante_por_id(feirante_id) is None:
        return None

    # Import local evita importação circular
    from app.controllers.reserva_controller import reservas

    # Retorna lista vazia se o feirante não tem reservas
    return [
        _reserva_para_dicionario(r)
        for r in reservas
        if r.mostrar_feirante().mostrar_id() == feirante_id
    ]