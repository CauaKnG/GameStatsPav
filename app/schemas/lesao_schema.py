from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class JogadorSimples(BaseModel):
    nome: str

    class Config:
        orm_mode = True

class LesaoBase(BaseModel):
    nome_jogador: str = Field(..., example="Neymar Jr")  
    tipo_lesao: str = Field(..., example="Lesão muscular")
    data_lesao: date = Field(..., example="2025-07-15")
    duracao_estimada_dias: int = Field(..., example=30)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class LesaoCreate(LesaoBase):
    pass

class LesaoUpdate(BaseModel):
    tipo_lesao: Optional[str]
    data_lesao: Optional[date]
    duracao_estimada_dias: Optional[int]
    nome_jogador: Optional[str]



class LesaoResponse(BaseModel):
    id: int
    nome_jogador: str
    tipo_lesao: str
    data_lesao: date
    duracao_estimada_dias: int 
    jogador_id: int

    class Config:
        orm_mode = True
