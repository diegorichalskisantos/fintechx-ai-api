import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Caminho relativo correto pois você está na pasta app/faiss_index
with open("docs.json", "r") as f:
    docs = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(docs)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, "index.faiss")
print("index.faiss gerado com sucesso!")
