from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.core.database import engine, Base
from app.routes.api_router import router as api_router

load_dotenv()

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

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"mensagem": "Bem-vindo à GameStats API! ⚽"}
