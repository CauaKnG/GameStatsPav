from fastapi import APIRouter
from app.controllers import (
    jogador_controller,
    clube_controller,
    liga_controller,
    partida_controller,
    lesao_controller,
    falta_controller,
    estatisticas_jogador_controller
)

router = APIRouter()

router.include_router(jogador_controller.router, prefix="/jogadores", tags=["Jogadores"])
router.include_router(clube_controller.router, prefix="/clubes", tags=["Clubes"])
router.include_router(liga_controller.router, prefix="/ligas", tags=["Ligas"])
router.include_router(partida_controller.router, prefix="/partidas", tags=["Partidas"])
router.include_router(lesao_controller.router, prefix="/lesoes", tags=["Lesões"])
router.include_router(falta_controller.router, prefix="/faltas", tags=["Faltas"])
router.include_router(estatisticas_jogador_controller.router, prefix="/estatisticas_jogador", tags=["Estatísticas Jogador"])