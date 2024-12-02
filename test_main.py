from fastapi.testclient import TestClient
from main import app, clientes, Cliente
import pytest


testes = TestClient(app)

@pytest.fixture
def mock_cliente():
    """
    Função de fixture que cria um cliente fictício
    para testar a listagem e cadastro de clientes.
    """
    cliente = Cliente(
        nome="Cleberton Silva",
        idade=32,
        email="cleberton@cleberton",
        telefone="111234567890",
        cidade="São Paulo",
        salario=2540.50
    )
    clientes.append(cliente)
    return cliente

def test_root():
    """ Testa o endpoint inicial ("/") """
    response = testes.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo a API de clientes"}

def test_get_clientes(mock_cliente):
    response = testes.get("/clientes")
    assert response.status_code == 200

def test_cadastrar_cliente():
    """ 
    cadastrar um novo cliente
    """
    novo_cliente = {
        "nome": "Maria Oliveira",
        "idade": 28,
        "email": "maria@exemplo.com",
        "telefone": "9876543210",
        "cidade": "Rio de Janeiro",
        "salario": 3000.00
    }

    response = testes.post("/clientes", json=novo_cliente)
    assert response.status_code == 200
    assert response.json()["mensagem"] == "Cliente cadastrado com sucesso!"
    

def test_cadastrar_cliente_invalido():
    """ Teste de dados incorretos """
    cliente_invalido = {
        "nome": "Carlos",
        "idade": "Vinte e Um", # idade como string
        "email": "carlos@exemplo.com",
        "telefone": "1234567890",
        "cidade": "Curitiba",
        "salario": 1800.50
    }
