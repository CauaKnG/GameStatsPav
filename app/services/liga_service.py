from sqlalchemy.orm import Session
from app.models.models import Liga
from app.schemas.liga_schema import LigaCreate, LigaUpdate

def listar_ligas(db: Session):
    return db.query(Liga).all()

def buscar_liga_por_id(liga_id: int, db: Session):
    return db.query(Liga).filter(Liga.id == liga_id).first()

def criar_liga(liga: LigaCreate, db: Session):
    db_liga = Liga(**liga.dict())
    db.add(db_liga)
    db.commit()
    db.refresh(db_liga)
    return db_liga

def atualizar_liga(liga_id: int, liga_data: LigaUpdate, db: Session):
    db_liga = buscar_liga_por_id(liga_id, db)
    if not db_liga:
        return None

    for campo, valor in liga_data.dict(exclude_unset=True).items():
        setattr(db_liga, campo, valor)

    db.commit()
    db.refresh(db_liga)
    return db_liga

def deletar_liga(liga_id: int, db: Session):
    db_liga = buscar_liga_por_id(liga_id, db)
    if not db_liga:
        return None

    db.delete(db_liga)
    db.commit()
    return db_liga
