from fastapi import FastAPI

from app.routes import (
    barraca_routes,
    feirante_routes,
    relatorio_routes,
    reserva_routes,
)

app = FastAPI(
    title="Feira de Bairro API",
    description="Sistema de gestão de feira de bairro",
    version="1.0.0"
)


@app.get("/")
def raiz():
    return {"mensagem": "API da Feira de Bairro rodando! Acesse /docs para a documentação."}

app.include_router(barraca_routes.router)
app.include_router(feirante_routes.router)
app.include_router(reserva_routes.router)
app.include_router(relatorio_routes.router)
