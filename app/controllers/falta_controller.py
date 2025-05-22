from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import falta_schema
from app.services import falta_service

router = APIRouter()

@router.get("/", response_model=list[falta_schema.FaltaResponse])
def listar_faltas(db: Session = Depends(get_db)):
    return falta_service.listar_faltas(db)

@router.get("/{falta_id}", response_model=falta_schema.FaltaResponse)
def buscar_falta(falta_id: int, db: Session = Depends(get_db)):
    falta = falta_service.buscar_falta_por_id(falta_id, db)
    if not falta:
        raise HTTPException(status_code=404, detail="Falta não encontrada")
    return falta

@router.post("/", response_model=falta_schema.FaltaResponse, status_code=status.HTTP_201_CREATED)
def criar_falta(falta: falta_schema.FaltaCreate, db: Session = Depends(get_db)):
    return falta_service.criar_falta(falta, db)

@router.put("/{falta_id}", response_model=falta_schema.FaltaResponse)
def atualizar_falta(falta_id: int, falta: falta_schema.FaltaUpdate, db: Session = Depends(get_db)):
    falta_atualizada = falta_service.atualizar_falta(falta_id, falta, db)
    if not falta_atualizada:
        raise HTTPException(status_code=404, detail="Falta não encontrada")
    return falta_atualizada

@router.delete("/{falta_id}", response_model=falta_schema.FaltaResponse)
def deletar_falta(falta_id: int, db: Session = Depends(get_db)):
    falta = falta_service.deletar_falta(falta_id, db)
    if not falta:
        raise HTTPException(status_code=404, detail="Falta não encontrada")
    return falta
