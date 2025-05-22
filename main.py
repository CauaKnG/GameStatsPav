from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.core.database import engine, Base
from app.controllers import jogador_controller, clube_controller,liga_controller,partida_controller, lesao_controller, falta_controller, estatisticas_jogador_controller

load_dotenv()  # Carrega as variáveis do .env

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GameStats API",
    description="API para gerenciar jogadores, partidas e estatísticas em jogos de futebol estilo FIFA/PES.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui rotas dos controladores
app.include_router(jogador_controller.router, prefix="/jogadores", tags=["Jogadores"])
app.include_router(clube_controller.router, prefix="/clubes", tags=["Clubes"])
app.include_router(liga_controller.router, prefix="/ligas", tags=["Ligas"])
app.include_router(partida_controller.router, prefix="/partidas", tags=["Partidas"])
app.include_router(lesao_controller.router, prefix="/lesoes", tags=["Lesões"])
app.include_router(falta_controller.router, prefix="/faltas", tags=["Faltas"])
app.include_router(estatisticas_jogador_controller.router, prefix="/estatisticas_jogador", tags=["Estatísticas Jogador"])

# Endpoint raiz
@app.get("/")
def read_root():
    return {"mensagem": "Bem-vindo à GameStats API! ⚽"}
