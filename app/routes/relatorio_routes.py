
from fastapi import APIRouter

from app.controllers.reserva_controller import calcular_faturamento_total

router = APIRouter(
    prefix="/api/relatorio",
    tags=["Relatórios"]
)


@router.get("/faturamento")
def obter_relatorio_faturamento():
    faturamento = calcular_faturamento_total()

    return {
        "faturamento_total": faturamento
    }