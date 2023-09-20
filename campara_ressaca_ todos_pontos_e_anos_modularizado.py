import xarray as xr
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def separa_dias_ressaca_waverys(main_dir):
    # Crie o caminho completo para o arquivo de dados climatológicos
    dado_waverys = f'{main_dir}teste_chico/variaveis_dissertacao.csv'

    print('Abrindo dados climatológicos...')
    df_waverys = pd.read_csv(dado_waverys, index_col=0, parse_dates=['time'])
    # Selecione o período de dados específico
    dados_ano = df_waverys[(df_waverys.time >= data_inicio) & (df_waverys.time <= data_fim)]

    # Criar um dicionário para armazenar os dias de ressaca para cada ponto
    ressaca_waverys_por_ponto = {}

    # Loop sobre os pontos de 0 a 10
    for ponto in range(11):
        # Selecione o ponto
        dados_ponto = dados_ano[dados_ano['ponto'] == ponto]

        # Mantenha todas as variáveis e apenas filtre os dias com Hs superior a 2.5 metros
        dias_ressaca = dados_ponto[dados_ponto['Hs'] >= 2.5]

        # Configure a coluna 'time' como índice
        dias_ressaca.set_index('time', inplace=True)

        # Resample para calcular a média diária
        dias_ressaca = dias_ressaca.resample('D').mean()

        # Elimine os valores NaN
        dias_ressaca.dropna(inplace=True)

        # Armazene os dados de ressaca no dicionário
        ressaca_waverys_por_ponto[ponto] = dias_ressaca

    # Retorna o dicionário com os dados processados
    return ressaca_waverys_por_ponto
 
def carregar_avisos_de_ressaca_CHM(ano):
    # Carregar o arquivo de avisos de ressaca correspondente ao ano
    arquivo_avisos = f'/p1-nemo/rtecchio/lista_ressacas_RS/lista_ressacas_RS_{ano}.csv'

    lista_header = ['arquivo', 'data_aviso', 'cidade1', 'cidade2', 'inicio', 'validade']
    df_avisos = pd.read_csv(arquivo_avisos, sep=';', names=lista_header, parse_dates=True, encoding='latin-1')
    df_avisos.index = pd.to_datetime(df_avisos['data_aviso'], dayfirst=True)

    codigos_inicio_aviso = df_avisos['inicio'].values 
    codigos_fim_aviso = df_avisos['validade'].values 

    # CRIA LISTA COM STRING P/ DURACAO DO AVISO
    strings_data_inicio = []
    strings_data_fim = [] 
    for index_codigo in range(len(codigos_inicio_aviso)):
        strings_data_inicio.append(str(codigos_inicio_aviso[index_codigo]))
        strings_data_fim.append(str(codigos_fim_aviso[index_codigo]))

    # COLOCA 0 NA FRENTE DA STRING
    for index_string in range(len(strings_data_inicio)):
        if len(strings_data_inicio[index_string]) <= 5:
            strings_data_inicio[index_string] = '0' +strings_data_inicio[index_string] 
        else:
            strings_data_inicio[index_string] = strings_data_inicio[index_string] 

        if len(strings_data_fim[index_string]) <= 5:
            strings_data_fim[index_string] = '0' +strings_data_fim[index_string] 
        else:
            strings_data_fim[index_string] = strings_data_fim[index_string] 

    # CRIA LISTA COM OS DIAS DE AVISO NO FORMATO DATETIME
    inicio_aviso = []
    fim_aviso = [] 
    for index_strings in range(len(strings_data_inicio)):

        dia1 = strings_data_inicio[index_strings]
        dia2 = strings_data_fim[index_strings]
        
        if df_avisos.index.month[index_strings] < 10:
            diax =  '0' +str(df_avisos.index.month[index_strings])+ "-"  + dia1[0:2] + "-" + str(df_avisos.index.year[index_strings]) + " " + dia1[2:4] + ":" + dia1[4:6] 
            diax2 = '0' +str(df_avisos.index.month[index_strings])+ "-"  + dia2[0:2] + "-" + str(df_avisos.index.year[index_strings]) + " " + dia2[2:4] + ":" + dia2[4:6] 
        
        else:
            diax =  str(df_avisos.index.month[index_strings])+ "-"  + dia1[0:2] + "-" + str(df_avisos.index.year[index_strings]) + " " + dia1[2:4] + ":" + dia1[4:6] 
            diax2 = str(df_avisos.index.month[index_strings])+ "-"  + dia2[0:2] + "-" + str(df_avisos.index.year[index_strings]) + " " + dia2[2:4] + ":" + dia2[4:6] 

        
        date1 = datetime.strptime(diax, '%m-%d-%Y %H:%M')
        date2 = datetime.strptime(diax2, '%m-%d-%Y %H:%M')
        
        # Se o aviso foi emitido no mes anterior da vigencia, adiciona um mes na vigencia
        if date1.day < df_avisos.index.day[index_strings]:
            date1 = date1 + relativedelta(months=1)
            diax = date1.strftime("%m-%d-%Y %H:%M")

        elif date2.day < df_avisos.index.day[index_strings]:
            date2 = date2 + relativedelta(months=1)
            diax2 = date2.strftime("%m-%d-%Y %H:%M")
            
        
        diay = pd.to_datetime(diax)
        diay2 = pd.to_datetime(diax2) 

        print(f"Start: {diay}, end: {diay2}")

        
        inicio_aviso.append(diay) 
        fim_aviso.append(diay2) 

    ndt = []
    for index_aviso in range(len(inicio_aviso)):
        
        min_date_time = inicio_aviso[index_aviso]
        max_date_time = fim_aviso[index_aviso]
        
        new_date_time = pd.date_range(start=min_date_time, end=max_date_time, freq ="H")
        if len(new_date_time) == 0:
            print(min_date_time,max_date_time)
        ndt.append(new_date_time) 
        
    novo_index = []
    for i in ndt:
        dias_aviso = pd.Series(i).dt.normalize().unique()
        for d in dias_aviso:
            novo_index.append(d)
        #dnt2.append(pd.Series(i).dt.normalize().unique())
        
    dias_unicos =  pd.Series(pd.Series(novo_index).unique(),name='avisos')
    dias_unicos = dias_unicos.sort_values()


    # Retorne o DataFrame com os avisos de ressaca
    return df_avisos, strings_data_inicio, strings_data_fim

