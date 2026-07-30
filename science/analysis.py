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

# Number of articles per country between 1996-2018
plt.figure(figsize=(40,40))
data_publications_low = pd.read_csv('data/publications-low.csv')
plt.style.use('seaborn-darkgrid')
my_dpi = 96
plt.figure(figsize=(800 / my_dpi, 800 / my_dpi), dpi=my_dpi)

countries = data_publications_low['Country'].unique()
for country in countries:
     years = data_publications_low.query('Country == @country')['Year'].tolist()
     manuscripts = np.log10(data_publications_low.query('Country == @country')['Citable documents'].tolist())
     if country != 'Cuba':
          plt.plot(years, manuscripts, marker='', color='grey', linewidth=1, alpha=0.4)
          if country in ['Venezuela', 'Puerto Rico', 'Iran', 'Chile', 'Colombia', 'Cyprus', 'Peru', 'Viet Nam', 'Ecuador', 'Croatia', 'Indonesia', 'Philippines', 'Uruguay', 'Thailand']:
               plt.text(2018, manuscripts[-1], country, horizontalalignment='left', size='small', color='grey', fontsize=5)
     else:
          plt.plot(years, manuscripts, marker='', color='red', linewidth=4, alpha=0.7)
          plt.text(2017, manuscripts[-2], country, horizontalalignment='left', size='small', color='red')

# Add titles
plt.title("Number of publications by Country (1996-2018)", loc='center', fontsize=12, fontweight=0, color='black')
plt.xlabel("Year")
plt.ylabel("Log10 of number of publications")

plt.savefig("images/publication-low-1996.svg", format="svg")



# Number of citations per country between 1996-2018
plt.figure(figsize=(40,40))
plt.style.use('seaborn-darkgrid')
my_dpi = 96
plt.figure(figsize=(800 / my_dpi, 800 / my_dpi), dpi=my_dpi)

data_publications_low = data_publications_low.query('Year < 2010')
countries = data_publications_low['Country'].unique()
for country in countries:
     years = data_publications_low.query('Country == @country')['Year'].tolist()
     manuscripts = np.log10(data_publications_low.query('Country == @country')['Citations per document'].tolist())
     if country != 'Cuba':
          plt.plot(years, manuscripts, marker='', color='grey', linewidth=1, alpha=0.4)
          if country in ['Venezuela', 'Puerto Rico', 'Iran', 'Chile', 'Colombia', 'Cyprus', 'Peru', 'Viet Nam', 'Ecuador', 'Croatia', 'Philippines', 'Uruguay']:
               plt.text(2009, manuscripts[-1], country, horizontalalignment='left', size='small', color='grey', fontsize=5)
     else:
          plt.plot(years, manuscripts, marker='', color='red', linewidth=4, alpha=0.7)
          plt.text(2006, manuscripts[-2], country, horizontalalignment='left', size='small', color='red')

# Add titles
plt.title("Number of citations per publication by Country (1996-2018)", loc='center', fontsize=12, fontweight=0, color='black')
plt.xlabel("Year")
plt.ylabel("Log10 of number of citations")

plt.savefig("images/citations-perdocument-low-1996.svg", format="svg")

"""
Number of articles per country between 1996-2018
"""
plt.figure(figsize=(40,40))
data_publications_high = pd.read_csv('data/publications-high.csv')

plt.style.use('seaborn-darkgrid')
my_dpi = 96
plt.figure(figsize=(800 / my_dpi, 800 / my_dpi), dpi=my_dpi)

