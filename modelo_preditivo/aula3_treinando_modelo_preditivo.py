import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Carregar e preparar os dados
df = pd.read_excel("relatorio_vindi_25.xlsx")
df = df[df["Entidade"] == "Cliente"].copy()
df["matriculado"] = (df["Cliente.Status"] == "Ativo").astype(int)
df["Ano de Matrícula"] = pd.to_datetime(df["Cliente.DataDeCadastro"], errors="coerce").dt.year

# Seleção de colunas
colunas = ["Endereço.Região", "Endereço.Cidade", "Endereço.Bairro", "Endereço.Estado", "Ano de Matrícula"]
df_features = df[colunas].copy()
df_encoded = pd.get_dummies(df_features)
X = df_encoded
y = df["matriculado"]

# Separar em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Fazer previsões
y_pred = modelo.predict(X_test)

# Avaliar
print("Relatório de Classificação:")
print(classification_report(y_test, y_pred))

print("Matriz de Confusão:")
print(confusion_matrix(y_test, y_pred))

# Obter importâncias
importancias = modelo.feature_importances_
nomes_features = X.columns

# Criar dataframe para exibir em ordem decrescente
df_importancias = pd.DataFrame({
    "feature": nomes_features,
    "importancia": importancias
}).sort_values(by="importancia", ascending=False)

# Mostrar top 10
print(" Top 10 variáveis mais importantes:")
print(df_importancias.head(10))

# Plotar gráfico
plt.figure(figsize=(10, 6))
sns.barplot(
    data=df_importancias.head(15),
    x="importancia",
    y="feature",
    hue="feature",       # ← associa as cores a cada feature
    palette="viridis",
    legend=False         # ← evita mostrar a legenda duplicada
)
plt.title("Importância das Variáveis no Modelo")
plt.xlabel("Importância")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()




# Exportar o modelo
joblib.dump(modelo, "modelo_matricula_rf.joblib")

# Exportar as features (importante para fazer previsões novas depois)
joblib.dump(X.columns.tolist(), "features_usadas.joblib")

print("Modelo e features exportados com sucesso!")
