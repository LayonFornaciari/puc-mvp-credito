from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd

# Instanciando a aplicação
app = FastAPI(
    title="API de Previsão de Risco de Crédito",
    description="API para classificar clientes como Baixo Risco ou Alto Risco de inadimplência.",
    version="1.0"
)

# Configuração de Segurança (CORS) - Permite que o nosso Front-end (HTML) faça requisições
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para produção, isso seria restrito ao domínio do banco
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregando o modelo e as colunas na memória assim que a API liga
try:
    modelo = joblib.load('modelo_credito.pkl')
    colunas_treino = joblib.load('colunas.pkl')
except FileNotFoundError:
    print("ERRO: Os arquivos .pkl não foram encontrados. Coloque-os na mesma pasta do app.py")


# ==============================================================================
# DISCIPLINA DE SEGURANÇA: Input Validation (Validação de Entrada) com Pydantic
# ==============================================================================
class Cliente(BaseModel):
    # O usuário digitará apenas estes 5 campos no Front-end:
    age: int = Field(..., gt=17, lt=100, description="Idade do cliente (deve ser > 17 e < 100)")
    amount: float = Field(..., gt=0, description="Valor do empréstimo solicitado (deve ser > 0)")
    months_loan_duration: int = Field(..., gt=0, description="Duração do empréstimo em meses")
    checking_balance: str = Field(...,
                                  description="Status da conta corrente ('< 0 DM', '1 - 200 DM', '> 200 DM', 'unknown')")
    purpose: str = Field(...,
                         description="Propósito do empréstimo ('car', 'furniture/equipment', 'radio/tv', 'education')")

    # Valores padrão inseridos automaticamente para não cansar o usuário no MVP
    credit_history: str = "existing paid"
    savings_balance: str = "< 100 DM"
    employment_length: str = "1 - 4 yrs"
    installment_rate: int = 4
    personal_status: str = "single male"
    other_debtors: str = "none"
    residence_history: int = 4
    property: str = "real estate"
    installment_plan: str = "none"
    housing: str = "own"
    existing_credits: int = 1
    dependents: int = 1
    telephone: str = "none"
    foreign_worker: str = "yes"
    job: str = "skilled employee"


@app.post("/prever")
def prever_risco(cliente: Cliente):
    try:
        # 1. Transforma o JSON validado pelo Pydantic em um DataFrame (1 linha)
        df_entrada = pd.DataFrame([cliente.dict()])

        # 2. Aplica o One-Hot Encoding (get_dummies) nos dados de entrada
        df_encoded = pd.get_dummies(df_entrada)

        # 3. ROBUSTEZ: Realinha as colunas com as 48 colunas exatas do treinamento.
        # Preenche com 0 as categorias de colunas que não apareceram neste cliente único.
        df_final = df_encoded.reindex(columns=colunas_treino, fill_value=0)

        # 4. Chama a Inteligência Artificial para fazer a previsão
        predicao = modelo.predict(df_final)

        # 5. Formata a resposta
        resultado = int(predicao[0])
        mensagem = "Alto Risco de Inadimplência (Reprovado)" if resultado == 1 else "Baixo Risco (Aprovado)"

        return {
            "codigo_risco": resultado,
            "mensagem": mensagem
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao realizar a predição: {str(e)}")


# Endpoint raiz só para verificar se a API está de pé
@app.get("/")
def root():
    return {"status": "API de Risco de Crédito Operacional. Use o endpoint POST /prever"}

# ==============================================================================
# BLOCO PARA RODAR A API DIRETO PELO PYCHARM (SEM PRECISAR DO TERMINAL)
# ==============================================================================
if __name__ == "__main__":
    import uvicorn
    print("Iniciando a API de Risco de Crédito...")
    uvicorn.run(app, host="127.0.0.1", port=8000)