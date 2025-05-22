from typing import Optional

from pydantic import BaseModel, Field
from datetime import time

class FaltaBase(BaseModel):
    jogador_id: int = Field(..., example=1)
    minuto_ocorrido: int = Field(..., example=45)
    tipo: str = Field(..., example="Falta cometida")
    descricao: Optional[str] = Field(None, example="Falta na entrada da área")

class FaltaCreate(FaltaBase):
    pass

class FaltaUpdate(BaseModel):
    minuto_ocorrido: Optional[int]
    tipo: Optional[str]
    descricao: Optional[str]

class FaltaResponse(FaltaBase):
    id: int

    class Config:
        orm_mode = True
