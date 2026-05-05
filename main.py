from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

app = FastAPI(title="Gerenciador de Alunos", version="1.0")

alunos_db = []
contadores_cursos = {"GES": 0, "GEC": 0, "GET": 0, "GEP": 0}

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

@app.post("/api/v1/alunos/", response_model=AlunoResponse, status_code=201)
def criar_aluno(aluno: AlunoBase):
    curso = aluno.curso.upper()
    
    contadores_cursos[curso] += 1
    matricula = contadores_cursos[curso]
    aluno_id = f"{curso}{matricula}"
    
    novo_aluno = {
        "id": aluno_id,
        "matricula": matricula,
        "nome": aluno.nome,
        "email": aluno.email,
        "curso": curso
    }
    alunos_db.append(novo_aluno)
    return novo_aluno

@app.get("/api/v1/alunos/", response_model=List[AlunoResponse])
def listar_alunos():
    return alunos_db

@app.get("/api/v1/alunos/{aluno_id}", response_model=AlunoResponse)
def buscar_aluno(aluno_id: str):
    aluno_id = aluno_id.upper()
    for aluno in alunos_db:
        if aluno["id"] == aluno_id:
            return aluno
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

@app.patch("/api/v1/alunos/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(aluno_id: str, aluno_atualizado: AlunoUpdate):
    aluno_id = aluno_id.upper()
    for aluno in alunos_db:
        if aluno["id"] == aluno_id:
            if aluno_atualizado.nome is not None:
                aluno["nome"] = aluno_atualizado.nome
            if aluno_atualizado.email is not None:
                aluno["email"] = aluno_atualizado.email
            if aluno_atualizado.curso is not None:
                aluno["curso"] = aluno_atualizado.curso.upper()
            return aluno
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

@app.delete("/api/v1/alunos/{aluno_id}", status_code=204)
def excluir_aluno(aluno_id: str):
    aluno_id = aluno_id.upper()
    for i, aluno in enumerate(alunos_db):
        if aluno["id"] == aluno_id:
            del alunos_db[i]
            return
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

@app.delete("/api/v1/alunos/", status_code=204)
def resetar_alunos():
    alunos_db.clear()
