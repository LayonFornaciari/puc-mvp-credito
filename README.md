# puc-mvp-credito
MVP da Disciplina: Sprint: Qualidade de Software, Segurança e Sistemas Inteligentes

**Aluno:** Layon Fornaciari  
**Curso:** Pós-Graduação em Engenharia de Software (PUC-Rio)  

## 🎯 Sobre o Projeto

Este é o Minimum Viable Product (MVP) desenvolvido para a disciplina de Engenharia de Sistemas de Software Inteligentes. O objetivo do projeto é aplicar os conceitos de Machine Learning, Desenvolvimento Full Stack e Segurança/Qualidade de Software para resolver um problema real: **a previsão de inadimplência (risco de crédito) de clientes bancários.**

O modelo utiliza o clássico *German Credit Data* e foi treinado para identificar padrões que levam um cliente a ser classificado como "Bom Pagador" ou "Mau Pagador".

## 🛡️ Reflexão sobre Segurança e LGPD (Requisito 6)

No contexto de uma instituição financeira real, a base de dados original contaria com PIIs (Personally Identifiable Information), como Nome, CPF, Endereço e Contatos. Para garantir a **Confidencialidade** e o estrito cumprimento da **LGPD (Lei Geral de Proteção de Dados)**:

1. **Anonimização:** O dataset utilizado foi previamente anonimizado. Não há identificadores diretos.

2. **Minimização de Dados:** As variáveis sensíveis (idade, sexo, moradia) são mantidas estritamente para o propósito de modelagem estatística do risco financeiro.

3. **Segurança de API:** A API (Back-end) foi construída utilizando o `Pydantic` para realizar **Validação de Entrada (Input Validation) Rigorosa**. A aplicação rejeita automaticamente idades ilógicas (<18 ou >100) ou valores negativos, mitigando ataques de injeção ou comportamento anômalo do modelo.

## ⚙️ Arquitetura do Sistema

O projeto é um monorepo Full Stack contendo:

* **Machine Learning (O Cérebro):** Treinado no Google Colab usando Scikit-Learn (Pipelines, StandardScaler, GridSearchCV) e algoritmos como KNN, Decision Tree, Naive Bayes e SVM. O modelo vencedor (SVM) foi exportado via `joblib`.

* **Back-end (O Motor):** API construída em **FastAPI** rodando no servidor Uvicorn. Responsável por carregar o modelo `.pkl` e servir o endpoint `POST /prever`.

* **Front-end (A Interface):** Página estática (HTML/CSS/JS) com **Bootstrap 5**, que consome a API de forma assíncrona (`fetch`).

* **Qualidade (A Blindagem):** Testes automatizados criados com **PyTest** para garantir o desempenho e impedir regressão das métricas de Acurácia e Recall do modelo em produção.

## 🚀 Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter o Python 3.10+ instalado.
Instale as dependências executando:

```bash
pip install fastapi uvicorn pydantic pandas scikit-learn joblib pytest
```

### 1. Rodando a API (Back-end)

Pelo terminal, dentro da pasta do projeto, execute:

```bash
python -m uvicorn app:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`. Você pode acessar a documentação interativa (Swagger) em `http://127.0.0.1:8000/docs`.

### 2. Rodando o Front-end

Basta abrir o arquivo `index.html` em qualquer navegador web (Chrome, Firefox, Edge). Preencha o formulário e clique em "Analisar Risco".

### 3. Rodando a Esteira de Testes

Para executar o teste automatizado de qualidade do modelo, abra o terminal e execute:

```bash
python -m pytest test_modelo.py -v
```