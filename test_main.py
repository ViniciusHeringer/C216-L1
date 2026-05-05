from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_resetar_banco_inicial():
    """Garante que começamos com o banco limpo"""
    response = client.delete("/api/v1/alunos/")
    assert response.status_code == 204

def test_adicionar_3_alunos_ges():
    """Adiciona 3 alunos do curso GES"""
    for i in range(1, 4):
        payload = {"nome": f"Aluno GES {i}", "email": f"ges{i}@inatel.br", "curso": "GES"}
        response = client.post("/api/v1/alunos/", json=payload)
        assert response.status_code == 201
        assert response.json()["id"] == f"GES{i}"

def test_adicionar_3_alunos_gec():
    """Adiciona 3 alunos do curso GEC"""
    for i in range(1, 4):
        payload = {"nome": f"Aluno GEC {i}", "email": f"gec{i}@inatel.br", "curso": "GEC"}
        response = client.post("/api/v1/alunos/", json=payload)
        assert response.status_code == 201
        assert response.json()["id"] == f"GEC{i}"

def test_listar_alunos():
    """Verifica se os 6 alunos foram listados"""
    response = client.get("/api/v1/alunos/")
    assert response.status_code == 200
    assert len(response.json()) == 6

def test_buscar_aluno_por_id():
    """Busca um aluno específico (GES2)"""
    response = client.get("/api/v1/alunos/GES2")
    assert response.status_code == 200
    assert response.json()["nome"] == "Aluno GES 2"

def test_atualizar_aluno():
    """Atualiza os dados de GEC1 via PATCH"""
    payload = {"nome": "Aluno GEC 1 Atualizado", "email": "novoemail@inatel.br"}
    response = client.patch("/api/v1/alunos/GEC1", json=payload)
    assert response.status_code == 200
    assert response.json()["nome"] == "Aluno GEC 1 Atualizado"

def test_remover_aluno():
    """Deleta o aluno GES3 e verifica regra de ID não reutilizável"""
    response_del = client.delete("/api/v1/alunos/GES3")
    assert response_del.status_code == 204

    response_get = client.get("/api/v1/alunos/GES3")
    assert response_get.status_code == 404

    payload = {"nome": "Novo Aluno GES", "email": "novo@inatel.br", "curso": "GES"}
    response_novo = client.post("/api/v1/alunos/", json=payload)
    assert response_novo.status_code == 201
    assert response_novo.json()["id"] == "GES4"

def test_resetar_lista_final():
    """Testa a rota de limpeza total (DELETE /)"""
    response = client.delete("/api/v1/alunos/")
    assert response.status_code == 204
    
    response_get = client.get("/api/v1/alunos/")
    assert response.status_code == 204
    assert len(response_get.json()) == 0
