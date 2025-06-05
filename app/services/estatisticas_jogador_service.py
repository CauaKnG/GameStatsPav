from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import EstatisticaJogador, Jogador, Partida
from app.schemas.estatisticas_jogador_schema import EstatisticasJogadorCreate, EstatisticasJogadorUpdate
from app.validators import validar_estatisticas

def listar_estatisticas_jogador(db: Session):
    return db.query(EstatisticaJogador).all()

def buscar_estatisticas_por_jogador(jogador_id: int, db: Session):
    return db.query(EstatisticaJogador).filter(EstatisticaJogador.jogador_id == jogador_id).all()

def criar_estatisticas_jogador(estatisticas: EstatisticasJogadorCreate, db: Session):
    try:
        validar_estatisticas(estatisticas)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    jogador = db.query(Jogador).filter(Jogador.nome == estatisticas.nome_jogador).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")

    partida = db.query(Partida).filter(Partida.id == estatisticas.partida_id).first()
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")

    if jogador.clube_id not in [partida.clube_casa_id, partida.clube_fora_id]:
        raise HTTPException(status_code=400, detail="O clube do jogador não participou da partida")

    estatisticas_existentes = db.query(EstatisticaJogador).filter(
        EstatisticaJogador.partida_id == estatisticas.partida_id
    ).all()

    gols_atuais = sum(e.gols for e in estatisticas_existentes if e.jogador and e.jogador.clube_id == jogador.clube_id)
    gols_disponiveis = partida.gols_casa if jogador.clube_id == partida.clube_casa_id else partida.gols_fora

    if gols_atuais + estatisticas.gols > gols_disponiveis:
        raise HTTPException(
            status_code=400,
            detail=f"Número de gols excede os gols do clube na partida (disponível: {gols_disponiveis - gols_atuais})"
        )

    nova_estatistica = EstatisticaJogador(
        jogador_id=jogador.id,
        nome_jogador=jogador.nome,
        partida_id=estatisticas.partida_id,
        gols=estatisticas.gols,
        assistencias=estatisticas.assistencias,
        passes_completos=estatisticas.passes_completos,
        finalizacoes=estatisticas.finalizacoes,
    )

    db.add(nova_estatistica)
    db.commit()
    db.refresh(nova_estatistica)
    return nova_estatistica

def atualizar_estatisticas_jogador(estatistica_id: int, estatisticas: EstatisticasJogadorCreate, db: Session):
    

    estatistica_existente = db.query(EstatisticaJogador).filter(EstatisticaJogador.id == estatistica_id).first()
    if not estatistica_existente:
        raise HTTPException(status_code=404, detail="Estatística não encontrada")

    try:
        validar_estatisticas(estatisticas)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    jogador = db.query(Jogador).filter(Jogador.nome == estatisticas.nome_jogador).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")

    partida = db.query(Partida).filter(Partida.id == estatistica_existente.partida_id).first()
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")

    if jogador.clube_id not in [partida.clube_casa_id, partida.clube_fora_id]:
        raise HTTPException(status_code=400, detail="O clube do jogador não participou da partida")

    estatisticas_existentes = db.query(EstatisticaJogador).filter(
        EstatisticaJogador.partida_id == partida.id,
        EstatisticaJogador.id != estatistica_id
    ).all()

    gols_atuais = sum(e.gols for e in estatisticas_existentes if e.jogador and e.jogador.clube_id == jogador.clube_id)
    gols_disponiveis = partida.gols_casa if jogador.clube_id == partida.clube_casa_id else partida.gols_fora

    if gols_atuais + estatisticas.gols > gols_disponiveis:
        raise HTTPException(
            status_code=400,
            detail=f"Número de gols excede os gols do clube na partida (disponível: {gols_disponiveis - gols_atuais})"
        )

    estatistica_existente.jogador_id = jogador.id
    estatistica_existente.nome_jogador = jogador.nome
    estatistica_existente.gols = estatisticas.gols
    estatistica_existente.assistencias = estatisticas.assistencias
    estatistica_existente.passes_completos = estatisticas.passes_completos
    estatistica_existente.finalizacoes = estatisticas.finalizacoes

    db.commit()
    db.refresh(estatistica_existente)
    return estatistica_existente

def deletar_estatisticas_jogador(estatisticas_id: int, db: Session):
    db_estatisticas = db.query(EstatisticaJogador).filter(EstatisticaJogador.id == estatisticas_id).first()
    if not db_estatisticas:
        return None

    db.delete(db_estatisticas)
    db.commit()
    return db_estatisticas
