import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Análise de anúncios de veículos')

# Carregar os dados
car_data = pd.read_csv('vehicles.csv')

# Remover linhas com dados essenciais ausentes
car_data = car_data.dropna(subset=['model_year', 'fuel', 'model', 'type', 'condition', 'price'])

# Criar coluna 'manufacturer' extraída da primeira palavra do campo 'model'
car_data['manufacturer'] = car_data['model'].apply(lambda x: x.split()[0] if isinstance(x, str) else 'unknown')

# --- SEÇÃO 1: Data Viewer + filtro de fabricantes ---
st.subheader("Tipos de veículos por fabricante")

# Contagem de anúncios por fabricante
manufacturer_counts = car_data['manufacturer'].value_counts()

# Checkbox para incluir ou não fabricantes pequenos
include_small = st.checkbox('Include manufacturers with less than 1000 ads', value=True)

if include_small:
    data_for_plot = car_data.copy()
else:
    # Filtra apenas fabricantes com 1000 ou mais anúncios
    big_manufacturers = manufacturer_counts[manufacturer_counts >= 1000].index
    data_for_plot = car_data[car_data['manufacturer'].isin(big_manufacturers)].copy()

# Mostrar tabela com os dados filtrados
st.dataframe(data_for_plot)

# --- SEÇÃO 2: Gráfico de tipos de veículos por fabricante ---
fig1 = px.histogram(
    data_for_plot,
    x='manufacturer',
    color='type',
    title='Vehicle types by manufacturer',
    labels={'manufacturer': 'Fabricante', 'count': 'Quantidade', 'type': 'Tipo de veículo'},
    barmode='stack',
    height=500
)
st.plotly_chart(fig1)

# --- SEÇÃO 3: Histograma de condição vs ano do modelo ---
st.subheader("Histogram of condition vs model_year")

fig2 = px.histogram(
    car_data,
    x='model_year',
    color='condition',
    title='Histogram of condition vs model_year',
    labels={'model_year': 'Ano do modelo', 'count': 'Quantidade', 'condition': 'Condição'},
    barmode='stack',
    height=500
)
st.plotly_chart(fig2)

# --- SEÇÃO 4: Comparar distribuição de preço entre fabricantes ---
st.subheader("Compare price distribution between manufacturers")

manufacturers = car_data['manufacturer'].unique().tolist()
manufacturer1 = st.selectbox("Select manufacturer 1", manufacturers, index=manufacturers.index("chevrolet") if "chevrolet" in manufacturers else 0)
manufacturer2 = st.selectbox("Select manufacturer 2", manufacturers, index=manufacturers.index("bmw") if "bmw" in manufacturers else 1)

normalize = st.checkbox("Normalize histogram (percent)", value=True)

# Filtrar dados dos dois fabricantes
price_data = car_data[car_data['manufacturer'].isin([manufacturer1, manufacturer2])]

# Criar histograma
fig3 = px.histogram(
    price_data,
    x='price',
    color='manufacturer',
    barmode='overlay',
    histnorm='percent' if normalize else None,
    title=f"Price distribution: {manufacturer1} vs {manufacturer2}",
    labels={'price': 'Preço', 'count': 'Quantidade (%)' if normalize else 'Quantidade', 'manufacturer': 'Fabricante'},
    nbins=50
)
st.plotly_chart(fig3)
