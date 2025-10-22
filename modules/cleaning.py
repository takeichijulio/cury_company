#-----------------------------------------------------------------------------
#Funções de Limpeza
#-----------------------------------------------------------------------------
import pandas as pd
import numpy as np
from datetime import datetime


def limpar_dataframe(df, *, dropna_mode=None, subset=None, lowercase=False):
    """
    dropna_mode: None | 'any' | 'all'
    subset: lista de colunas para considerar no dropna (opcional)
    lowercase: True para padronizar texto em minúsculas
    """
    # 1) tira espaços de texto
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].str.strip()
        if lowercase:
            df[col] = df[col].str.lower()
    # 2) normaliza "nulos de texto"
    df = df.replace(["NaN", "nan", "NULL", ""], np.nan)

    # 3) regra de remoção de nulos
    if dropna_mode in ("any", "all"):
        df = df.dropna(how=dropna_mode, subset=subset).copy()

    # 4) reindexa
    return df.reset_index(drop=True)

def mudar_tipo(df1):
    '''Esta função muda os tipos de dados contidos em estruturas específicas do dataframe.'''
    df1["Delivery_person_Age"] = df1["Delivery_person_Age"].astype(int)
    df1["Order_Date"] = pd.to_datetime(df1["Order_Date"],format = '%d-%m-%Y')
    df1["multiple_deliveries"] = df1["multiple_deliveries"].astype(int)
    df1["Delivery_person_Ratings"] = df1["Delivery_person_Ratings"].astype(float)
    df1["year_week"] = df1["Order_Date"].dt.strftime("%U")
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    
    return df1


def clean_code(df1):
    ''' Esta função tem responsabilidade de limpar o Dataframe

        Tipos de Limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços das variáveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)

        Input: Dataframe
        Output: Dataframe
    '''
    
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1= df1.loc[linhas_selecionadas, :].copy()    
    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1= df1.loc[linhas_selecionadas, :].copy()    
    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1= df1.loc[linhas_selecionadas, :].copy()    
    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1= df1.loc[linhas_selecionadas, :].copy()   
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1= df1.loc[linhas_selecionadas, :].copy()
    
    df1,loc[:,'ID'] = df1.loc[:,'ID'].str.strip()
    df1,loc[:,'Road_traffic_density'] = df1.loc[:,'Road_traffic_density'].str.strip()
    df1,loc[:,'Type_of_order'] = df1.loc[:,'Type_of_order'].str.strip()
    df1,loc[:,'Type_of_vehicle'] = df1.loc[:,'Type_of_vehicle'].str.strip()
    df1,loc[:,'City'] = df1.loc[:,'City'].str.strip()
    df1,loc[:,'Festival'] = df1.loc[:,'Festival'].str.strip()
       
    df1["Delivery_person_Age"] = df1["Delivery_person_Age"].astype(int)
    df1["Order_Date"] = pd.to_datetime(df1["Order_Date"],format = '%d-%m-%Y')
    df1["multiple_deliveries"] = df1["multiple_deliveries"].astype(int)
    df1["Delivery_person_Ratings"] = df1["Delivery_person_Ratings"].astype(float)
    df1["year_week"] = df1["Order_Date"].dt.strftime("%U")
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1.reset_index(drop=True)

