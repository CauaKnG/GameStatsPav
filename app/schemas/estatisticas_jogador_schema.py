from pydantic import BaseModel
from datetime import date

class EstatisticasJogadorBase(BaseModel):
    gols: int
    assistencias: int
    passes_completos: int
    finalizacoes: int
    partida_id: int

class EstatisticasJogadorCreate(EstatisticasJogadorBase):
    pass

class EstatisticasJogadorUpdate(BaseModel):
    nome_jogador: str
    gols: int
    assistencias: int
    passes_completos: int
    finalizacoes: int

class EstatisticasJogadorResponse(EstatisticasJogadorBase):
    id: int

    class Config:
        orm_mode = True