def calcular_matches_por_ponto(ressaca_waverys_por_ponto, dias_unicos):
    matches_por_ponto = {}

    for ponto, df in ressaca_waverys_por_ponto.items():
        matches_ponto = {}

        for ano, df_ano in df.groupby(df.index.year):
            matches_ano = []

            for d in dias_unicos:
                if d.year == ano and d in df_ano.index:
                    matches_ano.append(d)

            matches_ponto[ano] = matches_ano

        matches_por_ponto[ponto] = matches_ponto

    return matches_por_ponto



def criar_dataframe_informacoes_comparacao(ressaca_waverys_por_ponto, matches_por_ponto):
    # Calcular o ano atual para criar uma chave única no DataFrame
    ano_atual = pd.Timestamp.now().year

    # Criar listas para armazenar informações separadamente para cada ponto
    pontos = []
    anos = []  # Lista para armazenar o ano de cada ponto
    dias_de_ressaca = []
    dias_unicos = []
    matches = []

    for ponto, df in ressaca_waverys_por_ponto.items():
        pontos.append(ponto)
        anos.append(df.index.year[0])  # Obtém o ano do primeiro registro
        dias_de_ressaca.append(len(ressaca_waverys_por_ponto[ponto]))
        dias_unicos.append(len(dias_unicos))
        matches.append(len(matches_por_ponto[ponto]))

    # Criar um DataFrame com as informações
    data = {
        'Ano': anos,  # Adiciona a coluna do ano
        'Pontos': pontos,
        'Dias_de_Ressaca': dias_de_ressaca,
        'Dias_Únicos': dias_unicos,
        'Matches': matches
    }

    df_informacoes = pd.DataFrame(data)

    # Adicione as colunas com os percentuais de acerto
    df_informacoes['Percentual_Matches'] = (df_informacoes['Matches'] / df_informacoes['Dias_Únicos']) * 100
    df_informacoes['Percentual_Avisos_Waverys'] = (df_informacoes['Dias_Únicos']) / df_informacoes['Dias_de_Ressaca']  * 100

    return df_informacoes

 
main_dir = '/p1-nemo/rtecchio/'
data_inicio = pd.Timestamp('2020-01-01T00:00:00')
data_fim = pd.Timestamp('2021-12-31T23:00:00')
ressaca_waverys_por_ponto = separa_dias_ressaca_waverys(main_dir)
for ano in range(2020, 2022):
    df_avisos, strings_data_inicio, strings_data_fim = carregar_avisos_de_ressaca_CHM(ano)
    dias_unicos = pd.Series(pd.date_range(start=df_avisos.index.min(), end=df_avisos.index.max(), freq='D')).dt.normalize()
    matches_por_ponto = calcular_matches_por_ponto(ressaca_waverys_por_ponto, dias_unicos)
    df_informacoes = criar_dataframe_informacoes_comparacao(ressaca_waverys_por_ponto, matches_por_ponto)