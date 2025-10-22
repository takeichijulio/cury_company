#=======================================================================================
### Importações e Função de Limpeza
#=======================================================================================
import pandas as pd
import numpy as np 
import streamlit as st
from datetime import datetime
from PIL import Image
from modules.cleaning import limpar_dataframe, mudar_tipo, clean_code
from modules.charts import distance_haversine, fest_std_mean_time_delivery,avg_std_time_graph, avg_std_time_on_traffic

st.set_page_config(page_title="Visão Restaurantes", page_icon="🍽", layout="wide")
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
st.header('Marketplace - Visão Restaurantes')

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
city_options = st.sidebar.multiselect(
    'Qual o tipo de cidade?',
    ['Metropolitian','Semi-Urban','Urban'],
    default = ['Metropolitian','Semi-Urban','Urban'] )

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

#Filtro de tipo de cidade
linhas_selecionadas = df1['City'].isin(city_options)
df1= df1.loc[linhas_selecionadas,:]

#=======================================================================================
# Layout no Streamlit
#=======================================================================================

tab1,tab2,tab3 = st.tabs(['Visão Gerencial', '_', '_'])
with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            unicos = df1["Delivery_person_ID"].nunique()
            col1.metric('Entreg. únicos', unicos)
                              
        with col2:
            avg_distance = distance_haversine(df1,False)
            col2.metric('Distância média',f'{avg_distance:.2f}')
            
        #tempo médio com festival            
        with col3:
            tempo_medio = fest_std_mean_time_delivery(df1, 'avg_time','Yes')
            col3.metric('TM com festival', f'{tempo_medio:.2f}')
            
        #desvio padrão com festival    
        with col4:
            desvio_p = fest_std_mean_time_delivery(df1, 'std_time','Yes')
            col4.metric('DP com festival',f'{desvio_p:.2f}')
        #tempo médio sem festival
        with col5:
            tempo_medio = fest_std_mean_time_delivery(df1, 'avg_time','No')
            col5.metric('TM sem festival', f'{tempo_medio:.2f}')
            
        #desvio padrão sem festival 
        with col6:
            desvio_p =fest_std_mean_time_delivery(df1, 'std_time','No')
            col6.metric('DP sem festival',f'{desvio_p:.2f}')
                

    with st.container():
        st.subheader('Distância média por cidade') 
        fig = distance_haversine(df1, True)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.subheader('Indicadores de Tempo')
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('##### Distribuição de tempo por cidade')
            fig = avg_std_time_graph(df1) 
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('##### Tempo médio por tipo de entrega')
            cols = ['City', 'Time_taken(min)','Type_of_order']
            df_aux = df1.loc[:,cols].groupby(['City','Type_of_order']).agg({'Time_taken(min)': ['mean','std']})
            df_aux.columns = ['avg_time','std_time']
            df_aux = df_aux.reset_index()
            st.dataframe(df_aux)
            
    with st.container():
        st.subheader('Tempo médio por cidade e por tráfego')
        fig = avg_std_time_on_traffic(df1)
        st.plotly_chart(fig, use_container_width=True)



