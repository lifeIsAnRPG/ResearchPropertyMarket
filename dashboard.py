from dash import Dash, html, dash_table, dcc, callback, Output, Input, State, clientside_callback
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_mantine_components as dmc
from ml_model import predict_cost
from dash_iconify import DashIconify
import plotly.colors as colors
from time import sleep
import scipy
import json
from create_graphics import create_line_fig

link_data_hist = 'https://docs.google.com/spreadsheets/d/e/' \
       '2PACX-1vQxxmZm6YG54VucQ9yRgWFQXtOI-RFJ5-sOLT93LpaYGYc-vabL9LOzzkRXX' \
       '-LmSROTA7hOL1C327nZ/pub?gid=213261502&single=true&output=csv'
link_selectors = 'https://docs.google.com/spreadsheets/d/e/' \
                 '2PACX-1vTbiTqW6HaKWKeK4TpujjktkIEa8qw9zBdgFzVerM-TLF9G8ww' \
                 'RCjZoTuE_dnDCl9DbMdcYc39bg5IN/pub?gid=2117269470&single=true&output=csv'
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
server = app.server
theme_status = 'dark'

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
def create_hist_fig(col_chosen):
    top10_devs = (df.query('city == @col_chosen').author.value_counts(normalize=True) * 100).to_frame().reset_index()[:10]
    x = top10_devs.author.str.slice(stop=12)
    x = x.where(x.str.len() != 12, x.str.cat(['..'] * len(top10_devs)))
    labels = {'x': 'Субъект', 'proportion': '% на рынке'}
    global theme_status
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
    hist_fig = px.histogram(top10_devs,
                            x=x,
                            y='proportion',
                            labels=labels,
                            text_auto='.2f',
                            title='Топ-10 застройщиков/агенств')
    hist_fig.update_layout(
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
        xaxis_title='Продавцы',
        yaxis_title='% на рынке',
        title_font_color=title_font_color,
        font_color=font_color
    )
    return hist_fig

def create_map():
    global theme_status
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
    map_fig = px.choropleth_mapbox(geodata_msk,
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
    map_fig.update_layout(
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
        title_font_color=title_font_color,
        font_color=font_color
    )
    return map_fig

lines_fig = create_line_fig("Moskva", theme_status)
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
                                     size="sm",
                                     style={"marginTop": 15, "marginBottom": 15}),
                                    dcc.Graph(figure={}, id='graph-placeholder')
                                ]
                            )
                         ], shadow="xs", p="xs", radius="lg",withBorder = True)], span=6),
            dmc.Col([
                dmc.Paper(
                    children=[
                        dmc.Container(
                            children=[
                                    dcc.Graph(figure=create_map(), id='map-placeholder'
                                              )
                                ],  style={"marginTop": 30, "marginBottom": 30}
                            )
                        ], shadow="xs", p="xs", radius="lg", withBorder=True)], span=6),
            dmc.Col([
                dmc.Paper(
                    children=[
                        dmc.Container(
                            children=[
                                dmc.Tabs(
                                    [
                                        dmc.TabsList(
                                            [
                                                dmc.Tab('Продавцы', value="authors"),
                                                dmc.Tab("Средняя общая площадь", value="total_meters"),
                                            ]
                                        ),
                                        dmc.TabsPanel(
                                            dmc.Container(
                                                style={"height": 110, "width": "95%"},
                                                children=[
                                                    dmc.Space(h=15),
                                                    dmc.MultiSelect(
                                                        id = 'authors-multi-selector',
                                                        data=pd.Series(data_bubbles['author'].unique()).dropna(),
                                                        searchable=True,
                                                        nothingFound="Не найдено",
                                                        style={"width": '100%'},
                                                        value=['Homeapp', 'Физическое лицо','ANT Development']
                                                        )
                                                    ]
                                                ), value="authors"
                                            ),
                                        dmc.TabsPanel(
                                            dmc.Container(
                                                style={"height": 110, "width": "75%"},
                                                children=[
                                                    dmc.Space(h=15),
                                                    dmc.RangeSlider(
                                                        id="rng-slider-bubble_graph",
                                                        min = data_bubbles['total_meters'].min(),
                                                        max = data_bubbles['total_meters'].max(),
                                                        value=[data_bubbles['total_meters'].min(), data_bubbles['total_meters'].max()],
                                                        marks=[
                                                            {"value": data_bubbles['total_meters'].max() * 0.5, "label": "50%"},
                                                        ],
                                                        style={"marginTop": 25, "marginBottom": 35}
                                                    )
                                                ]
                                            ), value="total_meters"),
                                    ],
                                    color="blue",
                                    orientation="horizontal",
                                    value = "authors",
                                ),
                                dcc.Graph(figure={},id = 'bubble-placeholder')
                            ]
                            )
                         ], shadow="xs", p="xs", radius="lg", withBorder=True)], span=6),
            dmc.Col([
                dmc.Paper(
                    children=[
                        dmc.Container(
                            children=[
                                dmc.SegmentedControl(
                                    id="lines-segmented",
                                    value="Moskva",
                                    data=[
                                        {"value": "Moskva", "label": "Москва"},
                                        {"value": 'Sankt-Peterburg', "label": 'Санкт-Петербург'}
                                    ],
                                    mt=10,
                                    style={"marginTop": 50, "marginBottom": 56}
                                ),
                                dcc.Graph(figure=lines_fig, id='lines-placeholder')
                            ]
                        )
                    ], shadow="xs", p="xs", radius="lg", withBorder=True)], span=6)
            ]
        ),
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
    children=[
        dcc.Interval(
                id='interval-component',
                interval=1*1000,
                n_intervals=0,
                max_intervals=1
            ),
        dmc.NotificationsProvider(
            children=[
                html.Div(
                        [
                            html.Div(id="notifications-container"),
                        ]
                    ),
                create_content()
            ]
        )
    ]
)

