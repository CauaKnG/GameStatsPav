from pydantic import BaseModel, Field
from typing import Optional

class ClubeBase(BaseModel):
    nome: str = Field(..., example="Flamengo")
    liga_id: int = Field(..., example=1)

class ClubeCreate(ClubeBase):
    pass

class ClubeUpdate(BaseModel):
    nome: Optional[str] = Field(None, example="Fluminense")
    liga_id: Optional[int] = Field(None, example=2)

class ClubeResponse(ClubeBase):
    id: int

    class Config:
        orm_mode = True
