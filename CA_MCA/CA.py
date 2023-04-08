# -*- coding: utf-8 -*-

"""
Correspondence Analysis (CA)

"""
# Load packages
# Install required packages: pip install -r requirements.txt

import pandas as pd
import prince
from scipy.stats import chi2_contingency

# Correspondence Analysis (CA)

# Import dataset
# Font: Fávero e Belfiore (2017, Chapter 11)

perfil = pd.read_excel("perfil_de_aplicação.xlsx")

print(perfil)

# Analyzing the dataset

print(perfil.info())

# Analyzing the descriptive characteristics of the variables in the dataset

print(perfil.describe())

# Creating the contingency table

tabela = pd.crosstab(perfil["Perfil"], perfil["Tipo de Aplicação"])

print(tabela)

# Analyzing the statistical significance of the association (chi² test)

chi2, pvalor, df, freq_esp = chi2_contingency(tabela)

print(f"Chi^2 Statistics: {chi2}") # Chi^2 Statistics
print(f"P-Value of the Statistics: {pvalor}") # P-Value of the Statistics
print(f"Degrees of Freedom: {df}") # Degrees of Freedom

# Elaborating the CA

# Initializing the Anacor instance

ca = prince.CA()

# Dataframe settings

# Renaming the rows and columns of the dataframe

tabela.columns.rename('Investiment', inplace=True)
tabela.index.rename('Profile', inplace=True)

print(tabela)

# Fitting the model

ca = ca.fit(tabela)

# Obtaining the coordinates in line and column

print(ca.row_coordinates(tabela), "\n")
print(ca.column_coordinates(tabela))

# Obtaining the eigenvalues

print(ca.eigenvalues_)

# Obtaining the total principal inertia

# Greater the total principal inertia, greater the association between categories

print(ca.total_inertia_)

# Obtaining the inertia explained by dimension

# Indicates the percentage of total principal inertia explained by each dimension

print(ca.explained_inertia_)

# Masses in lines

print(ca.row_masses_)

# Masses in columns

print(ca.col_masses_)

# Plot the perceptual map

ax = ca.plot_coordinates(X=tabela,
                         ax=None,
                         figsize=(10,10),
                         x_component=0,
                         y_component=1,
                         show_row_labels=True,
                         show_col_labels=True)

# Plot interactive perceptual map

import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default='browser'

chart_df = pd.DataFrame({'obs_x':ca.row_coordinates(tabela)[0].values,
                         'obs_y': ca.row_coordinates(tabela)[1].values})

fig = go.Figure(data=go.Scatter(x=chart_df['obs_x'],
                                y=chart_df['obs_y'],
                                name=tabela.index.name,
                                textposition="top center",
                                text=tabela.index,
                                mode="markers+text",))

fig.add_trace(go.Scatter(
    x=ca.column_coordinates(tabela)[0].values,
    mode="markers+text",
    name=tabela.columns.name,
    textposition="top center",
    y=ca.column_coordinates(tabela)[1].values,
    text=ca.column_coordinates(tabela).index
))

fig.update_layout(
    autosize=False,
    width=800,
    height=800,
    title_text='Principal Coordinates'

)

fig.show()