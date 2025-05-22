from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import models
from app.services import jogador_service
from app.schemas import jogador_schema
from app.core.database import get_db

router = APIRouter( tags=["Jogadores"])

@router.post("/", response_model=jogador_schema.JogadorResponse)
def criar_jogador(jogador: jogador_schema.JogadorCreate, db: Session = Depends(get_db)):
    try:
        novo_jogador = models.Jogador(**jogador.dict())
        return jogador_service.adicionar_jogador(db, novo_jogador)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[jogador_schema.JogadorResponse])
def listar_jogadores(db: Session = Depends(get_db)):
    return db.query(models.Jogador).all()


@router.get("/{jogador_id}", response_model=jogador_schema.JogadorResponse)
def obter_jogador(jogador_id: int, db: Session = Depends(get_db)):
    jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return jogador


@router.put("/{jogador_id}", response_model=jogador_schema.JogadorResponse)
def atualizar_jogador(jogador_id: int, jogador_dados: jogador_schema.JogadorUpdate, db: Session = Depends(get_db)):
    try:
        return jogador_service.editar_jogador(db, jogador_id, jogador_dados.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{jogador_id}")
def deletar_jogador(jogador_id: int, db: Session = Depends(get_db)):
    jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    db.delete(jogador)
    db.commit()
    return {"detail": "Jogador excluído com sucesso"}
