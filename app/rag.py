import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Caminhos dos arquivos
INDEX_PATH = "app/faiss_index/index.faiss"
DOCS_PATH = "app/faiss_index/docs.json"

# Carrega modelos e dados
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(INDEX_PATH)
with open(DOCS_PATH, "r") as f:
    docs = json.load(f)

def buscar_contexto_relevante(pergunta: str, k: int = 3) -> str:
    """Busca os k trechos mais semelhantes à pergunta"""
    pergunta_embedding = model.encode([pergunta])
    _, indices = index.search(np.array(pergunta_embedding), k)
    trechos = [docs[i] for i in indices[0]]
    return "\n---\n".join(trechos)
