from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.partida_schema import PartidaCreate, PartidaUpdate, PartidaResponse
from app.services import partida_service
from app.services.partida_service import formatar_partida_response
from app.models.models import Clube,Partida
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=list[PartidaResponse])
def listar_partidas(db: Session = Depends(get_db)):
    return partida_service.listar_partidas(db)

@router.get("/{partida_id}", response_model=PartidaResponse)
def buscar_partida(partida_id: int, db: Session = Depends(get_db)):
    partida = partida_service.buscar_partida_por_id(partida_id, db)
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return partida

@router.post("/", response_model=PartidaResponse)
def criar_partida(partida: PartidaCreate, db: Session = Depends(get_db)):
    try:
        partida_criada = partida_service.criar_partida(partida, db)
        return formatar_partida_response(partida_criada)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{partida_id}", response_model=PartidaResponse)
def atualizar_partida(partida_id: int, partida: PartidaUpdate, db: Session = Depends(get_db)):
    clube_casa = db.query(Clube).filter(Clube.nome == partida.clube_casa).first()
    clube_fora = db.query(Clube).filter(Clube.nome == partida.clube_fora).first()

    if not clube_casa or not clube_fora:
        raise HTTPException(status_code=404, detail="Clube casa ou fora não encontrado")

    partida_db = db.query(Partida).filter(Partida.id == partida_id).first()
    if not partida_db:
        raise HTTPException(status_code=404, detail="Partida não encontrada")

    partida_db.data_partida = partida.data_partida
    partida_db.local = partida.local
    partida_db.clube_casa_id = clube_casa.id
    partida_db.clube_fora_id = clube_fora.id
    partida_db.gols_casa = partida.gols_casa
    partida_db.gols_fora = partida.gols_fora

    db.commit()
    db.refresh(partida_db)

    return formatar_partida_response(partida_db)

@router.delete("/{partida_id}", response_model=PartidaResponse)
def deletar_partida(partida_id: int, db: Session = Depends(get_db)):
    partida = partida_service.deletar_partida(partida_id, db)
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return partida
