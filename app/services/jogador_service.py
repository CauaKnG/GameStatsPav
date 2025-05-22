from app.models.models import Jogador, EstatisticaJogador, Lesao
from app.validators import (
    validar_estatisticas, validar_participacao_jogador,
    validar_duracao_lesao, validar_posicao
)
from sqlalchemy.orm import Session

# Função para adicionar um jogador
def adicionar_jogador(db: Session, jogador: Jogador):
    validar_posicao(jogador.posicao)
    db.add(jogador)
    db.commit()
    db.refresh(jogador)
    return jogador

# Função para editar jogador
def editar_jogador(db: Session, jogador_id: int, jogador_dados: dict):
    jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()
    if not jogador:
        raise ValueError("Jogador não encontrado.")

    for key, value in jogador_dados.items():
        setattr(jogador, key, value)

    validar_posicao(jogador.posicao)
    db.commit()
    db.refresh(jogador)
    return jogador

# Função para adicionar estatísticas ao jogador
def registrar_estatisticas(db: Session, jogador_id: int, partida_id: int, estatisticas: EstatisticaJogador):
    validar_estatisticas(estatisticas)
    validar_participacao_jogador(partida_id, jogador_id, db)
    estatisticas.jogador_id = jogador_id
    estatisticas.partida_id = partida_id
    db.add(estatisticas)
    db.commit()
    db.refresh(estatisticas)
    return estatisticas
