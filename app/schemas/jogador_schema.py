from pydantic import BaseModel

class JogadorCreate(BaseModel):
    nome: str
    idade: int
    posicao: str
    overall: int
    clube_nome: str

class JogadorUpdate(JogadorCreate):
    pass

class ClubeResponse(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True

class JogadorResponse(BaseModel):
    id: int
    nome: str
    idade: int
    posicao: str
    overall: int
    clube: ClubeResponse

    class Config:
        orm_mode = True
