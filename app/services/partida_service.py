from sqlalchemy.orm import Session,joinedload
from app.models.models import Partida, Clube
from app.schemas.partida_schema import PartidaCreate, PartidaUpdate, PartidaResponse
from fastapi import HTTPException
from datetime import datetime, date

def buscar_clube_por_nome(nome: str, db: Session):
    clube = db.query(Clube).filter(Clube.nome == nome).first()
    if not clube:
        raise HTTPException(status_code=404, detail=f"Clube '{nome}' não encontrado.")
    return clube

def listar_partidas(db: Session):
    partidas = db.query(Partida).options(joinedload(Partida.clube_casa), joinedload(Partida.clube_fora)).all()
    return [formatar_partida_response(p) for p in partidas]

def converter_data_partida(data):
    if isinstance(data, str):
        return datetime.strptime(data, "%d/%m/%Y %H:%M")
    elif isinstance(data, datetime):
        return data
    else:
        raise ValueError("Tipo inválido para data_partida")

        
def buscar_partida_por_id(partida_id: int, db: Session):
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if not partida:
        return None
    return formatar_partida_response(partida)

def criar_partida(partida: PartidaCreate, db: Session):
    clube_casa = buscar_clube_por_nome(partida.clube_casa, db)
    clube_fora = buscar_clube_por_nome(partida.clube_fora, db)

    if clube_casa.id == clube_fora.id:
        raise HTTPException(status_code=400, detail="Clube da casa e visitante devem ser diferentes.")

    db_partida = Partida(
        data_partida=converter_data_partida(partida.data_partida),
        local=partida.local,
        clube_casa_id=clube_casa.id,
        clube_fora_id=clube_fora.id,
        gols_casa=partida.gols_casa,
        gols_fora=partida.gols_fora
    )
    db.add(db_partida)
    db.commit()
    db.refresh(db_partida)
    return db_partida

def atualizar_partida(partida_id: int, partida_data: PartidaUpdate, db: Session):
    db_partida = buscar_partida_por_id(partida_id, db)
    if not db_partida:
        return None

    if partida_data.clube_casa:
        clube_casa = buscar_clube_por_nome(partida_data.clube_casa, db)
        db_partida.clube_casa_id = clube_casa.id

    if partida_data.clube_fora:
        clube_fora = buscar_clube_por_nome(partida_data.clube_fora, db)
        db_partida.clube_fora_id = clube_fora.id

    if partida_data.data_partida:
        db_partida.data_partida = converter_data_partida(partida_data.data_partida)

    if partida_data.local:
        db_partida.local = partida_data.local

    if partida_data.gols_casa is not None:
        db_partida.gols_casa = partida_data.gols_casa

    if partida_data.gols_fora is not None:
        db_partida.gols_fora = partida_data.gols_fora

    db.commit()
    db.refresh(db_partida)
    return db_partida

def formatar_partida_response(partida: Partida) -> PartidaResponse:
    return PartidaResponse(
        id=partida.id,
        data_partida=partida.data_partida.strftime("%d/%m/%Y %H:%M"),  
        local=partida.local,
        clube_casa=partida.clube_casa.nome,
        clube_fora=partida.clube_fora.nome,
        gols_casa=partida.gols_casa,
        gols_fora=partida.gols_fora
    )

def deletar_partida(partida_id: int, db: Session):
    partida = db.query(Partida).options(joinedload(Partida.clube_casa), joinedload(Partida.clube_fora)).filter(Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    
    partida_response = formatar_partida_response(partida)  
    db.delete(partida)
    db.commit()
    return partida_response
