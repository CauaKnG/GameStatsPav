from sqlalchemy.orm import Session
from app.models.models import Lesao
from app.schemas.lesao_schema import LesaoCreate, LesaoUpdate
from app.validators import validar_duracao_lesao, validar_data_lesao

def listar_lesoes(db: Session):
    return db.query(Lesao).all()

def buscar_lesao_por_id(lesao_id: int, db: Session):
    return db.query(Lesao).filter(Lesao.id == lesao_id).first()

def criar_lesao(lesao: LesaoCreate, db: Session):
    validar_duracao_lesao(lesao)
    validar_data_lesao(lesao)

    db_lesao = Lesao(**lesao.dict())
    db.add(db_lesao)
    db.commit()
    db.refresh(db_lesao)
    return db_lesao

def atualizar_lesao(lesao_id: int, lesao_data: LesaoUpdate, db: Session):
    db_lesao = buscar_lesao_por_id(lesao_id, db)
    if not db_lesao:
        return None

    dados_atualizados = lesao_data.dict(exclude_unset=True)

    for campo, valor in dados_atualizados.items():
        setattr(db_lesao, campo, valor)

    db.commit()
    db.refresh(db_lesao)
    return db_lesao

def deletar_lesao(lesao_id: int, db: Session):
    db_lesao = buscar_lesao_por_id(lesao_id, db)
    if not db_lesao:
        return None

    db.delete(db_lesao)
    db.commit()
    return db_lesao
