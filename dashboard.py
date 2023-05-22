from dash import Dash, html, dash_table, dcc, callback, Output, Input, State, clientside_callback
import pandas as pd
import numpy as np
import plotly.express as px
import dash_mantine_components as dmc
from ml_model import predict_cost
from dash_iconify import DashIconify
import plotly.colors as colors
from time import sleep
import json

link_data_hist = 'https://docs.google.com/spreadsheets/d/e/' \
       '2PACX-1vQxxmZm6YG54VucQ9yRgWFQXtOI-RFJ5-sOLT93LpaYGYc-vabL9LOzzkRXX' \
       '-LmSROTA7hOL1C327nZ/pub?gid=213261502&single=true&output=csv'
link_selectors = 'https://docs.google.com/spreadsheets/d/e/' \
                 '2PACX-1vRyT9LKa2_b3-92CiZxG5w1NDYQUWWo8HipsB7DRTjUZxItCaem' \
                 'm2yL56oSXgjapti7_pUTEjUoNUPq/pub?gid=853725322&single=true&output=csv'
link_geodata_msk = 'https://docs.google.com/spreadsheets/d/e/' \
                   '2PACX-1vSPfEe4M6P2lpaEdDL87E7GtIDfWFctAGbMjrAbj6U9rFKn8f2' \
                   '-G5X0FK_hw1xFqx1Qq80CdU9C5kU5/pub?gid=1057824050&single=true&output=csv'
link_data_bubbles = 'https://docs.google.com/spreadsheets/d/e/' \
                    '2PACX-1vTQk2hwcxS74FiRZaXHcqnXZ4pqt9S7tbPXuuAtNpqes4AmQdu' \
                    'EBsFVB-O0zTx6t6wHOe8y8OBdN_qr/pub?gid=1962707013&single=true&output=csv'
df = pd.read_csv(link_data_hist)
selectors_data = pd.read_csv(link_selectors)
geodata_msk = pd.read_csv(link_geodata_msk)
data_bubbles = pd.read_csv(link_data_bubbles)
with open('mo.geojson', 'r', encoding ='UTF-8') as f:
    msk_geojson = json.load(f)

external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)


def create_text(label):
    return dmc.Text(
        label,
        size="xl",
        color="gray",
    )
def create_select(id,label, data):
    return dmc.Select(
        id=f"select_{id}",
        label=label,
        description="Выбрать(есть поиск)",
        searchable=True,
        clearable=True,
        style={"width": 200},
        data=[{"value": item, "label": item} for item in data]
        )
def create_number_input(id, label):
    return dmc.NumberInput(
        id = f"number_{id}",
        label=label,
        description="Указать или удерживать стрелку",
        stepHoldDelay=500,
        stepHoldInterval=100,
        value=0,
        style={"width": 200}
)


def create_content():
    return dmc.Container([
        dmc.Header(
            height=70,
            fixed=True,
            p="md",
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
                                dmc.Group(
                                    position="right",
                                    align="center",
                                    children=[
                                    html.A(
                                        dmc.Tooltip(
                                            dmc.Avatar(
                                                src="https://avatars.githubusercontent.com/u/97909195?v=4",
                                                size="sm",
                                                radius="xl",
                                            ),
                                            label="Github",
                                            position="bottom",
                                        ),
                                        href="https://github.com/HinkevichRoadToDs/QualificationWork",
                                        target = "_blank"
                                    ),
                                    dmc.Switch(
                                        id='theme_switcher',
                                        offLabel=DashIconify(icon="radix-icons:sun", width=20),
                                        onLabel=DashIconify(icon="radix-icons:moon", width=20),
                                        size="xl",
                                    )
                                ])
                            ]),
                        ),
                    ]),
        dmc.Space(h=70),
        dmc.Grid([
                dmc.Col(
                    dmc.Container([
                        dmc.SimpleGrid(
                        cols=4,
                        spacing="xs",
                        breakpoints=[
                                {"maxWidth": 980, "cols": 3, "spacing": "xs"},
                                {"maxWidth": 755, "cols": 2, "spacing": "xs"},
                                {"maxWidth": 600, "cols": 1, "spacing": "xs"},
                            ],
                            children=[
                                        create_number_input(1,"Этаж"),
                                        create_number_input(2, "Этажей в доме"),
                                        create_number_input(3, "Кол-во комнат"),
                                        create_number_input(4, "Общая площадь"),
                                        create_number_input(5, "Год постройки"),
                                        create_number_input(6, "Жилая площадь"),
                                        create_number_input(7, "Площадь кухни"),
                                        create_select(8,'Застройщик/Агенство', selectors_data['author'].unique()),
                                        create_select(9,'Город', np.array(['Moskva','Sankt-Peterburg'])),
                                        create_select(10,'Район', selectors_data['district'].unique()),
                                        create_select(11,'Улица', selectors_data['street'].unique()),
                                        create_select(12,'Ближайшее метро', selectors_data['underground'].unique()),
                                ])
                            ],size=940)
                        ),
                dmc.Col(dmc.Container([
                    dmc.Text(id="prediction", mt=20),
                    html.Div(
                                [
                                    dmc.Button(
                                        "Узнать стоимость",
                                        id="loading-button-pred",
                                        leftIcon=DashIconify(icon="ph:currency-rub-fill"),
                                    ),
                                ]
                            )
                        ],size=940)
                    )
                ], gutter = 'xs', justify="center",align="center"),
        dmc.Stack(
            children=[dmc.Space(h=10),dmc.Divider(variant="solid"),dmc.Space(h=10)]
            ),
        dmc.Grid([
            dmc.Col([
                dmc.Paper(
                    children=[
                        dmc.Container(
                            children=[dmc.RadioGroup([
                                    dmc.Radio(i, value=k) for i,k in [['Москва','Moskva'],['Санкт-Петербург',
                                                                                           'Sankt-Peterburg']]],
                                     id='my-dmc-radio-item',
                                     value='Moskva',
                                     size="sm"),
                                    dcc.Graph(figure={}, id='graph-placeholder')
                                ]
                            )
                         ], shadow="xs", p="xs", radius="lg",withBorder = True)], span=6),
            dmc.Col([
                dmc.Paper(
                    children=[
                        dmc.Container(
                            children=[
                                    dcc.Graph(figure=px.choropleth_mapbox(geodata_msk,
                                                             geojson=msk_geojson,
                                                             locations='OKATO',
                                                             color='Цена за м2',
                                                             color_continuous_scale=colors.sequential.Plasma,
                                                             featureidkey='properties.OKATO',
                                                             mapbox_style="carto-positron",
                                                             zoom=8.5,
                                                             center={"lat": 55.75, "lon": 37.61},
                                                             opacity=0.2,
                                                             range_color=(
                                                             geodata_msk['Цена за м2'].min(), geodata_msk['Цена за м2'].max()),
                                                             labels={'Цена за м2': 'Цена за м2'}
                                                            )
                                                      , id='map-placeholder'
                                              )
                                ]
                            )
                        ], shadow="xs", p="xs", radius="lg",withBorder = True)], span=6),
            dmc.Col([
                dmc.Paper(
                    children=[
                        dmc.Container(
                            children=[
                                dmc.SimpleGrid(
                                    cols=2,
                                    children=[
                                        dmc.RangeSlider(
                                            id="rng-slider-bubble_graph",
                                            min = data_bubbles['total_meters'].min(),
                                            max = data_bubbles['total_meters'].max(),
                                            value=[data_bubbles['total_meters'].min(), data_bubbles['total_meters'].max()],
                                            marks=[
                                                {"value": data_bubbles['total_meters'].max() * 0.5, "label": "50%"},
                                            ],

                                        ),

                                    ]
                                )
                            ]
                            )
                         ], shadow="xs", p="xs", radius="lg",withBorder = True)], span=6)
        ]),
    ], fluid=True)
