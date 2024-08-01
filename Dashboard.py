import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
from ImportDataFromApi import getDataUSD
from ImportDataFromSBS import getDataEUR
from ImportDataTuCambista import getExchangeTuCambista


# Obtener el año y mes actual
currentYear = datetime.now().year
currentMonth = datetime.now().month
lastMonth = currentMonth - 1

dfUSD = getDataUSD(currentYear, currentMonth)
dfEUR = getDataEUR(currentYear, currentMonth)

# Convertir la columna Fecha a formato datetime
dfUSD['Fecha'] = pd.to_datetime(dfUSD['Fecha'])
dfEUR['Fecha'] = pd.to_datetime(dfEUR['Fecha'])

# Concatenamos los Df
df = pd.concat([dfUSD, dfEUR], ignore_index=True)

# Agregar columnas de Año y Mes
df['Año'] = df['Fecha'].dt.year
df['Mes'] = df['Fecha'].dt.month

# Diccionario de nombres de meses
nameMonths = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

# Título del dashboard
st.title('Tipo Cambio SBS Venta')

# Filtros de año, mes y moneda
years = df['Año'].unique()
months = df['Mes'].unique()
nameMonthsFiltred = [nameMonths[m] for m in months]
currency = df['Moneda'].unique()

# Definir los valores predeterminados para los filtros
#defaultMonthsSelected = [nameMonths[currentMonth], nameMonths[lastMonth]]
defaultMonthSelected = nameMonths[currentMonth]

yearSelected = st.selectbox('Selecciona un año:', sorted(years), index=list(years).index(currentYear))
monthsNameSelected = st.multiselect('Selecciona meses:', nameMonthsFiltred, default=defaultMonthSelected)
monthsSelected = [list(nameMonths.keys())[list(nameMonths.values()).index(m)] for m in monthsNameSelected]

# Moneda
currencySelected = st.radio('Moneda:', options=currency, index=0)

# Filtrar el DataFrame según los filtros seleccionados
df_filtrado = df[(df['Año'] == yearSelected) & (df['Mes'].isin(monthsSelected)) & (df['Moneda'] == currencySelected)]

# Crear el gráfico de líneas
fig = px.line(df_filtrado, x='Fecha', y='Venta', title=f'Tipo Cambio {currencySelected}', labels={'Fecha':'Fecha','Venta':'Exchange'}, markers=True, hover_name='Venta', hover_data={'Venta':False, 'Fecha':True})

if not df_filtrado.empty:
    # Ultimo día
    lastDate = df_filtrado['Fecha'].iloc[-1]
    lastValue = df_filtrado['Venta'].iloc[-1]

    # Agregar anotacion
    fig.add_annotation(
        x=lastDate,
        y=lastValue,
        text=lastValue,
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-30,
        font=dict(
            color="black",
            size=12
        ),
        bgcolor="white"
    )

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

col1, col2 = st.columns(2)

exchangeTuCambista = getExchangeTuCambista()['Venta']


card_tuCambista = f"""
<div style="background-color: #FFF078; padding: 5px; border-radius: 10px; text-align: center;">
   <h3 style="color: #0F0F0F; padding: 5px;">$TuCambista</h3>
    <p style="color: black; font-size: 20px; padding: 5px; margin: 0px;">Hoy: $ {exchangeTuCambista}</p>
</div>
"""

#  Ultimo valor Venta SBS
lastValue = df[df['Moneda'] == currencySelected]['Venta'].iloc[-1]

card_SBS = f"""
<div style="background-color: #6EACDA; padding: 5px; border-radius: 10px; text-align: center;">
    <h3 style="color: #0F0F0F; padding: 5px;">SBS</h3>
    <p style="color: black; font-size: 20px; padding: 5px; margin: 0px;">Hoy: $ {lastValue}</p>
</div>
"""
with col1:
    st.markdown(card_tuCambista, unsafe_allow_html=True)

with col2:
    st.markdown(card_SBS, unsafe_allow_html=True)


# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

#Firma
st.markdown("Developed by Andy Cruz")


#st.caption("Developed by Andy Cruz")
#.\venv\Scripts\activate
#streamlit run Dashboard.py