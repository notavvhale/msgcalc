# visualization.py
# Построение графиков сравнения маршрутов

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def create_comparison_chart(results):
    """Создание сравнительной диаграммы стоимости и сроков"""
    df = pd.DataFrame(results)

    fig = go.Figure()

    # Добавляем столбцы стоимости
    fig.add_trace(go.Bar(
        name='Стоимость (USD)',
        x=df['Маршрут'],
        y=df['Стоимость'],
        marker_color='steelblue',
        text=df['Стоимость'].apply(lambda x: f'${x:,.2f}'),
        textposition='outside'
    ))

    # Добавляем линию сроков
    fig.add_trace(go.Scatter(
        name='Срок (дней)',
        x=df['Маршрут'],
        y=df['Срок'],
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='red', width=3),
        marker=dict(size=12)
    ))

    fig.update_layout(
        title='Сравнение маршрутов доставки: стоимость и сроки',
        xaxis_title='Вид перевозки',
        yaxis_title='Стоимость (USD)',
        yaxis2=dict(
            title='Срок доставки (дней)',
            overlaying='y',
            side='right'
        ),
        template='plotly_white',
        height=500
    )

    return fig

def create_pie_chart(customs_data):
    """Круговая диаграмма структуры таможенных платежей"""
    labels = ['Пошлина', 'НДС', 'Таможенный сбор']
    values = [customs_data['duty'], customs_data['vat'], customs_data['fee']]

    fig = px.pie(
        names=labels,
        values=values,
        title='Структура таможенных платежей',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_traces(textposition='inside', textinfo='percent+label+value')
    return fig