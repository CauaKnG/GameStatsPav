from datetime import date
from sqlalchemy.orm import Session
from app.models.models import Jogador, Partida, Lesao, Falta, Clube, Liga

def validar_estatisticas(estatisticas):
    if estatisticas.gols < 0 or estatisticas.assistencias < 0 or estatisticas.passes_completos < 0 or estatisticas.finalizacoes < 0:
        raise ValueError("Gols, assistências, passes e finalizações não podem ser negativos.")

def validar_clubes_distintos(partida, db: Session):
    if partida.clube_casa_id == partida.clube_fora_id:
        raise ValueError("Não pode haver clubes iguais nos dois lados da partida.")

def validar_falta(falta):
    if falta.minuto_ocorrido < 0 or falta.minuto_ocorrido > 120:
        raise ValueError("Minuto ocorrido da falta deve estar entre 0 e 120.")

def validar_participacao_jogador(partida_id, jogador_id, db: Session):
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if not partida:
        raise ValueError("Partida não encontrada.")

    if partida.clube_casa_id not in [db.query(Jogador).filter(Jogador.id == jogador_id).first().clube_id,
                                     partida.clube_fora_id not in [db.query(Jogador).filter(Jogador.id == jogador_id).first().clube_id]]:
        raise ValueError("Jogador não participou desta partida.")

def validar_duracao_lesao(lesao):
    if lesao.duracao_estimada_dias < 0:
        raise ValueError("A duração da lesão não pode ser negativa.")

def validar_posicao(posicao):
    posicoes_validas = ['Goleiro', 'Zagueiro', 'Lateral', 'Volante', 'Meia', 'Atacante']
    if posicao not in posicoes_validas:
        raise ValueError(f"A posição {posicao} não é válida.")

def validar_liga_existente(clube, db: Session):
    liga = db.query(Liga).filter(Liga.id == clube.liga_id).first()
    if not liga:
        raise ValueError("Liga não encontrada.")

def validar_exclusao_clube(clube_id, db: Session):
    jogadores = db.query(Jogador).filter(Jogador.clube_id == clube_id).all()
    if jogadores:
        raise ValueError("Não é possível excluir um clube com jogadores associados.")

def validar_clube_unico(jogador_id, db: Session):
    jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()
    if jogador:
        clube_atual = jogador.clube_id
        jogadores_no_clube = db.query(Jogador).filter(Jogador.clube_id == clube_atual).all()
        if len(jogadores_no_clube) > 1:
            raise ValueError("Jogador não pode estar em mais de um clube simultaneamente.")

def validar_data_lesao(lesao):
    if lesao.data_lesao > date.today():
        raise ValueError("A data da lesão não pode ser no futuro.")
