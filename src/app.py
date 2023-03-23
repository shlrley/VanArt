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
public_art_df['Year Of Installation'] = public_art_df['YearOfInstallation'].dt.year
years_list = sorted(list(public_art_df['Year Of Installation'].unique()))       # get list of years 
start_neighbourhoods_list = ['Downtown', 'Fairview', 'Marpole', 'West End', 'Sunset', 'Oakridge']
pa_cols = [{'name': 'Title of Work', 'id': 'Title of Work'},
{'name': 'Type', 'id': 'Type'},
{'name': 'Neighbourhood', 'id': 'Neighbourhood'},
{'name': 'Year Installed', 'id': 'Year Of Installation'},
{'name': 'SiteAddress', 'id': 'SiteAddress'}]
# image 
image_path = 'assets/goofyahh.png' # reference: https://blog.vancity.com/free-activity-exploring-public-art/
image_2_path = 'assets/girlinwetsuit2.png' # reference: https://covapp.vancouver.ca/PublicArtRegistry/ArtworkDetail.aspx?ArtworkId=97

####################
# styling 
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.MINTY])

# deployment 
server = app.server

#################### FRONT END
app.layout = dbc.Container([

    # title
    html.Br(),
    dbc.Row(),
    dbc.Row([
        # side bar column 
        dbc.Col([
            html.Br(),
            html.H4('Art in Vancouver Neighbourhoods', style={'font-weight': 'bold'}),
            html.Br(),
            html.P('Welcome!', style={'color': '#4682B4', 'font-weight': 'bold', 'font-size': '18px'}),
            html.P('Explore art pieces installed around Vancouver by the neighbourhood \
                   and the years they were installed. 🎨', style={'font-size': '13px'}),
            # image 
            html.Div([
                html.Img(src=image_2_path, alt='image', 
                style={'textAlign': 'center', 'width': '90%', 'height': '90%'})
                ],   
            ),
            #html.P('"Girl in Wetsuit", Elek Imredy', 
            #       style={'font-style': 'italic', 'font-size': '10px'}),
            html.Br(), 
            #html.Hr(),
            # multi-select dropdown for choosing neighbourhood
            html.P('Select Neighbourhood(s)', style={'font-size': '15px'}),
            dbc.Row(
                dbc.Col(
                    dcc.Dropdown(
                            id='neighbourhood-widget',
                            value=start_neighbourhoods_list,  # REQUIRED to show the plot on the first page load
                            options=[{'label': neigh, 'value': neigh} for neigh in neighbourhoods_list],
                            multi = True
                            )
                        )
                    ),
                    html.Br(),
                    dbc.Row([
                        # start year 
                        dbc.Col([
                            html.P('Select Start Year', style={"font-size": "15px"}),
                            dcc.Dropdown(id='startyear-widget',
                                         value='1990',  # REQUIRED to show the plot on the first page load
                                         options=[{'label': year, 'value': year} for year in years_list]
                                )
                        ],
                        md=6
                        ),
                        # end year 
                        dbc.Col([
                            html.P('Select End Year', style={"font-size": "15px"}),
                            dcc.Dropdown(id='endyear-widget',
                                         value='2022',  # REQUIRED to show the plot on the first page load
                                         options=[{'label': year, 'value': year} for year in years_list]
                                )
                            ],
                            md=6
                            )
                        ]),
                    ], 
                    # styling for outside of column 
                    style={'background-color': 'whitesmoke',
                        'padding': 20,
                        'border-radius': 1},
                    md=3),
        # main column 
        dbc.Col([
            dbc.Col([
                    dbc.Row([
                        # display chart 1
                        html.H6('Installations Over Time'),
                        html.Iframe(id='charts2',
                                    style={"display": "inline-block", 
                                           'border-width': '0', 
                                           #'width': '200%', 
                                           'height': '370px'
                                           }),
                    ], 
                    style={'background-color': 'white',
                        'padding': 20,
                        'border-radius': 3},),
                    html.Br(),
                    dbc.Row([
                        # display chart 2
                        html.H6('Pieces per Neighbourhood'),
                        html.Iframe(id='charts',
                                    style={"display": "inline-block", 
                                           'border-width': '0', 
                                           #'width': '200%', 
                                           'height': '175px'
                                           }
                                           ),
                    ], 
                    style={'background-color': 'white',
                        'padding': 20,
                        'border-radius': 3},),
                    html.Br(),
                    dbc.Row([
                        # display table 
                        html.H6('Data'),
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
                                'font_size': '13px',
                                'text_align': 'center'
                            }
                        ),
                    ], 
                    style={'background-color': 'white',
                        'padding': 20,
                        'border-radius': 3},
                    ),
                    ], 
            style={'background-color': 'whitesmoke',
                'padding': 20,
                'border-radius': 3},
            md=12),
        ], 
        style={'background-color': 'whitesmoke', #EDEDED
               'padding': 20,
               'border-radius': 3},
        md=9)
    ]),    
])

