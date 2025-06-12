from sqlalchemy.orm import Session,  joinedload
from app.models.models import Clube, Liga
from app.schemas.clube_schema import ClubeCreate, ClubeUpdate
from app.validators import validar_liga_existente, validar_exclusao_clube

def listar_clubes(db: Session):
    return db.query(Clube).options(joinedload(Clube.liga)).all()

def buscar_clube_por_id(clube_id: int, db: Session):
    return db.query(Clube).options(joinedload(Clube.liga)).filter(Clube.id == clube_id).first()

def criar_clube(clube: ClubeCreate, db: Session):
    liga = db.query(Liga).filter(Liga.nome == clube.nome_liga).first()

    if not liga:
        raise ValueError(f"Liga com nome '{clube.nome_liga}' não existe")

    novo_clube = Clube(
        nome=clube.nome,
        cidade=clube.cidade,
        liga_id=liga.id
    )

    db.add(novo_clube)
    db.commit()
    db.refresh(novo_clube)
    return novo_clube

def atualizar_clube(clube_id: int, clube: ClubeUpdate, db: Session):
    clube_existente = db.query(Clube).filter(Clube.id == clube_id).first()

    if not clube_existente:
        return None

    if clube.nome is not None:
        clube_existente.nome = clube.nome
    if clube.cidade is not None:
        clube_existente.cidade = clube.cidade

    if clube.nome_liga is not None:
        liga = db.query(Liga).filter(Liga.nome == clube.nome_liga).first()
        if not liga:
            raise ValueError(f"Liga com nome '{clube.nome_liga}' não existe")
        clube_existente.liga_id = liga.id

    db.commit()
    db.refresh(clube_existente)
    return clube_existente


def deletar_clube(clube_id: int, db: Session):
    db_clube = buscar_clube_por_id(clube_id, db)
    if not db_clube:
        return None

    validar_exclusao_clube(clube_id, db)

    db.delete(db_clube)
    db.commit()
    return db_clube
