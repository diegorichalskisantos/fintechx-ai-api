from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.llm import pergunta_para_sql
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PerguntaRequest(BaseModel):
    pergunta: str

@app.post("/pergunta")
async def responder_pergunta(body: PerguntaRequest):
    resposta = pergunta_para_sql(body.pergunta)
    return resposta

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "cursorclass": pymysql.cursors.DictCursor
}

@app.get("/tabelas")
async def listar_tabelas():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLES;")
                tabelas = [row[f'Tables_in_{DB_CONFIG["database"]}'] for row in cursor.fetchall()]

                estrutura = []
                for tabela in tabelas:
                    cursor.execute(f"SHOW COLUMNS FROM {tabela};")
                    colunas = [coluna["Field"] for coluna in cursor.fetchall()]
                    estrutura.append({
                        "nome": tabela,
                        "campos": colunas
                    })

        return estrutura
    except Exception as e:
        return {"erro": str(e)}
