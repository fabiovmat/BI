import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def ler_excel(caminho_arquivo):
    """
    Lê um arquivo Excel com endereços e regiões e retorna um DataFrame.

    Parâmetros:
    caminho_arquivo (str): Caminho do arquivo .xlsx a ser lido.

    Retorna:
    pd.DataFrame: Dados carregados do Excel.
    """
    try:
        df = pd.read_excel("G:/estudos/Penglai/BI/relatorio_vindi_25.xlsx")
        print("Arquivo carregado com sucesso!")
        return df
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None

# Exemplo de uso
caminho = "relatorio_vindi_25.xlsx"
df_ler = ler_excel(caminho)

#filtro primeira coluna
df_clientes = df_ler[df_ler["Entidade"] == "Cliente"]
#filtro somente ativos
df_somente_ativos = df_clientes[df_clientes["Cliente.Status"] == "Ativo"] 

#print(df_somente_ativos)
#print(df_ler.columns.tolist())

#filtra somente as coluans que eu quero
# 3. Manter apenas as colunas desejadas
colunas_desejadas = [
    "Entidade", "Cliente.Id", "Cliente.Nome", "Cliente.NúmeroDoDocumento",
    "Cliente.EMail", "Cliente.CódigoExterno", "Cliente.Telefones",
    "Endereço.Endereço", "Endereço.Número", "Endereço.Bairro", "Endereço.Região",
    "Endereço.Complemento", "Endereço.Cep", "Endereço.Cidade", "Endereço.Estado",
    "Endereço.País", "Cliente.DataDeCadastro", "Cliente.Status"]

df_reduzido = df_somente_ativos[colunas_desejadas].copy()

#cria um coluna ano de cadastro e imprime o ano pegando da coluna de data de matricula
df_reduzido["Ano de Matrícula"] = pd.to_datetime(df_reduzido["Cliente.DataDeCadastro"]).dt.year

# Filtrar apenas clientes ativos
df_clientes = df_ler[df_ler["Entidade"] == "Cliente"]
df_ativos = df_clientes[df_clientes["Cliente.Status"] == "Ativo"].copy()

# Criar a coluna "Ano de Matrícula"
df_ativos["Ano de Matrícula"] = pd.to_datetime(df_ativos["Cliente.DataDeCadastro"], errors='coerce').dt.year

sns.set(style="whitegrid")

#print(df_reduzido)
# === GRÁFICO 1: Clientes por Região ===
# === GRÁFICO 1: Clientes por Região ===
plt.figure(figsize=(10, 6))
ax1 = sns.countplot(
    data=df_ativos,
    y="Endereço.Região",
    order=df_ativos["Endereço.Região"].value_counts().index,
    hue="Endereço.Região",
    palette="pastel",
    legend=False
)
plt.title("Clientes Ativos por Região")
plt.xlabel("Quantidade")
plt.ylabel("Região")
for p in ax1.patches:
    ax1.annotate(f'{int(p.get_width())}', (p.get_width() + 0.5, p.get_y() + p.get_height() / 2), va='center')
plt.tight_layout()
plt.show()

# === GRÁFICO 2: Matrículas por Ano ===
# === GRÁFICO 2: Matrículas por Ano ===
plt.figure(figsize=(10, 6))
anos_ordenados = sorted(df_ativos["Ano de Matrícula"].dropna().unique())
ax2 = sns.countplot(
    data=df_ativos,
    x="Ano de Matrícula",
    order=anos_ordenados,
    hue="Ano de Matrícula",
    palette="Set2",
    legend=False
)
plt.title("Matrículas por Ano")
plt.xlabel("Ano")
plt.ylabel("Quantidade")
for p in ax2.patches:
    ax2.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2, p.get_height() + 0.3), ha='center')
plt.tight_layout()
plt.show()


# Gráfico 3: Top 10 Cidades
# === GRÁFICO 3: Top 10 Cidades ===
top_cidades = df_ativos["Endereço.Cidade"].value_counts().head(10)
df_top_cidades = df_ativos[df_ativos["Endereço.Cidade"].isin(top_cidades.index)]
plt.figure(figsize=(10, 6))
ax3 = sns.countplot(
    data=df_top_cidades,
    y="Endereço.Cidade",
    order=top_cidades.index,
    hue="Endereço.Cidade",
    palette="coolwarm",
    legend=False
)
plt.title("Top 10 Cidades com Mais Clientes Ativos")
plt.xlabel("Quantidade")
plt.ylabel("Cidade")
for p in ax3.patches:
    ax3.annotate(f'{int(p.get_width())}', (p.get_width() + 0.5, p.get_y() + p.get_height() / 2), va='center')
plt.tight_layout()
plt.show()

# === GRÁFICO 4: Top 10 Bairros ===
top_bairros = df_ativos["Endereço.Bairro"].value_counts().head(10)
df_top_bairros = df_ativos[df_ativos["Endereço.Bairro"].isin(top_bairros.index)]
plt.figure(figsize=(10, 6))
ax4 = sns.countplot(
    data=df_top_bairros,
    y="Endereço.Bairro",
    order=top_bairros.index,
    hue="Endereço.Bairro",
    palette="Blues_d",
    legend=False
)
plt.title("Top 10 Bairros com Mais Clientes Ativos")
plt.xlabel("Quantidade")
plt.ylabel("Bairro")
for p in ax4.patches:
    ax4.annotate(f'{int(p.get_width())}', (p.get_width() + 0.5, p.get_y() + p.get_height() / 2), va='center')
plt.tight_layout()
plt.show()

# === GRÁFICO 5: Pizza - Ativos vs Inativos ===
status_counts = df_clientes["Cliente.Status"].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
plt.title("Distribuição de Clientes Ativos vs Inativos")
plt.tight_layout()
plt.show()

# === GRÁFICO 6: Crescimento acumulado por ano ===
cadastros_por_ano = df_ativos["Ano de Matrícula"].value_counts().sort_index()
cresc_acumulado = cadastros_por_ano.cumsum()
plt.figure(figsize=(10, 6))
sns.lineplot(x=cresc_acumulado.index, y=cresc_acumulado.values, marker="o", color="teal")
plt.title("Crescimento Acumulado de Clientes Ativos por Ano")
plt.xlabel("Ano")
plt.ylabel("Total Acumulado de Clientes Ativos")
for x, y in zip(cresc_acumulado.index, cresc_acumulado.values):
    plt.text(x, y + 2, str(y), ha='center')
plt.grid(True)
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt

# Total de clientes ativos
total_ativos = df_ativos.shape[0]

#Criar uma visualização estilo cartão
plt.figure(figsize=(6, 3))
plt.text(0.5, 0.5, f'{total_ativos:,} Clientes Ativos',  # separador de milhar
         fontsize=24, fontweight='bold', color='green',
         ha='center', va='center')

# Remover eixos e moldura
plt.axis('off')
plt.title("Total Geral de Clientes Ativos", fontsize=16)
plt.tight_layout()
plt.show()


