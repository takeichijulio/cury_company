### Importações e Função de Limpeza
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from PIL import Image
from modules.charts import order_metric, orders_road_traffic, orders_city_traffic, orders_id_week, orders_week, orders_map
from modules.cleaning import limpar_dataframe, mudar_tipo, clean_code

st.set_page_config(page_title="Visão Empresa", page_icon="📊", layout="wide")
 
#=======================================================================================
# Dataframe e Transformação de dados
#=======================================================================================
df = pd.read_csv('train.csv')
df1 = df.copy()
df1 = limpar_dataframe(df1, dropna_mode = 'any')
df1 = mudar_tipo(df1)
#=======================================================================================
# Barra Lateral
#=======================================================================================
st.header('Marketplace - Visão Cliente')

image = Image.open('logo_flecha.png')
st.sidebar.image(image, width =120)
st.sidebar.markdown('### Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 6),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY'
)
st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições de trânsito?',
    ['Low', 'Medium', 'High', 'Jam'],
    default = ['Low', 'Medium', 'High', 'Jam'])
st.sidebar.markdown("""---""")
st.sidebar.markdown('Powered by Comunidade DS')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1= df1.loc[linhas_selecionadas,:]

#Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1= df1.loc[linhas_selecionadas,:]

#=======================================================================================
# Layout no Streamlit
#=======================================================================================

tab1,tab2,tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
    # Order Metric
        st.header('Orders by day')
        st.plotly_chart(order_metric(df1), use_container_width=True)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('Orders by Road Traffic Density')
            st.plotly_chart(orders_road_traffic(df1), use_container_width=True)
    
        with col2:
            st.markdown('Orders by City and Road Traffic Density')
            st.plotly_chart(orders_city_traffic(df1), use_container_width=True)

with tab2:
    st.markdown('Orders by Week')
    with st.container():  
        # Quantidade de pedidos por entregador por Semana
        # Quantas entregas na semana / Quantos entregadores únicos por semana
        st.plotly_chart(orders_id_week(df1), use_container_width=True)
        
    with st.container():
        st.plotly_chart(orders_week(df1), use_container_width=True)
    
with tab3:
    st.markdown('Map')
    fig = orders_map(df1)









