from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Carregar modelo e features
modelo = joblib.load("../modelo_matricula_rf.joblib")
features = joblib.load("../features_usadas.joblib")

# Inicializar app
app = FastAPI(title="API de Previsão de Matrícula")

# Modelo de dados esperado na requisição
class ClienteInput(BaseModel):
    regiao: str
    ano: int

@app.post("/predict")
def prever_matricula(dados: ClienteInput):
    # Criar dicionário com todas as features zeradas
    entrada = {col: 0 for col in features}
    
    # Preencher com dados do cliente
    col_regiao = f"Endereço.Região_{dados.regiao}"
    if col_regiao in entrada:
        entrada[col_regiao] = 1
    entrada["Ano de Matrícula"] = dados.ano

    # Criar DataFrame e prever
    df_input = pd.DataFrame([entrada])
    pred = modelo.predict(df_input)[0]
    prob = modelo.predict_proba(df_input)[0][1]

    return {
        "previsao": "Matriculado" if pred == 1 else "Não Matriculado",
        "probabilidade": round(prob * 100, 2)
    }
