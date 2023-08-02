import pandas as pd
import matplotlib.pyplot as plt
import cmocean as cmo
import xarray as xr
import numpy as np
import matplotlib.dates as mdates
import matplotlib.colors as colors
from matplotlib import cm
from matplotlib.colors import ListedColormap
from matplotlib.font_manager import FontProperties

def dados_para_xarray(df_entrada, variavel):
    '''
    df_entrada: pd.DataFrame
        Dados de entrada organizados em um DataFrame, com colunas
        separando as variaveis, tempo e respectivos pontos
    '''
    pontos = df_entrada.ponto.unique()
    arrays_pontos = []
    for ponto in pontos:
        df_ponto = df_entrada[df_entrada['ponto'] == ponto][variavel]
        da_ponto =  xr.DataArray(df_ponto,dims=['time'],coords=dict(
                        time=df_entrada.time.unique()))
        da_ponto = da_ponto.expand_dims({'ponto':[ponto]})                
        arrays_pontos.append(da_ponto)
       
    return xr.concat(arrays_pontos,dim='ponto')
     
def compara_quantis(quantis_climatologia_pontos, da_entrada):
    '''
    quantis_climatologia_pontos: xr.DataArray
        Array que contém os quantis climatolõgicos de uma variável, para cada ponto
    da_entrada: xr.DataArray
        Array contendo os dados a serem comparados com a climatologia
    '''
    da_quantiles = da_entrada.copy()
    iq = 0
    while iq < len(quantiles):
        quantile = quantiles[iq]
        if quantile != 1:
            da_q = da_entrada.where((da_entrada >= clim_quantiles.isel(quantile=iq)) &
                             (da_entrada <= clim_quantiles.isel(quantile=iq+1)))
        da_quantiles = da_quantiles.where(da_q.isnull(),quantiles[iq])
        iq += 1
        
    da_q = da_entrada.where(da_entrada <= clim_quantiles.sel(quantile=0.5))
    da_quantiles = da_quantiles.where(da_q.isnull(),quantiles[0])
    da_q = da_entrada.where(da_entrada >= clim_quantiles.sel(quantile=1))
    da_quantiles = da_quantiles.where(da_q.isnull(),quantiles[-1])
    
    return da_quantiles
 
    
