import os
import matplotlib.gridspec as gridspec
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import xarray as xr
import pandas as pd
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature, COASTLINE, BORDERS
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cmocean as cmo
import matplotlib
import matplotlib.colors as mcolors


# Colormap setas
colors_setas = ['#943126', '#E74C3C', '#f37012', '#F39C12', '#F9E79F',
          '#F8F2DB', 'white', '#D8EDF0',
          '#9eb3c2', '#1c7293', '#065a82', '#1b3b6f', '#21295c']
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors_setas[::-1])

def map_features(ax):
    ax.add_feature(COASTLINE)
    ax.add_feature(BORDERS, edgecolor='#383838')
    return ax

def Brazil_states(ax):    
    states = NaturalEarthFeature(category='cultural', scale='50m', facecolor='none',
                                  name='admin_1_states_provinces_lines')
    _ = ax.add_feature(states, edgecolor='#383838')
    
    cities = NaturalEarthFeature(category='cultural', scale='50m', facecolor='none',
                                  name='populated_places')
    _ = ax.add_feature(cities)
    
def grid_labels_params(ax,i):
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=1, color='gray', alpha=0.5,linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    if i not in [2,3]:
        gl.bottom_labels=False
    if i not in [0,2]:
        gl.left_labels = False
    gl.xlabel_style = {'size': 12, 'color': '#383838'}
    gl.ylabel_style = {'size': 12, 'color': '#383838'}
    ax.spines['geo'].set_edgecolor('#383838')
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return ax


def converter_direcao(dado_direcao, mag=2.5):
    """
    Convert the given direction from degrees to radians and calculate the x and y components of the vector.

    Parameters:
    - dado_direcao (float): The direction in degrees.
    - mag (float, optional): The magnitude of the vector. Default is 2.5.

    Returns:
    - u (float): The x component of the vector.
    - v (float): The y component of the vector.
    """
    mag = 2.5
    # Converter a direção para radianos
    direcao_radianos = np.deg2rad(dado_direcao)
    # Calcular as componentes x e y do vetor
    u = mag * np.cos(direcao_radianos)
    v = mag * np.sin(direcao_radianos)
    return u, v

def plot_mapa_setas(dados_energia, dados_ptos, prof_filtred, lat_pto, lon_pto):
    
    print('plotando setas..')
    dir_perp = dados_ptos['DIR_NOR']
    
    # Filtrar os dados dentro da janela de tempo
    inicio_janela = pd.to_datetime('2023-01-27T00:00:00')
    fim_janela = pd.to_datetime('2023-02-01T23:59:59')
    dados_janela = dados_energia[(dados_energia["time"] >= inicio_janela) & (dados_energia["time"] <= fim_janela)]
    
    # Agrupar os dados por ponto e período de 6 horas e obter os índices dos valores máximos de PPer
    indices_maximos = dados_janela.groupby([pd.Grouper(freq='6H'), dados_janela["ponto"]])["PPer"].idxmax()
    
    # Obter os valores de PPer para cada ponto e período de 6 horas
    PPer_pontos = dados_janela.loc[indices_maximos, "PPer"].values
    
    # Criar uma figura 
    fig, ax = plt.subplots(figsize=(12, 10), nrows=1, ncols=1, subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Configurar o mapa e suas características
    ax = fig.add_subplot(111, projection=proj)
    ax.set_extent([-60,-30,-40,-16])
    map_features(ax)
    Brazil_states(ax)
    grid_labels_params(ax, 0)
    cf1 = ax.contourf(prof_filtred.lon[::20], prof_filtred.lat[::20], prof_filtred[::20, ::20], cmap="cmo.deep_r")
    
    ax.contourf(prof_filtred.lon[::20], prof_filtred.lat[::20], prof_filtred[::20, ::20], cmap="cmo.deep_r")
    
    # Plotar as setas de energia
    lon_pto1 = list(map(float, lon_pto.values))
    lat_pto1 = list(map(float, lat_pto.values))
    
    # Define your discrete color levels here
    levels = np.linspace(-10, 50, 11)

    # Create a BoundaryNorm instance to map values to discrete colors
    cmap = plt.get_cmap("jet")
    norm_dia = mcolors.BoundaryNorm(levels, ncolors=cmap.N, clip=False)

    colors_dia = cmap(norm_dia(PPer_pontos))

    u_perp, v_perp = converter_direcao(dir_perp)
        
    ax.quiver(lon_pto1, lat_pto1,  u_perp, v_perp, color=colors_dia, edgecolor='k',
               linewidth=1, pivot='tip', scale=20, width=0.015)
    
    # Adicionar título ao subplot com a data e hora do período de 6 em 6 horas
    for idx, (date, ponto) in enumerate(indices_maximos.index):
        titulo = f'Data e Hora: {date:%Y-%m-%d %H:%M:%S} - Ponto {ponto}'
        ax.text(lon_pto1[idx], lat_pto1[idx], titulo, fontsize=8, ha='center', va='bottom', color='black')
    
    # Adicionar barra de cores para PPer
    cbar_PPer = fig.add_axes([0.057, 0.05, 0.40, 0.02])  # Posição da colorbar PPer
    cbper = fig.colorbar(cm.ScalarMappable(norm=norm_dia, cmap=cmap), cax=cbar_PPer, orientation='horizontal')
    cbper.ax.tick_params(labelsize=8)
    cbper.set_label('PPer', labelpad=0, fontsize=12, fontweight='bold')
    
    plt.subplots_adjust(left=0.02, right=1, bottom=0.15, top=0.90)
    
    # Salvar a figura em um arquivo separado com o nome baseado na data do evento de ressaca
    nome_arquivo = f'P_setas_grid2_{inicio_janela.strftime("%Y%m%d")}.png'
    plt.savefig(nome_arquivo, dpi=300)
    
    # Fechar a figura para liberar memória
    plt.close(fig)

def main():

    #os.makedirs("../figures_waves", exist_ok=True)

    # Carregar os dados diários de um arquivo CSV
    dados_energia = pd.read_csv('/p1-nemo/rtecchio/teste_chico/variaveis_diarias_ww3.csv', sep=',', parse_dates=["time"])

    # figure_dir = "../figures_waves/serie_temporal"
    # os.makedirs(figure_dir, exist_ok=True)
    # for variavel in dados_energia.columns[1:-2]:
    #     plot_serie_temporal(dados_energia, datas_ressaca, variavel, figure_dir)

    # figure_dir = "../figures_waves/serie_temporal_eventos"
    # os.makedirs(figure_dir, exist_ok=True)
    # for direcao in ['PPer', 'Ppar']:
    #     plot_serie_temporal_evento(dados_energia, datas_ressaca, direcao, figure_dir)

    # Profundidades para deixar a figura mais bonita
    ds = xr.open_dataset('/p1-nemo/rtecchio/Dados/GEBCO/gebco_costa_s_se.nc')
    prof2 = ds['elevation'][:]
    prof_filtred = prof2.where(prof2 <= 0)

    # Pontos
    dados_ptos = pd.read_csv('/p1-nemo/rtecchio/teste_chico/pontos_disertacao_normal_final.csv', sep=';', decimal=',')
    lat_pto = dados_ptos['lat']
    lon_pto = dados_ptos['lon']
    dir_perp = dados_ptos['DIR_NOR']
    dir_par = dados_ptos['DIR_PAR']

    plot_mapa_setas(dados_energia, dados_ptos, prof_filtred, lat_pto, lon_pto)

if __name__ == '__main__':
    main()