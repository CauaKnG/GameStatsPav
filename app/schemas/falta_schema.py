from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
from datetime import time

class FaltaBase(BaseModel):
    jogador_id: int = Field(..., example=1)
    minuto_ocorrido: int = Field(..., example=45)
    tipo_cartao: str = Field(..., example="Falta cometida")
    descricao: Optional[str] = Field(None, example="Falta na entrada da área")

class TipoCartaoEnum(str, Enum):
    amarelo = "amarelo"
    vermelho = "vermelho"
    sem_cartao = "sem_cartao"
   

class FaltaCreate(BaseModel):
    nome_jogador: str
    minuto_ocorrido: int
    tipo_cartao: TipoCartaoEnum  
    descricao: str
    dentro_area: bool
class FaltaUpdate(BaseModel):
    nome_jogador: str
    minuto_ocorrido: Optional[int]
    tipo_cartao: Optional[TipoCartaoEnum]
    descricao: Optional[str]
    dentro_area: Optional[bool]

class FaltaResponse(BaseModel):
    nome_jogador: str
    minuto_ocorrido: int
    tipo_cartao: str
    descricao: Optional[str]
    dentro_area: bool

    class Config:
        orm_mode = True
