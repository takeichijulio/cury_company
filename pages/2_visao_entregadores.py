#=======================================================================================
### Importações e Função de Limpeza
#=======================================================================================
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from PIL import Image
from modules.cleaning import limpar_dataframe, mudar_tipo, clean_code
from modules.charts import resolver_operacao, dataframe_mean_std,top_delivers

st.set_page_config(page_title="Visão Entregadores", page_icon="🚚", layout="wide")
#=======================================================================================    
### Dataframe e Transformação de dados
#=======================================================================================
df = pd.read_csv('train.csv')
df1 = df.copy()
df1 = limpar_dataframe(df1, dropna_mode = "any")
df1 = mudar_tipo(df1)
#=======================================================================================
# Barra Lateral
#=======================================================================================
st.header('Marketplace - Visão Entregadores')

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
    default = ['Low','Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")
weather_options = st.sidebar.multiselect(
    'Quais as condições climáticas?',
    ['conditions Cloudy','conditions Fog','conditions Sandstorms','conditions Stormy','conditions Sunny','conditions Windy'],
    default = ['conditions Cloudy','conditions Fog','conditions Sandstorms','conditions Stormy','conditions Sunny','conditions Windy'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('Powered by Comunidade DS')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1= df1.loc[linhas_selecionadas,:]

#Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1= df1.loc[linhas_selecionadas,:]

#Filtro de Condição Climática
linhas_selecionadas = df1['Weatherconditions'].isin(weather_options)
df1= df1.loc[linhas_selecionadas,:]

#=======================================================================================
# Layout no Streamlit
#=======================================================================================
tab1,tab2,tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1, col2, col3, col4 = st.columns(4)
    with col1:
        col1.metric('Maior Idade', resolver_operacao(df1, 'Delivery_person_Age', max))
        
    with col2:
        col2.metric('Menor Idade', resolver_operacao(df1, 'Delivery_person_Age', min))
    
    with col3:
        col3.metric('Melhor condição', resolver_operacao(df1, 'Vehicle_condition', max))
    
    with col4:
        col4.metric('Pior condição', resolver_operacao(df1, 'Vehicle_condition', min))

            
    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('##### Avaliação média por entregador')
            df2 = dataframe_mean_std(df1, 'ID')
            st.dataframe(df2)

        with col2:
            st.markdown('##### Avaliação média por trânsito')
            df2 = dataframe_mean_std(df1, 'Road_traffic_density')
            df2 = df2.reset_index()                
            st.dataframe(df2)
            
            st.markdown('##### Avaliação média por clima')
            df2 = dataframe_mean_std(df1, 'Weatherconditions')
            st.dataframe(df2)
            

    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de Entrega')

        col1,col2 = st.columns(2)

        with col1:
            st.markdown('##### Top 10 entregadores mais rápidos')
            st.dataframe(top_delivers(df1, top_asc=True))
        
        with col2:
            st.markdown('##### Top 10 entregadores mais lentos')          
            st.dataframe(top_delivers(df1, top_asc=False))
            
        
    





