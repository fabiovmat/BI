# 📊 Dashboard de Clientes - Relatório em PDF

Este projeto gera automaticamente um **relatório profissional em PDF** com gráficos e indicadores sobre os clientes cadastrados no sistema. Foi desenvolvido em Python com foco em clareza, automação e compatibilidade com usuários não técnicos.

---

## 📁 Funcionalidades

- ✅ Filtra automaticamente **clientes ativos**
- ✅ Gera **6 gráficos** com `Seaborn` e `Matplotlib`
- ✅ Cria uma **capa personalizada** com título, data e KPIs
- ✅ Salva os gráficos em um **PDF com múltiplas páginas**
- ✅ Captura erros e salva em `erro_dashboard.log` para suporte técnico

---

## 🖼️ Gráficos gerados

1. **Clientes por Região**
2. **Matrículas por Ano**
3. **Top 10 Cidades**
4. **Top 10 Bairros**
5. **Distribuição de Status (Ativos vs Inativos)**
6. **Crescimento Acumulado por Ano**
7. **Card de Total de Clientes Ativos**

---

## 🧰 Tecnologias

- Python 3.8+
- Pandas
- Seaborn
- Matplotlib

---

## ▶️ Como executar

1. Instale os pacotes necessários (use um ambiente virtual se desejar):
  
   pip install pandas matplotlib seaborn
2. Execute python gera_relatorio_shao.py
