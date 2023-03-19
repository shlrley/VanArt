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

#################### BACK END
# callback 
@app.callback(
    Output('charts', 'srcDoc'),
    Input('neighbourhood-widget', 'value')
    )
# chart functions
# (1) how many art pieces in each neighbourhood 
def create_charts(neighbourhood):
    # filter the data  
    public_art_df2 = public_art_df[public_art_df['Neighbourhood'].isin(neighbourhood)]
    # create bar chart
    bar = alt.Chart(public_art_df2).mark_bar().encode(
        x = alt.X('count()', title='Number of Art Pieces'),
        y = alt.Y('Neighbourhood', sort='x'),
        tooltip = alt.Tooltip(['Neighbourhood', 'count()'])
    ).interactive() 
    # create line chart
    line = alt.Chart(public_art_df2).mark_line(point=True, size=2, opacity=0.7).encode(
        x=alt.X('YearOfInstallation', title='Year of Installation'),
        y=alt.Y('count()', title='Number of Art Pieces'),
        color=alt.Color('Neighbourhood'),
        tooltip=alt.Tooltip(['YearOfInstallation', 'Neighbourhood', 'count()'])
    ).interactive()
    # combine charts 
    charts = (bar & line)
    # return 
    return charts.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)