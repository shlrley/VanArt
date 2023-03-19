# imports
from dash import dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt


####################
# data wrangling 
public_art_df = pd.read_csv('../data/public-art.csv', sep=';', parse_dates=['YearOfInstallation'])      # import
public_art_df = public_art_df[~public_art_df.Neighbourhood.isna()]  # remove nas
neighbourhoods_list = sorted(list(public_art_df['Neighbourhood'].unique()))
# image 
image_path = 'assets/goofyahh.png' # reference: https://blog.vancity.com/free-activity-exploring-public-art/

####################
# styling 
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.MINTY])

# deployment 
server = app.server

#################### FRONT END
app.layout = dbc.Container([
    # title
    dbc.Row(html.H2('Art in Vancouver Neighbourhoods')),
    html.Br(), html.Br(),
    # image 
    html.Div([
        html.Img(src=image_path, alt='image')], 
        style={'textAlign': 'center', 'width': '100%', 'height': '500px'}
    ),
    html.Br(), html.Br(),
    # multi-select dropdown for choosing neighbourhood
    html.H6('Select Neighbourhood(s)'),
    dbc.Row(
        dbc.Col(
            dcc.Dropdown(
                    id='neighbourhood-widget',
                    value=['Downtown'],  # REQUIRED to show the plot on the first page load
                    options=[{'label': neigh, 'value': neigh} for neigh in neighbourhoods_list],
                    multi = True
                    )
        )
    ),
    html.Br(),
    # double-sided slider for choosing years
    html.H6('Select Year(s)'),
    dcc.RangeSlider(min=0, max=5, 
                    value=[1, 3], 
                    marks={0: '0', 5: '5'}),
    html.Br(),
    # display charts
    html.H6('Charts'),
    dbc.Row([
        dbc.Col(
            html.P('...')
        ),
        dbc.Col(
            html.Iframe(
            id='charts',
            style={'border-width': '0', 'width': '100%', 'height': '800px'}) 
            )
    ])     
])


if __name__ == '__main__':
    app.run_server(debug=True)