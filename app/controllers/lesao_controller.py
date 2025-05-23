from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import models
from app.models.models import Lesao, Jogador
from app.schemas import lesao_schema
from app.schemas.lesao_schema import LesaoResponse, LesaoCreate, LesaoUpdate
from app.services import lesao_service

from typing import List

router = APIRouter()



@router.get("/", response_model=list[LesaoResponse])
def listar_lesoes(db: Session = Depends(get_db)):
    resultados = db.query(
        Lesao.id,
        Lesao.jogador_id,
        Lesao.data_lesao,
        Lesao.tipo_lesao,
        Lesao.duracao_estimada_dias,
        Jogador.nome.label("nome_jogador")
    ).join(Jogador, Lesao.jogador_id == Jogador.id).all()

    return [LesaoResponse(**lesao._asdict()) for lesao in resultados]

@router.get("/{lesao_id}", response_model=lesao_schema.LesaoResponse)
def buscar_lesao_por_id(lesao_id: int, db: Session = Depends(get_db)):
    resultado = db.query(
        Lesao.id,
        Lesao.jogador_id,
        Lesao.tipo_lesao,
        Lesao.data_lesao,
        Jogador.nome.label("nome_jogador")
    ).join(Jogador, Lesao.jogador_id == Jogador.id).filter(Lesao.id == lesao_id).first()

    if not resultado:
        raise HTTPException(status_code=404, detail="Lesão não encontrada")

    return LesaoResponse(**resultado._asdict())

@router.post("/", response_model=lesao_schema.LesaoResponse, status_code=status.HTTP_201_CREATED)
def criar_lesao(lesao: lesao_schema.LesaoCreate, db: Session = Depends(get_db)):
    return lesao_service.criar_lesao(lesao, db)


@router.put("/{lesao_id}", response_model=lesao_schema.LesaoResponse)
def atualizar_lesao(lesao_id: int, lesao: LesaoUpdate, db: Session = Depends(get_db)):
    jogador_id = None
    if lesao.nome_jogador:
        jogador = db.query(Jogador).filter(Jogador.nome == lesao.nome_jogador).first()
        if not jogador:
            raise HTTPException(status_code=404, detail="Jogador não encontrado")
        jogador_id = jogador.id

    dados_atualizacao = lesao.dict(exclude_unset=True)
    if jogador_id is not None:
        dados_atualizacao["jogador_id"] = jogador_id
    dados_atualizacao.pop("nome_jogador", None)

    lesao_atualizada = lesao_service.atualizar_lesao(lesao_id, dados_atualizacao, db)
    if not lesao_atualizada:
        raise HTTPException(status_code=404, detail="Lesão não encontrada")

    return lesao_atualizada

@router.delete("/{lesao_id}", response_model=lesao_schema.LesaoResponse)
def deletar_lesao(lesao_id: int, db: Session = Depends(get_db)):
    lesao = lesao_service.deletar_lesao(lesao_id, db)
    if not lesao:
        raise HTTPException(status_code=404, detail="Lesão não encontrada")
    return lesao
