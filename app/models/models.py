from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean, Date
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class TipoCartaoEnum(enum.Enum):
    amarelo = 'amarelo'
    vermelho = 'vermelho'

class Liga(Base):
    __tablename__ = 'ligas'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    pais = Column(String(100), nullable=False)

    clubes = relationship("Clube", back_populates="liga")

class Clube(Base):
    __tablename__ = 'clubes'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cidade = Column(String(100))
    liga_id = Column(Integer, ForeignKey('ligas.id'))

    liga = relationship("Liga", back_populates="clubes")
    jogadores = relationship("Jogador", back_populates="clube")
    partidas_casa = relationship("Partida", back_populates="clube_casa", foreign_keys='Partida.clube_casa_id')
    partidas_fora = relationship("Partida", back_populates="clube_fora", foreign_keys='Partida.clube_fora_id')

class Jogador(Base):
    __tablename__ = 'jogadores'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer)
    posicao = Column(String(50))
    overall = Column(Integer)
    clube_id = Column(Integer, ForeignKey('clubes.id'))

    clube = relationship("Clube", back_populates="jogadores")
    estatisticas = relationship("EstatisticaJogador", back_populates="jogador")
    lesoes = relationship("Lesao", back_populates="jogador")
    faltas = relationship("Falta", back_populates="jogador")

class Partida(Base):
    __tablename__ = 'partidas'
    id = Column(Integer, primary_key=True, index=True)
    data_partida = Column(DateTime, nullable=False)  
    local = Column(String, nullable=False) 
    clube_casa_id = Column(Integer, ForeignKey('clubes.id'))
    clube_fora_id = Column(Integer, ForeignKey('clubes.id'))
    gols_casa = Column(Integer)
    gols_fora = Column(Integer)

    clube_casa = relationship("Clube", foreign_keys=[clube_casa_id], back_populates="partidas_casa")
    clube_fora = relationship("Clube", foreign_keys=[clube_fora_id], back_populates="partidas_fora")
    estatisticas = relationship("EstatisticaJogador", back_populates="partida")
    faltas = relationship("Falta", back_populates="partida")

class EstatisticaJogador(Base):
    __tablename__ = 'estatisticas_jogador'
    id = Column(Integer, primary_key=True, index=True)
    jogador_id = Column(Integer, ForeignKey('jogadores.id'))
    partida_id = Column(Integer, ForeignKey('partidas.id'))
    nome_jogador = Column(String(100))
    gols = Column(Integer)
    assistencias = Column(Integer)
    passes_completos = Column(Integer)
    finalizacoes = Column(Integer)

    jogador = relationship("Jogador", back_populates="estatisticas")
    partida = relationship("Partida", back_populates="estatisticas")

class Lesao(Base):
    __tablename__ = 'lesoes'
    id = Column(Integer, primary_key=True, index=True)
    jogador_id = Column(Integer, ForeignKey('jogadores.id'))
    data_lesao = Column(Date)
    tipo_lesao = Column(String(100))
    duracao_estimada_dias = Column(Integer)

    jogador = relationship("Jogador", back_populates="lesoes")

class Falta(Base):
    __tablename__ = 'faltas'
    id = Column(Integer, primary_key=True, index=True)
    jogador_id = Column(Integer, ForeignKey('jogadores.id'))
    partida_id = Column(Integer, ForeignKey('partidas.id'))
    tipo_cartao = Column(Enum(TipoCartaoEnum))
    minuto_ocorrido = Column(Integer)
    dentro_area = Column(Boolean)

    jogador = relationship("Jogador", back_populates="faltas")
    partida = relationship("Partida", back_populates="faltas")

