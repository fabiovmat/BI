from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime
import traceback
import logging

# Configurar log
logging.basicConfig(
    filename="erro_dashboard.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

try:
    # Carrega dados
    df = pd.read_excel("relatorio_vindi_25.xlsx")
    df_clientes = df[df["Entidade"] == "Cliente"]
    df_ativos = df_clientes[df_clientes["Cliente.Status"] == "Ativo"].copy()
    df_ativos["Ano de Matrícula"] = pd.to_datetime(df_ativos["Cliente.DataDeCadastro"], errors='coerce').dt.year
    total = df_clientes.shape[0]
    ativos = df_ativos.shape[0]
    inativos = total - ativos

    # Criar PDF (agora tudo em um único bloco)
    with PdfPages("dashboard_clientes.pdf") as pdf:
        
        # === CAPA ===
        fig_capa = plt.figure(figsize=(10, 6))
        plt.axis('off')
        plt.text(0.5, 0.9, "Dashboard de Clientes", fontsize=24, fontweight='bold', ha='center')
        plt.text(0.5, 0.78, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", fontsize=12, ha='center')
        plt.text(0.5, 0.66, f"Total de Clientes: {total:,}", fontsize=14, ha='center')
        plt.text(0.5, 0.60, f"Clientes Ativos: {ativos:,}  |  Inativos: {inativos:,}", fontsize=14, ha='center')
        plt.text(0.5, 0.48, "Este relatório apresenta visualizações de distribuição, evolução\n"
                            "temporal e características geográficas dos clientes cadastrados.",
                 fontsize=12, ha='center')
        plt.text(0.5, 0.30, "Fonte: Sistema de Cadastro", fontsize=10, ha='center', color='gray')
        pdf.savefig(fig_capa)
        plt.close(fig_capa)

        # === Página 1 ===
        fig1, axs = plt.subplots(1, 2, figsize=(14, 6))
        sns.countplot(data=df_ativos, y="Endereço.Região", order=df_ativos["Endereço.Região"].value_counts().index,
                    hue="Endereço.Região", palette="pastel", legend=False, ax=axs[0])
        axs[0].set_title("Clientes Ativos por Região")
        for p in axs[0].patches:
            axs[0].annotate(f'{int(p.get_width())}', (p.get_width() + 0.5, p.get_y() + p.get_height() / 2), va='center')

        anos_ordenados = sorted(df_ativos["Ano de Matrícula"].dropna().unique())
        sns.countplot(data=df_ativos, x="Ano de Matrícula", order=anos_ordenados,
                    hue="Ano de Matrícula", palette="Set2", legend=False, ax=axs[1])
        axs[1].set_title("Matrículas por Ano")
        for p in axs[1].patches:
            axs[1].annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2, p.get_height() + 0.3), ha='center')

        plt.tight_layout()
        pdf.savefig(fig1)
        plt.close(fig1)

        # === Página 2 ===
        fig2, axs = plt.subplots(1, 2, figsize=(14, 6))
        top_cidades = df_ativos["Endereço.Cidade"].value_counts().head(10)
        df_top_cidades = df_ativos[df_ativos["Endereço.Cidade"].isin(top_cidades.index)]
        sns.countplot(data=df_top_cidades, y="Endereço.Cidade", order=top_cidades.index,
                    hue="Endereço.Cidade", palette="coolwarm", legend=False, ax=axs[0])
        axs[0].set_title("Top 10 Cidades com Mais Clientes")
        for p in axs[0].patches:
            axs[0].annotate(f'{int(p.get_width())}', (p.get_width() + 0.5, p.get_y() + p.get_height() / 2), va='center')

        top_bairros = df_ativos["Endereço.Bairro"].value_counts().head(10)
        df_top_bairros = df_ativos[df_ativos["Endereço.Bairro"].isin(top_bairros.index)]
        sns.countplot(data=df_top_bairros, y="Endereço.Bairro", order=top_bairros.index,
                    hue="Endereço.Bairro", palette="Blues_d", legend=False, ax=axs[1])
        axs[1].set_title("Top 10 Bairros com Mais Clientes")
        for p in axs[1].patches:
            axs[1].annotate(f'{int(p.get_width())}', (p.get_width() + 0.5, p.get_y() + p.get_height() / 2), va='center')

        plt.tight_layout()
        pdf.savefig(fig2)
        plt.close(fig2)

        # === Página 3 ===
        fig3 = plt.figure(figsize=(10, 12))
        plt.subplot(2, 1, 1)
        status_counts = df_clientes["Cliente.Status"].value_counts()
        plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90,
                colors=sns.color_palette("pastel"))
        plt.title("Distribuição de Clientes Ativos vs Inativos")

        plt.subplot(2, 1, 2)
        cadastros_por_ano = df_ativos["Ano de Matrícula"].value_counts().sort_index()
        cresc_acumulado = cadastros_por_ano.cumsum()
        sns.lineplot(x=cresc_acumulado.index, y=cresc_acumulado.values, marker="o", color="teal")
        plt.title("Crescimento Acumulado de Clientes Ativos por Ano")
        plt.xlabel("Ano")
        plt.ylabel("Total Acumulado")
        for x, y in zip(cresc_acumulado.index, cresc_acumulado.values):
            plt.text(x, y + 2, str(y), ha='center')

        plt.tight_layout()
        pdf.savefig(fig3)
        plt.close(fig3)

    print("Dashboard gerado com sucesso!")

except Exception as e:
    erro_completo = traceback.format_exc()
    logging.error("Erro ao gerar o dashboard:\n" + erro_completo)
    print("Ocorreu um erro. Veja o arquivo 'erro_dashboard.log' para detalhes.")
