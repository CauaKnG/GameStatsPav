from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import estatisticas_jogador_schema
from app.services import estatisticas_jogador_service

router = APIRouter()

@router.get("/", response_model=list[estatisticas_jogador_schema.EstatisticasJogadorResponse])
def listar_estatisticas(db: Session = Depends(get_db)):
    return estatisticas_jogador_service.listar_estatisticas_jogador(db)

@router.get("/{jogador_id}", response_model=list[estatisticas_jogador_schema.EstatisticasJogadorResponse])
def buscar_estatisticas_por_jogador(jogador_id: int, db: Session = Depends(get_db)):
    estatisticas = estatisticas_jogador_service.buscar_estatisticas_por_jogador(jogador_id, db)
    if not estatisticas:
        raise HTTPException(status_code=404, detail="Estatísticas do jogador não encontradas")
    return estatisticas

@router.post("/", response_model=estatisticas_jogador_schema.EstatisticasJogadorResponse, status_code=status.HTTP_201_CREATED)
def criar_estatisticas(estatisticas: estatisticas_jogador_schema.EstatisticasJogadorCreate, db: Session = Depends(get_db)):
    return estatisticas_jogador_service.criar_estatisticas_jogador(estatisticas, db)

@router.put("/{estatistica_id}")
def atualizar_estatisticas(
    estatistica_id: int,
    estatisticas: estatisticas_jogador_schema.EstatisticasJogadorCreate,
    db: Session = Depends(get_db)
):
    return estatisticas_jogador_service.atualizar_estatisticas_jogador(estatistica_id, estatisticas, db)

@router.delete("/{estatisticas_id}", response_model=estatisticas_jogador_schema.EstatisticasJogadorResponse)
def deletar_estatisticas(estatisticas_id: int, db: Session = Depends(get_db)):
    estatisticas = estatisticas_jogador_service.deletar_estatisticas_jogador(estatisticas_id, db)
    if not estatisticas:
        raise HTTPException(status_code=404, detail="Estatísticas não encontradas")
    return estatisticas
