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
                             {"lable": cut, "value": cut}
                             for cut in sorted(df["cut"].unique())
                         ],
                         value=list(df["cut"].unique()),
                         multi=True, )
        ], width=4),

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
    ], className="mb-4"),  # filtros

    dbc.Row([

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("N.º de diamantes"),
                    html.H3(id="kpi_count", children="12")
                ])
            ), width=3
        ),  # Kpi 1

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

    ]),  # Kpis

    dbc.Row([
        dbc.Col(
            dcc.Graph(id="scatter_graph"),
            width=8),

        dbc.Col(
            dcc.Graph(id="hist_graph"),
            width=4),
    ]),  # Graficos

    html.H3("Tabela de dados", className="mt-4"),

    dash_table.DataTable(
        id="data_table",
        page_size=10,
        sort_action="native",
        filter_action="native", )

], fluid=True)


@app.callback(
    Output("kpi_count", "children"),
    Output("kpi_avg_price", "children"),
    Output("kpi_max_price", "children"),
    Output("kpi_avg_carat", "children"),

    Output("scatter_graph", "figure"),
    # Output("hist_graph", "figure"),

    # Output("data_table", "data"),
    # Output("data_table", "columns"),

    Input('cut_filter', 'value'),
    Input('color_filter', 'value'),
    Input('price_filter', 'value')
)
def update_dashboard(select_cut, select_color, max_price):
    df_filtrada = df[
        (df["cut"].isin(select_cut)) &
        (df["color"].isin(select_color)) &
        (df["price"] <= max_price)
        ]

    # Calcular KPIs

    count = len(df_filtrada)
    kpi_count = f"{count:,}".replace(",", " ")

    avg_price = df_filtrada["price"].mean()
    kpi_avg_price = f"{avg_price:.2f} €"

    max_price = df_filtrada["price"].max()
    kpi_max_price = f"{max_price:.2f} €"

    avg_carat = df_filtrada["carat"].mean()
    kpi_avg_carat = f"{avg_carat:.2f} €"

    scatter_fig = px.scatter(
        df_filtrada,
        x="carat",
        y="price",
        color="cut",
        size="depth",
        hover_data=["color", "clarity", "table"],
        title="Relação entre preço e quilates"
    )

    scatter_fig.update_layout(
        xaxis_title="Quilates",
        yaxis_title="preço"
    )

    return (kpi_count,
            kpi_avg_price,
            kpi_max_price,
            kpi_avg_carat,
            scatter_fig,
            )


if __name__ == "__main__":
    app.run(debug=True, port=8082)