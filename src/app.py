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

# styles for the main content, position it to the right and add some padding 
CONTENT_STYLE = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}


# sidebar 
sidebar = html.Div(
    [
        html.H2('VanArt', className='display-4'),
        html.P(      # paragraph
            'Discover Public Art in Vancouver!', className='lead'
        ),    
    ]
)

content = html.Div(style=CONTENT_STYLE)

app.layout = html.Div([sidebar, content])

if __name__ == '__main__':
    app.run_server(debug=True)