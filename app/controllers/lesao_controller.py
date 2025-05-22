from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import lesao_schema
from app.services import lesao_service

router = APIRouter()

@router.get("/", response_model=list[lesao_schema.LesaoResponse])
def listar_lesoes(db: Session = Depends(get_db)):
    return lesao_service.listar_lesoes(db)

@router.get("/{lesao_id}", response_model=lesao_schema.LesaoResponse)
def buscar_lesao(lesao_id: int, db: Session = Depends(get_db)):
    lesao = lesao_service.buscar_lesao_por_id(lesao_id, db)
    if not lesao:
        raise HTTPException(status_code=404, detail="Lesão não encontrada")
    return lesao

@router.post("/", response_model=lesao_schema.LesaoResponse, status_code=status.HTTP_201_CREATED)
def criar_lesao(lesao: lesao_schema.LesaoCreate, db: Session = Depends(get_db)):
    return lesao_service.criar_lesao(lesao, db)

@router.put("/{lesao_id}", response_model=lesao_schema.LesaoResponse)
def atualizar_lesao(lesao_id: int, lesao: lesao_schema.LesaoUpdate, db: Session = Depends(get_db)):
    lesao_atualizada = lesao_service.atualizar_lesao(lesao_id, lesao, db)
    if not lesao_atualizada:
        raise HTTPException(status_code=404, detail="Lesão não encontrada")
    return lesao_atualizada

@router.delete("/{lesao_id}", response_model=lesao_schema.LesaoResponse)
def deletar_lesao(lesao_id: int, db: Session = Depends(get_db)):
    lesao = lesao_service.deletar_lesao(lesao_id, db)
    if not lesao:
        raise HTTPException(status_code=404, detail="Lesão não encontrada")
    return lesao
