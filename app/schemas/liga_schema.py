from pydantic import BaseModel, Field
from typing import Optional

class LigaBase(BaseModel):
    nome: str = Field(..., example="Brasileirão Série A")

class LigaCreate(LigaBase):
    pass

class LigaUpdate(BaseModel):
    nome: Optional[str] = Field(None, example="Brasileirão Série B")

class LigaResponse(LigaBase):
    id: int

    class Config:
        orm_mode = True
