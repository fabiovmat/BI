import pandas as pd

# 1. Carregar os dados
df = pd.read_excel("G:/estudos/Penglai/BI/relatorio_vindi_25.xlsx")

# 2. Filtrar apenas registros do tipo 'Cliente'
df = df[df["Entidade"] == "Cliente"].copy()

# 3. Criar a variável alvo: 1 se o cliente está ativo, 0 caso contrário
df["matriculado"] = (df["Cliente.Status"] == "Ativo").astype(int)

# 4. Visualizar as primeiras colunas para entender
print("Colunas disponíveis:")
print(df.columns.tolist())

# 5. Verificar quantos clientes estão matriculados e não
print("\nDistribuição dos clientes:")
print(df["matriculado"].value_counts())
