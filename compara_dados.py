import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_pdf(df_weverys, df_boia, variavel, variavel_waverys, variavel_boia,
              label='boia', color='b'):
    plt.close('all')
    plt.figure(figsize=(5, 5))
    sns.kdeplot(df_weverys[variavel_waverys], label='Weverys', color='black', linewidth=3)
    sns.kdeplot(df_boia[variavel_boia], color=color, label=label, linewidth=3)
    if variavel == 'Hs':
        plt.xlabel('Altura Significativa das Ondas (Hs)', fontsize=14)
    elif variavel == 'Tp':
        plt.xlabel('Período de Pico (Tp)', fontsize=14)
    plt.ylabel('')
    plt.legend(loc='upper right', fontsize=14)
    fname = f"{diretorio_figuras}/PDF_{label}_{variavel}.png"
    plt.savefig(fname, dpi=500)
    print(f"{fname} criado")

def plot_regressao(df_weverys, df_boia, variavel, variavel_waverys, variavel_boia, boia):
    
    df_boia.index, df_weverys.index  = pd.to_datetime(df_boia.index), pd.to_datetime(df_weverys.index)
    df_boia_resampled = df_boia.resample('3H').mean().loc[df_weverys.index[0]: df_weverys.index[-1]]
    df_weverys_resampled = df_weverys.loc[df_boia_resampled.index[0]: df_boia_resampled.index[-1]]

    plt.figure(figsize=(10, 6))
    sns.regplot(x=df_weverys_resampled[variavel_waverys],
                 y=df_boia_resampled[variavel_boia],
                 label=variavel, fit_reg=True,
                 scatter_kws={'s': 20, "color": "black"},
                 line_kws={"color": "red"})
    plt.xlabel('Weverys')
    plt.ylabel(f'Boia')
    plt.legend(loc='upper right', fontsize=14)

    fname = f"{diretorio_figuras}/regressao_{boia}_{variavel}.png"
    plt.savefig(fname, dpi=500)
    print(f"{fname} criado")
    print()


# Leitura dos dados das boias a partir dos arquivos CSV
df_riogde = pd.read_csv('/p1-nemo/rtecchio/Dados_dissertacao/boia_rg.csv', header=0, usecols=['Datetime', 'Wvht', 'Dpd'], na_values=-9999.0, index_col=0)
df_itajai = pd.read_csv('/p1-nemo/rtecchio/Dados_dissertacao/boia_ita.csv', header=0, usecols=['Datetime' ,'Wvht', 'Dpd'], na_values=-9999.0,  index_col=0)
df_santos = pd.read_csv('/p1-nemo/rtecchio/Dados_dissertacao/boia_santos.csv', header=0, usecols=['Datetime', 'Wvht', 'Dpd'], na_values=-9999.0,  index_col=0)
df_vitoria = pd.read_csv('/p1-nemo/rtecchio/Dados_dissertacao/boia_es.csv', header=0, usecols=['Datetime', 'Wvht', 'Dpd'], na_values=-9999.0,  index_col=0)

# Leitura dos dados do Weverys a partir do arquivo NetCDF
ds = xr.open_mfdataset('/p1-nemo/mbonjour/onda_dados/waverys_1993_2019.nc', parallel=True)

# Coordenadas das boias (latitude e longitude)
boia_coords = {
    'RG': {'latitude': -31.53, 'longitude': -49.86, 'color':'#bc6c25'},
    'ITA': {'latitude': -28.48, 'longitude': -47.52, 'color':'#457b9d'},
    'SANTOS': {'latitude': -25.28, 'longitude': -44.92, 'color': '#7cb518'},
    'ES': {'latitude': -19.93, 'longitude': -39.70, 'color': '#9e2a2b'}
}
target_time = slice('2009-01-01T00:00:00','2019-12-31T21:00:00')

# Interpolação espacial para os dados do Weverys nas coordenadas de cada boia no tempo desejado
latitudes = [boia_coords['RG']['latitude'], boia_coords['ITA']['latitude'], boia_coords['SANTOS']['latitude'], boia_coords['ES']['latitude']]
longitudes = [boia_coords['RG']['longitude'], boia_coords['ITA']['longitude'], boia_coords['SANTOS']['longitude'], boia_coords['ES']['longitude']]
weverys_hs_boias = ds['VHM0'].sel(latitude=latitudes, longitude=longitudes, method='nearest'). sel(time=target_time)
weverys_tp_boias = ds['VTPK'].sel(latitude=latitudes, longitude=longitudes, method='nearest'). sel(time=target_time)

# Store the 'Wvht' columns from each dataframe into a list
data = {'RG': df_riogde,
         'ITA': df_itajai,
           'SANTOS': df_santos,
             'ES': df_vitoria}

diretorio_figuras = './figuras_validacao_waverys'

for variavel in ['Hs', 'Tp']:
    if variavel == 'Hs':
        variavel_waverys, variavel_boia = 'VHM0', 'Wvht'
    elif variavel == 'Tp':
        variavel_waverys, variavel_boia = 'VTPK', 'Dpd'

    for boia in ['RG', 'ITA', 'SANTOS', 'ES']:
        df_weverys = ds[variavel_waverys].sel(latitude=boia_coords[boia]['latitude'],
                                        longitude=boia_coords[boia]['longitude'], method='nearest'
                                        ).sel(time=target_time).to_dataframe().drop('latitude', axis=1).drop('longitude', axis=1)
        df_boia = data[boia]

        # plot_pdf(df_weverys, df_boia, variavel, variavel_waverys, variavel_boia,
        #           label=boia, color=boia_coords[boia]['color'])
        
        plot_regressao(df_weverys, df_boia, variavel, variavel_waverys, variavel_boia, boia)
