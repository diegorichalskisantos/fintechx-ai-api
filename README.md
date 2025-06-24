
# 💸 FintechX — Desafio Técnico Laborit

API inteligente que transforma perguntas em linguagem natural em consultas SQL otimizadas sobre o banco de dados Northwind. Projeto construído com foco em arquitetura limpa, escalabilidade e deploy automatizado via CI/CD.

---

## 📦 Tecnologias utilizadas

- **Python 3.11**
- **FastAPI**
- **Docker + Docker Compose**
- **MySQL (Northwind)**
- **OpenAI GPT-4 (via API)**
- **FAISS (vector search)**
- **GitHub Actions (CI/CD)**
- **AWS EC2 (Deploy)**

---

## 🧠 Funcionalidade principal

A API expõe um endpoint que recebe perguntas em linguagem natural e retorna a resposta da consulta SQL equivalente, executada no banco **Northwind**:

```http
POST /pergunta
```

### Exemplo de payload:

```json
{
  "pergunta": "Quais produtos foram mais vendidos?"
}
```

### Exemplo de resposta:

```json
{
  "resposta": [
    {
      "product_name": "Côte de Blaye",
      "total_vendido": 110
    },
    ...
  ]
}
```

---

## 🧱 Estrutura do Projeto

```text
fintechx-ai-api/
├── app/
│   ├── main.py                 # Ponto de entrada da API
│   ├── llm.py                  # Função pergunta_para_sql() com LLM + FAISS
│   ├── database.py             # Conexão com MySQL (Northwind)
│   ├── faiss_index/            # Índice vetorial FAISS
│   └── utils/                  # Utilitários internos
├── docker-compose.yml         # Orquestração de containers
├── Dockerfile                 # Imagem da API
├── .env                       # Variáveis de ambiente (ignorado no git)
├── .github/workflows/
│   └── deploy.yml             # CI/CD via GitHub Actions
├── requirements.txt
└── README.md
```

---

## 🚀 Como rodar localmente

### 1. Clone o projeto

```bash
git clone https://github.com/diegorichalskisantos/fintechx-ai-api.git
cd fintechx-ai-api
```

### 2. Configure o `.env`

Crie um arquivo `.env` com:

```env
DB_HOST=db
DB_USER=root
DB_PASSWORD=123456
DB_NAME=northwind
OPENAI_API_KEY=sk-xxxx
```

### 3. Suba os containers

```bash
docker-compose up --build
```

Acesse localmente via:  
📍 `http://localhost:8000/docs`

---

## 🧠 Como a inteligência funciona?

1. O usuário envia uma pergunta
2. O sistema busca documentos relacionados com FAISS (RAG)
3. Gera prompt e envia para o OpenAI (GPT-4)
4. Recebe um SQL otimizado como resposta
5. Executa no banco de dados MySQL (Northwind)
6. Retorna os dados para o usuário

---

## 📚 Sobre o banco Northwind

O projeto utiliza uma versão MySQL do clássico banco Northwind (clientes, produtos, pedidos, etc).

Ele é automaticamente importado no container MySQL via volume e init script.

---

## 🌐 Deploy em produção (EC2)

A aplicação está rodando em produção via Docker na AWS EC2, com deploy automatizado:

### 🔗 Link de acesso

🟢 Acesse a API em produção:  
👉 [http://56.124.51.31:8000/docs](http://56.124.51.31:8000/docs)

---

## 🔄 CI/CD com GitHub Actions

Toda vez que um push é feito na branch `main`, o seguinte fluxo é executado automaticamente:

- GitHub Actions inicia pipeline
- Ativa chave SSH (armazenada como secret `EC2_SSH_KEY`)
- Conecta via SSH na EC2
- Roda comandos remotos:
  ```bash
  git pull origin main
  docker-compose down
  docker-compose up -d --build
  ```

🛠️ Arquivo de workflow: `.github/workflows/deploy.yml`

---

## 🛡️ Segurança e Boas Práticas

- `.env` está no `.gitignore`
- Acesso SSH feito com **chave exclusiva para CI/CD**
- Secrets mantidos no GitHub (`EC2_SSH_KEY`)
- Consulta SQL validada antes de execução
- Dockerizado e isolado por serviço (API / banco)

---

## 📸 Diagrama de arquitetura

![Arquitetura FintechX](./docs/arquitetura.png)

---

## 👨‍💻 Autor

Desenvolvido por [Diego Richalski Santos](https://github.com/diegorichalskisantos)  

---
