#-----------------------------------------------------------------------------
#Funções de Gráficos
#-----------------------------------------------------------------------------
import pandas as pd
import numpy as np
import plotly.express as px 
import plotly.io as pio
import plotly.graph_objects as go
from haversine import haversine
import folium
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static
from haversine import haversine

### Visão Empresa

def order_metric(df):
    ''' Função de criar gráfico de barras do numero de entregas por data para o dashboard no primeiro container '''
    df2 = (df.loc[:, ['ID','Order_Date']]
           .groupby('Order_Date')
           .count()
           .reset_index() )
    fig = px.bar(df2, x='Order_Date', y='ID', title="Entregas por Data")
    return fig

def orders_road_traffic(df):
    ''' Função de criar gráfico de barras do numero de entregas por densidade do tráfego para o dashboard no primeiro container '''
    df2 = (df.loc[:,['ID','Road_traffic_density']]
                   .groupby('Road_traffic_density')
                   .count()
                   .reset_index()
                   .sort_values(by="ID", ascending=True))
            
    fig = px.bar(df2, x = 'Road_traffic_density', y = 'ID')
    fig.update_layout(yaxis=dict(tickformat="d"))
    return fig

def orders_city_traffic(df):
    ''' Função de criar gráfico de barras do numero de entregas por cidade e por densidade do tráfego para o dashboard no primeiro container '''
    
    df2 = (df.loc[:,['ID','City','Road_traffic_density']]
                                   .groupby(['City','Road_traffic_density'])
                                   .count()
                                   .reset_index()
                                  )
    fig = px.bar(df2, x = 'City', y = 'ID',
                             color="Road_traffic_density",
                            barmode="stack",
                            title="Volume de pedidos por Cidade e Tráfego (Empilhado)")
    return fig


def orders_id_week(df):
    '''Função de criar gráfico de linha do numero de entregas por entregador e por semana do tráfego para o dashboard no primeiro container '''
    df_aux1 = (df.loc[:, ['ID', 'year_week']]
               .groupby( 'year_week' )
               .count()
               .reset_index())
    df_aux2 = (df.loc[:, ['Delivery_person_ID', 'year_week']]
               .groupby( 'year_week')
               .nunique()
               .reset_index())
    df_aux = pd.merge( df_aux1, df_aux2, how='inner' )
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line( df_aux, x='year_week', y='order_by_delivery')
    return fig
    
def orders_week(df):
    '''Função de criar gráfico de linha que retorna a quantidade de pedidos nas semanas determinadas no gráfico'''
    df2 = (df.loc[:,['ID','year_week']]
           .groupby('year_week')
           .count()
           .reset_index())
    fig = px.line(df2, x = 'year_week', y = 'ID')
    return fig

def orders_map(df):
    ''' Função que cria mapa que aponta locais das entregas de acordo com o dataframe entregue no parâmetro
    '''
    df_aux = df.loc[:, ['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']].groupby(
            ['City','Road_traffic_density']).median().reset_index()       
    map = folium.Map()
        
    for index, location_info in df_aux.iterrows():
        folium.Marker ([location_info['Delivery_location_latitude'],
                     location_info['Delivery_location_longitude']],
                     popup=location_info[['City','Road_traffic_density']]).add_to(map)
    folium_static(map, width=1024, height=600)

def resolver_operacao(df, coluna: str, operacao: callable):
    """
    Aplica uma operação (ex: max, min, mean, sum) sobre uma coluna numérica.
    Retorna o valor resultante, tratado para erros.
    """
    if coluna not in df.columns:
        return None
    
    serie = df[coluna]  # já está limpa
    
    try:
        return operacao(serie)
    except Exception as e:
        print(f"Erro ao calcular {operacao.__name__} para {coluna}: {e}")
        return None

