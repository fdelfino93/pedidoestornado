import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Dashboard Consolidado - Olist",
    page_icon="📊",
    layout="wide"
)

# Título e Descrição
st.title("📊 Análise Consolidada de E-commerce (Olist)")
st.markdown("""
Este dashboard apresenta os insights extraídos da base de dados, respondendo às principais perguntas de negócio.
Os dados abaixo são consolidados das análises realizadas no projeto.
""")

st.markdown("---")

# --- KPIs Globais ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Tempo Médio de Entrega", "11 Dias", help="Média calculada entre aprovação e entrega")
col2.metric("Satisfação Média (1-5)", "4.00", help="Média das notas de avaliação")
col3.metric("Clientes Recorrentes", "11.978", help="Clientes com mais de uma compra")
col4.metric("Entregas no Prazo", "92.16%", help="Percentual observado em clientes recorrentes")

st.markdown("---")

# --- Estrutura de Abas ---
tab_logistica, tab_vendas, tab_satisfacao, tab_produtos, tab_geo = st.tabs([
    "🚚 Logística & Frete",
    "💰 Vendas & Sazonalidade",
    "⭐ Satisfação do Cliente",
    "📦 Produtos & Categorias",
    "🗺️ Geografia"
])

# --- ABA 1: Logística ---
with tab_logistica:
    st.header("Performance Logística")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Tempo de Entrega")
        df_tempo = pd.DataFrame({
            "Métrica": ["Média", "Mediana"],
            "Dias": [11, 9]
        })
        fig_tempo = px.bar(df_tempo, x="Métrica", y="Dias", text="Dias", color="Métrica",
                           title="Tempo de Entrega (Aprovação -> Cliente)")
        st.plotly_chart(fig_tempo, use_container_width=True)
    
    with c2:
        st.subheader("Origem dos Atrasos")
        df_atraso = pd.DataFrame({
            "Tipo": ["Estados Diferentes", "Mesmo Estado"],
            "Quantidade": [6331, 2384]
        })
        fig_atraso = px.pie(df_atraso, values="Quantidade", names="Tipo", 
                            title="Onde ocorrem os atrasos?", hole=0.4)
        st.plotly_chart(fig_atraso, use_container_width=True)
    
    st.divider()
    st.subheader("Correlação: Frete vs Peso/Volume")
    st.info("Valores indicam correlação de Pearson (0 a 1). Quanto mais próximo de 1, maior a influência no preço.")
    
    col_corr1, col_corr2 = st.columns(2)
    col_corr1.metric("Peso (g) x Frete", "0.610", "Forte Influência")
    col_corr2.metric("Volume (cm³) x Frete", "0.587", "Moderada/Forte Influência")

# --- ABA 2: Vendas ---
with tab_vendas:
    st.header("Sazonalidade e Vendas")
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("📅 **Mês com mais Pedidos:** Agosto (08) - 10.843 pedidos")
    with c2:
        st.success("💲 **Mês com maior Faturamento:** Maio - R$ 2.24 Milhões")
        
    st.divider()
    st.subheader("Perfil do Cliente Recorrente (Recompra)")
    st.markdown("""
    Análise de **11.978 clientes** que voltaram a comprar (110.018 registros analisados):
    - **Localização Principal:** São Paulo (Capital e Estado)
    - **Pagamento Preferido:** Cartão de Crédito (83.165 registros) — parcela mais comum: 1x (52.811)
    - **Experiência de Entrega:** Recebimento no prazo ou antecipado (92,16%)
    - **Satisfação:** Nota 5 predominante (60.828 registros)
    - **Categoria Mais Comprada:** Cama Mesa Banho (10.826 registros)
    """)

# --- ABA 3: Satisfação ---
with tab_satisfacao:
    st.header("Análise de Satisfação (Reviews)")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        df_notas = pd.DataFrame({
            "Nota": [5, 4, 3, 2, 1],
            "Quantidade": [62669, 21056, 9450, 3977, 15050]
        })
        fig_notas = px.bar(df_notas, x="Nota", y="Quantidade", text="Quantidade",
                           title="Distribuição de Notas (1-5)", color="Nota")
        st.plotly_chart(fig_notas, use_container_width=True)
        
    with c2:
        st.subheader("Comentários")
        df_coment = pd.DataFrame({
            "Status": ["Com Comentário", "Sem Comentário"],
            "Percentual": [42.73, 57.27]
        })
        fig_coment = px.pie(df_coment, values="Percentual", names="Status", hole=0.4)
        st.plotly_chart(fig_coment, use_container_width=True)
        
    st.divider()
    st.subheader("Impacto do Prazo na Nota")
    col_p1, col_p2 = st.columns(2)
    col_p1.metric("Nota Média (Entrega no Prazo)", "4.20")
    col_p2.metric("Nota Média (Entrega Atrasada)", "2.53", delta="-1.67", delta_color="inverse")

