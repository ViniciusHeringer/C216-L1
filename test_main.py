from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_resetar_banco_inicial():
    response = client.delete("/api/v1/alunos/")
    assert response.status_code == 204

def test_adicionar_3_alunos_ges():
    for i in range(1, 4):
        payload = {"nome": f"Aluno GES {i}", "email": f"ges{i}@inatel.br", "curso": "GES"}
        response = client.post("/api/v1/alunos/", json=payload)
        assert response.status_code == 201

def test_adicionar_3_alunos_gec():
    for i in range(1, 4):
        payload = {"nome": f"Aluno GEC {i}", "email": f"gec{i}@inatel.br", "curso": "GEC"}
        response = client.post("/api/v1/alunos/", json=payload)
        assert response.status_code == 201

def test_listar_alunos():
    response = client.get("/api/v1/alunos/")
    assert response.status_code == 200
    assert len(response.json()) >= 6

def test_buscar_aluno_por_id():
    response = client.get("/api/v1/alunos/GES2")
    assert response.status_code == 200
    assert response.json()["nome"] == "Aluno GES 2"

def test_atualizar_aluno():
    payload = {"nome": "Aluno GEC 1 Modificado"}
    response = client.patch("/api/v1/alunos/GEC1", json=payload)
    assert response.status_code == 200
    assert response.json()["nome"] == "Aluno GEC 1 Modificado"

def test_remover_aluno():
    response_del = client.delete("/api/v1/alunos/GES3")
    assert response_del.status_code == 204
    
    response_get = client.get("/api/v1/alunos/GES3")
    assert response_get.status_code == 404