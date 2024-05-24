import dash
import requests
from dash import html, dcc, Input, Output, ClientsideFunction

# Assuming AREA_NAMES is imported from controls.py
from controls import AREA_NAMES

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True
)
app.title = "UHI Dashboard"
server = app.server

area_name_options = [
    {"label": name, "value": name}  # Use the area names as both label and value
    for name in AREA_NAMES.values()
]

# Include Font Awesome CSS and OpenLayers CSS and JS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <script src="https://cdn.jsdelivr.net/npm/ol@v9.2.3/dist/ol.js"></script>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol@v9.2.3/ol.css">
        <style>
            .mini_container {
                flex: 1;
                margin: 10px;
                padding: 20px;
                background-color: #f9f9f9;
                border-radius: 5px;
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .icon-text {
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                font-weight: bold;
            }
            .container-display {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-around;
            }
            #map {
                height: 600px;
                width: 100%;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={"height": "60px", "width": "auto", "margin-bottom": "25px"},
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Urban Heat Island Dashboard", style={"margin-bottom": "0px"}),
                                html.H3("Helsinki City", style={"margin-top": "0px"}),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                )
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P("Filter by Year:", className="control_label"),
                        dcc.RangeSlider(
                            id="year_slider",
                            min=2000,
                            max=2024,
                            marks={i: "{}".format(i) for i in range(2000, 2024, 6)},
                            step=1,
                            value=[2020, 2024],
                            className="dcc_control",
                        ),
                        html.P("Filter by Area Type:", className="control_label"),
                        dcc.Dropdown(
                            id="AREA_NAMES",
                            options=area_name_options,
                            multi=True,
                            value=[],
                            className="dcc_control",
                        ),
                        html.P("Data Type:", className="control_label"),
                        dcc.Dropdown(
                            id="data_type",
                            options=[
                                {"label": "Temperature", "value": "temperature"},
                                {"label": "Digital Elevation Model", "value": "dem"},
                                {"label": "Wind Speed", "value": "wind_speed"},
                                {"label": "3D Buildings", "value": "3d_buildings"}
                            ],
                            value=[],
                            className="dcc_control",
                        ),
                        html.Button("calculate", id="search_button", className="dcc_control"),
                        html.Button("Reset", id="reset_button", className="dcc_control"),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(id="temp_text", className="icon-text"),
                                        html.P("Temperature"),
                                        html.I(className="fas fa-thermometer-half"),
                                    ],
                                    id="temperature",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6(id="humidity_text", className="icon-text"),
                                        html.P("Humidity"),
                                        html.I(className="fas fa-tint"),
                                    ],
                                    id="humidity",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6(id="wind_text", className="icon-text"),
                                        html.P("Wind Speed"),
                                        html.I(className="fas fa-wind"),
                                    ],
                                    id="wind",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6(id="uv_text", className="icon-text"),
                                        html.P("UV Index"),
                                        html.I(className="fas fa-sun"),
                                    ],
                                    id="uv_index",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="container-display",
                        ),
                        dcc.Interval(
                            id='interval-component',
                            interval=1*60*60*1000,  # in milliseconds
                            n_intervals=0
                        ),
                        html.Div(
                            id="map",
                            className="pretty_container",
                            style={"height": "600px"}
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

@app.callback(
    [Output("temp_text", "children"),
     Output("humidity_text", "children"),
     Output("wind_text", "children"),
     Output("uv_text", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_weather(n):
    city_name = "Helsinki"
    api_key = "9dd332c2cdf5ad3eee158912aa75b747"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    current_data = response.json()

    one_call_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={current_data['coord']['lat']}&lon={current_data['coord']['lon']}&appid={api_key}&units=metric"
    one_call_response = requests.get(one_call_url)
    five_day_data = one_call_response.json()

    temperature = f"{current_data['main']['temp']} °C"
    humidity = f"{current_data['main']['humidity']}%"
    wind_speed = f"{current_data['wind']['speed']} m/s"
    uv_index = five_day_data['current']['uvi']

    return temperature, humidity, wind_speed, uv_index

# OpenLayers map script integration
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='initializeMap'
    ),
    Output('map', 'children'),
    [Input('map', 'id'), Input('data_type', 'value'), Input('AREA_NAMES', 'value')]
)

# Main
if __name__ == "__main__":
    app.run_server(debug=True, port=5000)
