# imports
from dash import dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt


####################
# data wrangling 
public_art_df = pd.read_csv('data/public-art.csv', sep=';', parse_dates=['YearOfInstallation'])      # import
public_art_df = public_art_df[~public_art_df.Neighbourhood.isna()]              # remove nas
neighbourhoods_list = sorted(list(public_art_df['Neighbourhood'].unique()))     # get list of neighbourhoods
public_art_df['Year Of Installation'] = pd.DatetimeIndex(public_art_df['YearOfInstallation']).year  # Add a column with just year
pa_cols = [{'name': 'Title of Work', 'id': 'Title of Work'},
{'name': 'Type', 'id': 'Type'},
{'name': 'Neighbourhood', 'id': 'Neighbourhood'},
{'name': 'Year Installed', 'id': 'Year Of Installation'},
{'name': 'SiteAddress', 'id': 'SiteAddress'}]
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
        style={'textAlign': 'center', 'width': '100%', 'height': '70%'}
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
    dbc.Row([
        # display charts
        dbc.Col([
            html.H6('Charts'),
            html.Iframe(
            id='charts',
            style={'border-width': '0', 'width': '100%', 'height': '800px'}) 
        ]),
        # display table 
        dbc.Col([
            html.H6('Data'),
            html.Br(), html.Br(),
            dash_table.DataTable(
                id='table',
                columns=pa_cols,
                # styling      
                page_size=10,
                sort_action='native',
                page_action='native',
                fill_width=False,
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'}],
                 style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'},
                style_cell = {
                'font_family': 'arial',
                'font_size': '12px',
                'text_align': 'center'
                 }
            )
        ])
    ]),    
])

#################### BACK END
# chart callback
@app.callback(
    Output('charts', 'srcDoc'),
    Input('neighbourhood-widget', 'value')
    )
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

# table callback
@app.callback(
    Output('table', 'data'),
    Input('neighbourhood-widget', 'value'))
# update filtering of table 
def update_table(neighbourhood):
    #filter the data 
    public_art_df2 = public_art_df[public_art_df['Neighbourhood'].isin(neighbourhood)]
    # create data
    data = public_art_df2.to_dict('records')
    # return 
    return data

if __name__ == '__main__':
    app.run_server(debug=True)