countries = data_publications_high['Country'].unique()
count = 0
ycount = 0
for country in countries:
     years = data_publications_high.query('Country == @country')['Year'].tolist()
     manuscripts = np.log10(data_publications_high.query('Country == @country')['Citable documents'].tolist())
     if country != 'Cuba':
          plt.plot(years, manuscripts, marker='', color='grey', linewidth=1, alpha=0.4)
          if country in ['United Kingdom', 'Germany', 'India', 'Spain', 'Japan', 'New Zealand', 'Russian Federation', 'South Korea', 'France', 'Poland', 'Sweden','Belgium', 'Finland', 'Norway', 'Netherlands']:
                plt.text(2018, manuscripts[-1], country, horizontalalignment='left', size='small', color='grey', fontsize=5)
     if country in ['China', 'United States', 'Brazil']:
          plt.plot(years, manuscripts, marker='', color='blue', linewidth=4, alpha=0.7)
          plt.text(2018-count, manuscripts[-3], country, horizontalalignment='left', fontsize=15, color='blue')
          count += 10
          ycount += 2

# Add titles
plt.title("Number of publications by Country (1996-2018)", loc='center', fontsize=12, fontweight=0, color='black')
plt.xlabel("Year")
plt.ylabel("Log10 of number of publications")

plt.savefig("images/publication-high-1996.svg", format="svg")


"""
Number of articles per country between 1996-2018
"""
plt.figure(figsize=(40,40))
data_publications_high = pd.read_csv('data/publications-high.csv')
data_publications_high = data_publications_high.query('Year < 2010')
plt.style.use('seaborn-darkgrid')
my_dpi = 96
plt.figure(figsize=(800 / my_dpi, 800 / my_dpi), dpi=my_dpi)

countries = data_publications_high['Country'].unique()
count = 0
ycount = 0
for country in countries:
     years = data_publications_high.query('Country == @country')['Year'].tolist()
     manuscripts = np.log10(data_publications_high.query('Country == @country')['Citations per document'].tolist())
     if country != 'Cuba':
          plt.plot(years, manuscripts, marker='', color='grey', linewidth=1, alpha=0.4)
          if country in ['United Kingdom', 'Germany', 'India', 'Spain', 'Japan', 'New Zealand', 'Russian Federation', 'South Korea', 'France', 'Poland', 'Sweden','Belgium', 'Finland', 'Norway', 'Netherlands']:
                plt.text(2009, manuscripts[-1], country, horizontalalignment='left', size='small', color='grey', fontsize=5)
     if country ==  'China':
          plt.plot(years, manuscripts, marker='', color='blue', linewidth=4, alpha=0.7)
          plt.text(2009, manuscripts[-1], country, horizontalalignment='left', fontsize=15, color='blue')
     if country == 'United States':
          plt.plot(years, manuscripts, marker='', color='blue', linewidth=4, alpha=0.7)
          plt.text(2004, manuscripts[-1], country, horizontalalignment='left', fontsize=15, color='blue')
     if country == 'Brazil':
          plt.plot(years, manuscripts, marker='', color='blue', linewidth=4, alpha=0.7)
          plt.text(2006, manuscripts[-1], country, horizontalalignment='left', fontsize=15, color='blue')

# Add titles
plt.title("Number of citations per publication by Country (1996-2018)", loc='center', fontsize=12, fontweight=0, color='black')
plt.xlabel("Year")
plt.ylabel("Log10 of number of citations")

plt.savefig("images/citations-perdocument-high-1996.svg", format="svg")


"""
Number of publications per institution
"""
# ------- PART 1: Create background
fig, ax = plt.subplots()
def change_width(ax, new_value) :
    for patch in ax.patches :
        current_width = patch.get_width()
        diff = current_width - new_value

        # we change the bar width
        patch.set_width(new_value)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)

# number of variable
fig = plt.gcf()
fig.set_size_inches(200, 10)
publications_institutes = pd.read_csv('data/centers-publications-province.csv')
sns.set(font_scale=0.7)
g = sns.FacetGrid(publications_institutes, hue="City", palette="Set1", height=4.5, aspect=2.5)
g= (g.map(plt.scatter, "Instituto", "Articulos")
    .set_axis_labels("Country)", "Number of publications"))
g.add_legend()
for ax in g.axes.flat:
    for label in ax.get_xticklabels():
        label.set_rotation(25)
        label.set_fontsize(5)

plt.savefig("images/institutes.svg", format="svg")