#################### BACK END
# chart1 callback
@app.callback(
    Output('charts', 'srcDoc'),
    Input('neighbourhood-widget', 'value'),
    Input('startyear-widget', 'value'),
    Input('endyear-widget', 'value')
    )
# (1) how many art pieces in each neighbourhood 
def create_charts(neighbourhood, startyear, endyear):
    #print(years[0])
    print(startyear)
    print(endyear)
    # filter the data  
    public_art_df2 = public_art_df[public_art_df['Neighbourhood'].isin(neighbourhood)]
    public_art_df2 = public_art_df2.query('YearOfInstallation >= @startyear & YearOfInstallation <= @endyear')
    # create bar chart
    bar = alt.Chart(public_art_df2).mark_bar().encode(
        x = alt.X('count()', 
                  title='Number of Pieces',
                  ),
        y = alt.Y('Neighbourhood', sort='x', title=''),
        tooltip = alt.Tooltip(['Neighbourhood', 'count()'])
    ).configure_mark(
        opacity=0.8,
    #).configure_range(
    #    category={'scheme': 'accent'}
    ).properties(
        width=600,
    ).interactive() 
    charts = bar
    return charts.to_html()

# chart callback
@app.callback(
    Output('charts2', 'srcDoc'),
    Input('neighbourhood-widget', 'value'),
    Input('startyear-widget', 'value'),
    Input('endyear-widget', 'value')
    )
# (2) years art pices were installed 
def create_charts2(neighbourhood, startyear, endyear):
    # filter the data  
    public_art_df2 = public_art_df[public_art_df['Neighbourhood'].isin(neighbourhood)]
    public_art_df2 = public_art_df2.query('YearOfInstallation >= @startyear & YearOfInstallation <= @endyear')
    # create line chart
    line = alt.Chart(public_art_df2).mark_line(point=True, size=3, opacity=0.7).encode(
        x=alt.X('YearOfInstallation', title='Year'),
        y=alt.Y('count()', title='Number of Pieces'),
        color=alt.Color('Neighbourhood'),
        tooltip=alt.Tooltip(['Year Of Installation', 'Neighbourhood', 'count()'])
    #).configure_range(
    #    category={'scheme': 'set3'}
    ).properties(
        width=530,
    ).interactive()
    charts = line
    # return 
    return charts.to_html()

# table callback
@app.callback(
    Output('table', 'data'),
    Input('neighbourhood-widget', 'value'),
    Input('startyear-widget', 'value'),
    Input('endyear-widget', 'value')
    )
# update filtering of table 
def update_table(neighbourhood, startyear, endyear):
    #filter the data 
    public_art_df2 = public_art_df[public_art_df['Neighbourhood'].isin(neighbourhood)]
    public_art_df2 = public_art_df2.query('YearOfInstallation >= @startyear & YearOfInstallation <= @endyear')
    # create data
    data = public_art_df2.to_dict('records')
    # return 
    return data

if __name__ == '__main__':
    app.run_server(debug=True)