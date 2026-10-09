from app.models.feirante import Feirante
# from app.models.reserva import Reserva, carregar_reservas

# Estado em memória do módulo (lista vazia enquanto o Vinicius não cria o carregar_reservas)
reservas = []

def _para_dicionario(reserva):
    return {
        "id": reserva.mostrar_id(),
        "barraca_id": reserva.mostrar_barraca().mostrar_id(),
        "feirante_id": reserva.mostrar_feirante().mostrar_id(),
        "data": reserva.mostrar_data(),
        "taxa_diaria": reserva.mostrar_barraca().calcular_taxa_diaria(),
    }

def _buscar_barraca(barraca_id):
    from app.controllers.barraca_controller import barracas
    return next((b for b in barracas if b.mostrar_id() == barraca_id), None)

def _buscar_feirante(feirante_id):
    from app.controllers.feirante_controller import feirantes
    return next((f for f in feirantes if f.mostrar_id() == feirante_id), None)

def registrar_reserva(barraca_id, feirante_id, data):
    barraca = _buscar_barraca(barraca_id)
    feirante = _buscar_feirante(feirante_id)
    if barraca is None or feirante is None:
        return None

    if any(r.mostrar_barraca().mostrar_id() == barraca_id and r.mostrar_data() == data for r in reservas):
        raise ValueError("Barraca já reservada nesta data.")

    # Busca a constante da própria classe, regra de negócio no modelo!
    total_feirante = len([r for r in reservas if r.mostrar_feirante().mostrar_id() == feirante_id])
    if total_feirante >= Feirante.LIMITE_RESERVAS:
        raise ValueError(f"Feirante atingiu o limite de {Feirante.LIMITE_RESERVAS} reservas.")

    raise NotImplementedError("A criação real do objeto Reserva depende da classe do Vinicius!")
    # Quando ele criar:
    # nova = Reserva(len(reservas) + 1, feirante, barraca, data)
    # reservas.append(nova)
    # return _para_dicionario(nova)

def calcular_faturamento_total():
    return sum(r.mostrar_barraca().calcular_taxa_diaria() for r in reservas)