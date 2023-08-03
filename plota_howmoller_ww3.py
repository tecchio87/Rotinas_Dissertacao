import pandas as pd
import matplotlib.pyplot as plt
import cmocean as cmo
import xarray as xr
import numpy as np
import matplotlib.dates as mdates
import matplotlib.colors as colors
from matplotlib import cm
from matplotlib.colors import ListedColormap
import matplotlib

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
 
 # Função para encontrar o quantil de um valor específico
def find_quantile_for_point(value, column, ponto, quantiles_df):
    quantile_values = quantiles_df.loc[ponto, column]
    for quantile, quantile_value in zip(quantiles, quantile_values):
        if value <= quantile_value:
            return quantile
    return 1.0  # Caso o valor seja maior que o maior quantil (1.0), retorna 1.0

def find_quantiles_for_data(row, ponto, quantiles_df):
    data = row['time']
    quantiles_values = quantiles_df.loc[ponto]
    quantiles_dict = {column: find_quantile_for_point(value, column, ponto, quantiles_df) for column, value in row.iteritems() if column != 'time' and column != 'ponto'}
    quantiles_row = pd.DataFrame(quantiles_dict, index=[data])
    return quantiles_row

def create_quantiles_dict(df_data_selecionada, quantiles_df_clim):
    pontos = df_data_selecionada['ponto'].unique()
    quantiles_dict = {}
    for ponto in pontos:
        print(f'criando quantil para o ponto {ponto}')
        df_ponto = df_data_selecionada[df_data_selecionada['ponto'] == ponto].copy()
        quantiles_df_ponto = df_ponto.apply(find_quantiles_for_data, args=(ponto, quantiles_df_clim), axis=1)
        quantiles_dict[ponto] = pd.concat(list(quantiles_df_ponto))
    return quantiles_dict

def create_quantiles_dataset(quantiles_dict):
    # Crie uma lista de DataArrays correspondentes a cada ponto
    da_list = []
    for ponto, quantiles_ponto in quantiles_dict.items():
        # Transforme o DataFrame de quantiles em um DataArray
        da_quantiles = xr.Dataset.from_dataframe(quantiles_ponto)
        # Adicione a coordenada 'ponto' com o valor atual
        da_quantiles.coords['ponto'] = ponto
        da_list.append(da_quantiles)
    
    # Concatene todos os DataArrays em um único DataSet
    return xr.concat(da_list, dim='ponto')

def hovmoller(da_entrada, **kwargs):
    '''
    variavel: str
        variavel a ser plotada (hs ou tp)
	da_entrada: DataArray 
        Dado de entrada, onde as dimensoes sao o tempo e os pontos
    '''
    
    if kwargs['name'] == 'Hs':
        colors_hs = ['#943126', '#E74C3C', '#f37012', '#F39C12', '#F9E79F',
          '#F8F2DB', 'white', '#D8EDF0',
          '#9eb3c2', '#1c7293', '#065a82', '#1b3b6f', '#21295c']
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors_hs[::-1])
        ticks = list(np.linspace(0, 7, 15))
        levs =  np.arange(0, 7, 0.5)
        norm = colors.Normalize(vmin=0, vmax=7)
        fmt = '%.1f'

    elif kwargs['name'] == 'Tp':
        cmap = 'RdYlGn_r'
        ticks = np.linspace(0, 25, 26)
        levs =  np.arange(0, 26, 2)
        norm = colors.Normalize(vmin=5, vmax=21)
        fmt = '%d'

    elif kwargs['name'] == 'Hsp':
        colors_hs = ['#943126', '#E74C3C', '#f37012', '#F39C12', '#F9E79F',
          '#F8F2DB', 'white', '#D8EDF0',
          '#9eb3c2', '#1c7293', '#065a82', '#1b3b6f', '#21295c']
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors_hs[::-1])
        ticks = list(np.linspace(0, 7, 15))
        levs =  np.arange(0, 7.5, 1)
        norm = colors.Normalize(vmin=0, vmax=7.5)
        fmt = '%.1f'

    elif kwargs['name'] == 'Pw':
        cmap = 'cmo.thermal'
        ticks = np.linspace(0, 300, 50)
        levs =  np.arange(25, 300, 25)
        norm = colors.Normalize(vmin=25, vmax=300)
        fmt = '%d'

    elif kwargs['name'] == 'P':
        cmap = 'cmo.thermal'
        ticks = np.linspace(0, 50, 11)
        levs =  np.arange(0, 51, 10)
        norm = colors.Normalize(vmin=0, vmax=50)
        fmt = '%d'

    elif kwargs['name'] == 'PPer':
        colors_hs = ['#344e41', '#3a5a40', '#588157', '#a3b18a', '#dad7cd',
          '#829cbc', '#6290c8', '#376996', '#1f487e', '#1d3461']
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors_hs[::-1])
        ticks = np.linspace(-150, 150, 10)
        levs =  np.arange(-150, 151, 20)
        norm = divnorm = colors.TwoSlopeNorm(vmin=-150, vcenter=0, vmax=150)
        fmt = '%d' 

    elif kwargs['name'] == 'Ppar':
        cmap = 'cmo.diff'
        ticks = np.linspace(-50, 200, 21)
        levs =  np.arange(-50, 201, 20)
        norm = divnorm = colors.TwoSlopeNorm(vmin=-50, vcenter=0, vmax=200)
        fmt = '%d' 

    elif 'quantile' in kwargs['name']:
        cmap = 'afmhot_r'
        norm = colors.Normalize(vmin=0.5, vmax=1)
        ticks = np.arange(0.5,1.,0.05)
        levs = np.arange(0.6,1.,0.1)
        fmt = '%.2f'
   
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

    plt.grid(linestyle='dashed',linewidth=0.25, color='gray')
    ax.set_yticks(ptos)
    plt.colorbar(cf, drawedges=True, extend='None')
    plt.title(kwargs['name'])

    dates = da_entrada.time
    
    sdate1 = pd.Timestamp(dates[0].values).strftime('%Y%m%d')
    sdate2 = pd.Timestamp(dates[1].values).strftime('%Y%m%d')
    if 'fname' in kwargs.keys():
        fname = kwargs['fname']
    else:
        fname = kwargs['name']+'_'+sdate1+'-'+sdate2
    # plt.savefig(f'{main_dir}teste_chico/'+fname+'.png', dpi=300)
    print('teste_chico/'+fname,'created')
    plt.show()

