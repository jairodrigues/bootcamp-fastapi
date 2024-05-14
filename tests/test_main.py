from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get('/health-check')
    assert response.status_code == 200
    assert response.text == '"OK"'

#Esta linha usa o decorador `patch` do `unittest.mock` para substituir a classe `SessionLocal` do módulo `app.db` durante o teste.
@patch("app.dependencies.db_instance")
def test_create_user(mock_session):
    #  Configura o método `commit` do banco de dados mock para retornar `None` ao ser chamado.
    mock_db = mock_session.return_value
    mock_db.add.return_value = None
    mock_db.commit.return_value = None

    # Envia uma solicitação POST para a rota `/users/` com os dados do usuário.
    response = client.post("/assistant/", json={
        "name": "vegeta", 
        "description": "vegeta description", 
        "interaction_example": "vegeta example interactions"
    })
    
    # Verifica se o código de status da resposta é 200, indicando uma resposta bem-suced
    assert response.status_code == 200
    assert response.json()["name"] == "vegeta"
    assert response.json()["description"] == "vegeta description"
    assert response.json()["interaction_example"] == "vegeta example interactions"
