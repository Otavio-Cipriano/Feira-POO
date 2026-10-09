from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.controllers.reserva_controller import (
    ConflitoReservaError,
    listar_reservas,
    registrar_reserva,
)

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])


class ReservaEntrada(BaseModel):
    barraca_id: int = Field(strict=True, gt=0)
    feirante_id: int = Field(strict=True, gt=0)
    data: str = Field(strict=True, min_length=1, max_length=10)

    class Config:
        extra = "forbid"


@router.get("")
def obter_reservas():
    return listar_reservas()


@router.post("", status_code=201)
def criar_reserva(entrada: ReservaEntrada):
    try:
        resultado = registrar_reserva(
            entrada.barraca_id,
            entrada.feirante_id,
            entrada.data,
        )
    except ConflitoReservaError as erro:
        raise HTTPException(status_code=409, detail=str(erro)) from erro
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro)) from erro

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Feirante ou barraca não encontrado.",
        )
    return resultado
