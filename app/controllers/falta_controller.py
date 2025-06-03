from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import falta_schema
from app.services import falta_service
from app.models.models import EstatisticaJogador, Falta, Jogador, Partida
from app.schemas.falta_schema import FaltaCreate  

router = APIRouter()

def falta_to_response(falta):
    return {
        "nome_jogador": falta.jogador.nome,
        "minuto_ocorrido": falta.minuto_ocorrido,
        "tipo_cartao": falta.tipo_cartao.value if falta.tipo_cartao else None,
        "descricao": falta.descricao,
        "dentro_area": falta.dentro_area
    }

@router.get("/", response_model=list[falta_schema.FaltaResponse])
def listar_faltas(db: Session = Depends(get_db)):
    faltas = falta_service.listar_faltas(db)
    return [falta_to_response(f) for f in faltas]

@router.get("/{falta_id}", response_model=falta_schema.FaltaResponse)
def buscar_falta(falta_id: int, db: Session = Depends(get_db)):
    falta = falta_service.buscar_falta_por_id(falta_id, db)
    if not falta:
        raise HTTPException(status_code=404, detail="Falta não encontrada")
    return falta_to_response(falta)


@router.post("/")
def criar_falta(falta: FaltaCreate, db: Session = Depends(get_db)):
    jogador = db.query(Jogador).filter(Jogador.nome == falta.nome_jogador).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")

    clube_id = jogador.clube_id
    if not clube_id:
        raise HTTPException(status_code=400, detail="Jogador não está associado a um clube")

    partidas = db.query(Partida).filter(
        or_(
            Partida.clube_casa_id == clube_id,
            Partida.clube_fora_id == clube_id
        )
    ).all()
    if not partidas:
        raise HTTPException(status_code=400, detail="Nenhuma partida encontrada para o clube do jogador")

    agora = datetime.now()
    partida_mais_proxima = min(partidas, key=lambda p: abs((p.data_partida - agora).total_seconds()))

    nova_falta_data = {
        "jogador_id": jogador.id,
        "partida_id": partida_mais_proxima.id,
        "minuto_ocorrido": falta.minuto_ocorrido,
        "tipo_cartao": falta.tipo_cartao,
        "descricao": falta.descricao,
        "dentro_area": falta.dentro_area
    }

    nova_falta = falta_service.criar_falta(nova_falta_data, db)

    db.add(nova_falta)
    db.commit()
    db.refresh(nova_falta)

    return falta_to_response(nova_falta)

@router.put("/{falta_id}", response_model=falta_schema.FaltaResponse)
def atualizar_falta(falta_id: int, falta: falta_schema.FaltaUpdate, db: Session = Depends(get_db)):
    try:
        falta_atualizada = falta_service.atualizar_falta(falta_id, falta, db)
        if not falta_atualizada:
            raise HTTPException(status_code=404, detail="Falta não encontrada")
        return falta_to_response(falta_atualizada)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{falta_id}")
def deletar_falta(falta_id: int, db: Session = Depends(get_db)):
    falta = falta_service.deletar_falta(falta_id, db)
    if not falta:
        raise HTTPException(status_code=404, detail="Falta não encontrada")
    return {"mensagem": "Falta deletada com sucesso"}
