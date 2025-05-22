from pydantic import BaseModel

class JogadorBase(BaseModel):
    nome: str
    idade: int
    posicao: str
    clube_id: int

class JogadorCreate(JogadorBase):
    pass

class JogadorUpdate(JogadorBase):
    pass

class JogadorResponse(JogadorBase):
    id: int

    class Config:
        orm_mode = True