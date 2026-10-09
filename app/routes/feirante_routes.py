
from fastapi import APIRouter, HTTPException, Path

from app.controllers.feirante_controller import (
    listar_feirantes,
    buscar_feirante_por_id,
    historico_reservas,
)

router = APIRouter(
    prefix="/api/feirantes",
    tags=["Feirantes"]
)


@router.get("")
def obter_feirantes():
    return listar_feirantes()


@router.get("/{id}")
def obter_feirante(id: int = Path(gt=0)):
    feirante = buscar_feirante_por_id(id)

    if feirante is None:
        raise HTTPException(
            status_code=404,
            detail="Feirante não encontrado."
        )

    return feirante


@router.get("/{id}/reservas")
def obter_historico_reservas(id: int = Path(gt=0)):
    historico = historico_reservas(id)

    if historico is None:
        raise HTTPException(
            status_code=404,
            detail="Feirante não encontrado."
        )

    return historico