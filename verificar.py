"""Verificacao do dominio Feira-POO.

Roda sem subir a API: testa models e controllers, como o exemplo do Kioferta.
"""
from app.controllers import reserva_controller
from app.controllers.barraca_controller import (
    listar_barracas,
    listar_barracas_disponiveis,
)
from app.controllers.feirante_controller import (
    historico_reservas,
    listar_feirantes,
)
from app.data.barraca_mock import BARRACAS
from app.data.feirante_mock import FEIRANTES
from app.data.reserva_mock import RESERVAS
from app.models.barraca import (
    BARRACAS_TIPOS,
    Barraca,
    BarracaAlimentacao,
    BarracaGourmet,
    carregar_barracas,
)
from app.models.feirante import Feirante, carregar_feirantes
from app.models.reserva import Reserva, carregar_reservas


falhas = 0


def checar(ok, descricao):
    global falhas
    if ok:
        print(f"  ok      {descricao}")
    else:
        print(f"  FALHOU  {descricao}")
        falhas += 1


def rejeita_value_error(acao):
    try:
        acao()
    except ValueError:
        return True
    return False


print("\n1. Encapsulamento: o objeto nasce valido")
feirante_teste = Feirante(99, "Teste", "12345678901", "11999999999")
checar(
    feirante_teste.mostrar_documento() == "12345678901",
    "Feirante guarda o documento valido",
)
checar(
    rejeita_value_error(
        lambda: Feirante(99, "Teste", "123", "11999999999")
    ),
    "construtor recusa documento invalido",
)
checar(
    rejeita_value_error(lambda: Barraca(99, "B99", 0)),
    "construtor recusa metragem igual a zero",
)
checar(
    rejeita_value_error(lambda: Barraca(99, "B99", float("nan"))),
    "construtor recusa metragem nao finita",
)
checar(not hasattr(Feirante, "alterar_id"), "nao existe alterar_id")

print("\n2. Heranca: a hierarquia de barracas esta correta")
checar(issubclass(BarracaAlimentacao, Barraca), "Alimentacao herda de Barraca")
checar(
    BarracaGourmet.__base__ is BarracaAlimentacao,
    "Gourmet herda diretamente de Alimentacao",
)
checar(Barraca.TAXA_BASE == 50.0, "Barraca define taxa base 50")
checar(BarracaAlimentacao.TAXA_BASE == 80.0, "Alimentacao define taxa base 80")
checar(BarracaGourmet.TAXA_BASE == 120.0, "Gourmet define taxa base 120")
checar(
    "calcular_taxa_diaria" in BarracaGourmet.__dict__,
    "Gourmet sobrescreve calcular_taxa_diaria",
)

print("\n3. Polimorfismo: uma chamada calcula taxas diferentes")
taxas = {
    tipo: classe(99, "TESTE", 10).calcular_taxa_diaria()
    for tipo, classe in BARRACAS_TIPOS.items()
}
checar(
    taxas == {"barraca": 50.0, "alimentacao": 80.0, "gourmet": 120.0},
    "cada tipo calcula sua taxa pelo mesmo metodo",
)
checar(
    all(isinstance(barraca, Barraca) for barraca in carregar_barracas()),
    "o carregador instancia objetos da hierarquia Barraca",
)

print("\n4. Validacao: os modelos rejeitam dados invalidos")
checar(
    rejeita_value_error(
        lambda: Feirante(99, "Teste", "123", "11999999999")
    ),
    "Feirante rejeita documento fora do tamanho permitido",
)
barraca_teste = Barraca(99, "B99", 10)
checar(
    rejeita_value_error(
        lambda: Reserva(99, feirante_teste, barraca_teste, "")
    ),
    "Reserva rejeita data vazia",
)
checar(
    rejeita_value_error(
        lambda: Reserva(99, feirante_teste, barraca_teste, "2026-02-30")
    ),
    "Reserva rejeita data inexistente",
)
checar(
    rejeita_value_error(lambda: Reserva(99, None, barraca_teste, "2026-10-15")),
    "Reserva rejeita feirante ausente",
)

print("\n5. Associacao: Reserva guarda objetos, nao apenas ids")
feirantes = carregar_feirantes()
barracas = carregar_barracas()
reservas = carregar_reservas(feirantes, barracas)
primeira_reserva = reservas[0]
checar(
    isinstance(primeira_reserva.mostrar_feirante(), Feirante),
    "mostrar_feirante devolve um objeto Feirante",
)
checar(
    isinstance(primeira_reserva.mostrar_barraca(), Barraca),
    "mostrar_barraca devolve um objeto Barraca",
)
checar(
    len(reservas) == len(RESERVAS),
    "carregar_reservas instancia os dados do mock",
)

print("\n6. Regras de negocio: reservas duplicadas e limite")
checar(
    rejeita_value_error(
        lambda: reserva_controller.registrar_reserva(1, 5, "2026-10-15")
    ),
    "recusa barraca ja reservada na mesma data",
)
checar(
    rejeita_value_error(
        lambda: reserva_controller.registrar_reserva(6, 1, "2026-11-01")
    ),
    "recusa feirante que atingiu o limite de reservas",
)
checar(
    reserva_controller.registrar_reserva(999, 5, "2026-11-01") is None,
    "recurso inexistente retorna None no controller",
)

print("\n7. Colecoes: controllers filtram e consultam os dados")
checar(
    len(listar_feirantes()) == len(FEIRANTES),
    "controller lista os feirantes do mock",
)
checar(
    len(listar_barracas()) == len(BARRACAS),
    "controller lista as barracas do mock",
)
disponiveis = listar_barracas_disponiveis()
checar(
    len(disponiveis) > 0
    and all(barraca["disponivel"] for barraca in disponiveis),
    "controller retorna apenas barracas disponiveis",
)
checar(
    len(historico_reservas(1)) == 2,
    "historico retorna as duas reservas do feirante 1",
)
checar(
    historico_reservas(999) is None,
    "historico de feirante inexistente retorna None",
)
checar(
    reserva_controller.calcular_faturamento_total() > 0,
    "faturamento soma taxas das reservas",
)
reserva_criada = reserva_controller.registrar_reserva(6, 5, "2026-11-01")
checar(
    reserva_criada is not None and reserva_criada["barraca_id"] == 6,
    "registra reserva valida para recursos existentes",
)

print("\n8. Camadas: models e controllers nao conhecem FastAPI")
import app.controllers.barraca_controller as bc
import app.controllers.feirante_controller as fc
import app.controllers.reserva_controller as rc
import app.models.barraca as mb
import app.models.feirante as mf
import app.models.reserva as mr

for modulo in (mb, mf, mr):
    conteudo = open(modulo.__file__, encoding="utf-8").read().lower()
    nome = modulo.__name__.split(".")[-1]
    checar("fastapi" not in conteudo, f"{nome}.py nao importa FastAPI")

for modulo in (bc, fc, rc):
    conteudo = open(modulo.__file__, encoding="utf-8").read()
    nome = modulo.__name__.split(".")[-1]
    checar("HTTPException" not in conteudo, f"{nome}.py nao usa HTTPException")

print()
if falhas == 0:
    print("TUDO CERTO. Agora suba a API e teste no /docs.")
else:
    print(f"{falhas} verificacao(oes) falharam.")
    raise SystemExit(1)
