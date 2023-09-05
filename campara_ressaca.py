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
df_avisos=pd.read_csv('/p1-nemo/rtecchio/ressacas/2021/lista_ressacas_RS_2021.csv',sep=';',names=lista_header, parse_dates=True)

#Avisos de Ressaca
df_avisos.index = pd.to_datetime(df_avisos['data_aviso'],dayfirst=True) 

#df.columns=lista_header

#pd.to_datetime(df.index) 

ini = df_avisos['inicio'].values 
fin = df_avisos['validade'].values 

# CRIA LISTA COM STRING P/ DURACAO DO AVISO
stini = []
stfin = [] 
for dtz in range(len(ini)):
    stini.append(str(ini[dtz]))
    stfin.append(str(fin[dtz]))

# COLOCA 0 NA FRENTE DA STRING
for zeron in range(len(stini)):
    if len(stini[zeron]) <= 5:
        stini[zeron] = '0' +stini[zeron] 
    else:
        stini[zeron] = stini[zeron] 
for zeron in range(len(stfin)):
    if len(stfin[zeron]) <= 5:
        stfin[zeron] = '0' +stfin[zeron] 
    else:
        stfin[zeron] = stfin[zeron] 

# CRIA LISTA COM OS DIAS DE AVISO NO FORMATO DATETIME

avisos = []
validade = [] 
for zr in range(len(stini)):
    dia1 = stini[zr]
    dia2 = stfin[zr]
    
    if df_avisos.index.month[zr] < 10:
        diax =  '0' +str(df_avisos.index.month[zr])+ "-"  + dia1[0:2] + "-" + str(df_avisos.index.year[zr]) + " " + dia1[2:4] + ":" + dia1[4:6] 
        diax2 = '0' +str(df_avisos.index.month[zr])+ "-"  + dia2[0:2] + "-" + str(df_avisos.index.year[zr]) + " " + dia2[2:4] + ":" + dia2[4:6] 
    
    else:
        diax =  str(df_avisos.index.month[zr])+ "-"  + dia1[0:2] + "-" + str(df_avisos.index.year[zr]) + " " + dia1[2:4] + ":" + dia1[4:6] 
        diax2 = str(df_avisos.index.month[zr])+ "-"  + dia2[0:2] + "-" + str(df_avisos.index.year[zr]) + " " + dia2[2:4] + ":" + dia2[4:6] 

    
    date1 = datetime.strptime(diax, '%m-%d-%Y %H:%M')
    date2 = datetime.strptime(diax2, '%m-%d-%Y %H:%M')
    
    # Se o aviso foi emitido no mes anterior da vigencia, adiciona um mes na vigencia
    if date1.day < df_avisos.index.day[zr]:
        date1 = date1+ relativedelta(months=1)
        diax = date1.strftime("%m-%d-%Y %H:%M")
    if date2.day < df_avisos.index.day[zr]:
        date2 = date2+ relativedelta(months=1)
        diax2 = date2.strftime("%m-%d-%Y %H:%M")
        
    # Se a vigencia inicia num mes anterior ao termino, adiciona um mes nela
    if date1.day > date2.day:
        date2 = date2+ relativedelta(months=1)
        diax2 = date2.strftime("%m-%d-%Y %H:%M")
        #break
    
    diay = pd.to_datetime(diax)
    diay2 = pd.to_datetime(diax2) 
    
    avisos.append(diay) 
    validade.append(diay2) 


ndt = []
for fx in range(len(avisos)):
    
    min_date_time = avisos[fx]
    max_date_time = validade[fx]
    
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


matches = []
for d in dias_unicos:
    if d in dias_ressaca.index:
        matches.append(d)
len(matches)
len(dias_unicos)
len(dias_ressaca)