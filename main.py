from fastapi import FastAPI
from pydantic import BaseModel, field_validator
from typing import List

app = FastAPI()

class Cliente(BaseModel):
    """
    Modelo de dados para o cadastro de clientes.

    Atributos:
    - nome: Nome do cliente (tipo string)
    - idade: Idade do cliente (tipo inteiro)
    - email: Email do cliente (tipo string)
    - telefone: Número de telefone do cliente (tipo string)
    - cidade: Cidade onde o cliente reside (tipo string)
    - salario: Salário do cliente (tipo float)
    """
    
    nome: str
    idade: int
    email: str
    telefone: str
    cidade: str
    salario: float

    # Validador de idade atualizado para Pydantic v2
    @field_validator('idade')
    def idade_deve_ser_inteiro(cls, v):
        """
        Valida que o valor da idade seja um número inteiro. Caso contrário,
        gera um erro personalizado.
        
        Parâmetros:
        - v: Valor da idade a ser validado
        
        Retorna:
        - v: Valor validado
        
        Exceção:
        - Lança um ValueError se o valor da idade não for um inteiro
        """
        if not isinstance(v, int):
            raise ValueError('Idade não é um valor inteiro')
        return v

    # Usando ConfigDict para configurações no Pydantic v2
    class ConfigDict:
        """
        Configurações adicionais para o modelo. Usado para definir exemplos
        na documentação gerada automaticamente pela FastAPI.
        """
        json_schema_extra = {
            "example": {
                "nome": "Cleberton Silva",
                "idade": 32,
                "email": "cleberton@cleberton",
                "telefone": "111234567890",
                "cidade": "São Paulo",
                "salario": 2540.50,
            }
        }

clientes = []  # Lista que armazenará os clientes cadastrados.

@app.get("/")
def root():
    """
    Endpoint de boas-vindas.

    Retorna uma mensagem simples de boas-vindas.
    
    Retorna:
    - dict: {"message": "Bem-vindo a API de clientes"}
    """
    return {"message": "Bem-vindo a API de clientes"}

@app.get("/clientes", response_model=List[Cliente])
def get_clientes():
    """
    Endpoint para listar todos os clientes cadastrados.

    Retorna:
    - List[Cliente]: Lista de objetos cliente no formato JSON
    """
    return clientes

@app.post("/clientes")
def cadastrar_cliente(cliente: Cliente):
    """
    Endpoint para cadastrar um novo cliente.

    Recebe um objeto do tipo `Cliente` no corpo da requisição e o adiciona
    à lista de clientes cadastrados.

    Parâmetros:
    - cliente: Objeto do tipo `Cliente` com os dados do cliente a ser cadastrado

    Retorna:
    - dict: Mensagem de sucesso com os detalhes do cliente cadastrado
    """
    clientes.append(cliente)
    return {"mensagem": "Cliente cadastrado com sucesso!", "cliente": cliente}
