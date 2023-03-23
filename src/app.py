# imports
from dash import dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
import plotly.express as px


####################
# data wrangling 
# git push 
public_art_df = pd.read_csv('../data/public-art.csv', sep=';', parse_dates=['YearOfInstallation'])      # import
# local 
#public_art_df = pd.read_csv('data/public-art.csv', sep=';', parse_dates=['YearOfInstallation'])      # import
public_art_df = public_art_df[~public_art_df.Neighbourhood.isna()]              # remove nas
neighbourhoods_list = sorted(list(public_art_df['Neighbourhood'].unique()))     # get list of neighbourhoods
public_art_df['Year Of Installation'] = public_art_df['YearOfInstallation'].dt.year
years_list = sorted(list(public_art_df['Year Of Installation'].unique()))       # get list of years 

start_neighbourhoods_list = ['Downtown', 'Fairview', 'Marpole', 'West End', 'Sunset', 'Oakridge']
#start_neighbourhoods_list = ['Downtown', 'DowntownEastside']

pa_cols = [{'name': 'Title of Work', 'id': 'Title of Work'},
{'name': 'Type', 'id': 'Type'},
{'name': 'Neighbourhood', 'id': 'Neighbourhood'},
{'name': 'Year Installed', 'id': 'Year Of Installation'},
{'name': 'Site Address', 'id': 'SiteAddress'}]
# image 
image_path = 'assets/goofyahh.png' # reference: https://blog.vancity.com/free-activity-exploring-public-art/
image_2_path = 'assets/girlinwetsuit2.png' # reference: https://covapp.vancouver.ca/PublicArtRegistry/ArtworkDetail.aspx?ArtworkId=97

# get latitude and longitude for map 
public_art_df[['latitude', 'longitude']] = public_art_df.geo_point_2d.str.split(", ", expand=True).astype(float)    # cred: Robin

####################
# styling 
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.MORPH])

# title
app.title = "VanArt"

# deployment 
server = app.server