@callback(
    Output(component_id='graph-placeholder', component_property='figure'),
    Input(component_id='my-dmc-radio-item', component_property='value')
)
def update_graph(col_chosen):
    hist_fig = create_hist_fig(col_chosen)
    return hist_fig
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
    [Output(component_id="theme-provider", component_property='theme'),
     Output(component_id='graph-placeholder', component_property='figure', allow_duplicate=True),
     Output(component_id='map-placeholder', component_property='figure'),
     Output(component_id='lines-placeholder', component_property="figure",allow_duplicate=True),],
    Input(component_id="theme_switcher", component_property='checked'),
    State(component_id='my-dmc-radio-item', component_property='value'),
    prevent_initial_call=True
)
def change_theme(checked, col_chosen):
    global theme_status
    global lines_fig
    if checked:
        theme_status = 'light'
        hist_fig = create_hist_fig(col_chosen)
        map_fig = create_map()
        lines_fig.update_layout(
            paper_bgcolor='rgb(255, 255, 255)',
            plot_bgcolor='rgb(255, 255, 255)',
            title_font_color='black',
            font_color="black"
            )
        return {
            "colorScheme": 'light',
            "fontFamily": "'Inter', sans-serif",
            "primaryColor": "green",
        }, hist_fig, map_fig, lines_fig
    else:
        theme_status = 'dark'
        hist_fig = create_hist_fig(col_chosen)
        map_fig = create_map()
        lines_fig.update_layout(
            paper_bgcolor='rgb(51, 51, 51)',
            plot_bgcolor='rgb(51, 51, 51)',
            title_font_color='white',
            font_color="white"
        )
        return {
            "colorScheme": 'dark',
            "fontFamily": "'Inter', sans-serif",
            "primaryColor": "green",
        }, hist_fig, map_fig, lines_fig

@callback(
    Output("bubble-placeholder", "figure"),
    [Input("authors-multi-selector", "value"),
     Input("rng-slider-bubble_graph", "value")]
)
def update_bubbles_graph(authors_arr, tmeters_range):
    tmeters_left = tmeters_range[0]
    tmeters_right = tmeters_range[1]
    global theme_status
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

    # Create figure
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
        title='Средний метраж жилья/Средняя цена предложения',
        xaxis=dict(
            title='Средняя цена предложения',
            gridcolor='white',
            type='log',
            gridwidth=1,
        ),
        yaxis=dict(
            title='Средний метраж жилья',
            gridcolor='white',
            gridwidth=1,
        ),
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
        title_font_color=title_font_color,
        font_color=font_color
    )
    return bubbles_fig

@callback(
    Output('lines-placeholder', "figure"),
    Input("lines-segmented", "value"),
    prevent_initial_call=True
)
def update_lines_graph(chosen_segment):
    global lines_fig
    lines_fig = create_line_fig(chosen_segment,theme_status)
    return lines_fig

@callback(
    Output("notifications-container", "children"),
    Input('interval-component', 'n_intervals')
)
def show(n_intervals):
    return dmc.Notification(
        title="Доброго времени суток!",
        id="simple-notify",
        action="show",
        autoClose = False,
        message="Дэшборд еще будет дорабатываться, прошу не обращать внимания на мелкие баги.",
        icon=DashIconify(icon="ic:round-celebration"),
    )

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
def start_engine():
    app.run_server(debug=False, port=80)

if __name__ == '__main__':
    start_engine()
