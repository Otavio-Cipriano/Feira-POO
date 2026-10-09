from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.controllers.reserva_controller import listar_reservas, registrar_reserva

router = APIRouter(
    prefix="/api/reservas",
    tags=["Reservas"]
)

class ReservaInput(BaseModel):
    barraca_id: int
    feirante_id: int
    data: str

@router.get("/")
def obter_reservas():
    return listar_reservas()

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_reserva(reserva_input: ReservaInput):
    try:
        reserva = registrar_reserva(
            reserva_input.barraca_id,
            reserva_input.feirante_id,
            reserva_input.data
        )
        if reserva is None:
            raise HTTPException(
                status_code=404,
                detail="Barraca ou feirante não encontrado."
            )
        return reserva
    except ValueError as e:
        msg = str(e)
        if "inválida" in msg.lower() or "formato" in msg.lower():
            raise HTTPException(status_code=422, detail=msg)
        else:
            raise HTTPException(status_code=409, detail=msg)