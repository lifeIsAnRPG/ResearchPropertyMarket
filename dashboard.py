from dash import Dash, html, dash_table, dcc, callback, Output, Input
#Dash Core Components. Этот модуль включает компонент Graph с именем dcc.Graph, который используется для отображения
# интерактивных графиков.
import pandas as pd
import plotly.express as px


# конструктор dash, отвечает за инициализацию приложения
app = Dash(__name__)
link = 'https://docs.google.com/spreadsheets/d/e/' \
       '2PACX-1vQxxmZm6YG54VucQ9yRgWFQXtOI-RFJ5-sOLT93LpaYGYc-vabL9LOzzkRXX-LmSROTA7hOL1C327nZ/pub?gid=213261502&single=true&output=csv'
df = pd.read_csv(link)
developers_count = df.groupby(['city','author']) \
    .agg({'author_type':'count'}) \
    .rename({'author_type': 'count'}, axis = 1).sort_values('count', ascending = False)
# Макет приложения представляет компоненты приложения, которые будут отображаться в веб-браузере, обычно содержащиеся
# в файле html.Div
app.layout = html.Div([
    html.Div(children='Первый трай'),
    html.Hr(),
    dcc.RadioItems(options=['Moskva', 'Sankt-Peterburg'], value='Moskva', id='controls-and-radio-item'),
    dcc.Graph(figure={},id='controls-and-graph')
])

@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(developers_count, x=developers_count.index.get_level_values(0)[
        developers_count.index.get_level_values(1) == col_chosen][:10],
        y=developers_count[developers_count.index.get_level_values(0) ==
                                                            col_chosen]['count'][:10])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
