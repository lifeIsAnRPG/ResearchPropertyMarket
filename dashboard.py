from dash import Dash, html, dash_table, dcc, callback, Output, Input
#Dash Core Components. Этот модуль включает компонент Graph с именем dcc.Graph, который используется для отображения
# интерактивных графиков.
import pandas as pd
import numpy as np
import plotly.express as px
import dash_mantine_components as dmc
link = 'https://docs.google.com/spreadsheets/d/e/' \
       '2PACX-1vQxxmZm6YG54VucQ9yRgWFQXtOI-RFJ5-sOLT93LpaYGYc-vabL9LOzzkRXX' \
       '-LmSROTA7hOL1C327nZ/pub?gid=213261502&single=true&output=csv'
df = pd.read_csv(link)

external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dmc.Container([
    dmc.Title('Dashboard', color="black", size="h3"),
    dmc.RadioGroup(
        [dmc.Radio(i, value=i) for i in  ['Moskva', 'Sankt-Peterburg']],
        id='my-dmc-radio-item',
        value='Moskva',
        size="sm"),
    dmc.Grid([
        dmc.Col([
            dcc.Graph(figure={}, id='graph-placeholder')
            ], span=6),
        ]),
], fluid=True)
@callback(
    Output(component_id='graph-placeholder', component_property='figure'),
    Input(component_id='my-dmc-radio-item', component_property='value')
)
def update_graph(col_chosen):
        top10_devs = (df.query('city == @col_chosen').author.value_counts(normalize=True) * 100).to_frame().reset_index()[:10]
        x = top10_devs.author.str.slice(stop=12)
        x = x.where(x.str.len() != 12,x.str.cat(['..'] * len(top10_devs)))
        labels = {'x': 'Застройщик','proportion':'% на рынке'}
        fig = px.histogram(top10_devs, x=x,y='proportion',text_auto ='.2f',labels=labels, title = 'Топ-10 застройщиков')
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
