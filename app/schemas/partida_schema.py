from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class PartidaBase(BaseModel):
    data_partida: datetime = Field(..., example="10/08/2025 15:30")
    local: str = Field(..., example="Estádio do Maracanã")
    clube_casa: str = Field(..., example="Flamengo")
    clube_fora: str = Field(..., example="Vasco")
    gols_casa: Optional[int] = 0
    gols_fora: Optional[int] = 0

    @validator('data_partida', pre=True)
    def parse_data_partida(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d/%m/%Y %H:%M")
        return value

class PartidaCreate(PartidaBase):
    pass

class PartidaUpdate(BaseModel):
    data_partida: datetime = Field(..., example="10/08/2025 15:30")
    local: str = Field(..., example="Estádio do Maracanã")
    clube_casa: str = Field(..., example="Flamengo")
    clube_fora: str = Field(..., example="Vasco")
    gols_casa: Optional[int] = 0
    gols_fora: Optional[int] = 0

    @validator('data_partida', pre=True)
    def parse_data_partida(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d/%m/%Y %H:%M")
        return value

class PartidaResponse(BaseModel):
    id: int
    data_partida: str  
    local: str
    clube_casa: str
    clube_fora: str
    gols_casa: Optional[int]
    gols_fora: Optional[int]

    class Config:
        orm_mode = True
