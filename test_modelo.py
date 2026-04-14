import pytest
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score


# ==============================================================================
# TESTE AUTOMATIZADO DE DESEMPENHO DO MODELO (Requisito 5 do MVP)
# ==============================================================================

def test_desempenho_modelo():
    """
    Testa se o modelo exportado atinge os thresholds mínimos de desempenho
    (Acurácia >= 70% e Recall >= 50%) utilizando o dataset original.
    """

    # 1. Carrega o modelo e as colunas esperadas pela API
    try:
        modelo = joblib.load('modelo_credito.pkl')
        colunas_treino = joblib.load('colunas.pkl')
    except FileNotFoundError:
        pytest.fail("Os arquivos do modelo (.pkl) não foram encontrados na pasta.")

    # 2. Carrega o dataset original para validação
    url = 'https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/credit.csv'
    dataset = pd.read_csv(url)

    # 3. Pré-processamento mínimo (Igual ao do Colab)
    # Mapeando: 1 = Good (0), 2 = Bad (1)
    dataset['default'] = dataset['default'].map({1: 0, 2: 1})
    dataset = dataset.dropna(subset=['default'])

    X = dataset.drop('default', axis=1)
    y_true = dataset['default']

    # 4. Aplica o One-Hot Encoding e realinha as colunas para o formato do modelo
    X_encoded = pd.get_dummies(X)
    X_final = X_encoded.reindex(columns=colunas_treino, fill_value=0)

    # 5. Faz as predições com o modelo carregado
    y_pred = modelo.predict(X_final)

    # 6. Calcula as métricas de desempenho
    acuracia = accuracy_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)

    print(f"\n[Métricas do Modelo] Acurácia: {acuracia:.2f} | Recall: {recall:.2f}")

    # 7. OS ASSERTS (A "Blindagem")
    # Se alguma dessas condições for falsa, o PyTest trava a esteira de CI/CD
    assert acuracia >= 0.70, f"Acurácia abaixo do limite aceitável! Atual: {acuracia:.2f}"
    assert recall >= 0.50, f"Recall abaixo do limite aceitável! Atual: {recall:.2f}"