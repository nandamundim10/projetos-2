# API de Endereço

API simples feita com **FastAPI** que recebe um **CEP**, consulta os dados no ViaCEP e salva o endereço em um banco **MySQL**.

Também é possível buscar um endereço já cadastrado usando o CEP.

## Tecnologias

* FastAPI
* Uvicorn
* Pandas
* MySQL
* ViaCEP

## Como rodar o projeto

1. Instalar as dependências

```
pip install -r requirements.txt
```

2. Rodar a API

```
uvicorn main:app --reload
```

3. Acessar a documentação

```
http://127.0.0.1:8000/docs
```

## Endpoints

**Cadastrar endereço**

```
POST /cadastrar-endereco/
```

Recebe um CEP, consulta o ViaCEP e salva no banco.

**Buscar endereço**

```
GET /buscar-endereco/{cep}
```

Retorna o endereço cadastrado no banco.
