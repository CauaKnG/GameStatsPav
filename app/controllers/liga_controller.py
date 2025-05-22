from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import liga_schema
from app.services import liga_service

router = APIRouter()

@router.get("/", response_model=list[liga_schema.LigaResponse])
def listar_ligas(db: Session = Depends(get_db)):
    return liga_service.listar_ligas(db)

@router.get("/{liga_id}", response_model=liga_schema.LigaResponse)
def buscar_liga(liga_id: int, db: Session = Depends(get_db)):
    liga = liga_service.buscar_liga_por_id(liga_id, db)
    if not liga:
        raise HTTPException(status_code=404, detail="Liga não encontrada")
    return liga

@router.post("/", response_model=liga_schema.LigaResponse, status_code=status.HTTP_201_CREATED)
def criar_liga(liga: liga_schema.LigaCreate, db: Session = Depends(get_db)):
    return liga_service.criar_liga(liga, db)

@router.put("/{liga_id}", response_model=liga_schema.LigaResponse)
def atualizar_liga(liga_id: int, liga: liga_schema.LigaUpdate, db: Session = Depends(get_db)):
    liga_atualizada = liga_service.atualizar_liga(liga_id, liga, db)
    if not liga_atualizada:
        raise HTTPException(status_code=404, detail="Liga não encontrada")
    return liga_atualizada

@router.delete("/{liga_id}", response_model=liga_schema.LigaResponse)
def deletar_liga(liga_id: int, db: Session = Depends(get_db)):
    liga = liga_service.deletar_liga(liga_id, db)
    if not liga:
        raise HTTPException(status_code=404, detail="Liga não encontrada")
    return liga
