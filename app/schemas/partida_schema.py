from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PartidaBase(BaseModel):
    data_hora: datetime = Field(..., example="2025-08-10T16:00:00")
    local: str = Field(..., example="Estádio do Maracanã")
    clube_casa_id: int = Field(..., example=1)
    clube_fora_id: int = Field(..., example=2)

class PartidaCreate(PartidaBase):
    pass

class PartidaUpdate(BaseModel):
    data_hora: Optional[datetime]
    local: Optional[str]
    clube_casa_id: Optional[int]
    clube_fora_id: Optional[int]

class PartidaResponse(PartidaBase):
    id: int

    class Config:
        orm_mode = True
