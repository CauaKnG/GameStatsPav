from sqlalchemy.orm import Session
from app.models.models import EstatisticaJogador
from app.schemas.estatisticas_jogador_schema import EstatisticasJogadorCreate, EstatisticasJogadorUpdate
from app.validators import validar_estatisticas

def listar_estatisticas_jogador(db: Session):
    return db.query(EstatisticaJogador).all()

def buscar_estatisticas_por_jogador(jogador_id: int, db: Session):
    return db.query(EstatisticaJogador).filter(EstatisticaJogador.jogador_id == jogador_id).all()

def criar_estatisticas_jogador(estatisticas: EstatisticasJogadorCreate, db: Session):
    validar_estatisticas(estatisticas)

    db_estatisticas = EstatisticaJogador(**estatisticas.dict())
    db.add(db_estatisticas)
    db.commit()
    db.refresh(db_estatisticas)
    return db_estatisticas

def atualizar_estatisticas_jogador(estatisticas_id: int, estatisticas_data: EstatisticasJogadorUpdate, db: Session):
    db_estatisticas = db.query(EstatisticaJogador).filter(EstatisticaJogador.id == estatisticas_id).first()
    if not db_estatisticas:
        return None

    dados_atualizados = estatisticas_data.dict(exclude_unset=True)

    for campo, valor in dados_atualizados.items():
        setattr(db_estatisticas, campo, valor)

    db.commit()
    db.refresh(db_estatisticas)
    return db_estatisticas

def deletar_estatisticas_jogador(estatisticas_id: int, db: Session):
    db_estatisticas = db.query(EstatisticaJogador).filter(EstatisticaJogador.id == estatisticas_id).first()
    if not db_estatisticas:
        return None

    db.delete(db_estatisticas)
    db.commit()
    return db_estatisticas
