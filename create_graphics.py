import pandas as pd
import plotly.graph_objects as go
def create_line_fig():
    dynamics_data_link = 'https://docs.google.com/spreadsheets/d/e/' \
                         '2PACX-1vRAEk-aa_OeTJF3cJNK5HWXj4J4j3Ipix8' \
                         'MGImNyYlsWY9xG6RFVYAPcVKo_17avMq_u1O02Bjg' \
                         'V5bK/pub?gid=1064497805&single=true&output=csv'
    dynamics_data = pd.read_csv(dynamics_data_link)
    lines_fig = go.Figure()
    fig_new = go.Scatter(x=dynamics_data.query("city == 'Moskva'")['Даты'], y=dynamics_data.query("city == 'Moskva'")['Квартиры в новостройке, за м2, руб.'],
                        mode='lines+markers+text',
                        name='Первичное',
                        text=dynamics_data.query("city == 'Moskva'")['Изменение'])
    fig_secondary = go.Scatter(x=dynamics_data.query("city == 'Moskva'")['Даты'], y=dynamics_data.query("city == 'Moskva'")['Квартиры вторичка, за м2, руб.'],
                        mode='lines+markers+text',
                        name='Вторичное',
                        text=dynamics_data.query("city == 'Moskva'")['Изменение.1'])
    lines_fig.add_trace(fig_new)
    lines_fig.add_trace(fig_secondary)
    return lines_fig