def plot_series_with_quantiles(quantiles_dict, df_data_selecionada, quantiles_df_clim, ponto=25, variavel='Hs'):
    # Selecionar os dataframes correspondentes ao ponto e à variável escolhida
    quantiles_ponto = quantiles_dict[ponto]
    
    # Selecionar a série temporal da variável escolhida
    time_series = df_data_selecionada[df_data_selecionada['ponto'] == ponto].set_index('time')[variavel]
    
    # Selecionar os quantis correspondentes para a variável escolhida
    quantiles_values = quantiles_ponto[f'{variavel}']
    
    # Selecionar o valor do quantil 0.9 para a variável escolhida
    quantile_90 = quantiles_df_clim.loc[ponto, variavel].iloc[-1]
    
    # Plotar a série temporal
    plt.figure(figsize=(10, 6))
    plt.plot(time_series.index, time_series, label='Série Temporal', color='blue')
    plt.xlabel('Tempo')
    plt.ylabel(variavel, color='blue')
    plt.title(f'Série Temporal e Quantis para o Ponto {ponto}')
    
    # Criar o segundo eixo para plotar o quantil
    ax2 = plt.gca().twinx()
    ax2.set_ylim([0,1])
    ax2.plot(quantiles_values.index, quantiles_values, label='Quantis', color='green')
    ax2.axhline(quantile_90, color='red', linestyle='--', label='Quantil 0.9')
    ax2.set_ylabel('Quantis', color='green')
    
    # Adicionar as legendas
    lines, labels = plt.gca().get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')
    
    plt.grid(True)
    plt.show()

main_dir = '/p1-nemo/rtecchio/'

# Dados climatologia
dado_climatologia_completa = f'{main_dir}teste_chico/variaveis_dissertacao.csv'
dados_ww3 = f'{main_dir}teste_chico/variaveis_diarias_ww3.csv'

print('abrindo dados climatológicos...')
df_clim = pd.read_csv(dado_climatologia_completa, index_col=0, parse_dates=['time'])

print('abrindo dados da rodada do ww3...')
# Agora você pode utilizar 'dates' na comparação
df_data_selecionada = pd.read_csv(dados_ww3, index_col=0, parse_dates=['time'])

# Cálculo dos quantis da climatologia (df_clim)
quantiles = np.linspace(0.5,1,51)
quantiles_df_clim = df_clim.groupby('ponto').quantile(quantiles)

print('criando quantis...')
quantiles_dict = create_quantiles_dict(df_data_selecionada, quantiles_df_clim)

# Criar o DataSet dos quantis
ds_quantiles = create_quantiles_dataset(quantiles_dict)
ds_quantiles = ds_quantiles.rename({'index':'time'})

# Exemplo de uso da função para plotar os dados da variável 'Hs' e seus quantis climatológicos para o ponto 0
#plot_series_with_quantiles(quantiles_dict, df_data_selecionada, quantiles_df_clim, ponto=0, variavel='Hs')

for var in ['Hs', 'Tp', 'Hsp', 'P', 'PPer','Ppar']:
    # Plota variável
    da_entrada = dados_para_xarray(df_data_selecionada, var)
    kwargs = {'name':var} 
    hovmoller(da_entrada, **kwargs)
    
    # Plota quantis
    kwargs = {'name':var+'_quantile'}
    da_quantis = ds_quantiles[var]
    hovmoller(da_quantis, **kwargs)

    print()