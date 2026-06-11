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
        dbc.Col([
            html.Label("Qualidade do corte"),
            dcc.Dropdown(id="cut_filter",)

        ]),
        dbc.Col([
            html.Label("Cor"),
            dcc.Dropdown(id="color_filter", )
        ]),

        dbc.Col([
            html.Label("Preço máximo"),
            dcc.Slider(id="price_filter", )
        ])
    ] ,className="mb-4")


], fluid=True)

if __name__ == "__main__":
    app.run(debug=True, port=8081)