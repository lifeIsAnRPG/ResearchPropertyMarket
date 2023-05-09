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


def create_text(label):
    return dmc.Text(
        label,
        size="xl",
        color="gray",
    )

# App layout
app.layout = dmc.Container([
    dmc.Header(
        height=50,
        children=[dmc.Container(
                    fluid=True,
                    style={"paddingRight": 12, "paddingLeft": 12},
                    children=dmc.Group(
                        position="apart",
                        align="flex-start",
                        children=[
                            dmc.Center(
                                dcc.Link(
                                    [
                                        dmc.MediaQuery(
                                            create_text("Research Property Market"),
                                            smallerThan="sm",
                                            styles={"display": "none"},
                                        ),
                                        dmc.MediaQuery(
                                            create_text("RPM"),
                                            largerThan="sm",
                                            styles={"display": "none"},
                                        ),
                                    ],
                                    href="/",
                                    style={"paddingTop": 3, "textDecoration": "none"},
                                ),
                            ),
                        ],
                    ),
                )
            ],
        ),
    dmc.Space(h=40),
    html.Div([
        dmc.Group(
            position="apart",
            align="flex-start", #flex-start
            grow =False,
            children=[
                        dmc.Select(
                        id="select_1",
                        searchable=True,
                        clearable=True,
                        style={"width": 200},
                        data=[{"value":"ПИК", "label":"ПИК"}, {"value":"GloraX","label":"GloraX"}]
                        ),
                        dmc.Select(
                            id="select_2",
                            searchable=True,
                            clearable=True,
                            style={"width": 200},
                            data=[{"value": 'Moskva', "label": 'Moskva'},
                                  {"value": 'Sankt-Peterburg', "label": 'Sankt-Peterburg'}],
                        ),
                        dmc.Select(
                        id="select_3",
                        searchable=True,
                        clearable=True,
                        style={"width": 200},
                        data=[{"value":"ПИК", "label":"ПИК"}, {"value":"GloraX","label":"GloraX"}]
                        ),
                        dmc.Select(
                            id="select_4",
                            searchable=True,
                            clearable=True,
                            style={"width": 200},
                            data=[{"value": 'Moskva', "label": 'Moskva'},
                                  {"value": 'Sankt-Peterburg', "label": 'Sankt-Peterburg'}],
                        ),
                        dmc.Select(
                        id="select_5",
                        searchable=True,
                        clearable=True,
                        style={"width": 200},
                        data=[{"value":"ПИК", "label":"ПИК"}, {"value":"GloraX","label":"GloraX"}]
                        ),
                        dmc.Select(
                            id="select_6",
                            searchable=True,
                            clearable=True,
                            style={"width": 200},
                            data=[{"value": 'Moskva', "label": 'Moskva'},
                                  {"value": 'Sankt-Peterburg', "label": 'Sankt-Peterburg'}],
                        ),dmc.Select(
                        id="select_7",
                        searchable=True,
                        clearable=True,
                        style={"width": 200},
                        data=[{"value":"ПИК", "label":"ПИК"}, {"value":"GloraX","label":"GloraX"}]
                        ),
                        dmc.Select(
                            id="select_8",
                            searchable=True,
                            clearable=True,
                            style={"width": 200},
                            data=[{"value": 'Moskva', "label": 'Moskva'},
                                  {"value": 'Sankt-Peterburg', "label": 'Sankt-Peterburg'}],
                        )
                    ],
                ),
        dmc.Text(id="prediction", mt=20)]),
        dmc.Stack(
            children=[dmc.Space(h=10),dmc.Divider(variant="solid"),dmc.Space(h=10)]
            ),
            dmc.Grid([
                dmc.Col([
                    dmc.Paper(
                        children=[
                            dmc.Container(
                                children=[dmc.RadioGroup([
                                        dmc.Radio(i, value=i) for i in ['Moskva', 'Sankt-Peterburg']],
                                         id='my-dmc-radio-item',
                                         value='Moskva',
                                         size="sm"),
                                        dcc.Graph(figure={}, id='graph-placeholder')
                                    ]
                                )
                             ], shadow="xs", p="xs", radius="lg",withBorder = True)], span=6)
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
@callback(
    Output(component_id="prediction", component_property="children"),
    [Input(component_id="select_1", component_property="value"),
    Input(component_id="select_2", component_property="value")]
)
def new_item(author,city):
    return f'Примерная стоимость: ...'

if __name__ == '__main__':
    app.run_server(debug=True)
