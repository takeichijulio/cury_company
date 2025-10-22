import streamlit as st
from PIL import Image
from pathlib import Path
from textwrap import dedent

st.set_page_config(page_title="Home", page_icon="📈", layout="wide")

# --- Sidebar ---
image = Image.open("logo_flecha.png")
st.sidebar.image(image, width=120)
st.sidebar.markdown("### Cury Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("---")

# --- Header principal ---
st.title("Curry Company Growth Dashboard")
st.caption("Acompanhe as métricas de crescimento de Entregadores e Restaurantes.")

st.divider()

# --- Conteúdo (sem indentação para evitar 'bloco de código') ---
st.markdown(dedent("""
### Como usar este Growth Dashboard

- **Visão Empresa**
  - **Visão Gerencial**: Métricas gerais de comportamento.
  - **Visão Tática**: Indicadores semanais de crescimento.
  - **Visão Geográfica**: Insights de geolocalização.

- **Visão Entregador**
  - Acompanhamento dos indicadores semanais de crescimento.

- **Visão Restaurantes**
  - Indicadores semanais de crescimento dos restaurantes.

### Ask for help
- Time de Data Science no Discord  
  - @meigarom
"""))

# Opcional: “atalhos” de navegação (se estiver usando multipáginas)
st.subheader("Atalhos")
c1, c2, c3 = st.columns(3)

with c1:
    st.page_link("pages/1_visao_empresa.py", label="🏢 Visão Empresa", icon=":material/insights:")
with c2:
    st.page_link("pages/2_visao_entregadores.py", label="🚴 Visão Entregador", icon=":material/trending_up:")
with c3:
    st.page_link("pages/3_visao_restaurantes.py", label="🍽️ Visão Restaurantes", icon=":material/restaurant:")

