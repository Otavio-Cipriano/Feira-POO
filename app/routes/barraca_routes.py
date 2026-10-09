
from fastapi import APIRouter, HTTPException

from app.controllers.barraca_controller import (
    listar_barracas,
    listar_barracas_disponiveis,
    buscar_barraca_por_id,
)

router = APIRouter(
    prefix="/api/barracas",
    tags=["Barracas"]
)


@router.get("/")
def obter_barracas():
    return listar_barracas()


@router.get("/disponiveis")
def obter_barracas_disponiveis():
    return listar_barracas_disponiveis()


@router.get("/{id}")
def obter_barraca(id: int):
    barraca = buscar_barraca_por_id(id)

    if barraca is None:
        raise HTTPException(
            status_code=404,
            detail="Barraca não encontrada."
        )

    return barraca