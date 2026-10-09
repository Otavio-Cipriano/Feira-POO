from app.models.feirante import carregar_feirantes

# Estado em memória do módulo
feirantes = carregar_feirantes()

def _para_dicionario(feirante):
    return {
        "id": feirante.mostrar_id(),
        "nome": feirante.mostrar_nome(),
    }

def _reserva_para_dicionario(reserva):
    return {
        "id": reserva.mostrar_id(),
        "barraca_id": reserva.mostrar_barraca().mostrar_id(),
        "feirante_id": reserva.mostrar_feirante().mostrar_id(),
        "data": reserva.mostrar_data(),
    }

def listar_feirantes():
    return [_para_dicionario(f) for f in feirantes]

def buscar_feirante_por_id(feirante_id):
    for feirante in feirantes:
        if feirante.mostrar_id() == feirante_id:
            return _para_dicionario(feirante)
    return None

def historico_reservas(feirante_id):
    if buscar_feirante_por_id(feirante_id) is None:
        return None
        
    # Importação local para evitar erro de circularidade
    from app.controllers.reserva_controller import reservas
    
    return [
        _reserva_para_dicionario(r)
        for r in reservas
        if r.mostrar_feirante().mostrar_id() == feirante_id
    ]