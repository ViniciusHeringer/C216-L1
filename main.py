import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Literal
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@localhost:5432/faculdade_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AlunoDB(Base):
    __tablename__ = "alunos"
    id = Column(String, primary_key=True, index=True)
    matricula = Column(Integer, nullable=False)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    curso = Column(String, nullable=False)

class ContadorDB(Base):
    """Tabela para garantir que a matrícula/ID nunca seja reutilizada"""
    __tablename__ = "contadores"
    curso = Column(String, primary_key=True, index=True)
    ultimo_valor = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gerenciador de Alunos", version="1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AlunoBase(BaseModel):
    nome: str
    email: str
    curso: Literal["GES", "GEC", "GET", "GEP"]

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    curso: Optional[Literal["GES", "GEC", "GET", "GEP"]] = None

class AlunoResponse(AlunoBase):
    id: str
    matricula: int
    model_config = ConfigDict(from_attributes=True)

@app.post("/api/v1/alunos/", response_model=AlunoResponse, status_code=201)
def criar_aluno(aluno: AlunoBase, db: Session = Depends(get_db)):
    curso = aluno.curso.upper()
    
    contador = db.query(ContadorDB).filter(ContadorDB.curso == curso).first()
    if not contador:
        contador = ContadorDB(curso=curso, ultimo_valor=0)
        db.add(contador)
        db.commit()
        db.refresh(contador)
    
    contador.ultimo_valor += 1
    matricula = contador.ultimo_valor
    aluno_id = f"{curso}{matricula}"
    
    novo_aluno = AlunoDB(id=aluno_id, matricula=matricula, nome=aluno.nome, email=aluno.email, curso=curso)
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    
    return novo_aluno

@app.get("/api/v1/alunos/", response_model=List[AlunoResponse])
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(AlunoDB).all()

@app.get("/api/v1/alunos/{aluno_id}", response_model=AlunoResponse)
def buscar_aluno(aluno_id: str, db: Session = Depends(get_db)):
    aluno = db.query(AlunoDB).filter(AlunoDB.id == aluno_id.upper()).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@app.patch("/api/v1/alunos/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(aluno_id: str, aluno_atualizado: AlunoUpdate, db: Session = Depends(get_db)):
    aluno = db.query(AlunoDB).filter(AlunoDB.id == aluno_id.upper()).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    if aluno_atualizado.nome is not None:
        aluno.nome = aluno_atualizado.nome
    if aluno_atualizado.email is not None:
        aluno.email = aluno_atualizado.email
    if aluno_atualizado.curso is not None:
        aluno.curso = aluno_atualizado.curso.upper()
        
    db.commit()
    db.refresh(aluno)
    return aluno

@app.delete("/api/v1/alunos/{aluno_id}", status_code=204)
def excluir_aluno(aluno_id: str, db: Session = Depends(get_db)):
    aluno = db.query(AlunoDB).filter(AlunoDB.id == aluno_id.upper()).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(aluno)
    db.commit()

@app.delete("/api/v1/alunos/", status_code=204)
def resetar_alunos(db: Session = Depends(get_db)):
    db.query(AlunoDB).delete()
    db.query(ContadorDB).delete()
    db.commit()