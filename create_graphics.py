import pandas as pd
import plotly.graph_objects as go
import scipy
import numpy as np

def create_line_fig(chosen_segment, theme_status):
    dynamics_data_link = 'https://docs.google.com/spreadsheets/d/e/' \
                         '2PACX-1vRAEk-aa_OeTJF3cJNK5HWXj4J4j3Ipix8' \
                         'MGImNyYlsWY9xG6RFVYAPcVKo_17avMq_u1O02Bjg' \
                         'V5bK/pub?gid=1064497805&single=true&output=csv'
    dynamics_data = pd.read_csv(dynamics_data_link)
    lines_fig = go.Figure()
    fig_new = go.Scatter(x=dynamics_data.query("city == @chosen_segment")['Даты'],
                        y=dynamics_data.query("city == @chosen_segment")['Квартиры в новостройке, за м2, руб.'],
                        mode='lines+markers+text',
                        # marker=dict(size=5),
                        name='Первичное',
                        text=dynamics_data.query("city == @chosen_segment")['Изменение'])
    fig_secondary = go.Scatter(x=dynamics_data.query("city == @chosen_segment")['Даты'],
                        y=dynamics_data.query("city == @chosen_segment")['Квартиры вторичка, за м2, руб.'],
                        mode='lines+markers+text',
                        # marker=dict(size=5),
                        name='Вторичное',
                        text=dynamics_data.query("city == @chosen_segment")['Изменение.1'])
    lines_fig.add_trace(fig_new)
    lines_fig.add_trace(fig_secondary)
    lines_fig.update_traces(textposition="bottom center",
                            textfont_size=8)
    if theme_status == 'dark':
        paper_bgcolor = 'rgb(51, 51, 51)'
        plot_bgcolor = 'rgb(51, 51, 51)'
        title_font_color = 'white'
        font_color = "white"
    else:
        paper_bgcolor = 'rgb(255, 255, 255)'
        plot_bgcolor = 'rgb(255, 255, 255)'
        title_font_color = 'black'
        font_color = "black"
    lines_fig.update_layout(xaxis_tickangle=45,
                            legend=dict(x=0.5,y=1.25, xanchor="center", yanchor='top', orientation="h"),
                            paper_bgcolor=paper_bgcolor,
                            plot_bgcolor=plot_bgcolor,
                            title_font_color=title_font_color,
                            font_color=font_color,
                            yaxis=dict(
                                title='Средняя стоимость квадратного метра',
                                gridcolor='grey',
                                gridwidth=1,
                            ),
                            xaxis=dict(
                                gridcolor='grey',
                                gridwidth=1,
                            )
                            )
    return lines_fig

link_data_bubbles = 'https://docs.google.com/spreadsheets/d/e/' \
                        '2PACX-1vTQk2hwcxS74FiRZaXHcqnXZ4pqt9S7tbPXuuAtNpqes4AmQdu' \
                        'EBsFVB-O0zTx6t6wHOe8y8OBdN_qr/pub?gid=1962707013&single=true&output=csv'
data_bubbles = pd.read_csv(link_data_bubbles)
def create__bubbles_graph(authors_arr, tmeters_range, theme_status):
    tmeters_left = tmeters_range[0]
    tmeters_right = tmeters_range[1]
    def mode_func(arr):
        return scipy.stats.mode(arr, keepdims=False)[0]

    temp_data_bubble = data_bubbles.query("author in @authors_arr & \
                             total_meters >= @tmeters_left & total_meters <= @tmeters_right")
    temp_data_bubble = temp_data_bubble.groupby(['author_type', 'author']).agg({'price_per_m2': 'mean',
                                                                      'price': 'mean',
                                                                      'floors_count': mode_func,
                                                                      'total_meters': 'mean'}) \
        .reset_index(level=1, drop=False).reset_index()
    temp_data_bubble.rename(columns={'price_per_m2': 'mean_price_m2',
                                'price': 'mean_price',
                                'floors_count': 'floors_mode',
                                'total_meters': 'total_meters_mean'}, inplace=True)
    temp_data_bubble = temp_data_bubble.sort_values(['author_type', 'author'])

    hover_text = []
    bubble_size = []

    for index, row in temp_data_bubble.iterrows():
        hover_text.append(('Продавец: {author}<br>' +
                           'Средняя цена за м2: {mean_price_m2}<br>' +
                           'Средняя цена предложения: {mean_price}<br>' +
                           'Самое частое кол-во этажей в доме: {floors_mode}<br>' +
                           'Средний метраж квартиры: {total_meters_mean}').format(author=row['author'],
                                                                                  mean_price_m2=row['mean_price_m2'],
                                                                                  mean_price=row['mean_price'],
                                                                                  floors_mode=row['floors_mode'],
                                                                                  total_meters_mean=row[
                                                                                      'total_meters_mean']))
        bubble_size.append(np.sqrt(row['mean_price']))

    temp_data_bubble['hover_text'] = hover_text
    temp_data_bubble['bubble_size'] = bubble_size
    sizeref = 2 * temp_data_bubble['bubble_size'].max() / (100 ** 2)

    # Словарь с данными для каждого типа продавца
    types_names = temp_data_bubble['author_type'].unique()
    types_data = {author_type: temp_data_bubble.query("author_type == '%s'" % author_type)
                  for author_type in types_names}

    bubbles_fig = go.Figure()

    for author_type, filtered_df in types_data.items():
        bubbles_fig.add_trace(go.Scatter(
            x=filtered_df['mean_price'], y=filtered_df['total_meters_mean'],
            name=author_type, text=filtered_df['hover_text'],
            marker_size=filtered_df['bubble_size'],
        ))

    # Tune marker appearance and layout
    bubbles_fig.update_traces(mode='markers', marker=dict(sizemode='area',
                                                  sizeref=sizeref, line_width=1.5))
    if theme_status == 'dark':
        paper_bgcolor = 'rgb(51, 51, 51)'
        plot_bgcolor = 'rgb(51, 51, 51)'
        title_font_color = 'white'
        font_color = "white"
    else:
        paper_bgcolor = 'rgb(255, 255, 255)'
        plot_bgcolor = 'rgb(255, 255, 255)'
        title_font_color = 'black'
        font_color = "black"
    bubbles_fig.update_layout(
        title='Средняя площадь жилья/Средняя цена предложения',
        xaxis=dict(
            title='Средняя цена предложения(руб.)',
            gridcolor='grey',
            type='log',
            gridwidth=1,
        ),
        yaxis=dict(
            title='Средний площадь жилья(кв. м)',
            gridcolor='grey',
            gridwidth=1,
        ),
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
        title_font_color=title_font_color,
        font_color=font_color
    )
    return bubbles_fig