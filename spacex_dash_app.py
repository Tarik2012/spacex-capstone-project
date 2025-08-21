import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# === 1. Load data ===
spacex_df = pd.read_csv("data/processed/dataset_part_2.csv")

# === 2. Create the app with a Bootstrap theme ===
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "SpaceX Dashboard"

# === 3. Layout with improved header ===
app.layout = html.Div([

    # Hero section
    html.Div([
        html.H1("SpaceX Launch Records Dashboard",
                style={"textAlign": "center", "color": "white",
                       "fontWeight": "bold", "marginBottom": "0"}),
        html.P("Interactive analysis of SpaceX launches",
               style={"textAlign": "center", "color": "lightgray",
                      "marginTop": "5px"})
    ],
    style={
        "background": "linear-gradient(90deg, #0f2027, #203a43, #2c5364)",
        "padding": "40px 20px",
        "textAlign": "center",
        "marginBottom": "30px"
    }),

    # Main content
    dbc.Container([

        # Row 1: Dropdown and Pie chart
        dbc.Row([
            dbc.Col([
                html.Label("Select a launch site:"),
                dcc.Dropdown(
                    id='site-dropdown',
                    options=[{'label': 'All sites', 'value': 'ALL'}] +
                            [{'label': site, 'value': site} for site in spacex_df['LaunchSite'].unique()],
                    value='ALL',
                    placeholder="Select a launch site",
                    searchable=True,
                    style={'marginBottom': '20px'}
                )
            ], width=4),

            dbc.Col([
                dcc.Graph(id='success-pie-chart')
            ], width=8)
        ], align="center"),

        html.Hr(),

        # Row 2: RangeSlider and Scatter plot
        dbc.Row([
            dbc.Col([
                html.Label("Payload range (kg):"),
                dcc.RangeSlider(
                    id='payload-slider',
                    min=int(spacex_df['PayloadMass'].min()),
                    max=int(spacex_df['PayloadMass'].max()),
                    step=100,
                    value=[int(spacex_df['PayloadMass'].min()), int(spacex_df['PayloadMass'].max())],
                    marks={int(x): f"{int(x/1000)}k" for x in range(0, int(spacex_df['PayloadMass'].max())+1, 2000)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], width=12),
        ], style={'marginBottom': 30}),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='success-payload-scatter')
            ], width=12)
        ])

    ], fluid=True)

])

# === 4. Callbacks ===
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df,
                     names='LaunchSite',
                     values='Class',
                     title='Distribution of successful launches by site')
    else:
        filtered_df = spacex_df[spacex_df['LaunchSite'] == selected_site]
        fig = px.pie(filtered_df,
                     names='Class',
                     title=f'Success rate at {selected_site}')
        fig.update_traces(textinfo='percent+label')

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )
    return fig

@app.callback(
    Output('success-payload-scatter', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['PayloadMass'] >= low) & (spacex_df['PayloadMass'] <= high)

    if selected_site == 'ALL':
        filtered_df = spacex_df[mask]
    else:
        filtered_df = spacex_df[(spacex_df['LaunchSite'] == selected_site) & mask]

    fig = px.scatter(
        filtered_df,
        x="PayloadMass",
        y="Class",
        color="BoosterVersion",
        title="Correlation between payload mass and launch success",
        size="PayloadMass",
        hover_data=['LaunchSite']
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        xaxis_title="Payload mass (kg)",
        yaxis_title="Outcome (0 = Failure, 1 = Success)"
    )

    return fig

# === 6. Run server ===
if __name__ == '__main__':
    app.run(debug=True, port=8050)
