import ast
from pathlib import Path

from app.controllers import reserva_controller
from app.data.barraca_mock import BARRACAS
from app.data.feirante_mock import FEIRANTES
from app.data.reserva_mock import RESERVAS
from app.models.barraca import (
    Barraca,
    BarracaAlimentacao,
    BarracaGourmet,
    carregar_barracas,
)
from app.models.feirante import Feirante, carregar_feirantes
from app.models.reserva import Reserva, carregar_reservas
from main import app


ROOT = Path(__file__).resolve().parent
checks = 0


def verificar(condicao, mensagem):
    global checks
    checks += 1
    if not condicao:
        raise AssertionError(mensagem)


def esperar_value_error(acao):
    try:
        acao()
    except ValueError:
        return True
    return False


def nomes_de_classes_e_imports(caminho):
    arvore = ast.parse(caminho.read_text(encoding="utf-8"))
    return [
        no
        for no in ast.walk(arvore)
        if isinstance(no, (ast.ClassDef, ast.Import, ast.ImportFrom))
    ]


for caminho in (
    "app/__init__.py",
    "app/data/__init__.py",
    "app/models/__init__.py",
    "app/controllers/__init__.py",
    "app/routes/__init__.py",
    "app/data/feirante_mock.py",
    "app/data/barraca_mock.py",
    "app/data/reserva_mock.py",
    "app/models/feirante.py",
    "app/models/barraca.py",
    "app/models/reserva.py",
    "app/controllers/barraca_controller.py",
    "app/controllers/feirante_controller.py",
    "app/controllers/reserva_controller.py",
    "app/routes/barraca_routes.py",
    "app/routes/feirante_routes.py",
    "app/routes/reserva_routes.py",
    "app/routes/relatorio_routes.py",
    "main.py",
):
    verificar((ROOT / caminho).is_file(), f"Arquivo obrigatório ausente: {caminho}")

verificar(len(FEIRANTES) >= 5, "O mock deve conter pelo menos 5 feirantes.")
verificar(len(BARRACAS) >= 5, "O mock deve conter pelo menos 5 barracas.")
verificar(len(RESERVAS) >= 5, "O mock deve conter pelo menos 5 reservas.")
verificar(
    all(
        not nomes_de_classes_e_imports(caminho)
        for caminho in (ROOT / "app" / "data").glob("*_mock.py")
    ),
    "Os mocks devem conter apenas dados estáticos.",
)

modelos = tuple((ROOT / "app" / "models").glob("*.py"))
codigo_modelos = "\n".join(caminho.read_text(encoding="utf-8") for caminho in modelos)
verificar("fastapi" not in codigo_modelos.lower(), "Modelos não podem importar FastAPI.")
verificar(
    "isinstance(" not in codigo_modelos and "type(" not in codigo_modelos,
    "Modelos não devem usar verificações de tipo.",
)

for controller in (
    ROOT / "app" / "controllers" / "barraca_controller.py",
    ROOT / "app" / "controllers" / "feirante_controller.py",
    ROOT / "app" / "controllers" / "reserva_controller.py",
):
    codigo = controller.read_text(encoding="utf-8")
    arvore = ast.parse(codigo)
    verificar(
        any(
            isinstance(no, ast.FunctionDef) and no.name == "_para_dicionario"
            for no in ast.walk(arvore)
        ),
        f"{controller.name} deve definir _para_dicionario().",
    )
    verificar("fastapi" not in codigo.lower(), f"{controller.name} não deve usar HTTP.")

feirante = Feirante(99, "Teste", "12345678901", "11999999999")
verificar(feirante.mostrar_documento() == "12345678901", "Documento válido não carregou.")
verificar(
    esperar_value_error(lambda: feirante.alterar_documento("123")),
    "Documento inválido deveria lançar ValueError.",
)
verificar(
    esperar_value_error(lambda: Barraca(99, "X", 0)),
    "Metragem zero deveria lançar ValueError.",
)
verificar(
    esperar_value_error(lambda: Barraca(99, "X", float("nan"))),
    "Metragem não finita deveria lançar ValueError.",
)

barracas = carregar_barracas()
verificar(
    [b.calcular_taxa_diaria() for b in barracas[:1]]
    + [b.calcular_taxa_diaria() for b in barracas[2:3]]
    + [b.calcular_taxa_diaria() for b in barracas[4:5]]
    == [50.0, 80.0, 120.0],
    "Taxas polimórficas devem ser 50, 80 e 120.",
)
verificar(issubclass(BarracaGourmet, BarracaAlimentacao), "Hierarquia Gourmet inválida.")
verificar(issubclass(BarracaAlimentacao, Barraca), "Hierarquia Alimentação inválida.")
verificar(
    esperar_value_error(lambda: Reserva(99, feirante, barracas[0], "2026-02-30")),
    "Data inválida deveria lançar ValueError.",
)
verificar(
    len(carregar_reservas(carregar_feirantes(), barracas)) == len(RESERVAS),
    "Reservas do mock não foram carregadas.",
)

registro = reserva_controller.registrar_reserva(6, 4, "2026-10-15")
verificar(
    registro is not None and registro["feirante_id"] == 4,
    "Não foi possível registrar uma reserva válida.",
)
verificar(
    esperar_value_error(
        lambda: reserva_controller.registrar_reserva(1, 5, "2026-10-15")
    ),
    "Reserva duplicada deveria gerar ValueError.",
)
verificar(
    esperar_value_error(
        lambda: reserva_controller.registrar_reserva(2, 4, "2026-10-22")
    ),
    "Limite de reservas do feirante deveria ser aplicado.",
)
verificar(
    reserva_controller.registrar_reserva(999, 4, "2026-11-01") is None,
    "ID inexistente deveria retornar None.",
)

especificacao_api = app.openapi()
rotas = {
    (metodo.upper(), caminho)
    for caminho, operacoes in especificacao_api["paths"].items()
    for metodo in operacoes
}
for metodo, caminho in (
    ("GET", "/api/barracas"),
    ("GET", "/api/barracas/disponiveis"),
    ("GET", "/api/barracas/{id}"),
    ("GET", "/api/feirantes"),
    ("GET", "/api/feirantes/{id}"),
    ("POST", "/api/reservas"),
    ("GET", "/api/reservas"),
    ("GET", "/api/feirantes/{id}/reservas"),
    ("GET", "/api/relatorio/faturamento"),
):
    verificar((metodo, caminho) in rotas, f"Rota ausente: {metodo} {caminho}")

verificar(
    "201" in especificacao_api["paths"]["/api/reservas"]["post"]["responses"],
    "POST /api/reservas deve responder 201.",
)
verificar(
    "uvicorn main:app --reload" in (ROOT / "README.md").read_text(encoding="utf-8"),
    "README deve documentar o comando de execução.",
)

print(f"OK: {checks} verificações passaram.")
