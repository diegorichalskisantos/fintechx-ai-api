from app.rag import buscar_contexto_relevante
from app.graficos import gerar_grafico_barra_base64
from openai import OpenAI
import pymysql
import os
import re
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "cursorclass": pymysql.cursors.DictCursor
}

def validar_sql(sql: str) -> bool:
    sql = sql.strip().lower()
    comandos_proibidos = ["insert", "update", "delete", "drop", "alter", "create", "truncate"]
    if not sql.startswith("select"):
        return False
    if any(cmd in sql for cmd in comandos_proibidos):
        return False
    return True

@lru_cache(maxsize=128)
def _processar_pergunta_cached(pergunta: str) -> dict:
    contexto = buscar_contexto_relevante(pergunta)

    prompt = f"""
Você é um assistente que transforma perguntas em SQL.

Base de dados: Northwind (MySQL)

Contexto extraído dos documentos:
-------------------------------
{contexto}
-------------------------------

Pergunta: {pergunta}

Retorne apenas a query SQL válida.
"""

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente especializado em SQL para MySQL."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    conteudo = resposta.choices[0].message.content.strip()
    match = re.search(r"```sql\n(.*)\n```", conteudo, re.DOTALL)
    sql = match.group(1).strip() if match else conteudo.strip()

    if not validar_sql(sql):
        return {
            "pergunta": pergunta,
            "sql_sugerido": sql,
            "erro_validacao": "Query não permitida. Apenas SELECTs simples são aceitos."
        }

    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                resultado = cursor.fetchall()
    except Exception as e:
        return {
            "pergunta": pergunta,
            "sql_sugerido": sql,
            "erro_execucao": str(e)
        }

    grafico = None
    if resultado and isinstance(resultado, list) and len(resultado[0]) >= 2:
        colunas = list(resultado[0].keys())
        labels = [str(row[colunas[0]]) for row in resultado]
        try:
            valores = [float(row[colunas[1]]) for row in resultado]
            grafico = gerar_grafico_barra_base64(labels, valores, titulo=pergunta)
        except Exception:
            grafico = None

    return {
        "pergunta": pergunta,
        "sql_sugerido": sql,
        "resultado": resultado,
        "grafico_base64": grafico
    }

def pergunta_para_sql(pergunta: str):
    return _processar_pergunta_cached(pergunta)