# App layout
app.layout = dmc.MantineProvider(
    id="theme-provider",
    theme={
        "colorScheme": "dark",
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "green",
    },
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[create_content()]
)

@callback(
    Output(component_id='graph-placeholder', component_property='figure'),
    Input(component_id='my-dmc-radio-item', component_property='value')
)
def update_graph(col_chosen):
        top10_devs = (df.query('city == @col_chosen').author.value_counts(normalize=True) * 100).to_frame().reset_index()[:10]
        x = top10_devs.author.str.slice(stop=12)
        x = x.where(x.str.len() != 12,x.str.cat(['..'] * len(top10_devs)))
        labels = {'x': 'Субъект','proportion':'% на рынке'}
        fig = px.histogram(top10_devs, x=x,y='proportion',text_auto ='.2f',labels=labels, title = 'Топ-10 '
                                                                                                  'застройщиков/агенств')
        return fig
@callback(# синтаксис колбэк-функций должен быть именно таким
    [Output(component_id="loading-button-pred", component_property="loading"),
    Output(component_id="prediction", component_property="children")],
    [Input(component_id="loading-button-pred", component_property="n_clicks")],
    [State(component_id="number_1", component_property="value"),
    State(component_id="number_2", component_property="value"),
    State(component_id="number_3", component_property="value"),
    State(component_id="number_4", component_property="value"),
    State(component_id="number_5", component_property="value"),
    State(component_id="number_6", component_property="value"),
    State(component_id="number_7", component_property="value"),
    State(component_id="select_8", component_property="value"),
    State(component_id="select_9", component_property="value"),
    State(component_id="select_10", component_property="value"),
    State(component_id="select_11", component_property="value"),
    State(component_id="select_12", component_property="value")],
    prevent_initial_call=True,
)
def predict(n_clicks,floor, floors_count, rooms,
            total_meters, year, living_meters,
            kitchen_meters, author, city,
            district, street, underground):
    if n_clicks is not None:
        sleep(2)
        y_pred = predict_cost(np.array([author, city, floor, floors_count, rooms,
        total_meters, year, living_meters,
        kitchen_meters, district, street, underground]))
        return False, f'Примерная стоимость: {y_pred}'

@callback(
    Output(component_id="theme-provider", component_property='theme'),
    Input(component_id="theme_switcher", component_property='checked'),
    prevent_initial_call=True,
)
def change_theme(checked):
    if checked:
        return {
            "colorScheme": 'light',
            "fontFamily": "'Inter', sans-serif",
            "primaryColor": "green",
        }
    else:
        return {
            "colorScheme": 'dark',
            "fontFamily": "'Inter', sans-serif",
            "primaryColor": "green",
        }

# @callback(
#     Output("bubbles_graph", "figure"),
#     Input("rng-slider-bubble_graph", "value")
# )
# def update_bubbles_graph(value):
#     return f"You have selected: [{value[0]}, {value[1]}]"


clientside_callback(# функция JS, будет выполнена на стороне клиента
    """
    function updateLoadingState(n_clicks) {
        return true
    }
    """,
    Output("loading-button-pred", "loading", allow_duplicate=True),
    Input("loading-button-pred", "n_clicks"),
    prevent_initial_call=True,
)


if __name__ == '__main__':
    app.run_server(debug=True)