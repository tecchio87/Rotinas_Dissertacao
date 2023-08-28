import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.geometry.polygon import Polygon
import cartopy
import cartopy.feature as cfeature
from cartopy.feature import NaturalEarthFeature, COASTLINE
from cartopy.feature import BORDERS
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def grid_labels_params(ax):
    gl = ax.gridlines(draw_labels=True,zorder=2)    
    gl.xlabel_style = {'size': 16}
    gl.ylabel_style = {'size': 16}

def map_features(ax):
    ax.add_feature(COASTLINE,edgecolor='#283618',linewidth=1)
    ax.add_feature(BORDERS,edgecolor='#283618',linewidth=1)
    return ax

def Brazil_states(ax):    
    
    _ = ax.add_feature(cfeature.NaturalEarthFeature('physical',
                        'land', '50m', edgecolor='face', facecolor='#a4ab98'))
    
    states = NaturalEarthFeature(category='cultural', scale='50m', 
                                 facecolor='none',
                                  name='admin_1_states_provinces_lines')
    _ = ax.add_feature(states, edgecolor='#283618',linewidth=1)
    
    cities = NaturalEarthFeature(category='cultural', scale='50m',
                                 facecolor='none',
                                  name='populated_places')
    _ = ax.add_feature(cities, edgecolor='#283618',linewidth=1)


def plot_box(ax, color, *area):
    min_lon, max_lon, min_lat, max_lat = area
    pgon = Polygon(((min_lon, min_lat),
            (min_lon, max_lat),
            (max_lon, max_lat),
            (max_lon, min_lat),
            (min_lon, min_lat)))
    ax.add_geometries([pgon], crs=datacrs, 
                        facecolor='None', edgecolor=color,
                        linewidth = 3, alpha=1, zorder = 3)

SAM_area = [-90, -30, -60, 15]
SEBr_area = [-58, -35, -38, -17]
RJ_area = [-45, -40, -24, -19]

GB_lon, GB_lat = -43.1545, -22.8116
GB_area = [GB_lon-0.3, GB_lon+0.3, GB_lat-0.3, GB_lat+0.3]   

plt.close('all')
datacrs = ccrs.PlateCarree() # projection

# Bigger map
fig = plt.figure(figsize=(8, 8.5))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.83], projection=datacrs,
                frameon=True)
ax.set_extent(RJ_area, crs=datacrs)
Brazil_states(ax)
map_features(ax)
grid_labels_params(ax)
plot_box(ax, '#1D3461', *GB_area)

ax.text(-42.7, -22.4, "RJ", fontsize=30, fontweight='bold')

# Minimap
axins = inset_axes(ax, width="40%", height="40%", loc="upper left", 
                   axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                   axes_kwargs=dict(map_projection=cartopy.crs.PlateCarree()))
axins.set_extent(SAM_area, crs=datacrs)
axins.add_feature(cartopy.feature.COASTLINE)
Brazil_states(axins)
map_features(axins)
plot_box(axins, '#BF3D3B', *RJ_area)
plot_box(axins, '#3a5a40', *SEBr_area)


# Minimap 2
axins2 = inset_axes(ax, width="40%", height="40%", loc="upper right", 
                   axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                   axes_kwargs=dict(map_projection=cartopy.crs.PlateCarree()))
axins2.set_extent(SEBr_area, crs=datacrs)
axins2.add_feature(cartopy.feature.COASTLINE)
Brazil_states(axins2)
map_features(axins2)
plot_box(axins2, '#3a5a40', *SEBr_area)
axins2.text(-49, -22.36, "SP", fontsize=15, fontweight='bold', ha='center', va='center')

plt.show()
# plt.savefig()
print('\n')