import pandas as pd
import streamlit as st
from concurrent.futures import ThreadPoolExecutor
import plotly.express as px
from datetime import datetime
from ImportDataFromApi import getData
from ImportDataTuCambista import getExchangeTuCambista

# Ejecutar la operación costosa en segundo plano
#executor = ThreadPoolExecutor(2)

# Mostrar Tipo Cambio TuCambista
#url = 'https://tucambista.pe/'

#future = executor.submit(getExchangeTuCambista,url)

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
defaultMonthSelected = nameMonths[currentMonth]

yearSelected = st.selectbox('Selecciona un año:', sorted(years), index=list(years).index(currentYear))
monthsNameSelected = st.multiselect('Selecciona meses:', nameMonthsFiltred, default=defaultMonthSelected)
monthsSelected = [list(nameMonths.keys())[list(nameMonths.values()).index(m)] for m in monthsNameSelected]

# Filtrar el DataFrame según los filtros seleccionados
df_filtrado = df[(df['Año'] == yearSelected) & (df['Mes'].isin(monthsSelected))]

# Crear el gráfico de líneas
fig = px.line(df_filtrado, x='Fecha', y='Venta', title='Tipo Cambio USD', labels={'Fecha':'Fecha','Venta':'Exchange'}, markers=True, hover_name='Venta', hover_data={'Venta':False, 'Fecha':True})

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

#st.markdown(exchangeTuCambista)

col1, col2 = st.columns(2)

#card_tuCambista = """
#<div style="background-color: #FFEB3B; padding: 5px; border-radius: 10px; text-align: center;">
#    <iframe src="https://tucambista.pe/tipo-de-cambio?igu=1" frameborder=0>$TuCambista</iframe>
#</div>
#"""

card_tuCambista = """
<div style="background-color: #FFEB3B; padding: 5px; border-radius: 10px; text-align: center;">
    <h3 style="color: black; padding: 5px;">$TuCambista</h3>
    <p style="color: black; font-size: 20px; padding: 5px; margin: 0px;">loading...</p>
</div>
"""

# Tipo Cambio SBS al dia de Hoy
lastValue = df['Venta'].iloc[-1]

card_SBS = f"""
<div style="background-color: #2196F3; padding: 5px; border-radius: 10px; text-align: center;">
    <h3 style="color: black; padding: 5px;">SBS</h3>
    <p style="color: black; font-size: 20px; padding: 5px; margin: 0px;">$ {lastValue}</p>
</div>
"""
with col1:
    card_tuCambista_placeholder = st.empty()
    card_tuCambista_placeholder.markdown(card_tuCambista, unsafe_allow_html=True)

with col2:
    st.markdown(card_SBS, unsafe_allow_html=True)


# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

#Firma
st.markdown("Developed by Andy Cruz")

# Mostrar el resultado de la operación costosa una vez completada
exchangeTuCambista = "$ 3.736"
#exchangeTuCambista = "$ " + str(future.result())

card_tuCambista = f"""
<div style="background-color: #FFEB3B; padding: 5px; border-radius: 10px; text-align: center;">
   <h3 style="color: black; padding: 5px;">$TuCambista</h3>
    <p style="color: black; font-size: 20px; padding: 5px; margin: 0px;">{exchangeTuCambista}</p>
</div>
"""

# Actualizamos el card de TuCambista
with col1:
    card_tuCambista_placeholder.markdown(card_tuCambista, unsafe_allow_html=True)


#st.caption("Developed by Andy Cruz")
#.\venv\Scripts\activate
#streamlit run Dashboard.py