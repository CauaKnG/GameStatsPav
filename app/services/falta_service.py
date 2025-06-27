from sqlalchemy.orm import Session
from app.models.models import Falta, Jogador
from app.schemas.falta_schema import FaltaCreate, FaltaUpdate
from app.validators import validar_falta

def listar_faltas(db: Session):
    return db.query(Falta).all()

def buscar_falta_por_id(falta_id: int, db: Session):
    return db.query(Falta).filter(Falta.id == falta_id).first()

def criar_falta(falta: FaltaCreate, jogador_id: int, partida_id: int, db: Session):

    validar_falta(falta)

    db_falta = Falta(
        jogador_id=jogador_id,
        partida_id=partida_id,
        minuto_ocorrido=falta.minuto_ocorrido,
        tipo_cartao=falta.tipo_cartao,
        descricao=falta.descricao,
        dentro_area=falta.dentro_area
    )
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

    class FaltaTemp:
        def __init__(self, minuto_ocorrido):
            self.minuto_ocorrido = minuto_ocorrido

    minuto_para_validar = (
        falta_update.minuto_ocorrido 
        if falta_update.minuto_ocorrido is not None 
        else falta.minuto_ocorrido
    )

    validar_falta(FaltaTemp(minuto_para_validar))

    falta.jogador_id = jogador.id
    if falta_update.minuto_ocorrido is not None:
        falta.minuto_ocorrido = falta_update.minuto_ocorrido
    if falta_update.tipo_cartao is not None:
        falta.tipo_cartao = falta_update.tipo_cartao
    if falta_update.descricao is not None:
        falta.descricao = falta_update.descricao
    if falta_update.dentro_area is not None:
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
