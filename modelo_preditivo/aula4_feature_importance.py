import matplotlib.pyplot as plt
import seaborn as sns

# Obter importâncias
importancias = modelo.feature_importances_
nomes_features = X.columns

# Criar dataframe para exibir em ordem decrescente
df_importancias = pd.DataFrame({
    "feature": nomes_features,
    "importancia": importancias
}).sort_values(by="importancia", ascending=False)

# Mostrar top 10
print("\n🔍 Top 10 variáveis mais importantes:")
print(df_importancias.head(10))

# Plotar gráfico
plt.figure(figsize=(10, 6))
sns.barplot(data=df_importancias.head(15), x="importancia", y="feature", palette="viridis")
plt.title("Importância das Variáveis no Modelo")
plt.xlabel("Importância")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()
