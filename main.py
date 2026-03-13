from pathlib import Path
from sqlalchemy import create_engine, text
import pandas as pd
from fastapi import FastAPI
# configuracao do conexao com banco de dados
host = "127.0.0.1"
port = 3306
user = "root"
password = "Lilika10#"
banco_dados = "db_escola"
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{banco_dados}")
# instaciar
app = FastAPI()


@app.get("/alunos/")
def listar_alunos():
    query = "select * from tb_alunos"
    df_alunos = pd.read_sql(query, con=engine)
    return df_alunos.to_dict(orient="records")


@app.get("/enderecos/")
def listar_enderecos():
    query2 = " select * from tb_enderecos "
    df_enderecos=pd.read_sql(query2, con=engine)
    return df_enderecos.to_dict(orient="records")

@app.get("/enderecos+alunos/")
def listar_enderecos_alunos():
    query3 = " select * from  vw_alunos_enderecos"
    df_enderecos_alunos=pd.read_sql(query3, con=engine)
    return df_enderecos_alunos.to_dict(orient="records")

@app.post("/cadastrar-aluno/")
def cadastrar_alunos(aluno:dict):
   df = pd.DataFrame([aluno])
   df.to_sql("tb_alunos", engine, if_exists="append", index=False)
   return{"mensagem": "Aluno Cadastrado com sucesso"}



@app.put("/atualizar-alunos/{id}")
def atualizar_alunos(id: int, alunos: dict):
    with engine.begin() as conn:
        conn.execute(text(
            """
            update tb_alunos
            set matricula = matricula
            nome_aluno = nome_aluno
            endereco_id = endereco_id
            where id = id
            """,
        ), {"id": id, **alunos}
        )
    return {"mensagem": "Aluno atualizado com sucesso"}


@app.delete("/deletar-alunos/{id}")
def deletar_alunos(id:int):
    with engine.begin() as conn:
        conn.execute(
            text(
            """
            delete from tb_alunos
            where id = :id
            """
            ), {"id":id }
        )
    return{"message":"Aluno Removido"}

#enderecos

from fastapi import FastAPI
import pandas as pd
import requests

app = FastAPI()


@app.post("/cadastrar-endereco/")
def cadastrar_endereco(cep: str):

    url = f"https://viacep.com.br/ws/{cep}/json/"
    resposta = requests.get(url)

    dados = resposta.json()

    endereco = {
        "cep": dados["cep"],
        "endereco": dados["logradouro"],
        "bairro": dados["bairro"],
        "cidade": dados["localidade"],
        "estado": dados["uf"],
        "regiao": "Centro"
    }

    df = pd.DataFrame([endereco])
    df.to_sql("tb_enderecos", engine, if_exists="append", index=False)

    return {"mensagem": "Endereço cadastrado com sucesso"}

@app.get("/buscar-endereco/{cep}")
def buscar_endereco(cep: str):

    query = f"SELECT * FROM tb_enderecos WHERE cep = '{cep}'"
    df = pd.read_sql(query, con=engine)

    return df.to_dict(orient="records")
  
  @app.post("/cadastrar-endereco/")
def cadastrar_endereco(cpf: str, cep: str):

    url = f"https://viacep.com.br/ws/{cep}/json/"
    resposta = requests.get(url)

    dados = resposta.json()

    endereco = {
        "cpf": cpf,
        "cep": dados["cep"],
        "endereco": dados["logradouro"],
        "bairro": dados["bairro"],
        "cidade": dados["localidade"],
        "estado": dados["uf"],
        "regiao": "Centro"
    }

    df = pd.DataFrame([endereco])
    df.to_sql("tb_enderecos", engine, if_exists="append", index=False)

    return {"mensagem": "Endereço cadastrado com sucesso"}