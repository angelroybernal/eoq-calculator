"""
Calculadora de EOQ
"""

import math

import altair as alt
import pandas as pd
import streamlit as st

def calc_order_size(year_demand, order_cost, unit_storage_cost):
    """
    Calcula el tamaño del lote para las ordenes.
    """
    order_size = math.ceil(
        math.sqrt(
            (2 * year_demand * order_cost)/unit_storage_cost
        )
    )
    return order_size

def calc_reorder_point(year_demand, order_delay):
    """
    Calcula el punto de reorden.
    """
    day_demand = year_demand / 365
    reorder_point = math.ceil(day_demand * order_delay)
    return day_demand, reorder_point

def calc_order_lifetime(day_demand, order_size):
    """
    Calcula el tiempo de vida de la orden.
    """
    lifetime = math.ceil(order_size / day_demand)
    return lifetime

def calc_inventory_forecast(
    forecast_size,
    order_size,
    order_lifetime
    ):
    """
    Calcula la proyeccion del inventario.
    """
    period = [0, order_lifetime]
    while period[-1] < forecast_size:
        period.append(period[-1])
        period.append(period[-1]+order_lifetime)
    inventory = [order_size, 0]
    while len(inventory) < len(period):
        inventory.append(order_size)
        inventory.append(0)
    forecast = pd.DataFrame(
        {
            'days': period,
            'inventory': inventory
        }
    )
    return forecast

def chart_inventory_forecast(forecast):
    """
    Grafica de proyeccion del inventario.
    """
    chart = alt.Chart(forecast).mark_line().encode(
        x='days',
        y='inventory'
    )
    return chart

def chart_rop(
    reorder_point,
    order_delay,
    order_lifetime
    ):
    """
    Grafica de primer punto de reorden
    """
    when_order = order_lifetime - order_delay
    source = pd.DataFrame({
        'days': [when_order],
        'inventory': [reorder_point],
        'label': ['ROP']
    })
    rop = alt.Chart(source).mark_circle(color="black").encode(
        alt.X('days'), alt.Y('inventory')
    )

    text = rop.mark_text(
        align='left',
        baseline='middle',
        dx=7
    ).encode(
        text='label'
    )
    return rop + text

def main():
    """
    Funcion principal de la aplicacion.
    """
    st.title('Calculadora de EOQ')

    st.markdown(
        '''
        Según el módelo de EOQ, el tamaño óptimo de un pedido a realizar
        minimizando los costos totales,
        está determinado por:
        '''
    )
    st.latex('Q^{*} = \\sqrt{\\frac{2DS}{H}}')
    st.markdown(
        '''
        Donde:
        - *D* : La demanda en unidades por año
        - *S* : El costo de emitir una orden
        - *H* : El costo asociado a mantener una unidad en inventario en un año
        '''
    )

    st.markdown(
        '''
        Adicionalmente, el punto de reorden que representa la cantidad en
        inventario al momento en que debemos realizar el siguiente pedido,
        está determinado por:
        '''
    )
    st.latex('ROP = dL')
    st.markdown(
        '''
        Donde:
        - *d* : La demanda en unidades por día
        - *L* : El tiempo de espera para recibir el pedido
        '''
    )

    st.markdown('Ingrese los datos necesarios para calcular la cantidad economica de pedido.')

    year_demand = st.number_input(
        label='Demanda (Unidades por año):',
        min_value=0.0,
        max_value=float('1.797e+308'),
        step=1.0
        )
    order_cost = st.number_input(label='Costo de la orden ($):',
        min_value=0.0,
        max_value=float('1.797e+308'),
        step=1.0
        )
    unit_storage_cost = st.number_input(label='Costo de almacenamiento ($ por unidad):',
        min_value=0.0,
        max_value=float('1.797e+308'),
        step=1.0
        )
    order_delay = st.number_input(label='Tiempo de espera (días):',
        min_value=0.0,
        max_value=float('1.797e+308'),
        step=1.0
        )
    forecast_size = st.number_input(label='Tamaño de la proyección (días):',
        min_value=0.0,
        max_value=float('1.797e+308'),
        value=180.0,
        step=1.0
        )
    if st.button('Calcular'):
        order_size = calc_order_size(
            year_demand,
            order_cost,
            unit_storage_cost
        )
        day_demand, reorder_point = calc_reorder_point(
            year_demand,
            order_delay
        )
        order_lifetime = calc_order_lifetime(
            day_demand,
            order_size
        )
        st.markdown(
            '''
            El tamaño óptimo de pedido que minimiza los costos totales es **%s unidades**.
            Adicionalmente:
            \n- Cada vez que el inventario llega a **%s unidades** se emite
            un nuevo pedido por %s unidades.
            \n- El inventario llega a 0 cada **%s días** aproximadamente.
            '''
            % (order_size, reorder_point, order_size, order_lifetime)
        )
        forecast = calc_inventory_forecast(
            forecast_size,
            order_size,
            order_lifetime
            )
        forecast_chart = chart_inventory_forecast(forecast)
        rop_chart = chart_rop(reorder_point, order_delay, order_lifetime)
        inventory_chart = alt.layer(forecast_chart, rop_chart)
        st.altair_chart(inventory_chart, use_container_width=True)

if __name__ == '__main__':
    main()