def hovmoller(da_entrada, **kwargs):
    '''
    variavel: str
        variavel a ser plotada (hs ou tp)
	da_entrada: DataArray 
        Dado de entrada, onde as dimensoes sao o tempo e os pontos
    '''
    
    if kwargs['name'] == 'Hs':
        # top = cm.get_cmap('cmo.dense',256)
        # bottom = cm.get_cmap('cmo.matter_r')
        # newcolors = np.vstack((top(np.linspace(0, 1, 230)), bottom(np.linspace(0 , 1, 256))))
        # cmap = ListedColormap(newcolors, name='Tecchio')
        # ticks = np.linspace(0, 15, 16)
        # levs =  np.arange(2, 14, 1)
        # norm = colors.Normalize(vmin=0, vmax=15)
        # clevs = ticks
        # fmt = '%d'
        
        top = cm.get_cmap('cmo.dense',256)
        bottom = cm.get_cmap('cmo.matter_r')
        newcolors = np.vstack((top(np.linspace(0, 1, 230)), bottom(np.linspace(0 , 1, 256))))
        cmap = ListedColormap(newcolors, name='Tecchio')
        cmap = cm.get_cmap('cmo.tempo')
        cmap='rainbow'
        ticks = list(np.linspace(0, 7, 25))
        levs =  np.arange(0, 7, 0.5)
        norm = colors.Normalize(vmin=0, vmax=7)
        clevs = ticks
        fmt = '%.1f'
    elif kwargs['name'] == 'Hsp':
        # top = cm.get_cmap('cmo.dense',256)
        # bottom = cm.get_cmap('cmo.matter_r')
        # newcolors = np.vstack((top(np.linspace(0, 1, 230)), bottom(np.linspace(0 , 1, 256))))
        # cmap = ListedColormap(newcolors, name='Tecchio')
        # ticks = np.linspace(0, 15, 16)
        # levs =  np.arange(2, 14, 1)
        # norm = colors.Normalize(vmin=0, vmax=15)
        # clevs = ticks
        # fmt = '%d'
        top = cm.get_cmap('cmo.dense',256)
        bottom = cm.get_cmap('cmo.matter_r')
        newcolors = np.vstack((top(np.linspace(0, 1, 230)), bottom(np.linspace(0 , 1, 256))))
        cmap = ListedColormap(newcolors, name='Tecchio')
        cmap = cm.get_cmap('cmo.tempo')
        cmap='rainbow'
        ticks = list(np.linspace(0, 7, 25))
        levs =  np.arange(0, 7.5, 0.5)
        norm = colors.Normalize(vmin=0, vmax=7.5)
        clevs = ticks
        fmt = '%.1f'
    elif kwargs['name'] == 'Hsp_per':
        # top = cm.get_cmap('cmo.dense',256)
        # bottom = cm.get_cmap('cmo.matter_r')
        # newcolors = np.vstack((top(np.linspace(0, 1, 230)), bottom(np.linspace(0 , 1, 256))))
        # cmap = ListedColormap(newcolors, name='Tecchio')
        # ticks = np.linspace(0, 15, 16)
        # levs =  np.arange(2, 14, 1)
        # norm = colors.Normalize(vmin=0, vmax=15)
        # clevs = ticks
        # fmt = '%d'
        top = cm.get_cmap('cmo.dense',256)
        bottom = cm.get_cmap('cmo.matter_r')
        newcolors = np.vstack((top(np.linspace(0, 1, 230)), bottom(np.linspace(0 , 1, 256))))
        cmap = ListedColormap(newcolors, name='Tecchio')
        cmap = cm.get_cmap('cmo.tempo')
        cmap='rainbow'
        ticks = list(np.linspace(0, 5, 25))
        levs =  np.arange(0, 4.5, 0.5)
        norm = colors.Normalize(vmin=0, vmax=4.5)
        clevs = ticks
        fmt = '%.1f'
    elif kwargs['name'] == 'Tp':  
        # cmap = 'cmo.dense'
        # ticks = np.linspace(0, 20, 21)
        # levs =  np.arange(8, 20, 2)
        # norm = colors.Normalize(vmin=0, vmax=30)
        # fmt = '%d'
        
        cmap = 'cmo.dense'
        cmap = 'jet'
        ticks = np.linspace(5, 20, 15)
        levs =  np.arange(8, 21, 1)
        norm = colors.Normalize(vmin=5, vmax=21)
        fmt = '%d'
    elif kwargs['name'] == 'Pw':
        cmap = 'cmo.thermal'
        ticks = np.linspace(0, 300, 50)
        levs =  np.arange(25, 300, 25)
        norm = colors.Normalize(vmin=25, vmax=300)
        fmt = '%d'
    elif kwargs['name'] == 'P':
        cmap = 'cmo.thermal'
        ticks = np.linspace(0, 300, 50)
        levs =  np.arange(25, 300, 25)
        norm = colors.Normalize(vmin=25, vmax=300)
        fmt = '%d'
    elif kwargs['name'] == 'PPer':
        cmap = 'cmo.diff'
        ticks = np.linspace(-300, 50, 50)
        levs =  np.arange(-300, 50, 20)
        norm = divnorm = colors.TwoSlopeNorm(vmin=-300, vcenter=0, vmax=80)
        fmt = '%d' 
    elif kwargs['name'] == 'Px':
        cmap = 'cmo.diff'
        ticks = np.linspace(-50, 200, 50)
        levs =  np.arange(-50, 200, 20)
        norm = divnorm = colors.TwoSlopeNorm(vmin=-50, vcenter=0, vmax=200)
        fmt = '%d'    
    elif kwargs['name'] == 'Py':
        cmap = 'cmo.diff'
        ticks = np.linspace(-60, 215, 50)
        levs =  np.arange(-60, 215, 20)
        norm = divnorm = colors.TwoSlopeNorm(vmin=-60, vcenter=0, vmax=215)
        fmt = '%d'       
    elif kwargs['name'] == 'Ppar':
        cmap = 'cmo.diff'
        ticks = np.linspace(-150, 60, 10)
        levs =  np.arange(-150, 60, 20)
        norm = divnorm = colors.TwoSlopeNorm(vmin=-150, vcenter=0, vmax=80)
        fmt = '%d'  
    elif 'quantile' in kwargs['name']:
        cmap = cm.get_cmap('cmo.tempo')
        cmap = 'cmo.amp'
        cmap = 'afmhot_r'
        norm = colors.Normalize(vmin=0.5, vmax=1)
        ticks = np.arange(0.5,1.,0.01)
        levs = np.arange(0.6,1.,0.05)
        fmt = '%.2f'
        #fmt = '%1.1f'
        
   
    plt.close('all')
    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(111)
    ptos = range(1,len(da_entrada.ponto)+1)
    cf = plt.contourf(da_entrada.time.values,ptos,da_entrada,
                        cmap=cmap, norm=norm, levels=ticks, extend='max')
    if len(da_entrada.time) < 330:                
        ct = plt.contour(da_entrada.time.values,ptos,da_entrada,
                        colors='gray', norm=norm, levels=levs, linestyles='dashed',linewidth=0.2) 
        plt.clabel(ct, fmt=fmt)                    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%^b-%d'))

    #plt.grid(color='gray', alpha=0.7, grid_linestyle= 'dashed',linewidth=1)
    # font = fm.FontProperties(family='Calibri')
    # plt.rc('font', family='Calibri', size=12)
    # plt.rc('axes', labelsize=12, titlefont=font)
    plt.grid(linestyle='dashed',linewidth=0.25, color='gray')
    ax.set_yticks(ptos)
    plt.colorbar(cf, drawedges=True, extend='None')
    plt.title(kwargs['name'])
    
    sdate1 = pd.Timestamp(dates[0]).strftime('%Y%m%d')
    sdate2 = pd.Timestamp(dates[1]).strftime('%Y%m%d')
    if 'fname' in kwargs.keys():
        fname = kwargs['fname']
    else:
        fname = kwargs['name']+'_'+sdate1+'-'+sdate2
    plt.savefig('teste_chico/'+fname+'.png', dpi=300)
    print('teste_chico/'+fname,'created')
    plt.show()
   
   

