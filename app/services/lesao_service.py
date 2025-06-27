from http.client import HTTPException

from sqlalchemy.orm import Session
from app.models.models import Lesao, Jogador
from app.schemas import lesao_schema
from app.schemas.lesao_schema import LesaoCreate, LesaoUpdate
from app.validators import validar_duracao_lesao, validar_data_lesao

def listar_lesoes(db: Session):
    return db.query(Lesao).all()

def buscar_lesao_por_id(lesao_id: int, db: Session):
    return db.query(Lesao).filter(Lesao.id == lesao_id).first()

def criar_lesao(lesao_dados: lesao_schema.LesaoCreate, db: Session):
    jogador = db.query(Jogador).filter(Jogador.nome == lesao_dados.nome_jogador).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    validar_duracao_lesao(lesao_dados)
    validar_data_lesao(lesao_dados)

    nova_lesao = Lesao(
        jogador_id=jogador.id,
        tipo_lesao=lesao_dados.tipo_lesao,
        data_lesao=lesao_dados.data_lesao,
        duracao_estimada_dias=lesao_dados.duracao_estimada_dias
    )
    db.add(nova_lesao)
    db.commit()
    db.refresh(nova_lesao)

    return db.query(
        Lesao.id,
        Lesao.jogador_id,
        Lesao.tipo_lesao,
        Lesao.data_lesao,
        Lesao.duracao_estimada_dias,
        Jogador.nome.label("nome_jogador")
    ).join(Jogador, Lesao.jogador_id == Jogador.id).filter(Lesao.id == nova_lesao.id).first()


def atualizar_lesao(lesao_id: int, dados_atualizados: dict, db: Session):
    db_lesao = buscar_lesao_por_id(lesao_id, db)
    if not db_lesao:
        return None

    tipo_lesao = dados_atualizados.get("tipo_lesao", db_lesao.tipo_lesao)
    data_lesao = dados_atualizados.get("data_lesao", db_lesao.data_lesao)
    duracao_estimada_dias = dados_atualizados.get("duracao_estimada_dias", db_lesao.duracao_estimada_dias)

    class LesaoTemp:
        def __init__(self, data_lesao, duracao_estimada_dias):
            self.data_lesao = data_lesao
            self.duracao_estimada_dias = duracao_estimada_dias

    lesao_temp = LesaoTemp(data_lesao, duracao_estimada_dias)
    validar_duracao_lesao(lesao_temp)
    validar_data_lesao(lesao_temp)

    for campo, valor in dados_atualizados.items():
        setattr(db_lesao, campo, valor)

    db.commit()
    db.refresh(db_lesao)

    return db.query(
        Lesao.id,
        Lesao.jogador_id,
        Lesao.tipo_lesao,
        Lesao.data_lesao,
        Lesao.duracao_estimada_dias,
        Jogador.nome.label("nome_jogador")
    ).join(Jogador, Lesao.jogador_id == Jogador.id).filter(Lesao.id == lesao_id).first()


def deletar_lesao(lesao_id: int, db: Session):
    lesao = db.query(Lesao).filter(Lesao.id == lesao_id).first()
    if not lesao:
        return None

    lesao_info = db.query(
        Lesao.id,
        Lesao.jogador_id,
        Lesao.tipo_lesao,
        Lesao.data_lesao,
        Lesao.duracao_estimada_dias,
        Jogador.nome.label("nome_jogador")
    ).join(Jogador, Lesao.jogador_id == Jogador.id).filter(Lesao.id == lesao_id).first()

    db.delete(lesao)
    db.commit()

    return lesao_info

