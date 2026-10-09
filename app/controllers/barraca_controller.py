from app.models.barraca import carregar_barracas

# Estado em memória do módulo
barracas = carregar_barracas()

def _para_dicionario(barraca):
    from app.controllers.reserva_controller import reservas
    ocupada = any(r.mostrar_barraca().mostrar_id() == barraca.mostrar_id() for r in reservas)
    
    return {
        "id": barraca.mostrar_id(),
        "codigo": barraca.mostrar_codigo(),
        "taxa_diaria": barraca.calcular_taxa_diaria(),
        "disponivel": not ocupada,
    }

def listar_barracas():
    return [_para_dicionario(b) for b in barracas]

def buscar_barraca_por_id(barraca_id):
    for barraca in barracas:
        if barraca.mostrar_id() == barraca_id:
            return _para_dicionario(barraca)
    return None

def listar_barracas_disponiveis():
    from app.controllers.reserva_controller import reservas
    
    # Exigência do PDF: filtro com compreensão de lista
    return [
        _para_dicionario(b) 
        for b in barracas 
        if not any(r.mostrar_barraca().mostrar_id() == b.mostrar_id() for r in reservas)
    ]