# -*- coding: utf-8 -*-

"""
Multiple Correspondence Analysis (MCA)

"""
# Load packages
# Install required packages: pip install -r requirements.txt

import pandas as pd
import prince
from scipy.stats import chi2_contingency

# Multiple Correspondence Analysis (MCA)

# Import dataset
## Font: Fávero e Belfiore (2017, Capítulo 11)

perfil_mca = pd.read_excel("perfil_de_aplicação_civil.xlsx")

print(perfil_mca)

# Selecting only one variable for analysis

perfil_mca_select = perfil_mca.drop(columns=['estudante'])

print(perfil_mca_select)

# Analyzing the contingency tables

tabela_mca_1 = pd.crosstab(perfil_mca["perfil"], perfil_mca["aplicacao"])
tabela_mca_2 = pd.crosstab(perfil_mca["perfil"], perfil_mca["estado_civil"])
tabela_mca_3 = pd.crosstab(perfil_mca["aplicacao"], perfil_mca["estado_civil"])

print(tabela_mca_1)

print(tabela_mca_2)

print(tabela_mca_3)

# Analyzing the statistical significance of the association (chi² test)

chi2, pvalor, df, freq_esp = chi2_contingency(tabela_mca_1)

print("Association 1")
print(f"Chi^2 Statistics: {chi2}") # Chi^2 Statistics
print(f"P-Value of the Statistics: {pvalor}") # P-Value of the Statistics
print(f"Degrees of Freedom: {df}") # Degrees of Freedom

chi2, pvalor, df, freq_esp = chi2_contingency(tabela_mca_2)

print("Associação 2")
print(f"Chi^2 Statistics: {chi2}") # Chi^2 Statistics
print(f"P-Value of the Statistics: {pvalor}") # P-Value of the Statistics
print(f"Degrees of Freedom: {df}") # Degrees of Freedom

chi2, pvalor, df, freq_esp = chi2_contingency(tabela_mca_3)

print("Associação 3")
print(f"Chi^2 Statistics: {chi2}") # Chi^2 Statistics
print(f"P-Value of the Statistics: {pvalor}") # P-Value of the Statistics
print(f"Degrees of Freedom: {df}") # Degrees of Freedom

# Elaborating the MCA

# Uses Burt matrix method

mca = prince.MCA()
mca = mca.fit(perfil_mca_select)

# Obtaining the coordinates of the variables in the two dimensions of the map

print(mca.column_coordinates(perfil_mca_select))

# Obtaining the coordinates of each of the observations

print(mca.row_coordinates(perfil_mca_select))

# Obtaining the eigenvalues

print(mca.eigenvalues_)

# Principal total inertia

print(mca.total_inertia_)

# Obtaining the variance

print(mca.explained_inertia_)

# Plotting the perceptual map

mp_mca = mca.plot_coordinates(
             X = perfil_mca_select,
             figsize=(12,12),
             show_row_points = True,
             show_column_points = True,
             show_row_labels=False,
             column_points_size = 100,
             show_column_labels = True,
             legend_n_cols = 2)

# Plotting the interative perceptual map

import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default='browser'

chart_df = pd.DataFrame({'obs_x':mca.row_coordinates(perfil_mca_select)[0],
                         'estudante':perfil['Estudante'],
                         'obs_y': mca.row_coordinates(perfil_mca_select)[1]})

fig = go.Figure(data=go.Scatter(x=chart_df['obs_x'],
                                y=chart_df['obs_y'],
                                mode='markers',
                                name="Estudante",
                                text=chart_df['estudante']))

fig.add_trace(go.Scatter(
    x=mca.column_coordinates(perfil_mca_select)[0],
    mode='markers+text',
    name="Association",
    marker={'size':12},
    y=mca.column_coordinates(perfil_mca_select)[1],
    textposition="top center",
    text=mca.column_coordinates(perfil_mca_select).index
))

fig.update_layout(
    autosize=False,
    width=800,
    height=800,
    title_text='Rows and Columns Coordinates'
)

fig.show()