# Dados climatologia
dado_climatologia_completa = '/p1-nemo/rtecchio/teste_chico/variaveis_dissertacao.csv'
dados_ww3 = '/p1-nemo/rtecchio/teste_chico/variaveis_diarias_ww3.csv'

df_clim = pd.read_csv(dados_ww3, index_col=0, parse_dates=['time'])#para testar um período menor trocar 

# Defina as datas de início e fim desejadas
inicio_rodada = df_clim['time'].iloc[0]
fim_rodada = df_clim['time'].iloc[-1]

# Converta as datas para strings no formato 'YYYY-MM-DD HH:MM:SS'
inicio_str = inicio_rodada.strftime('%Y-%m-%d %H:%M:%S')
fim_str = fim_rodada.strftime('%Y-%m-%d %H:%M:%S')

# Crie a lista 'dates' com as datas de início e fim
dates = [inicio_str, fim_str]

# Agora você pode utilizar 'dates' na comparação
dummy = df_clim[(df_clim['time'] >=  dates[0]) & (df_clim['time'] <= dates[1])]


for var in ['Hsp','P', 'PPer','Ppar', 'Hsp_per' ]:
    da_entrada = dados_para_xarray(dummy, var)
    kwargs = {'name':var} 
    hovmoller(da_entrada, **kwargs)
    
    # Pega quantis da climatologia
    da_clim = dados_para_xarray(df_clim, var)
    quantiles = np.linspace(0.5,1,51)
    #quantiles = [0.5,0.55,0.6, 0.65, 0.7,0.75, 0.8,0.85, 0.9,0.92, 0.95, 0.97, 1]
    clim_quantiles = da_clim.quantile(quantiles, dim='time')
    # Compara os dados de entrada com a climatologia
    da_quantis = compara_quantis(clim_quantiles, da_entrada)
    kwargs = {'name':var+'_quantile'}
    hovmoller(da_quantis, **kwargs)
   


clim_quantiles = {} 
clim_quantiles_var = {}
for var in  ['Tp','Hsp']:
    clim_quantiles[var] = {}
    for q in quantiles:
        clim_quantiles[var][q] = []
        for p in range(18):
            value = df_clim[df_clim.ponto == p][var].quantile(q)
            clim_quantiles[var][q].append(value)
            
    clim_quantiles_var[var] = pd.DataFrame(clim_quantiles[var])
    df =  clim_quantiles_var[var]
    
    plt.close('all')
    plt.figure()
    plt.stackplot(df.index, df[0.5], df[0.6], df[0.7], df[0.8],
                    df[0.9], df[1.0], labels=df.columns, colors=colors)
    for i in range(18):
        plt.axvline(i, color='k', alpha=0.4, linestyle='dashed', linewidth=0.15)
    plt.xlabel('Ponto')
    plt.ylabel(var)
    plt.xticks(df_clim.ponto.unique())
    plt.legend(bbox_to_anchor=(1, 0.33))
    plt.tight_layout()
    plt.show()
    plt.savefig('quantis_pontos_'+var+str(q)+'.png', dpi=500)










# # Para testar
# var = 'hs'
# da_entrada = dados_para_xarray(dummy, var)
# hs_pto0 = da_entrada.sel(ponto=0)
# hsmax =  hs_pto0.max()
# hsmax_id = hs_pto0.idxmax()

# da_clim = dados_para_xarray(df_clim, var)
# clim_quantiles = da_clim.quantile(quantiles, dim='time')
# quantiles_pto0 = clim_quantiles.sel(ponto=0)
# quantil_8 = quantiles_pto0[-3]

# da_quantis = compara_quantis(clim_quantiles, da_entrada)
# da_quantis_pto0 = da_quantis.sel(ponto=0)
# da_quantis_pto0_hsmax = da_quantis_pto0.sel(time=hsmax_id)


#Não salvei HSp_perp no arquivo da climatologia, logo estou inserindo ele no arquivo criando mais duas colunas no df (Hsp e Hsp_per)

# Hsp= ((df_clim['P']/5)**0.5)
# Pper=df_clim['PPer']
# Hsp_Perp=[]
# for valor in Pper:
    # # Calcula o valor absoluto do número, se ele for negativo
    # Pper_absoluto = (abs(valor)/5)
    # # Eleva o valor absoluto a 0.5
    # Hsp_per = math.sqrt(Pper_absoluto)
    # # Mantém o sinal do número original, se ele for negativo
    # Hsp_per = math.copysign(Hsp_per, valor)
    # # Adiciona o resultado à lista de resultados
    # Hsp_Perp.append(Hsp_per)
# # Dado de entrada dummy para testes
# df_clim['Hsp_per']=Hsp_Perp


# df_clim.to_csv('teste_chico/climatologia_we_ptos_final.csv')