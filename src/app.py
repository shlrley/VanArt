# imports
from dash import dash, html, dcc 
import dash_bootstrap_components as dbc

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