#################### FRONT END
app.layout = dbc.Container([

    # title
    html.Br(),
    dbc.Row([
        # SIDE BAR COLUMN
        dbc.Col([
            #html.Br(),
            html.H3('Art in Vancouver Neighbourhoods', style={'font-weight': 'bold'}),
            html.Br(),
            html.P('Welcome!', style={'color': '#4682B4', 'font-weight': 'bold', 'font-size': '18px'}),
            html.P('Explore art pieces installed around Vancouver by the neighbourhood \
                   and the years they were installed.', style={'font-size': '14px'}),
            # image 
            html.Div([
                html.Img(src=image_2_path, alt='image', 
                style={'textAlign': 'center', 'width': '100%', 'height': '100%'},
                className = 'center')
                ],   
            ),
            #html.P('"Girl in Wetsuit", Elek Imredy', 
            #       style={'font-style': 'italic', 'font-size': '10px'}),
            html.Br(), 
            #html.Hr(),
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
                html.Br(),
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
                        ], 
                    # styling for outside of column 
                    style={'background-color': 'whitesmoke',
                        'padding': 20,
                        'border-radius': 1},
                    md=3),
        # MAIN COLUMN
        dbc.Col([
            # graphs tab 
            dbc.Tabs([
                dbc.Tab([
                    html.Br(),
                    dbc.Col([dcc.Graph(id="map")
                             ],
                            style={'background-color': '#E5E5E5',
                                'padding': 20,
                                'border-radius': 3},
                            md=12),
                ],
                    label='Map'),
                dbc.Tab([
                    dbc.Col([
                        # display chart 1
                        html.Br(),
                        dbc.Row([
                            html.H6('Installations Over Time', style={'font-weight': 'bold'}),
                            html.Iframe(id='charts2',
                                        style={"display": "inline-block", 
                                            'border-width': '0', 
                                            #'width': '200%', 
                                            'height': '345px'
                                            }
                                        ),
                        ], 
                        style={'background-color': 'white',
                            'padding': 20,
                            'border-radius': 3},),
                        html.Br(),
                        # display chart 2
                        dbc.Row([
                            html.H6('Pieces per Neighbourhood', style={'font-weight': 'bold'}),
                            html.Iframe(id='charts',
                                        style={"display": "inline-block", 
                                            'border-width': '0', 
                                            #'width': '200%', 
                                            'height': '165px'
                                            }
                                            ),
                        ], 
                        style={'background-color': 'white',
                            'padding': 20,
                            'border-radius': 3},),
                    ],
                    style={'background-color': '#E5E5E5',
                        'padding': 20,
                        'border-radius': 3},
                    md=12),
                    ],
                    label='Graphs'),
                # table tab 
                dbc.Tab([
                        dbc.Col([
                            dbc.Row([
                                # display table 
                                html.Br(),
                                html.H6('Vancouver Art Data', style={'font-weight': 'bold'}),
                                dash_table.DataTable(
                                    id='table',
                                    columns=pa_cols,
                                    # styling      
                                    page_size=15,
                                    sort_action='native',
                                    page_action='native',
                                    style_data={
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                    },
                                    #fill_width=False,
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
                        style={'background-color': '#E5E5E5',
                        'padding': 20,
                        'border-radius': 3},
                        ),    
                        ], 
                         label='Data')
                         ],),
        ], 
        style={'background-color': '#E5E5E5', #E5E5E5 #EDEDED
               'padding': 20,
               'border-radius': 3},
        md=9)
    ]),   
    html.Br(),
    html.P([
        html.A("GitHub", href = "https://github.com/shlrley/VanArt"),
        ' | Made with 🤍 by Shirley Zhang | UBC MDS \'23 '
    ], 
    style={'color': '#4682B4', 'font-size': '12px'})
    #dbc.Row(html.P('hi')), 
])

#################### BACK END
# map callback  
# cred: Robin + 
# https://plotly.com/python/scattermapbox/
# https://plotly.com/python/mapbox-layers/
@app.callback(
    Output("map", "figure"),
    Input("neighbourhood-widget", "value"),
    Input('startyear-widget', 'value'),
    Input('endyear-widget', 'value')
)
# create map 
# cred: Robin 
def get_map(neighbourhood, startyear, endyear):
    # filter data 
    # neighbourhoods 
    if neighbourhood == []:    # get all neighbourhoods
        public_art_df2 = public_art_df     
    else:   # get selected neighbourhoods
        public_art_df2 = public_art_df[public_art_df['Neighbourhood'].isin(neighbourhood)]   
    # year
    if (startyear == None) & (endyear == None):
        public_art_df2 = public_art_df2 
    elif (startyear == None) & (endyear != None):
        public_art_df2 = public_art_df2.query('YearOfInstallation >= 1901 & YearOfInstallation <= @endyear')
    elif (startyear != None) & (endyear == None):
        public_art_df2 = public_art_df2.query('YearOfInstallation >= @startyear & YearOfInstallation <= 2022')
    elif (int(endyear) < int(startyear)):
        public_art_df2 = public_art_df2 
    else:
        public_art_df2 = public_art_df2.query('YearOfInstallation >= @startyear & YearOfInstallation <= @endyear')

    # plot map 
    fig = px.scatter_mapbox(
        public_art_df2,
        lat="latitude",
        lon="longitude",
        hover_name="Title of Work",
        hover_data={"Neighbourhood":True,
                    "Year Of Installation":True,
                    "Type":True,
                    "latitude":False,
                    "longitude":False,
                    "SiteAddress":True},
        zoom=10.75
    )
    # mapbox style
    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":0,"l":0,"b":0},
        height=600
    )
    return fig

# chart 1 callback
@app.callback(
    Output('charts', 'srcDoc'),
    Input('neighbourhood-widget', 'value'),
    Input('startyear-widget', 'value'),
    Input('endyear-widget', 'value')
    )
# (1) how many art pieces in each neighbourhood 
def create_charts(neighbourhood, startyear, endyear):
    # filter data 
    # neighbourhoods 
    if neighbourhood == []:    # get all neighbourhoods
        public_art_df2 = public_art_df     
    else:   # get selected neighbourhoods
        public_art_df2 = public_art_df[public_art_df['Neighbourhood'].isin(neighbourhood)]   
    # year
    if (startyear == None) & (endyear == None):
        public_art_df2 = public_art_df2 
    elif (startyear == None) & (endyear != None):
        public_art_df2 = public_art_df2.query('YearOfInstallation >= 1901 & YearOfInstallation <= @endyear')
    elif (startyear != None) & (endyear == None):
        public_art_df2 = public_art_df2.query('YearOfInstallation >= @startyear & YearOfInstallation <= 2022')
    elif (int(endyear) < int(startyear)):
        public_art_df2 = public_art_df2 
    else:
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

# chart 2 callback
@app.callback(
    Output('charts2', 'srcDoc'),
    Input('neighbourhood-widget', 'value'),
    Input('startyear-widget', 'value'),
    Input('endyear-widget', 'value')
    )
# (2) years art pices were installed 
def create_charts2(neighbourhood, startyear, endyear):
    # filter data 
    # neighbourhoods 
    if neighbourhood == []:    # get all neighbourhoods
        public_art_df2 = public_art_df     
    else:   # get selected neighbourhoods
        public_art_df2 = public_art_df[public_art_df['Neighbourhood'].isin(neighbourhood)]   
    # year
    if (startyear == None) & (endyear == None):
        public_art_df2 = public_art_df2 
    elif (startyear == None) & (endyear != None):
        public_art_df2 = public_art_df2.query('YearOfInstallation >= 1901 & YearOfInstallation <= @endyear')
    elif (startyear != None) & (endyear == None):
        public_art_df2 = public_art_df2.query('YearOfInstallation >= @startyear & YearOfInstallation <= 2022')
    elif (int(endyear) < int(startyear)):
        public_art_df2 = public_art_df2 
    else:
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
        height=275,
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
    # filter data 
    # neighbourhoods 
    if neighbourhood == []:    # get all neighbourhoods
        public_art_df2 = public_art_df     
    else:   # get selected neighbourhoods
        public_art_df2 = public_art_df[public_art_df['Neighbourhood'].isin(neighbourhood)]   
    # year
    if (startyear == None) & (endyear == None):
        public_art_df2 = public_art_df2 
    elif (startyear == None) & (endyear != None):
        public_art_df2 = public_art_df2.query('YearOfInstallation >= 1901 & YearOfInstallation <= @endyear')
    elif (startyear != None) & (endyear == None):
        public_art_df2 = public_art_df2.query('YearOfInstallation >= @startyear & YearOfInstallation <= 2022')
    elif (int(endyear) < int(startyear)):
        public_art_df2 = public_art_df2 
    else:
        public_art_df2 = public_art_df2.query('YearOfInstallation >= @startyear & YearOfInstallation <= @endyear')
    
    # create data
    data = public_art_df2.to_dict('records')
    # return 
    return data

if __name__ == '__main__':
    app.run_server(debug=True)