# --- ABA 4: Produtos ---
with tab_produtos:
    st.header("Desempenho por Categoria")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top 5 Mais Vendidos")
        df_top = pd.DataFrame({
            "Categoria": ["Cama Mesa Banho", "Beleza Saúde", "Esporte Lazer", "Móveis Decoração", "Informática Acessórios"],
            "Vendas": [11115, 9670, 8641, 8334, 7827]
        })
        st.dataframe(df_top, hide_index=True, use_container_width=True)
        
    with c2:
        st.subheader("Top 5 Menos Vendidos")
        df_bottom = pd.DataFrame({
            "Categoria": ["CDs/DVDs Musicais", "La Cuisine", "PC Gamer", "Roupas Infanto Juvenil", "Seguros e Serviços"],
            "Vendas": [14, 14, 9, 8, 2]
        })
        st.dataframe(df_bottom, hide_index=True, use_container_width=True)
        
    st.divider()
    st.subheader("Preço Médio por Categoria")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Top 5 Menores Preços**")
        df_preco_menor = pd.DataFrame({
            "Categoria": ["Casa Conforto 2", "Flores", "Fraldas Higiene", "CDs/DVDs Musicais", "Alimentos Bebidas"],
            "Preço Médio (R$)": [25.34, 33.64, 40.19, 52.14, 54.60]
        })
        st.dataframe(df_preco_menor, hide_index=True, use_container_width=True)
    with c4:
        st.markdown("**Top 5 Maiores Preços**")
        df_preco_maior = pd.DataFrame({
            "Categoria": ["Instrumentos Musicais", "Agro Indústria e Comércio", "Eletrodomésticos 2", "Portáteis Casa Forno e Café", "PCs"],
            "Preço Médio (R$)": [281.62, 342.12, 476.12, 624.29, 1098.34]
        })
        st.dataframe(df_preco_maior, hide_index=True, use_container_width=True)

    st.divider()
    st.markdown("### 📸 Fotos vs Vendas")
    
    col_foto1, col_foto2 = st.columns([1, 2])
    with col_foto1:
        st.metric("Correlação (Pearson)", "-0.620")
        st.caption("Curiosamente, categorias com maior quantidade média de fotos tendem a ter menor volume total de vendas agregadas.")
        
    with col_foto2:
        # Dados ilustrativos para representar a correlação negativa observada
        df_corr = pd.DataFrame({
            "Média de Fotos": [1, 2, 3, 4, 5],
            "Vendas (Tendência)": [12000, 8000, 4500, 1500, 500]
        })
        fig_corr = px.scatter(df_corr, x="Média de Fotos", y="Vendas (Tendência)", 
                              title="Ilustração: Relação Fotos x Vendas", size="Vendas (Tendência)")
        st.plotly_chart(fig_corr, use_container_width=True)

# --- ABA 5: Geografia ---
with tab_geo:
    st.header("Distribuição Geográfica")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top 10 Estados (Clientes)")
        df_cli_uf = pd.DataFrame({
            "Estado": ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "DF", "GO", "ES"],
            "Clientes": [47820, 14669, 13220, 6269, 5787, 4201, 3821, 2421, 2346, 2264]
        })
        fig_cli = px.bar(df_cli_uf, x="Estado", y="Clientes", text="Clientes", title="Clientes por Estado")
        st.plotly_chart(fig_cli, use_container_width=True)

    with c2:
        st.subheader("Top 10 Estados (Vendedores)")
        df_vend_uf = pd.DataFrame({
            "Estado": ["SP", "MG", "PR", "RJ", "SC", "RS", "DF", "BA", "GO", "PE"],
            "Vendedores": [80342, 8827, 8671, 4818, 4075, 2199, 899, 643, 520, 448]
        })
        fig_vend = px.bar(df_vend_uf, x="Estado", y="Vendedores", text="Vendedores", title="Vendedores por Estado")
        st.plotly_chart(fig_vend, use_container_width=True)

    st.divider()
    st.subheader("Cidades Destaque")
    col_cid1, col_cid2 = st.columns(2)
    col_cid1.metric("Cidade que Mais Comprou", "São Paulo", "17.946 compras")
    col_cid2.metric("Cidade que Mais Vendeu", "São Paulo", "27.983 vendas")