import pandas as pd

# Carregar e preparar base
df = pd.read_excel("relatorio_vindi_25.xlsx")
df = df[df["Entidade"] == "Cliente"].copy()
df["matriculado"] = (df["Cliente.Status"] == "Ativo").astype(int)

# Extrair ano da matrícula
df["Ano de Matrícula"] = pd.to_datetime(df["Cliente.DataDeCadastro"], errors="coerce").dt.year

# Selecionar colunas de interesse (features)
colunas_features = [
    "Endereço.Região",
    "Endereço.Cidade",
    "Endereço.Bairro",
    "Endereço.Estado",
    "Ano de Matrícula"
]

df_features = df[colunas_features].copy()
df_target = df["matriculado"]

# Codificar variáveis categóricas (One Hot Encoding)
df_features_encoded = pd.get_dummies(df_features)

# Mostrar o shape (linhas x colunas) e primeiras colunas
print(f"Shape das features codificadas: {df_features_encoded.shape}")
print("Colunas codificadas:")
print(df_features_encoded.columns.tolist())

# Preparar para treino
X = df_features_encoded
y = df_target
