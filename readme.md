
# 📈 Pipeline de Cotação do Dólar — Apache Airflow

Este projeto implementa uma automação diária utilizando **Apache Airflow** para coletar a cotação do dólar (USD → BRL), salvar os dados em CSV, armazenar em um banco SQLite e registrar uma notificação final.  
É um pipeline simples, mas completo, ideal para estudos de orquestração e ETL.

---

## 🚀 Objetivo do Projeto

Criar uma DAG no Airflow que executa automaticamente todos os dias às **09:00**, realizando:

1. Consulta da cotação do dólar via API pública  
2. Armazenamento da cotação em um arquivo CSV  
3. Inserção dos dados em um banco SQLite  
4. Registro de uma notificação final no log  

Esse fluxo demonstra conceitos essenciais de automação:

- DAGs  
- PythonOperator  
- XCom  
- Dependências entre tarefas  
- Integração com APIs  
- Persistência de dados  

---

## 🧠 Arquitetura do Pipeline

[1] buscar_cotacao
↓
[2] salvar_csv
↓
[3] inserir_banco
↓
[4] notificar

Código

### **1. buscar_cotacao**
- Faz requisição HTTP para uma API de câmbio  
- Extrai o valor atual do dólar  
- Envia o valor para o XCom  

### **2. salvar_csv**
- Recebe o valor via XCom  
- Salva em um arquivo CSV dentro da pasta `dags/`  

### **3. inserir_banco**
- Insere a cotação em um banco SQLite  
- Cria a tabela automaticamente caso não exista  

### **4. notificar**
- Apenas registra no log que o pipeline foi executado com sucesso  

---

## 🛠️ Tecnologias Utilizadas

- **Apache Airflow 2.x**
- **Python 3.10+**
- **Docker e Docker Compose**
- **Pandas**
- **Requests**
- **SQLite**

---

## 📁 Estrutura do Projeto

airflow_dolar/
├── dags/
│    ├── cotacao_dolar.py
│    ├── cotacao_dolar.csv
│    └── cotacoes.db
├── docker-compose.yaml
└── requirements.txt

Código

---

## 📦 Instalação e Configuração

### 1. Clone o repositório

    ```bash
    git clone https://github.com/seu-usuario/airflow-dolar.git
    cd airflow-dolar
    ```

### 2. Instale as dependências do Airflow via requirements.txt
    Arquivo:

    Código
    requests
    pandas
    sqlalchemy

### 3. Suba o ambiente Airflow com Docker
    ```bash
    docker compose up airflow-init
    docker compose up

    A interface estará disponível em:
    
        http://localhost:8080

    Login padrão:

        usuário: airflow
        senha: airflow
    ```

### ▶️ Executando a DAG
    Acesse o painel do Airflow

    Ative a DAG cotacao_dolar_diaria

    Clique em Trigger DAG para testar

    Verifique:

    Logs das tarefas

    Arquivo cotacao_dolar.csv sendo atualizado

    Banco cotacoes.db sendo preenchido

### 📊 Exemplo de Dados Gerados

CSV (cotacao_dolar.csv)

2024-01-10 09:00:01,4.92
2024-01-11 09:00:01,4.95
2024-01-12 09:00:01,4.97

Banco SQLite (cotacoes.db)

Tabela: cotacao_dolar

data	            valor
2024-01-10 09:00:01	4.92
2024-01-11 09:00:01	4.95
