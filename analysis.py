import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

data_publications = pd.read_csv('data/country-latin-papers.csv')
sorted = data_publications.sort_values("Articulos", ascending=False)
custom_palette = sns.color_palette("Paired", 9)
sns.palplot(custom_palette)
sns.set(font_scale=1.7)

## Figure - Number articles by country
plt.figure(figsize=(30,20))
plt.box(on=None)

ax = sns.barplot(x="Pais", y="Articulos", data=data_publications, color=sns.xkcd_rgb["greyblue"], order=sorted["Pais"])
ax.set_xlabel('Country',fontsize=20)
ax.set_ylabel('Number of manuscripts',fontsize=20)
ax.yaxis.set_major_formatter(ticker.EngFormatter())

plt.title('Number of manuscripts published in Latin American countries (1970-2018)', fontsize=50)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
plt.savefig("images/manuscripts-author.svg", format="svg")

data_publications['ratio'] = (data_publications['Articulos']/data_publications['Habitantes'])*100
sorted = data_publications.sort_values("ratio", ascending=False)
plt.figure(figsize=(30,20))
plt.box(on=None)

ax = sns.barplot(x="Pais", y="ratio", data=data_publications.sort_index(), color=sns.xkcd_rgb["greyblue"], order=sorted["Pais"])
ax.set_xlabel('Country',fontsize=20)
ax.set_ylabel('Number of manuscripts normalized by population',fontsize=20)

plt.title('Number of manuscripts published in Latin American countries (1970-2018)', fontsize=50)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
plt.savefig("images/manuscripts-author-population.svg", format="svg")