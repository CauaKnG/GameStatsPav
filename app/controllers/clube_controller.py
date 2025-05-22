from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import clube_schema
from app.services import clube_service

router = APIRouter()

@router.get("/", response_model=list[clube_schema.ClubeResponse])
def listar_clubes(db: Session = Depends(get_db)):
    return clube_service.listar_clubes(db)

@router.get("/{clube_id}", response_model=clube_schema.ClubeResponse)
def buscar_clube(clube_id: int, db: Session = Depends(get_db)):
    clube = clube_service.buscar_clube_por_id(clube_id, db)
    if not clube:
        raise HTTPException(status_code=404, detail="Clube não encontrado")
    return clube

@router.post("/", response_model=clube_schema.ClubeResponse, status_code=status.HTTP_201_CREATED)
def criar_clube(clube: clube_schema.ClubeCreate, db: Session = Depends(get_db)):
    try:
        return clube_service.criar_clube(clube, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{clube_id}", response_model=clube_schema.ClubeResponse)
def atualizar_clube(clube_id: int, clube: clube_schema.ClubeUpdate, db: Session = Depends(get_db)):
    try:
        clube_atualizado = clube_service.atualizar_clube(clube_id, clube, db)
        if not clube_atualizado:
            raise HTTPException(status_code=404, detail="Clube não encontrado")
        return clube_atualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{clube_id}", response_model=clube_schema.ClubeResponse)
def deletar_clube(clube_id: int, db: Session = Depends(get_db)):
    try:
        clube = clube_service.deletar_clube(clube_id, db)
        if not clube:
            raise HTTPException(status_code=404, detail="Clube não encontrado")
        return clube
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
