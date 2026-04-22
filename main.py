from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="API Faculdade", description="CRUD de Alunos com FastAPI")

alunos_db = []
contadores_cursos = {}

class AlunoBase(BaseModel):
    nome: str
    email: str
    curso: str

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None

class AlunoResponse(AlunoBase):
    matricula: str

def gerar_matricula(curso: str) -> str:
    curso = curso.upper()
    if curso not in contadores_cursos:
        contadores_cursos[curso] = 1
    else:
        contadores_cursos[curso] += 1
    return f"{curso}{contadores_cursos[curso]}"

@app.post("/alunos", response_model=AlunoResponse, status_code=201)
def criar_aluno(aluno: AlunoBase):
    curso_upper = aluno.curso.upper()
    matricula = gerar_matricula(curso_upper)
    
    novo_aluno = {
        "nome": aluno.nome,
        "email": aluno.email,
        "curso": curso_upper,
        "matricula": matricula
    }
    alunos_db.append(novo_aluno)
    return novo_aluno

@app.get("/alunos", response_model=List[AlunoResponse])
def listar_alunos():
    return alunos_db

@app.get("/alunos/{matricula}", response_model=AlunoResponse)
def buscar_aluno(matricula: str):
    matricula = matricula.upper()
    for aluno in alunos_db:
        if aluno["matricula"] == matricula:
            return aluno
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

@app.put("/alunos/{matricula}", response_model=AlunoResponse)
def atualizar_aluno_completo(matricula: str, aluno_atualizado: AlunoBase):
    matricula = matricula.upper()
    for i, aluno in enumerate(alunos_db):
        if aluno["matricula"] == matricula:
            alunos_db[i] = {
                "nome": aluno_atualizado.nome,
                "email": aluno_atualizado.email,
                "curso": aluno_atualizado.curso.upper(),
                "matricula": matricula
            }
            return alunos_db[i]
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

@app.patch("/alunos/{matricula}", response_model=AlunoResponse)
def atualizar_aluno_parcial(matricula: str, aluno_atualizado: AlunoUpdate):
    matricula = matricula.upper()
    for aluno in alunos_db:
        if aluno["matricula"] == matricula:
            if aluno_atualizado.nome is not None:
                aluno["nome"] = aluno_atualizado.nome
            if aluno_atualizado.email is not None:
                aluno["email"] = aluno_atualizado.email
            return aluno
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

@app.delete("/alunos/{matricula}", status_code=204)
def excluir_aluno(matricula: str):
    matricula = matricula.upper()
    for i, aluno in enumerate(alunos_db):
        if aluno["matricula"] == matricula:
            del alunos_db[i]
            return
    raise HTTPException(status_code=404, detail="Aluno não encontrado")
