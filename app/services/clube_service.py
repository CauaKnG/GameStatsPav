from sqlalchemy.orm import Session
from app.models.models import Clube
from app.schemas.clube_schema import ClubeCreate, ClubeUpdate
from app.validators import validar_liga_existente, validar_exclusao_clube

def listar_clubes(db: Session):
    return db.query(Clube).all()

def buscar_clube_por_id(clube_id: int, db: Session):
    return db.query(Clube).filter(Clube.id == clube_id).first()

def criar_clube(clube: ClubeCreate, db: Session):
    validar_liga_existente(clube, db)
    db_clube = Clube(**clube.dict())
    db.add(db_clube)
    db.commit()
    db.refresh(db_clube)
    return db_clube

def atualizar_clube(clube_id: int, clube_data: ClubeUpdate, db: Session):
    db_clube = buscar_clube_por_id(clube_id, db)
    if not db_clube:
        return None

    if clube_data.liga_id:
        validar_liga_existente(clube_data, db)

    for campo, valor in clube_data.dict(exclude_unset=True).items():
        setattr(db_clube, campo, valor)

    db.commit()
    db.refresh(db_clube)
    return db_clube

def deletar_clube(clube_id: int, db: Session):
    db_clube = buscar_clube_por_id(clube_id, db)
    if not db_clube:
        return None

    validar_exclusao_clube(clube_id, db)

    db.delete(db_clube)
    db.commit()
    return db_clube
