from sqlalchemy.orm import Session
from app.models.models import Falta
from app.schemas.falta_schema import FaltaCreate, FaltaUpdate
from app.validators import validar_falta

def listar_faltas(db: Session):
    return db.query(Falta).all()

def buscar_falta_por_id(falta_id: int, db: Session):
    return db.query(Falta).filter(Falta.id == falta_id).first()

def criar_falta(falta: FaltaCreate, db: Session):
    validar_falta(falta)

    db_falta = Falta(**falta.dict())
    db.add(db_falta)
    db.commit()
    db.refresh(db_falta)
    return db_falta

def atualizar_falta(falta_id: int, falta_data: FaltaUpdate, db: Session):
    db_falta = buscar_falta_por_id(falta_id, db)
    if not db_falta:
        return None

    dados_atualizados = falta_data.dict(exclude_unset=True)

    for campo, valor in dados_atualizados.items():
        setattr(db_falta, campo, valor)

    db.commit()
    db.refresh(db_falta)
    return db_falta

def deletar_falta(falta_id: int, db: Session):
    db_falta = buscar_falta_por_id(falta_id, db)
    if not db_falta:
        return None

    db.delete(db_falta)
    db.commit()
    return db_falta
