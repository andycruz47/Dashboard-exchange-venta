import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
from ImportDataFromApi import getData

# Obtener el año y mes actual
currentYear = datetime.now().year
currentMonth = datetime.now().month
lastMonth = currentMonth - 1

#df = pd.read_csv('exchangeHistory.csv')
df = getData(currentYear, currentMonth, lastMonth)

# Convertir la columna Fecha a formato datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Agregar columnas de Año y Mes
df['Año'] = df['Fecha'].dt.year
df['Mes'] = df['Fecha'].dt.month

# Diccionario de nombres de meses
nameMonths = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

# Título del dashboard
st.title('Tipo Cambio SBS USD Venta')

# Filtros de año y mes
years = df['Año'].unique()
months = df['Mes'].unique()
nameMonthsFiltred = [nameMonths[m] for m in months]

# Definir los valores predeterminados para los filtros
#defaultMonthsSelected = [nameMonths[currentMonth], nameMonths[lastMonth]]
defaultMonthsSelected = [nameMonths[currentMonth]]

yearSelected = st.selectbox('Selecciona un año:', sorted(years), index=list(years).index(currentYear))
monthsNameSelected = st.multiselect('Selecciona meses:', nameMonthsFiltred, default=defaultMonthsSelected)
monthsSelected = [list(nameMonths.keys())[list(nameMonths.values()).index(m)] for m in monthsNameSelected]

# Filtrar el DataFrame según los filtros seleccionados
df_filtrado = df[(df['Año'] == yearSelected) & (df['Mes'].isin(monthsSelected))]

# Crear el gráfico de líneas
fig = px.line(df_filtrado, x='Fecha', y='Venta', title='Tipo Cambio USD', labels={'Fecha':'Fecha','Venta':'Exchange'}, markers=True, text='Venta', hover_data={'Fecha':True, 'Venta':False})

# Customizar el gráfico con un tema claro
fig.update_layout(
    template='plotly_white',
    title_font=dict(size=20, family="Arial"),
    font=dict(size=10, color='black'),
    xaxis=dict(title=None, tickfont=dict(color='black')),
    yaxis=dict(title=None, tickfont=dict(color='black')),
    hoverlabel=dict(font_color='black')
)

# Agregar etiqueta de datos
fig.update_traces(textposition='top center')


# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

#Firma
st.markdown("Developed by Andy Cruz")

#st.caption("Developed by Andy Cruz")
#.\venv\Scripts\activate
#streamlit run Dashboard.py