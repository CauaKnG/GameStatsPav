from sqlalchemy.orm import Session
from app.models.models import Partida
from app.schemas.partida_schema import PartidaCreate, PartidaUpdate
from app.validators import validar_clubes_distintos

def listar_partidas(db: Session):
    return db.query(Partida).all()

def buscar_partida_por_id(partida_id: int, db: Session):
    return db.query(Partida).filter(Partida.id == partida_id).first()

def criar_partida(partida: PartidaCreate, db: Session):
    validar_clubes_distintos(partida, db)

    db_partida = Partida(**partida.dict())
    db.add(db_partida)
    db.commit()
    db.refresh(db_partida)
    return db_partida

def atualizar_partida(partida_id: int, partida_data: PartidaUpdate, db: Session):
    db_partida = buscar_partida_por_id(partida_id, db)
    if not db_partida:
        return None

    dados_atualizados = partida_data.dict(exclude_unset=True)

    # Validação se clubes foram atualizados
    if "clube_casa_id" in dados_atualizados or "clube_fora_id" in dados_atualizados:
        clubes = {
            "clube_casa_id": dados_atualizados.get("clube_casa_id", db_partida.clube_casa_id),
            "clube_fora_id": dados_atualizados.get("clube_fora_id", db_partida.clube_fora_id),
        }
        validar_clubes_distintos(type("PartidaFake", (), clubes), db)

    for campo, valor in dados_atualizados.items():
        setattr(db_partida, campo, valor)

    db.commit()
    db.refresh(db_partida)
    return db_partida

def deletar_partida(partida_id: int, db: Session):
    db_partida = buscar_partida_por_id(partida_id, db)
    if not db_partida:
        return None

    db.delete(db_partida)
    db.commit()
    return db_partida
