# Install necessary libraries
# Run this in a terminal if required: pip install dash pandas plotly

# Import libraries
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the Gapminder dataset
url = "https://raw.githubusercontent.com/resbaz/r-novice-gapminder-files/master/data/gapminder-FiveYearData.csv"
gapminder = pd.read_csv(url)

# Create the Dash app
app = Dash(__name__)
app.title = "Gapminder Dashboard"

# App layout with multiple tabs
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label="Introduction", children=[
            html.H1("Gapminder Dataset Overview", style={"text-align": "center"}),
            html.P("The Gapminder dataset includes indicators such as GDP per capita, life expectancy, and population "
                   "across countries over time. It's useful for understanding global development trends."),
            html.Label("Preview Data: Select number of rows to display"),
            dcc.Slider(
                id="row-slider",
                min=5,
                max=50,
                step=5,
                value=10,
                marks={i: str(i) for i in range(5, 55, 5)}  # Python native integers
            ),
            html.Div(id="data-preview")
        ]),
        dcc.Tab(label="Scatterplots", children=[
            html.H1("Scatterplot Explorer", style={"text-align": "center"}),
            html.Label("Select X-axis"),
            dcc.Dropdown(
                id="x-axis",
                options=[{"label": col, "value": col} for col in ["gdpPercap", "lifeExp", "pop"]],
                value="gdpPercap",
                clearable=False
            ),
            html.Label("Select Y-axis"),
            dcc.Dropdown(
                id="y-axis",
                options=[{"label": col, "value": col} for col in ["gdpPercap", "lifeExp", "pop"]],
                value="lifeExp",
                clearable=False
            ),
            dcc.Graph(id="scatterplot")
        ]),
        dcc.Tab(label="Trend Analysis", children=[
            html.H1("Trend Analysis", style={"text-align": "center"}),
            html.Label("Select a country"),
            dcc.Dropdown(
                id="country-dropdown",
                options=[{"label": country, "value": country} for country in gapminder['country'].unique()],
                value="United States",
                clearable=False
            ),
            dcc.Graph(id="trend-chart")
        ]),
        dcc.Tab(label="Map Visualization", children=[
            html.H1("Map Visualization", style={"text-align": "center"}),
            html.Label("Select Year"),
            dcc.Slider(
                id="year-slider",
                min=int(gapminder['year'].min()),  # Convert to Python int
                max=int(gapminder['year'].max()),  # Convert to Python int
                step=5,
                value=2007,
                marks={int(year): str(year) for year in gapminder['year'].unique()}  # Convert to Python int
            ),
            html.Label("Select Variable"),
            dcc.Dropdown(
                id="map-variable",
                options=[
                    {"label": "GDP Per Capita", "value": "gdpPercap"},
                    {"label": "Life Expectancy", "value": "lifeExp"},
                    {"label": "Population", "value": "pop"}
                ],
                value="gdpPercap",
                clearable=False
            ),
            dcc.Graph(id="map-chart")
        ]),
        dcc.Tab(label="Correlation Analysis", children=[
            html.H1("Correlation Analysis", style={"text-align": "center"}),
            html.Label("Select Continent"),
            dcc.Dropdown(
                id="continent-dropdown",
                options=[{"label": cont, "value": cont} for cont in gapminder['continent'].unique()],
                value="Asia",
                clearable=False
            ),
            dcc.Graph(id="correlation-matrix")
        ])
    ])
])

# Callbacks for interactivity

# Introduction Tab: Data preview
@app.callback(
    Output("data-preview", "children"),
    Input("row-slider", "value")
)
def update_table(rows):
    preview = gapminder.head(rows).to_dict("records")
    return html.Div([
        html.Table([
            html.Thead(html.Tr([html.Th(col) for col in gapminder.columns])),
            html.Tbody([
                html.Tr([html.Td(cell) for cell in row.values()])
                for row in preview
            ])
        ], style={"width": "100%", "border": "1px solid black", "border-collapse": "collapse"})
    ])

# Scatterplots Tab
@app.callback(
    Output("scatterplot", "figure"),
    [Input("x-axis", "value"),
     Input("y-axis", "value")]
)
def update_scatterplot(x_col, y_col):
    fig = px.scatter(
        gapminder,
        x=x_col,
        y=y_col,
        color="continent",
        size="pop",
        hover_name="country",
        title=f"Scatterplot of {y_col} vs {x_col}"
    )
    return fig

# Trend Analysis Tab
@app.callback(
    Output("trend-chart", "figure"),
    Input("country-dropdown", "value")
)
def update_trend_chart(selected_country):
    country_data = gapminder[gapminder["country"] == selected_country]
    fig = px.line(
        country_data,
        x="year",
        y="lifeExp",
        title=f"Life Expectancy Over Time for {selected_country}",
        markers=True
    )
    return fig

# Map Visualization Tab
@app.callback(
    Output("map-chart", "figure"),
    [Input("year-slider", "value"),
     Input("map-variable", "value")]
)
def update_map_chart(selected_year, variable):
    year_data = gapminder[gapminder["year"] == selected_year]
    fig = px.choropleth(
        year_data,
        locations="country",
        locationmode="country names",
        color=variable,
        hover_name="country",
        title=f"{variable} in {selected_year}",
        color_continuous_scale=px.colors.sequential.Plasma
    )
    return fig

# Correlation Analysis Tab
@app.callback(
    Output("correlation-matrix", "figure"),
    Input("continent-dropdown", "value")
)
def update_correlation_matrix(selected_continent):
    continent_data = gapminder[gapminder["continent"] == selected_continent]
    correlation_matrix = continent_data[["gdpPercap", "lifeExp", "pop"]].corr()
    fig = px.imshow(
        correlation_matrix,
        text_auto=True,
        labels={"color": "Correlation"},
        title=f"Correlation Matrix for {selected_continent}"
    )
    return fig

# Run the app locally
if __name__ == "__main__":
    print("Dash app is running at: http://127.0.0.1:8050/")
    app.run_server(debug=True)
