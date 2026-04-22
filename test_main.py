from fastapi.testclient import TestClient
from main import app, alunos_db, contadores_cursos

client = TestClient(app)

def setup_function():
    """Limpa o banco de dados temporário antes de cada teste"""
    alunos_db.clear()
    contadores_cursos.clear()

def test_criar_aluno_sucesso():
    payload = {
        "nome": "João da Silva",
        "email": "joao@email.com",
        "curso": "GES"
    }
    
    response = client.post("/alunos", json=payload)

    assert response.status_code == 201
    dados = response.json()
    assert dados["nome"] == "João da Silva"
    assert dados["matricula"] == "GES1"

def test_listar_alunos_vazio():
    response = client.get("/alunos")
    assert response.status_code == 200
    assert response.json() == []

def test_buscar_aluno_inexistente():
    response = client.get("/alunos/GEC999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Aluno não encontrado"

def test_excluir_aluno():
    client.post("/alunos", json={"nome": "Maria", "email": "m@m.com", "curso": "GET"})

    response = client.delete("/alunos/GET1")
    assert response.status_code == 204

    response_busca = client.get("/alunos/GET1")
    assert response_busca.status_code == 404