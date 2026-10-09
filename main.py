from fastapi import FastAPI

# Importações dos roteadores (comentadas até o Vinicius criar a pasta app/routes/)
# from app.routes import barraca_routes, feirante_routes, reserva_routes, relatorio_routes

app = FastAPI(
    title="Feira de Bairro API",
    description="Sistema de gestão de feira de bairro",
    version="1.0.0"
)

@app.get("/")
def raiz():
    return {"mensagem": "API da Feira de Bairro rodando! Acesse /docs para a documentação."}

# Inclusão das rotas (comentadas até o Vinicius criar a pasta app/routes/)
# app.include_router(barraca_routes.router, prefix="/api", tags=["Barracas"])
# app.include_router(feirante_routes.router, prefix="/api", tags=["Feirantes"])
# app.include_router(reserva_routes.router, prefix="/api", tags=["Reservas"])
# app.include_router(relatorio_routes.router, prefix="/api", tags=["Relatórios"])
