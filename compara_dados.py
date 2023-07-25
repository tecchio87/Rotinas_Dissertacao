import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_pdf(df):

    plt.close('all')
    plt.figure(figsize=(10, 6))
    sns.kdeplot(weverys_hs_interp, label='Weverys', color='black', linewidth=2)
    sns.kdeplot(df_rg['Wvht'], label='RG')
    sns.kdeplot(df_ita['Wvht'], label='ITA')
    sns.kdeplot(df_santos['Wvht'], label='SANTOS')
    sns.kdeplot(df_es['Wvht'], label='ES')
    plt.xlabel('Altura Significativa das Ondas (Hs)')
    plt.ylabel('Densidade de Probabilidade')
    plt.title('Diagrama de Densidade de Probabilidade para Hs')
    plt.legend()
    plt.show()

def plot_regressao(df):
    
    plt.figure(figsize=(10, 6))
    sns.regplot(x=weverys_hs_interp, y=df_rg['Wvht'], scatter_kws={'s': 20}, label='RG')
    sns.regplot(x=weverys_hs_interp, y=df_ita['Wvht'], scatter_kws={'s': 20}, label='ITA')
    sns.regplot(x=weverys_hs_interp, y=df_santos['Wvht'], scatter_kws={'s': 20}, label='SANTOS')
    sns.regplot(x=weverys_hs_interp, y=df_es['Wvht'], scatter_kws={'s': 20}, label='ES')
    plt.xlabel('Weverys')
    plt.ylabel('Boias (Hs)')
    plt.title('Regressão Linear para Hs')
    plt.legend()
    plt.show()


# Leitura dos dados das boias a partir dos arquivos CSV
df_riogde = pd.read_csv('/p1-nemo/rtecchio/Dados_dissertacao/boia_rg.csv', header=0, usecols=['Datetime', 'Wvht', 'Dpd'], na_values=-9999.0)
df_itajai = pd.read_csv('/p1-nemo/rtecchio/Dados_dissertacao/boia_ita.csv', header=0, usecols=['Datetime' ,'Wvht', 'Dpd'], na_values=-9999.0)
df_santos = pd.read_csv('/p1-nemo/rtecchio/Dados_dissertacao/boia_santos.csv', header=0, usecols=['Datetime', 'Wvht', 'Dpd'], na_values=-9999.0)
df_vitoria = pd.read_csv('/p1-nemo/rtecchio/Dados_dissertacao/boia_es.csv', header=0, usecols=['Datetime', 'Wvht', 'Dpd'], na_values=-9999.0)

# Leitura dos dados do Weverys a partir do arquivo NetCDF
ds = xr.open_mfdataset('/p1-nemo/mbonjour/onda_dados/waverys_1993_2019.nc', parallel=True)

# Coordenadas das boias (latitude e longitude)
boia_coords = {
    'RG': {'latitude': -31.53, 'longitude': -49.86},
    'ITA': {'latitude': -28.48, 'longitude': -47.52},
    'SANTOS': {'latitude': -25.28, 'longitude': -44.92},
    'ES': {'latitude': -19.93, 'longitude': -39.70}
}
target_time = slice('2009-01-01T00:00:00','2019-12-31T21:00:00')

# Interpolação espacial para os dados do Weverys nas coordenadas de cada boia no tempo desejado
latitudes = [boia_coords['RG']['latitude'], boia_coords['ITA']['latitude'], boia_coords['SANTOS']['latitude'], boia_coords['ES']['latitude']]
longitudes = [boia_coords['RG']['longitude'], boia_coords['ITA']['longitude'], boia_coords['SANTOS']['longitude'], boia_coords['ES']['longitude']]
weverys_hs_interp = ds['VHM0'].interp(latitude=latitudes, longitude=longitudes, time=target_time )
weverys_tp_interp = ds['VTPK'].interp(latitude=latitudes, longitude=longitudes,time=target_time )

# Concatenar os DataFrames de cada boia em um único DataFrame (df)
df = pd.concat([df_riogde, df_itajai, df_santos, df_vitoria], axis=1)

print(df)

# Chamada da função, passando os DataFrames das boias diretamente
#compare_data_with_weverys(df_riogde, df_itajai, df_santos, df_vitoria, weverys_hs_interp, weverys_tp_interp)