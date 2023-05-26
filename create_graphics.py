import pandas as pd
import plotly.graph_objects as go
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