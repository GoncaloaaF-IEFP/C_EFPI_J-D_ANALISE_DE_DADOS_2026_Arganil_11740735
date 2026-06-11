import dash
from dash import Input, Output, dcc, dash_table, html
import dash_bootstrap_components as dbc
import plotly.express as px
import seaborn as sns


df = sns.load_dataset("diamonds")


app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                )

app.layout = dbc.Container([

    html.H1("Diamonds Dashboard",
            className="text-center my-4"),

    html.P("Descrição do dashboard",
           className="text-center"),


    dbc.Row([
        html.H3("Filtros"),
        dbc.Col([
            html.Label("Qualidade do corte"),
            dcc.Dropdown(id="cut_filter",
                         options=[
                             {"lable":cut, "value":cut}
                             for cut in sorted(df["cut"].unique())
                         ],
                         value=list(df["cut"].unique()),
                         multi=True,)
        ], width= 4),


        dbc.Col([
            html.Label("Cor"),
            dcc.Dropdown(id="color_filter",
                         options=[
                             {"lable": color, "value": color}
                             for color in sorted(df["color"].unique())
                         ],
                         value=list(df["color"].unique()),
                         multi=True,
                         )
        ]),

        dbc.Col([
            html.Label("Preço máximo"),
            dcc.Slider(id="price_filter",
                       min=int(df["price"].min()),
                       max=int(df.price.max()),

                       tooltip={"placement": "bottom",
                                "always_visible": False},
                       marks=None
                       )
        ])
    ] ,className="mb-4"), # filtros

    dbc.Row([

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("N.º de diamantes"),
                    html.H3(id="kpi_count", children="12")
                ])
            ), width= 3
        ), # Kpi 1

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Preço médio"),
                    html.H3(id="kpi_avg_price", children="12")
                ])
            ), width=3
        ),  # Kpi 2

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Maior preço"),
                    html.H3(id="kpi_max_price", children="12")
                ])
            ), width=3
        ),  # Kpi 3

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Quilates médios"),
                    html.H3(id="kpi_avg_carat", children="12")
                ])
            ), width=3
        ),  # Kpi 4

    ]), # Kpis

    dbc.Row([]) # Graficos
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True, port=8081)