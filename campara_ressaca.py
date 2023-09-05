import xarray as xr
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

main_dir = '/p1-nemo/rtecchio/'
dado_waverys = f'{main_dir}teste_chico/variaveis_dissertacao.csv'

print('abrindo dados climatológicos...')
df_waverys = pd.read_csv(dado_waverys, index_col=0, parse_dates=['time'])


# Defina as datas de início e fim do período desejado
data_inicio = pd.Timestamp('2021-01-01T00:00:00')
data_fim = pd.Timestamp('2021-12-31T23:00:00')

# Selecione o período de dados específico
dados_ano = df_waverys[(df_waverys.time>= data_inicio) & (df_waverys.time <= data_fim)]

# Selecione o ponto e a variavel que sera comparado com os avisos de ressaca
dados_ponto= dados_ano[dados_ano['ponto'] == 8]
dados_ponto_time= dados_ponto.time
dados_ponto.index=dados_ponto_time
dias_ressaca= dados_ponto['Hs'][dados_ponto['Hs']>=2.5]
pd.set_option('display.max_rows', dias_ressaca.shape[0]+1)
dias_ressaca=dias_ressaca.resample('1D').max().dropna()
print(dias_ressaca)
len(dias_ressaca)

#avisos de ressaca
lista_header=['arquivo','data_aviso','cidade1','cidade2','inicio','validade']
df_avisos=pd.read_csv('/p1-nemo/rtecchio/ressacas/2021/lista_ressacas_RS_2021.csv',
                      sep=';',names=lista_header, parse_dates=True, encoding='latin-1')

#Avisos de Ressaca
df_avisos.index = pd.to_datetime(df_avisos['data_aviso'], dayfirst=True) 

#df.columns=lista_header

#pd.to_datetime(df.index) 

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


matches = []
for d in dias_unicos:
    if d in dias_ressaca.index:
        matches.append(d)
len(matches)
len(dias_unicos)
len(dias_ressaca)