from pydantic import BaseModel, Field
from typing import Optional

class LigaSimples(BaseModel):
    nome: str

    class Config:
        from_attributes = True

class ClubeBase(BaseModel):
    nome: str = Field(..., example="Flamengo")
    liga_id: int = Field(..., example=1)

class ClubeCreate(BaseModel):
    nome: str = Field(..., example="Flamengo")
    cidade: str = Field(..., example="Rio de Janeiro")
    nome_liga: str = Field(..., example="Brasileirão")

class ClubeUpdate(BaseModel):
    nome: Optional[str] = Field(None, example="Fluminense")
    cidade: str = Field(..., example="Rio de Janeiro")

class ClubeResponse(BaseModel):
    id: int
    nome: str
    cidade: Optional[str]
    liga: LigaSimples

    class Config:
        from_attributes = True
