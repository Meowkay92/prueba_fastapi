from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Cliente(BaseModel):
    """ Modelo de dados para um cadastro simples de clientes no sistema ficticio

    atributos:
    nome: str => O nome completo do cliente
    idade: int => a idade do cliente em anos como numero inteiro
    email: str => recebe o email do cliente
    telefone: str => telefone do cliente
    cidade: str =>  cidade onde o cliente reside
    salario: float => salario atual ou ultimo salario do cliente como decimal
    """

    nome: str
    idade: int
    email: str
    telefone: str
    cidade: str
    salario: float

clientes = []

@app.get("/")
def root():
    """
        Endpoint de boas-vindas.
        Retorna mensagem de boas vindas quando acessado
    """
    return {"Bem-vindo a API de clientes"}

@app.get("/clientes", response_model=List[Cliente])
def get_clientes():
    """
        Endpoint para retornar todos os clientes cadastrados.
        Retorna uma lista de objetos `Cliente` no formato JSON.
    """
    return clientes

@app.post("/clientes")
def cadastrar_cliente(cliente: Cliente):
    """
        Endpoint para cadastrar um novo cliente.

        Recebe um objeto `Cliente` e o adiciona à lista de clientes.

        Parâmetros:
        - cliente: Objeto do tipo `Cliente` recebido no corpo da requisição.

        Retorna uma mensagem de sucesso com detalhes do cliente cadastrado.
    """
    clientes.append(cliente)
    return {"mensagem": "Cliente cadastrado com sucesso!", "cliente": cliente}
