from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class LesaoBase(BaseModel):
    jogador_id: int = Field(..., example=1)
    tipo: str = Field(..., example="Lesão muscular")
    descricao: Optional[str] = Field(None, example="Lesão na coxa")
    data_lesao: date = Field(..., example="2025-07-15")
    duracao_estimada_dias: int = Field(..., example=30)

class LesaoCreate(LesaoBase):
    pass

class LesaoUpdate(BaseModel):
    tipo: Optional[str]
    descricao: Optional[str]
    data_lesao: Optional[date]
    duracao_estimada_dias: Optional[int]

class LesaoResponse(LesaoBase):
    id: int

    class Config:
        orm_mode = True
