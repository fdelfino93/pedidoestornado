import pandas as pd
import streamlit as st

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_OK = True
except Exception:
    PLOTLY_OK = False


st.set_page_config(page_title="Dashboard de Inteligencia Olist", layout="wide")

st.markdown(
    """
    <style>
    :root {
      --bg: #f7f8fb;
      --card: #ffffff;
      --text: #2c2f36;
      --muted: #6b7280;
      --primary: #1d4ed8;
      --shadow: 0 8px 24px rgba(10, 22, 70, 0.08);
      --radius: 16px;
    }
    .stApp {
      background: var(--bg);
    }
    .title {
      font-size: 40px;
      font-weight: 800;
      color: var(--text);
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }
    .subtitle {
      color: var(--muted);
      font-size: 16px;
      margin-bottom: 24px;
    }
    .section-title {
      font-size: 26px;
      font-weight: 700;
      color: var(--text);
      margin: 10px 0 12px;
    }
    .kpi-card {
      background: var(--card);
      border-radius: var(--radius);
      padding: 18px 20px;
      box-shadow: var(--shadow);
      border: 1px solid rgba(20, 32, 68, 0.06);
    }
    .kpi-label {
      font-size: 14px;
      color: var(--muted);
      margin-bottom: 6px;
    }
    .kpi-value {
      font-size: 30px;
      font-weight: 800;
      color: var(--primary);
    }
    .card {
      background: var(--card);
      border-radius: var(--radius);
      padding: 18px 20px;
      box-shadow: var(--shadow);
      border: 1px solid rgba(20, 32, 68, 0.06);
    }
    .insight {
      background: #0f172a;
      color: #f8fafc;
      border-radius: 14px;
      padding: 16px 18px;
      font-size: 14px;
      line-height: 1.45;
      box-shadow: 0 10px 26px rgba(15, 23, 42, 0.25);
    }
    .muted {
      color: var(--muted);
      font-size: 13px;
    }
    .spacer {
      height: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def kpi_card(label: str, value: str):
    st.markdown(
        f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(text: str):
    st.markdown(
        f"""
        <div class="insight">{text}</div>
        """,
        unsafe_allow_html=True,
    )


def card_open():
    st.markdown('<div class="card">', unsafe_allow_html=True)


def card_close():
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown('<div class="title">🚀 Dashboard de Inteligencia Olist</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Indicadores e insights consolidados do projeto final.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">📍 Indicadores Principais</div>', unsafe_allow_html=True)
cols = st.columns(5)
with cols[0]:
    kpi_card("Faturamento", "R$ 16.0M")
with cols[1]:
    kpi_card("Media Entrega", "11.6 d")
with cols[2]:
    kpi_card("Mediana Entrega", "9 d")
with cols[3]:
    kpi_card("Satisfacao (⭐)", "4.07")
with cols[4]:
    kpi_card("Clientes Recompra", "2.997")

st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">🗓️ Evolucao das Vendas</div>', unsafe_allow_html=True)
col_left, col_right = st.columns([1.15, 1])
with col_left:
    card_open()
    vendas_mensais = pd.DataFrame(
        {
            "month": pd.date_range("2017-01-01", periods=20, freq="M"),
            "pedidos": [
                120, 340, 210, 850, 1800, 2650, 2400, 3700, 3300, 4100,
                4400, 4300, 4700, 7500, 5700, 7300, 6700, 7200, 6900, 6400
            ],
        }
    )
    if PLOTLY_OK:
        fig = px.line(
            vendas_mensais,
            x="month",
            y="pedidos",
            markers=True,
            color_discrete_sequence=["#2563eb"],
        )
        fig.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=10, b=10),
            xaxis_title="month",
            yaxis_title="pedidos",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(vendas_mensais.set_index("month")["pedidos"], height=360)
    card_close()
with col_right:
    card_open()
    clientes_estado = pd.DataFrame(
        {
            "estado": [
                "SP", "RJ", "MG", "RS", "PR", "SC", "BA", "DF", "GO", "ES",
                "PE", "PA", "CE", "MT", "MA", "MS", "PB", "RN", "AL", "PI", "SE", "RO", "TO", "AM", "AC", "AP", "RR"
            ],
            "clientes": [
                47820, 14669, 13220, 6269, 5787, 4201, 3821, 2421, 2346, 2264,
                1120, 1010, 990, 860, 780, 720, 690, 650, 620, 520, 460, 210, 180, 160, 120, 90, 70
            ],
        }
    )
    if PLOTLY_OK:
        fig = px.treemap(
            clientes_estado,
            path=["estado"],
            values="clientes",
            color="clientes",
            color_continuous_scale="Blues",
        )
        fig.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(clientes_estado.set_index("estado")["clientes"], height=360)
    card_close()

col1, col2 = st.columns(2)
with col1:
    insight_card(
        "Analise: O acompanhamento mensal permite identificar picos de demanda. "
        "Os dados evidenciam sazonalidade e indicam quando reforcar a capacidade operacional."
    )
with col2:
    insight_card(
        "Analise Geografica: A concentracao em SP domina o volume nacional, enquanto RJ e MG "
        "formam o segundo eixo mais relevante para a malha logistica."
    )

st.markdown('<div class="section-title">⏰ Prazo vs Satisfacao</div>', unsafe_allow_html=True)
col_left, col_right = st.columns([1, 1])
with col_left:
    card_open()
    prazo_df = pd.DataFrame(
        {"Status": ["Atrasado", "No Prazo"], "review_score": [2.53, 4.20]}
    )
    if PLOTLY_OK:
        fig = px.bar(
            prazo_df,
            x="Status",
            y="review_score",
            color="Status",
            color_discrete_map={"Atrasado": "#ef4444", "No Prazo": "#34d399"},
            text="review_score",
        )
        fig.update_traces(texttemplate="%{text:.2f}", textposition="inside")
        fig.update_layout(height=340, margin=dict(l=20, r=20, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(prazo_df.set_index("Status")["review_score"], height=340)
    card_close()
with col_right:
    card_open()
    categorias_df = pd.DataFrame(
        {
            "product_category_name": [
                "cama_mesa_banho",
                "beleza_saude",
                "esporte_lazer",
                "moveis_decoracao",
                "informatica_acessorios",
                "utilidades_domesticas",
                "relogios_presentes",
                "telefonia",
                "ferramentas_jardim",
                "automotivo",
            ],
            "vendas": [11115, 9670, 8641, 8334, 7827, 6900, 5400, 4300, 3200, 2800],
        }
    )
    if PLOTLY_OK:
        fig = px.bar(
            categorias_df.sort_values("vendas"),
            x="vendas",
            y="product_category_name",
            orientation="h",
            color="vendas",
            color_continuous_scale="Blues",
        )
        fig.update_layout(height=340, margin=dict(l=20, r=20, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(
            categorias_df.set_index("product_category_name")["vendas"],
            height=340,
        )
    card_close()

col1, col2 = st.columns(2)
with col1:
    insight_card(
        "Insight Logistico: Atrasos sao o maior detrator de nota. "
        "A diferenca de satisfacao mostra que prazo e o ativo mais valioso do e-commerce."
    )
with col2:
    insight_card(
        "Mix de Produtos: A dominancia de 'Cama, Mesa e Banho' indica um perfil de consumo "
        "utilitario e recorrente no marketplace."
    )

st.markdown('<div class="section-title">📊 Indicadores Analiticos</div>', unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)
with col_a:
    card_open()
    st.markdown("**Notas e comentarios**")
    st.markdown('<div class="muted">Media: 4,0001 | % com texto: 42,73%</div>', unsafe_allow_html=True)
    notas_df = pd.DataFrame(
        {
            "Nota": [5, 4, 3, 2, 1],
            "Quantidade": [62669, 21056, 9450, 3977, 15050],
        }
    )
    if PLOTLY_OK:
        fig = px.bar(
            notas_df,
            x="Nota",
            y="Quantidade",
            color="Quantidade",
            color_continuous_scale="Blues",
        )
        fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(notas_df.set_index("Nota")["Quantidade"], height=260)
    card_close()
with col_b:
    card_open()
    st.markdown("**Frete x Peso/Volume**")
    frete_df = pd.DataFrame(
        {"Variavel": ["Peso (g)", "Volume (cm3)"], "Correlacao": [0.610, 0.587]}
    )
    if PLOTLY_OK:
        fig = px.bar(
            frete_df,
            x="Variavel",
            y="Correlacao",
            color="Variavel",
            color_discrete_sequence=["#2563eb", "#60a5fa"],
        )
        fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(frete_df.set_index("Variavel")["Correlacao"], height=260)
    card_close()
with col_c:
    card_open()
    st.markdown("**Atrasos: estados diferentes**")
    atraso_df = pd.DataFrame(
        {"Relacao": ["Estados diferentes", "Mesmo estado"], "Quantidade": [6331, 2384]}
    )
    if PLOTLY_OK:
        fig = px.pie(
            atraso_df,
            names="Relacao",
            values="Quantidade",
            color_discrete_sequence=["#2563eb", "#93c5fd"],
        )
        fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(atraso_df.set_index("Relacao")["Quantidade"], height=260)
    card_close()

st.markdown('<div class="section-title">🧭 Recompra e Perfil</div>', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    card_open()
    st.markdown("**Resumo de recompra (proxy)**")
    recompra_df = pd.DataFrame(
        {
            "Indicador": [
                "Clientes com recompra",
                "Registros analisados",
                "Estado",
                "Cidade",
                "Metodo de pagamento",
                "Parcelas",
                "Entrega",
                "Nota",
                "Categoria",
            ],
            "Valor": [
                "11.978",
                "110.018",
                "SP (46.938)",
                "sao paulo (17.454)",
                "cartao_credito (83.165)",
                "1 (52.811)",
                "no prazo/antes (92,16%)",
                "5 (60.828)",
                "cama_mesa_banho (10.826)",
            ],
        }
    )
    st.dataframe(recompra_df, use_container_width=True, height=320)
    card_close()
with col2:
    card_open()
    st.markdown("**Arquivo consolidado**")
    try:
        with open("respostas.md", "r", encoding="utf-8") as f:
            respostas_texto = f.read()
    except UnicodeDecodeError:
        with open("respostas.md", "r", encoding="latin-1") as f:
            respostas_texto = f.read()
    st.text_area("respostas.md", respostas_texto, height=320)
    card_close()