def dataframe_mean_std(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Calcula média e desvio padrão das avaliações ('Delivery_person_Ratings')
    agrupadas por uma coluna categórica passada no parâmetro.
    Parâmetros:
    ----------
    df : pd.DataFrame
        DataFrame base de onde os dados serão extraídos.
    col : str
        Nome da coluna categórica usada para agrupar.
    Retorna:
    --------
    pd.DataFrame com colunas ['delivery_mean', 'delivery_std']
    """
    if col not in df.columns:
        print(f"Coluna '{col}' não encontrada no DataFrame.")
        return None

    df2 = (
        df.loc[:, ['Delivery_person_Ratings', col]]
          .groupby(col)
          .agg({'Delivery_person_Ratings': ['mean', 'std']})
    )

    df2.columns = ['delivery_mean', 'delivery_std']
    return df2.reset_index()

def top_delivers(df: pd.DataFrame, top_asc: bool) -> pd.DataFrame:
    df2 = (
        df.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
          .groupby(['City', 'Delivery_person_ID'])
          .mean()  # média do tempo por entregador em cada cidade
          .sort_values(['City', 'Time_taken(min)'], ascending=[True, top_asc])
          .reset_index()
    )

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat([df_aux01, df_aux02, df_aux03], ignore_index=True)
    return df3

import pandas as pd



def fest_std_mean_time_delivery(df: pd.DataFrame, operation: str, festival: str):
    """
    Retorna o valor de média ('avg_time') ou desvio padrão ('std_time') 
    do tempo de entrega ('Time_taken(min)') para um determinado Festival.
    Parâmetros:
    -----------
    df : pd.DataFrame
        Base de dados.
    operation : str
        'avg_time' ou 'std_time' — indica qual métrica retornar.
    festival : str
        'Yes' ou 'No' — indica se filtra entregas em período de festival.
    Retorna:
    --------
    float
        Valor da média ou do desvio padrão conforme solicitado.
    """
    # Validação básica dos parâmetros
    if operation not in ['avg_time', 'std_time']:
        raise ValueError("operation deve ser 'avg_time' ou 'std_time'.")
    if festival not in ['Yes', 'No']:
        raise ValueError("festival deve ser 'Yes' ou 'No'.")

    cols = ['Time_taken(min)', 'Festival']
    df_aux = (
        df.loc[:, cols]
        .groupby('Festival')
        .agg({'Time_taken(min)': ['mean', 'std']})
    )

    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    # Filtra o festival e seleciona a operação desejada
    resultado = df_aux.loc[df_aux['Festival'] == festival, operation]

    # Retorna o valor (float) em vez de Series
    return float(resultado.values[0]) if not resultado.empty else None

def distance_haversine(df: pd.DataFrame, fig: bool):
    """
    Calcula a distância média entre restaurante e cliente usando a fórmula de Haversine.
    
    - Se `fig=False`, retorna a distância média total em quilômetros.
    - Se `fig=True`, retorna um gráfico de pizza (Plotly) com a distância média por cidade.
    """
    if fig is False:
        cols = ['Delivery_location_latitude','Delivery_location_longitude','Restaurant_latitude','Restaurant_longitude']
        df['distance'] = df.loc[:,cols].apply(lambda x:
                                        haversine( (x['Restaurant_latitude'],x['Restaurant_longitude']),
                                        (x['Delivery_location_latitude'],x['Delivery_location_longitude'])), axis=1)
        avg_distance = df['distance'].mean()
        return avg_distance
    else:
        cols = ['Delivery_location_latitude','Delivery_location_longitude','Restaurant_latitude','Restaurant_longitude']
        df['distance'] = df.loc[:,cols].apply(lambda x:
                                       haversine( (x['Restaurant_latitude'],x['Restaurant_longitude']),
                                                    (x['Delivery_location_latitude'],x['Delivery_location_longitude'])), axis=1)

        avg_distance = df.loc[:, ['City','distance']].groupby('City').mean().reset_index()
        
        fig_obj = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])
        return fig_obj
def avg_std_time_graph(df:pd.DataFrame):
    '''Função recebe um dataframe e retorna um gráfico de barra da media e do desvio padrão das colunas abaixo
    '''
    cols = ['City', 'Time_taken(min)']
    df_aux = df.loc[:,cols].groupby('City').agg({'Time_taken(min)': ['mean','std']})
    df_aux.columns = ['avg_time','std_time']
    df_aux = df_aux.reset_index()
    
    fig = go.Figure()
    fig.add_trace( go.Bar( name='Control',
                          x=df_aux['City'],
                          y=df_aux['avg_time'],
                          error_y=dict( type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')
    return fig

def avg_std_time_on_traffic(df:pd.DataFrame):
    '''Função recebe um dataframe e retorna um gráfico de sunburst da media e do desvio padrão das colunas abaixo
    '''
    cols = ['City', 'Time_taken(min)','Road_traffic_density']
    df_aux = df.loc[:,cols].groupby(['City','Road_traffic_density']).agg({'Time_taken(min)': ['mean','std']})
    df_aux.columns = ['avg_time','std_time']
    df_aux = df_aux.reset_index()
    fig = px.sunburst(df_aux, path=['City','Road_traffic_density'], values='avg_time',
                      color = 'std_time', color_continuous_scale= 'RdBu',
                      color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig








