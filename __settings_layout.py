"""
@File        : __settings_layout.py
@Author      : Min Dai, shi4712
@Date        : 2022/8/26 9:48
@Description : define the UI related setting
"""
import numpy as np
from matplotlib import cm
from matplotlib import colors, colorbar
import seaborn as sns


## palette/cmap setting
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

myColors = [
    '#FF0000', '#00FF00', '#0000FF', '#00FFFF', '#FF00FF',
    '#FFA500', '#800080', '#008080', '#FFC0CB',
    # '#E6E6FA',
    '#A52A2A', '#808000', '#FF7F50', '#000080', '#40E0D0',
    '#FFD700', '#F5F5DC', '#D2B48C', '#FA8072', '#87CEEB',
]
# myCmp20 = ListedColormap(colors, "myCmp20")

from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap


cdict = {
    'red':   [(0.0, 1, 0.95), (1.0, 1.0, 1.0)],
    'green': [(0.0, 1, 0.95), (1.0, 0.0, 0.0)],
    'blue':  [(0.0, 1, 0.95), (1.0, 0.0, 0.0)]
}

# Create the colormap
myCmpGra = LinearSegmentedColormap('GrayToRed', cdict)
newColors = myCmpGra(np.linspace(0, 0.75, 256))
Greys = cm.get_cmap('Greys_r', 256)
# Greys = cm.get_cmap('Greys', 256)
newColors[:15, :] = Greys(np.linspace(0.8125, 0.8725, 15))
pos_cmap = colors.ListedColormap(newColors)
# pos_cmap = colors.ListedColormap("myCmpGra", newColors)
plt.register_cmap(name='myCmpGra', cmap=pos_cmap)

pos_cmap_dash = []
order_i = 0
n_split = 50
for i in pos_cmap(np.linspace(0, 1, n_split)):
    st = 'rgba('+str(i[0])+','+str(i[1])+','+str(i[2])+','+str(i[3])+')'
    pos_cmap_dash.append([order_i/(n_split-1), st])
    order_i = order_i + 1

