from sqlalchemy.orm import Session
from app.models.models import Falta, Jogador
from app.schemas.falta_schema import FaltaCreate, FaltaUpdate
from app.validators import validar_falta

def listar_faltas(db: Session):
    return db.query(Falta).all()

def buscar_falta_por_id(falta_id: int, db: Session):
    return db.query(Falta).filter(Falta.id == falta_id).first()

def criar_falta(dados_falta: dict, db: Session):
    db_falta = Falta(**dados_falta)
    db.add(db_falta)
    db.commit()
    db.refresh(db_falta)
    return db_falta

def atualizar_falta(falta_id: int, falta_update: FaltaUpdate, db: Session):
    falta = db.query(Falta).filter(Falta.id == falta_id).first()
    if not falta:
        return None

    jogador = db.query(Jogador).filter(Jogador.nome == falta_update.nome_jogador).first()
    if not jogador:
        raise Exception("Jogador não encontrado")

    falta.jogador_id = jogador.id
    falta.minuto_ocorrido = falta_update.minuto_ocorrido
    falta.tipo_cartao = falta_update.tipo_cartao
    falta.descricao = falta_update.descricao
    falta.dentro_area = falta_update.dentro_area

    db.commit()
    db.refresh(falta)  

    return falta
def deletar_falta(falta_id: int, db: Session):
    db_falta = buscar_falta_por_id(falta_id, db)
    if not db_falta:
        return None

    db.delete(db_falta)
    db.commit()
    return db_falta
