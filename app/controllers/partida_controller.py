from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import partida_schema
from app.services import partida_service

router = APIRouter()

@router.get("/", response_model=list[partida_schema.PartidaResponse])
def listar_partidas(db: Session = Depends(get_db)):
    return partida_service.listar_partidas(db)

@router.get("/{partida_id}", response_model=partida_schema.PartidaResponse)
def buscar_partida(partida_id: int, db: Session = Depends(get_db)):
    partida = partida_service.buscar_partida_por_id(partida_id, db)
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return partida

@router.post("/", response_model=partida_schema.PartidaResponse, status_code=status.HTTP_201_CREATED)
def criar_partida(partida: partida_schema.PartidaCreate, db: Session = Depends(get_db)):
    return partida_service.criar_partida(partida, db)

@router.put("/{partida_id}", response_model=partida_schema.PartidaResponse)
def atualizar_partida(partida_id: int, partida: partida_schema.PartidaUpdate, db: Session = Depends(get_db)):
    partida_atualizada = partida_service.atualizar_partida(partida_id, partida, db)
    if not partida_atualizada:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return partida_atualizada

@router.delete("/{partida_id}", response_model=partida_schema.PartidaResponse)
def deletar_partida(partida_id: int, db: Session = Depends(get_db)):
    partida = partida_service.deletar_partida(partida_id, db)
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return partida
