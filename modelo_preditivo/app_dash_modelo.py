import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import joblib
import pandas as pd

# Carregar modelo e features
modelo = joblib.load("modelo_matricula_rf.joblib")
features = joblib.load("features_usadas.joblib")

# Opções que aparecem no formulário
opcoes_regiao = ["Centro", "Zona Oeste", "Zona Sul", "Zona Leste", "Zona Norte", "Sudoeste", "Sudeste"]

# Criar app
app = dash.Dash(__name__)
app.title = "Previsão de Matrícula"

app.layout = html.Div([
    html.H2("Previsão de Matrícula de Cliente", style={"textAlign": "center"}),

    html.Label("Região"),
    dcc.Dropdown(
        id="regiao",
        options=[{"label": r, "value": r} for r in opcoes_regiao],
        value="Centro"
    ),

    html.Br(),
    html.Label("Ano de Cadastro"),
    dcc.Input(id="ano", type="number", value=2025),

    html.Br(), html.Br(),
    html.Button("Prever", id="botao", n_clicks=0),
    html.Div(id="saida_previsao", style={"marginTop": "20px", "fontSize": 20})
])

@app.callback(
    Output("saida_previsao", "children"),
    Input("botao", "n_clicks"),
    State("regiao", "value"),
    State("ano", "value")
)
def prever(n_clicks, regiao, ano):
    if n_clicks == 0:
        return ""

    # Criar dicionário com todas as features = 0
    entrada = {col: 0 for col in features}

    # Preencher as escolhidas
    col_regiao = f"Endereço.Região_{regiao}"
    if col_regiao in entrada:
        entrada[col_regiao] = 1

    entrada["Ano de Matrícula"] = ano

    # Criar DataFrame e prever
    df_novo = pd.DataFrame([entrada])
    pred = modelo.predict(df_novo)[0]
    prob = modelo.predict_proba(df_novo)[0][1]

    texto = f"Chance de matrícula: {round(prob * 100, 2)}%"

    if pred == 1:
        return html.Div([texto, html.Div("Resultado: Provável que se matricule", style={"color": "green"})])
    else:
        return html.Div([texto, html.Div("Resultado: Pouca chance de matrícula", style={"color": "red"})])

if __name__ == "__main__":
    app.run(debug=True)
