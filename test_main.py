from fastapi.testclient import TestClient
from main import app, clientes, Cliente
import pytest

testes = TestClient(app)

@pytest.fixture
def mock_cliente():
    """
    Função que cria um cliente fictício
    para testar a lista e cadastro de clientes.
    """
    # Limpa a lista de clientes antes de cada teste para evitar interferência entre os testes
    clientes.clear()
    
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
    """ Testa o endpoint GET /clientes para listar todos os clientes """
    response = testes.get("/clientes")
    assert response.status_code == 200
    # Verifica se o cliente inserido commo teste aparece na resposta
    assert len(response.json()) == 1  
    assert response.json()[0]["nome"] == mock_cliente.nome
    assert response.json()[0]["idade"] == mock_cliente.idade
    assert response.json()[0]["email"] == mock_cliente.email
    assert response.json()[0]["telefone"] == mock_cliente.telefone
    assert response.json()[0]["cidade"] == mock_cliente.cidade
    assert response.json()[0]["salario"] == mock_cliente.salario

def test_cadastrar_cliente():
    """ Cadastra um novo cliente """
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
    
    # Verifica se o cliente foi realmente adicionado
    response_get = testes.get("/clientes")
    assert len(response_get.json()) == 2  # Agora deve ter 2 clientes
    assert response_get.json()[-1]["nome"] == novo_cliente["nome"]

def test_cadastrar_cliente_invalido():
    """ Testa o cadastro de um cliente com dados incorretos """
    cliente_invalido = {
        "nome": "Carlos",
        "idade": "Vinte e Um",  # idade como string (inválido)
        "email": "carlos@exemplo.com",
        "telefone": "1234567890",
        "cidade": "Curitiba",
        "salario": 1800.50
    }

    response = testes.post("/clientes", json=cliente_invalido)
    assert response.status_code == 422  

    # Verifica se o erro contém a mensagem de que a idade é inválida
    assert "Input should be a valid integer" in response.json()["detail"][0]["msg"]
