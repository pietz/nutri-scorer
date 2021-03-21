"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
#1) FIX: When the 1st upload doesn't have a value in an attribute -> error
#2) Fix: The next ones, probably remember the previous value (needs to be 0 contribution if nan)

#html.Div: inside here we create the layout of the page. (Text, buttons, images) children need []!!!
from datetime import date
import datetime
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Button import Button
from dash_bootstrap_components._components.NavLink import NavLink
import dash_core_components as dcc
from dash_core_components.Markdown import Markdown
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_table as dt
from iris import IRIS
from PIL import Image
import pandas as pd
import base64
import io
import joblib
import plotly.express as px

#dbc.themes.BOOTSTRAP (was originally)
# Minty: https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/minty/bootstrap.min.css
theme = "E:\TechLabs\TechLabs_Group1\assets\bootstrap.min.css"
app = dash.Dash(external_stylesheets=[theme])

def load_data():
     #df = pd.read_csv(csv_path)
     return IRIS("E:\TechLabs\TechLabs_Group1\iris_210118090818.feather")

iris = load_data()

today=date.today()
yesterday = today - datetime.timedelta(days=1)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#516CAD",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Extra stuff for Christopher's function (About you)
# hide_style, show_style, cal_slider_text, cal_slider_reset for styling of calorie calculation page
hide_style = {
                    'display': 'none'
                    }

show_style = {
                      'display': 'block'
                      }

cal_slider_text = {
                      'width': '20%',
                      'verticalAlign': 'top',
                      'display': 'inline-block',
                      }

cal_slider_rest = {
                      'width': '39%',
                      'verticalAlign': 'top',
                      'display': 'inline-block',
                      } 

# Extra stuff for user information that appears on the top of the page.
params = ['Weight (kg)', 'Height (cm)', 'Cals/day (Kcal)', 'Proteins/day (g)', 'Sugar/day (g)']

sidebar = html.Div(
    [
        html.H1([html.Div([dcc.Markdown('''**N**''', style={'color':'#28B463','display':'inline-block'}), 
                        dcc.Markdown(['''**u**'''], style={'color':'#2ECC71','display':'inline-block'}),
                        dcc.Markdown(['''**t**'''], style={'color':'#F7DC6F','display':'inline-block'}),
                        dcc.Markdown(['''**r**'''], style={'color':'#F39C12','display':'inline-block'}),
                        dcc.Markdown(['''**i**'''], style={'color':'#E74C3C','display':'inline-block'})], style={'textAlign':'center','lineHeight':'1px', 'margin-top':'10px', 'fontWeight':'900'}),
                        dcc.Markdown(['''**Scorer**'''], style={'color':'#F7DC6F', 'textAlign':'center', 'fontWeight':'900'}),], className="display-4"),

        html.Hr(style={'background-color':'#fff', 'height':'1px'}),
        html.P(
            "A simple app for your healthy-eating needs", className="lead", style={'color':'#fff', 'textAlign':'center'}
        ),
        dbc.Nav(
            [
                dbc.NavLink("About You", href="/", active="exact"),
                dbc.NavLink("Single Product", href="/single", active="exact"),
                dbc.NavLink("Comparison", href="/page-1", active="exact"),
                dbc.NavLink("Custom Product", href="/page-2", active="exact"),
                dbc.NavLink("Many Products", href="/page-3", active="exact"),
                dbc.NavLink("My Calendar", href="/calendar", active="exact"),
                dbc.NavLink("New Day", href="/newday", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([
    html.Div([
        dcc.Store(id='lastmonth', storage_type='local'),
        dcc.Store(id='store-calendar', storage_type='local'),
        dcc.Store(id='store-user-info', storage_type='local'),
        html.Div(id='update-all', style={'display':'None'}),
        dt.DataTable(
            id = 'user-info',
            columns = [{"name": p, "id": p} for p in params],
            data = [],
            editable=False,
            style_table={'margin-top':'5px', 'borderRadius':'15px','overflow': 'hidden'},
            style_cell={'textAlign':'center', 'font_size':'20px', 'border':'0px','fontWeight':'bold','background-color':'#F1CFD1', 'color':'#000000'},
            style_header={'textAlign':'center', 'border':'0px', 'fontWeight':'bold', 'font_size':'20px','background-color':'#F2B4B6', 'color':'#000000'},
        )
    ], style = {"margin-left": "16rem"}),
    
    dcc.Location(id="url"), sidebar, content
])


# THIS CALLBACK IS FOR THE SIDEBAR
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/single": # THIS IS WHAT HAPPENS ON THE SINGLE PRODUCT PAGE
        return html.Div( # inside html.Div, we create the layout of the page
            [
            html.Div([
                html.H1('Single Product', style={'fontWeight':'bold', }),                  
            ], style={'margin-left':'33%', 'display':'inline-block'}),
            html.Div([
                dbc.Button("?", id="open?", size="lg"),
                dbc.Modal([
                    dbc.ModalHeader("Information", style={'margin-left':'35%'}),
                    dbc.ModalBody(["In this page you can upload a photo of a product and find out its NutriScore."]),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close?", className="ml-auto?",)
                    )
                ],  id="modal?",
                    centered=True,
                ),
            ], style={'margin-left':'27%', 'display':'inline-block','borderRadius':'30px',}),
            html.Hr(),
            html.H2("Upload a photo of the product"),
            dcc.Upload(
                id='upload-image-1',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '50%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'margin-left':'25%'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='output-image-upload-1'),
            
        ], style={'textAlign':'center', })
    elif pathname == "/page-1": # THIS IS WHAT HAPPENS ON THE COMPARISON PAGE 
        return html.Div([
            html.Div([
                    html.H1('Comparison', style={'fontWeight':'bold', }),                  
                ], style={'margin-left':'33%', 'display':'inline-block'}),
                html.Div([
                    dbc.Button("?", id="open?", size="lg"),
                    dbc.Modal([
                        dbc.ModalHeader("Information", style={'margin-left':'35%'}),
                        dbc.ModalBody(["In this page you can upload photos of two products, in order to compare their nutritional information"]),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close?", className="ml-auto?",)
                        )
                    ],  id="modal?",
                        centered=True,
                    ),
                ], style={'margin-left':'27%', 'display':'inline-block','borderRadius':'30px',}),
                html.Hr(),

            html.Div([
                dcc.Upload(
                id='upload-image-1',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '90%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            #html.Div(id='output-image-upload-1'),
            ], style = {'width':'45%', 'display':'inline-block'}),
            html.Div([
                dcc.Upload(
                id='upload-image-2',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '90%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            ], style = {'width':'45%', 'display':'inline-block',}),

            html.Div(id='output-image-upload-1' , style = {'width':'45%', 'display':'inline-block', 'textAlign':'center'}),
            html.Div(id='output-image-upload-2' , style = {'width':'45%', 'display':'inline-block', 'textAlign':'center', 'verticalAlign':'top'}),

        ], style={'textAlign':'center'})
    elif pathname == "/page-2": # THIS IS WHAT HAPPENS ON THE CUSTOM PRODUCT PAGE

        return html.Div([
                html.Div([
                    html.H1('Custom Product', style={'fontWeight':'bold', }),                  
                ], style={'margin-left':'33%', 'display':'inline-block'}),
                html.Div([
                    dbc.Button("?", id="open?", size="lg"),
                    dbc.Modal([
                        dbc.ModalHeader("Information", style={'margin-left':'35%'}),
                        dbc.ModalBody(["In this page you can insert the nutrition values of a single product and get an estimation for its NutriScore!"]),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close?", className="ml-auto?",)
                        )
                    ],  id="modal?",
                        centered=True,
                    ),
                ], style={'margin-left':'27%', 'display':'inline-block','borderRadius':'30px',}),
                html.Hr(),

                html.Div ([
                    html.Div([
                        html.H6("Kcal/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-kcal',
                            placeholder='Enter a value...',
                            type='number',
                            valid=False,
                            style={'borderRadius':'10px'}
                        ),
                    ], style = {'display':'inline-block', 'width':'20%'}),
                    html.Div([
                        html.H6("Fat/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-fat',
                            placeholder='Enter a value...',
                            type='number', 
                            style={'borderRadius':'10px'}
                        ),
                    ], style = {'display':'inline-block', 'margin-left':'40px', 'width':'20%'}),
                    html.Div([
                        html.H6("Saturated Fat/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-sat_fat',
                            placeholder='Enter a value...',
                            type='number',
                            style={'borderRadius':'10px'}
                        ),
                    ], style = {'display':'inline-block', 'margin-left':'40px', 'width':'20%'}),
                    html.Div([
                        html.H6("Proteins/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-proteins',
                            placeholder='Enter a value...',
                            type='number',        
                            style={'borderRadius':'10px'}       
                        ),
                    ], style = {'display':'inline-block', 'margin-left':'40px', 'width':'20%'}),
                    
                ], style = {'textAlign':'center'}),

                html.Div ([
                    html.Div([
                        html.H6("Carbohydrates/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-carbs',
                            placeholder='Enter a value...',
                            type='number',
                            style={'borderRadius':'10px', }
                        ),
                    ], style = {'display':'inline-block', 'width':'20%'}),
                    html.Div([
                        html.H6("Fibers/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-fibers',
                            placeholder='Enter a value...',
                            type='number',
                            style={'borderRadius':'10px'}
                        ),
                    ], style = {'display':'inline-block', 'margin-left':'40px', 'width':'20%'}),
                    html.Div([
                        html.H6("Sugars/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-sugars',
                            placeholder='Enter a value...',
                            type='number',
                            style={'borderRadius':'10px'}
                        ),
                    ], style = {'display':'inline-block', 'margin-left':'40px', 'width':'20%'}),
                    html.Div([
                        html.H6("Salt/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-salt',
                            placeholder='Enter a value...',
                            type='number',
                            style={'borderRadius':'10px'}
                        ),
                    ], style = {'display':'inline-block', 'margin-left':'40px', 'width':'20%'}),
                    
                ], style = {'textAlign':'center', 'margin-top':'70px'}),
                html.Hr(),
                html.Div([
                    dbc.Button('Calculate NutriScore', id='nutriscore-single-button', n_clicks = 0, style={'margin-top':'30px',}),
                ], style = {'textAlign':'center'}),
                html.Div(id='nutriscore-single-button-output', style = {'textAlign':'center'}),
                html.Hr(),
                html.H5('Warning: The NutriScore is only an estimation and may not be correct'),
            ]
        )
    elif pathname == "/page-3": # THIS IS WHAT HAPPENS ON THE MANY PRODUCTS PAGE    
         return html.Div([
            # I need this many Stores, because these values are essential to calculate the NutriScore
            # and they need to be saved between different functions and callbacks.
            dcc.Store(id='productinfo'), dcc.Store(id='totalgrams'),          
            dcc.Store(id='current_cal', ), dcc.Store(id='current_fat',), 
            dcc.Store(id='current_sat_fat', ), dcc.Store(id='current_prot', ), 
            dcc.Store(id='current_carb', ), dcc.Store(id='current_fiber', ), 
            dcc.Store(id='current_sugar',), dcc.Store(id='current_salt', ),
            dcc.Store(id='total_cal', ), dcc.Store(id='total_fat',), 
            dcc.Store(id='total_sat_fat', ), dcc.Store(id='total_prot', ), 
            dcc.Store(id='total_carb', ), dcc.Store(id='total_fiber', ), 
            dcc.Store(id='total_sugar',), dcc.Store(id='total_salt', ),

            html.Div([
                html.H1('Many Products', style={'fontWeight':'bold', }),                  
            ], style={'margin-left':'32%', 'display':'inline-block'}),
            html.Div([
                dbc.Button("?", id="open?", size="lg"),
                dbc.Modal([
                    dbc.ModalHeader("Information", style={'margin-left':'35%'}),
                    dbc.ModalBody(["In this page you can insert many products and get an estimation on the total NutriScore of your list!", html.Br(),
                                  "1) Upload a photo of a product.", html.Br(),
                                  "2) Input the amount of the product and then click on Add Product", html.Br(),
                                  "3) Repeat the above steps until you have all the desired products. ", html.Br(),
                                  "4) Click on Calculate NutriScore.", html.Br(),]),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close?", className="ml-auto?",)
                    )
                ],  id="modal?",
                    centered=True,
                ),
            ], style={'margin-left':'25%', 'display':'inline-block','borderRadius':'30px',}),
            html.Hr(),

            html.H2("Upload a photo of a product", style={'textAlign':'center',}),
            dcc.Upload(
                id='upload-image-custom',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '50%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'margin-left':'25%'
                },
                # Allow multiple files to be uploaded
                multiple=False
            ),
            html.Div(id='output-image-custom', children=[]),

            html.Hr(),
            html.H2("Products in list", style={'textAlign':'center'}),
            html.Div(id='custom-button-output', children=[], style={'textAlign':'center'}),
            html.Hr(),
            html.H2('List Totals', style={'textAlign':'center'}),
            html.Div([
                html.H5('Total Grams'),
                html.H5(id='totalgrams-value'),
            ], style={'textAlign':'center', 'display':'inline-block'}),
            html.Div([
                html.H5('Total Energy (kcal)'),
                html.H5(id='total_cal-value'), 
            ], style={'textAlign':'center', 'display':'inline-block', 'margin-left':'40px'}),
            html.Div([
                html.H5('Total Fat (g)'),
                html.H5(id='total_fat-value'), 
            ], style={'textAlign':'center', 'display':'inline-block', 'margin-left':'40px'}),
            html.Div([
                html.H5('Total Saturated Fat (g)'),
                html.H5(id='total_sat_fat-value'), 
            ], style={'textAlign':'center', 'display':'inline-block', 'margin-left':'40px'}), 
            html.Div([
                html.H5('Total Protein (g)'),
                html.H5(id='total_prot-value'), 
            ], style={'textAlign':'center', 'display':'inline-block', 'margin-left':'40px'}),
            html.Div([
                html.H5('Total Carbohydrates (g)'),
                html.H5(id='total_carb-value'), 
            ], style={'textAlign':'center', 'display':'inline-block', 'margin-left':'14px'}),
            html.Div([
                html.H5('Total Sugar (g)'),
                html.H5(id='total_sugar-value'),  
            ], style={'textAlign':'center', 'display':'inline-block', 'margin-left':'40px'}),
            html.Div([
                html.H5('Total Fibers (g)'),
                html.H5(id='total_fiber-value'),  
            ], style={'textAlign':'center', 'display':'inline-block', 'margin-left':'40px'}),
            html.Div([
                html.H5('Total Salt (g)'),
                html.H5(id='total_salt-value'),  
            ], style={'textAlign':'center', 'display':'inline-block', 'margin-left':'40px'}),
            
            html.Hr(),
            dbc.Button('Calculate NutriScore', id='nutriscore-button', n_clicks = 0,),
            html.Div(id='nutriscore-button-output'),
         ], style={'textAlign':'center'})
    elif pathname == "/":# THIS IS WHAT HAPPENS ON THE ABOUT YOU PAGE
        return html.Div(
            [   
                
                

                html.H1("Calorie Calculator", style={'textAlign':'center'}),
                #html.H5(id='store-user-info-value'),
                html.Hr(),
                html.H2("Enter your parameters:"),
                html.Hr(),
                # Box with four boxes (inline) inside
                html.Div([
                    html.Div([
                        html.H4("Enter your sex"),
                        dcc.Dropdown(
                            id='sex',
                            options=[
                                {'label': 'female', 'value': 'female'},
                                {'label': 'male', 'value': 'male'},
                            ],
                            value='sex',
                            style={'width': '180px', 'height': '35px'},                                   
                        ),
                    ],style={'width': '24%', 'display': 'inline-block','vertical-align': 'top'}),
                    html.Div([                            
                        html.H4("Enter your Age"),
                        html.Div(dcc.Input(id='input_age', type='number', placeholder='Age in years', min=1, style={'width': '180px', 'height': '35px'},)),                                
                        ],style={'width': '24%', 'display': 'inline-block','vertical-align': 'top'}),
                    html.Div([                      
                        html.H4("Enter your weight"),
                        html.Div(dcc.Input(id='input_weight', type='number', placeholder='Weight in kg', min=1, style={'width': '180px', 'height': '35px'},)),                                
                        ],style={'width': '24%', 'display': 'inline-block','vertical-align': 'top'}),
                    html.Div([   
                        html.H4("Enter your height"),
                        dcc.Input(id='input_height', type='number', placeholder='Height in cm', min=1, style={'width': '180px', 'height': '35px'},),
                        #html.P("cm", style={'width': '12%', 'verticalAlign': 'mid', 'display': 'inline-block'})
                        ],style={'width': '24%', 'display': 'inline-block','vertical-align': 'top', 'textAlign':'center'}),
                ]),
                html.Div([
                    html.Button('Calculate', id='calculateCal')
                ], style={'textAlign':'center', 'margin-top':'30px'}),
                html.Div([
                    html.Div(id='hidden-cal-container', style=hide_style), #hidden container for importing the simple Calorie need to PAL Calculation
                    html.Hr(),
                    html.Div(id='output-container-button',
                        children='You need to fill out every box'),
                ]),
                html.Div([
                    html.Button('click here', id='PAL_button', style=hide_style),
                ]),

                # Big Div-Block which includes: Slider on the left & Piechart on the right (not yet) & the result at bottom
                # First not shown
                html.Div([
                    html.Hr(),
                    # Left block with Sliders
                    html.Div([
                        html.Div([
                            html.Div([
                                html.P("Sleep"),
                            ], style=cal_slider_text),
                            html.Div([
                                dcc.Slider(id='slider-sleep', min=0, max=24, step=0.5,value=6,),
                            ], style=cal_slider_rest),
                            html.Div([
                                html.Div(id='slider-output-sleep'),
                            ], style=cal_slider_rest),
                        ]),
                        html.Div([
                            html.Hr(),
                            html.Div([
                                html.P("Light work (Office)"),
                            ], style=cal_slider_text),
                            html.Div([
                                dcc.Slider(id='slider-l-work', min=0, max=24, step=0.5,value=6,),
                            ], style=cal_slider_rest),
                            html.Div([
                                html.Div(id='slider-output-l-work'),
                            ], style=cal_slider_rest),
                        ]),
                        html.Div([
                            html.Hr(),
                            html.Div([
                                html.P("Medium work (Hairstylist)"),
                            ], style=cal_slider_text),
                            html.Div([
                                dcc.Slider(id='slider-m-work', min=0, max=24, step=0.5,value=6,),
                            ], style=cal_slider_rest),
                            html.Div([
                                html.Div(id='slider-output-m-work'),
                            ], style=cal_slider_rest),
                        ]),
                        html.Div([
                            html.Hr(),
                            html.Div([
                                html.P("Heavy work & Sport (Builder)"),
                            ], style=cal_slider_text),
                            html.Div([
                                dcc.Slider(id='slider-h-work', min=0, max=24, step=0.5,value=6,),
                            ], style=cal_slider_rest),
                            html.Div([
                                html.Div(id='slider-output-h-work'),
                            ], style=cal_slider_rest),
                        ]),
                        # Text with Results
                        html.Div(
                            [
                                html.Hr(),
                                html.Div(id='cal-output-container'),
                        ]),                                           
                        html.Div(id='hidden-hours-container', style=hide_style), #hidden container for importing the hours a day for piechart       
                    ],style={'width': '49%', 'display': 'inline-block','vertical-align': 'top',}),
                    
                    # Right block with Piechart
                    html.Div([
                        #Piechart: top, right block                        
                        html.Div([
                            dcc.Graph(id='piechart-calorie'),                            
                        ], style={'height': '300px'}),     
                                          
                    ],style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'top'}),
                ], id='PAL-values', style=hide_style)
            ]),
    elif pathname == "/calendar": # THIS IS WHAT HAPPENS ON THE MY CALENDAR PAGE
        return html.Div([
                html.Div(id='day-remove-output', style={'display':'None'}),
                html.Div([
                    html.H1('My Calendar', style={'fontWeight':'bold', }),                  
                ], style={'margin-left':'37%', 'display':'inline-block'}),
                html.Div([
                    dbc.Button("?", id="open?", size="lg"),
                    dbc.Modal([
                        dbc.ModalHeader("Information", style={'margin-left':'35%'}),
                        dbc.ModalBody(["In this page you can create your calendar which is color coded based on your daily eating habits.", html.Br(),
                                    "In order to add a day to your calendar, visit the 'New Day' page.", html.Br(),]),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close?", className="ml-auto?",)
                        )
                    ],  id="modal?",
                        centered=True,
                    ),
                ], style={'margin-left':'30%', 'display':'inline-block','borderRadius':'30px',}),
                html.Hr(),
                html.Div(id='store-calendar-value', style={'margin-top':'50px'}),
                html.Div([
                    dbc.Button('Press 3 times to reset', id="calendar-reset", style={'height':60, 'margin-top':'40px'}, n_clicks=0),
                    dbc.Modal(
                        [
                            dbc.ModalBody("Calendar succesfully reset"),
                            dbc.ModalFooter(
                                dbc.Button("Close", id="close2", className="ml-auto")
                            ),
                        ],
                        id="modal2",
                        centered=True,
                    ),
                ], style={'textAlign':'center', 'display':'inline-block', 'margin-left':'17%'}),
                html.Div([
                    dbc.Button('Press 3 times to remove a day', id="day-remove", style={'height':60, 'margin-top':'40px'}, n_clicks=0),
                    dbc.Modal(
                        [
                            #dbc.ModalHeader("Header"),
                            dbc.ModalBody("Day succesfully removed"),
                            dbc.ModalFooter(
                                dbc.Button("Close", id="close2", className="ml-auto")
                            ),
                        ],
                        id="modal22",
                        centered=True,
                    ),
                ], style={'textAlign':'center', 'display':'inline-block', 'margin-left':'25%'}),
            ])
    elif pathname == "/newday": # NEW DAY PAGE
        return html.Div([
            
            dcc.Store(id='productinfo'), dcc.Store(id='today-products', storage_type='local', data=[]),
            dcc.Store(id='day-total-cal', storage_type='local'),
            dcc.Store(id='day-total-prot', storage_type='local'),
            dcc.Store(id='day-total-sugar', storage_type='local'),
            dcc.Store(id='current_cal', ), dcc.Store(id='current_fat',), 
            dcc.Store(id='current_sat_fat', ), dcc.Store(id='current_prot', ), 
            dcc.Store(id='current_carb', ), dcc.Store(id='current_fiber', ), 
            dcc.Store(id='current_sugar',), dcc.Store(id='current_salt', ),

            html.Div([
                html.H1('New Day', style={'fontWeight':'bold', }),                  
            ], style={'margin-left':'41%', 'display':'inline-block'}),
            html.Div([
                dbc.Button("?", id="open?", size="lg"),
                dbc.Modal([
                    dbc.ModalHeader("Information", style={'margin-left':'35%'}),
                    dbc.ModalBody(["In this page you can insert all the products that you have consumed today and then save the day in your calendar.", html.Br(),
                                  "1) Choose a way to add a product.", html.Br(),
                                  "2) Fill in the required information.", html.Br(),
                                  "3) Click on Add Product to Day. ", html.Br(),
                                  "4) Once you have all the products you want, click on Add Day.", html.Br(),
                                  "The day will be added to your calendar."]),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close?", className="ml-auto?",)
                    )
                ],  id="modal?",
                    centered=True,
                ),
            ], style={'margin-left':'35%', 'display':'inline-block','borderRadius':'30px',}),
            html.Hr(),
            html.Div([
                dbc.Button('Add with nutrition values', id='button-nutvalue',  n_clicks=0,
                            style={'display':'inline-block',
                                    'textAlign':'center'}),
                dbc.Button('Add with product image', id='button-prodimage', n_clicks=0, 
                            style={'display':'inline-block',
                                    'margin-left':'100px'}),

            ], style={'textAlign':'center'}),
            html.Hr(),
            html.Div(id='buttons-choice-output'),
            html.Hr(),
            html.H4('Consumed Today', style={'textAlign':'center'}),
            html.Div(id='myday-button-output', style={'display':'None'}),
            html.Div(id='myday-button2-output', style={'display':'None'}),
            html.Div(id='today-products-value',),
            html.Hr(),
            html.Div([
                dbc.Button("Add Day", id="add-day", style={'height':60, 'width':'20%', 'margin-top':'40px'}, n_clicks=0),
                dbc.Modal(
                    [
                        dbc.ModalBody("Day succesfully added to Calendar"),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close", className="ml-auto")
                        ),
                    ],
                    id="modal",
                    centered=True,
                ),
            ], style={'textAlign':'center'}),
            html.Div(children = [], id='calendar-div', style = {'textAlign':'left', 'margin-top':'20px', 'display':'None'}),
            
        ])        

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

#*********************************************************************************************
#*                              CALLBACKS FOR "SINGLE PRODUCT"                               *
#*********************************************************************************************
def parse_contents(contents, filename, date):
    b64_body = contents
    b64_body = contents.split(",")[1]
    decoded = base64.b64decode(b64_body)
    raw = io.BytesIO(decoded)
    img = Image.open(raw).convert("RGB")
    img = img.rotate(270)                                   
    id = iris.search(img)[0]      
    brand = iris.meta.loc[id, "brands"]
    product = iris.meta.loc[id, "product_name"]
    row = iris.meta.loc[id]

    return html.Div([
        html.Hr(),
        html.Div([
            html.H5(brand + ' - ' + product),

            html.Img(src=contents, style={'height':300,}),

        ], style = {'width':'45%','display':'inline-block','textAlign':'center', 'verticalAlign':'top',}),

        html.Div([
            
            html.H5("Calories: " + str(round(row["energy-kcal_100g"], 1))),
            html.H5("Protein: " + str(round(row["proteins_100g"], 1)) + "g"),
            html.H5("Carbs: " + str(round(row["carbohydrates_100g"], 1)) + "g"),
            html.H5("Fat: " + str(round(row["fat_100g"], 1)) + "g"),
            html.H5("Sugar: " + str(round(row["sugars_100g"], 1)) + "g"),
            html.H5("Salt: " + str(round(row["salt_100g"], 3)) + "g"),
            html.Img(src="assets/" + row["nutriscore_grade"] + ".png", style={'height':100, 'width':200}),
        ], style = {'width':'45%','display':'inline-block','verticalAlign':'center'}),
        html.Hr(),
        html.H5('Warning: NutriScore is estimated and may not be correct.', style={'textAlign':'left'}),
    ])
         
#THIS CALLBACK IS FOR THE 1ST UPLOADER
@app.callback(Output('output-image-upload-1', 'children'),
              Input('upload-image-1', 'contents'),
              State('upload-image-1', 'filename'),
              State('upload-image-1', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

# THIS CALLBACK IS FOR THE 2ND UPLOADER
@app.callback(Output('output-image-upload-2', 'children'),
              Input('upload-image-2', 'contents'),
              State('upload-image-2', 'filename'),
              State('upload-image-2', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

#*********************************************************************************************
#*                              CALLBACKS FOR "MANY PRODUCTS"                                *
#*********************************************************************************************
# This callback is called when an image is uploaded and the only thing it does, is that it calls the
# function below which is called "parse_contents_custom". Everything happens in that function.
@app.callback(Output('output-image-custom', 'children'),
              Input('upload-image-custom', 'contents'))
def update_ingredient (contents):
    if contents is not None:
        children = [ parse_contents_custom(contents) ]
        return children

# This function is probably the most important. The "contents" variable holds the information of the
# image that is uploaded from the "dcc.Uploader" component. After every "print" of a nutrition
# attribute, the corresponding Store is called, so that the value of each attribute is saved in a
# Store. Inside here, there is also the Input component for giving the quantity, as well as the
# button that "accepts" the product and "includes" it in the recipe.
def parse_contents_custom (contents):
    b64_body = contents
    b64_body = contents.split(",")[1]
    decoded = base64.b64decode(b64_body)
    raw = io.BytesIO(decoded)
    img = Image.open(raw).convert("RGB")
    img = img.rotate(270)                                   
    id = iris.search(img)[0]      
    brand = iris.meta.loc[id, "brands"]
    product = iris.meta.loc[id, "product_name"]
    row = iris.meta.loc[id]

    return html.Div([
        html.Div([
            html.H5(brand + ' - ' + product, id='productinfo-input'),
            html.Img(src=contents, style={'height':300, }),
        
        ], style = {'width':'30%','display':'inline-block','textAlign':'center','verticalAlign':'top'}),

        html.Div([
            html.H5("Calories: " + str(round(row["energy-kcal_100g"], 1))),
            html.Div(row["energy-kcal_100g"], id='current_cal-input', style={'display':'None'}),
            html.H5("Protein: " + str(round(row["proteins_100g"], 1)) + "g"),
            html.Div(row["proteins_100g"], id='current_prot-input', style={'display':'None'}),
            html.H5("Carbs: " + str(round(row["carbohydrates_100g"], 1)) + "g"),
            html.Div(row["carbohydrates_100g"], id='current_carb-input', style={'display':'None'}),
            html.H5("Fat: " + str(round(row["fat_100g"], 1)) + "g"),
            html.Div(row["fat_100g"], id='current_fat-input', style={'display':'None'}),
            html.H5("Sugar: " + str(round(row["sugars_100g"], 1)) + "g"),
            html.Div(row["sugars_100g"], id='current_sugar-input', style={'display':'None'}),
            html.H5("Salt: " + str(round(row["salt_100g"], 3)) + "g"),
            html.Div(row["salt_100g"], id='current_salt-input', style={'display':'None'}),
            html.Div(row["fiber_100g"], id='current_fiber-input', style={'display':'None'}),
            html.Div(row["saturated-fat_100g"], id='current_sat_fat-input', style={'display':'None'}),

            html.Img(src="assets/" + row["nutriscore_grade"] + ".png", style={'height':100, 'width':200}),
        ], style = {'width':'30%','display':'inline-block','verticalAlign':'bottom','textAlign':'center'}),

        html.Div([
            html.H6("Amount of grams"),
            dbc.Input(
                id= 'input-custom',
                placeholder='Enter a value...',
                type='number',
                value='',
            ),
            dbc.Button('Add Product', id='custom-button', n_clicks = 0, style={'verticalAlign':'bottom', 'width':200, 'height':40, "margin-top": "15px"}),
        ], style = {'width':'30%','display':'inline-block','verticalAlign':'center','textAlign':'center', "margin-top": "100px"}),

    ])

# This callback is for the button that adds the product to the recipe. Inside the callback function,
# the values of the Stores that store the >TOTAL< values are refreshed. Since i want to update those 
# values, i need the States(data) of all the Stores that keep the nutrition values of the product 
# that is uploaded currently. In lines 595-603 when a user clicks, the program takes the value of 
# a nutrition attribute, multiplies it with the quantity that the user has specified and then it
# adds the value to the Store that keeps the TOTAL for that attribute. Line 607 is written this way
# because when a new ingredient is added, i want it to be shown in the next line of the page, 
# instead of overwriting whatever there was on the first line. (So in the end all the ingredients
# are shown in a list, from the first to the last)
@app.callback(Output('custom-button-output','children'),
              Input('custom-button', 'n_clicks'),
              State('input-custom', 'value'),
              State('custom-button-output','children'),
              State('productinfo','data'),
              State('current_cal','data'), State('current_fat','data'), State('current_sat_fat','data'),
              State('current_prot','data'), State('current_carb','data'), State('current_fiber','data'),
              State('current_sugar','data'), State('current_salt', 'data'))
def button_functionality(n_clicks, value, children, productinfo, currentcal, currentfat, currentsatfat,
                        currentprot, currentcarb, currentfiber, currentsugar, currentsalt):
    if (value != '' and n_clicks<2):
  
        new_ingredient = html.Div ([
            html.H5(productinfo, style={'display':'inline-block'}),
            html.H5(": " + str(value) + "g", style={'display':'inline-block'}),
            html.Div(value, id='totalgrams-input', style={'display':'None'} ),
            html.Div(currentcal*value/100, id='total_cal-input', style={'display':'None'}),
            html.Div(currentfat*value/100, id='total_fat-input', style={'display':'None'}),
            html.Div(currentsatfat*value/100, id='total_sat_fat-input', style={'display':'None'}),
            html.Div(currentprot*value/100, id='total_prot-input', style={'display':'None'}),
            html.Div(currentcarb*value/100, id='total_carb-input', style={'display':'None'}),
            html.Div(currentfiber*value/100, id='total_fiber-input', style={'display':'None'}),
            html.Div(currentsugar*value/100, id='total_sugar-input', style={'display':'None'}),
            html.Div(currentsalt*value/100, id='total_salt-input', style={'display':'None'}),
        ])
        children.append(new_ingredient)
        return children
    else:
        raise PreventUpdate

# This callback is for the button that calculates the NutriScore. To calculate the NutriScore, we 
# need the total amount of the recipe in grams (which is given from the State of the Store with 
# id='totalgrams'), as well as the total of each individual nutrition attribute (energy, fat, etc.).
# Once these values are passed on to a variable, the only thing left to do is create the correct
# structures to pass to the saved model. (the finalized_model.sav file in the folder). The final
# NutriScore is added to the Y_test variable.
@app.callback(Output('nutriscore-button-output','children'),
              Input('nutriscore-button','n_clicks'),
              State('totalgrams','data'), State('total_cal','data'), State('total_fat','data'),
              State('total_sat_fat','data'), State('total_prot','data'), State('total_carb','data'),
              State('total_fiber','data'), State('total_sugar','data'), State('total_salt','data'))
def nutriscore_button(n_clicks, totalgrams, totalcal, totalfat, totalsatfat, totalprot, totalcarb,
                        totalfiber, totalsugar, totalsalt):
    if totalgrams is not None:
        x_cols = ["energy-kcal_100g", "fat_100g", "saturated-fat_100g", "proteins_100g", 
                "carbohydrates_100g", "fiber_100g", "sugars_100g", "salt_100g"]

        X_test = pd.DataFrame([[totalcal*(100/totalgrams),totalfat*(100/totalgrams),
                                totalsatfat*(100/totalgrams),totalprot*(100/totalgrams),
                                totalcarb*(100/totalgrams),totalfiber*(100/totalgrams),
                                totalsugar*(100/totalgrams),totalsalt*(100/totalgrams)]], 
                                columns=list(x_cols))
        Y_test = pd.DataFrame([['e']], columns=list('A'))
        loaded_model = joblib.load('finalized_model.sav')
        Y_test = loaded_model.predict(X_test)

        return html.Div([
            html.H5('NutriScore is: ' + Y_test)
        ])
    else:
        raise PreventUpdate

# This callback helps to store the information (Brand - ProductName) of the product that is currently
# uploaded. (Store callback id='productinfo'). This is called in line 539. The 'children' arguement
# on the Input is the left part of the Div in line 539, "brand + ' - ' + product". This is then
# passed onto the variable brand and if that value is not None, it is then store onto the data
# attribute of the Store and available anytime i need it.

@app.callback(Output('productinfo', 'data'),
              Input('productinfo-input', 'children'),
              State('productinfo', 'data'))
def on_value(brand, data):
    if brand is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    #Give a default data dict with 0 clicks if there's no data.
    data = brand or 'No Data'

    return data
# Output callback of the above Store
@app.callback(Output('productinfo-value', 'children'),
                # Since we use the data prop in an output,
                # we cannot get the initial data on load with the data prop.
                # To counter this, you can use the modified_timestamp
                # as Input and the data as State.
                # This limitation is due to the initial None callbacks
                # https://github.com/plotly/dash-renderer/pull/81
                Input('productinfo', 'modified_timestamp'),
                State('productinfo', 'data'))
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate

    data = data or {}

    return data

# This callback is for the Store that holds the totalgrams of the recipe. This is called in line 600.
# Once i get the quantity of the current ingredient, i add it to the "data" variable of this Store.
@app.callback(Output('totalgrams', 'data'),
              Input('totalgrams-input', 'children'),
              State('totalgrams', 'data'))
def on_value(value, data):
    if value is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    #Give a default data dict with 0 clicks if there's no data.
    data = data or 0
    data = data + value

    return data
# Output callback of the above Store
@app.callback(Output('totalgrams-value', 'children'),
                # Since we use the data prop in an output,
                # we cannot get the initial data on load with the data prop.
                # To counter this, you can use the modified_timestamp
                # as Input and the data as State.
                # This limitation is due to the initial None callbacks
                # https://github.com/plotly/dash-renderer/pull/81
                Input('totalgrams', 'modified_timestamp'),
                State('totalgrams', 'data'))
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate

    data = data or {}

    return data

# CALLBACK FOR STORING THE NEEDED VALUES STARTS HERE
for store in ('current_cal', 'current_fat','current_sat_fat', 'current_prot','current_carb',
'current_fiber', 'current_sugar','current_salt'):

    # add a value to the appropriate store
    @app.callback(Output(store, 'data'),
                  Input('{}-input'.format(store), 'children'),
                  State(store, 'data'))
    def on_value(value, data):
        if value is None:
            # prevent the None callbacks is important with the store component.
            # you don't want to update the store for nothing.
            value=0.1

        #Give a default data dict with 0 clicks if there's no data.
        data = data or 0

        data = value
        return data

    @app.callback(Output('{}-value'.format(store), 'children'),
                  # Since we use the data prop in an output,
                  # we cannot get the initial data on load with the data prop.
                  # To counter this, you can use the modified_timestamp
                  # as Input and the data as State.
                  # This limitation is due to the initial None callbacks
                  # https://github.com/plotly/dash-renderer/pull/81
                  Input(store, 'modified_timestamp'),
                  State(store, 'data'))
    def on_data(ts, data):
        if ts is None:
            raise PreventUpdate

        data = data or {}

        return round(data,1)

# This callback is for the Stores that hold the total values of EACH nutrition attribute of the
# whole recipe. It is called in lines 601-608. If i didn't have lines thw two lines below 
# ("for store in"), i would need 8 different callbacks for the Stores (1 for each attribute). 
# This way less lines are needed. 
for store in ('total_cal', 'total_fat','total_sat_fat', 'total_prot','total_carb',
'total_fiber', 'total_sugar','total_salt'):

    # add a value to the appropriate store
    @app.callback(Output(store, 'data'),
                  Input('{}-input'.format(store), 'children'),
                  State(store, 'data'))
    def on_value(value, data,):
        if value is None:
            # prevent the None callbacks is important with the store component.
            # you don't want to update the store for nothing.
            raise PreventUpdate

        #Give a default data dict with 0 clicks if there's no data.
        data = data or 0

        data = data + value
        return data

    @app.callback(Output('{}-value'.format(store), 'children'),
                  # Since we use the data prop in an output,
                  # we cannot get the initial data on load with the data prop.
                  # To counter this, you can use the modified_timestamp
                  # as Input and the data as State.
                  # This limitation is due to the initial None callbacks
                  # https://github.com/plotly/dash-renderer/pull/81
                  Input(store, 'modified_timestamp'),
                  State(store, 'data'))
    def on_data(ts, data):
        if ts is None:
            raise PreventUpdate

        data = data or {}

        return round(data,1)

#*********************************************************************************************
#*                              CALLBACKS FOR "CUSTOM PRODUCT"                               *
#*********************************************************************************************
# For this page, only one callback is needed. This is for the "Calculate NutriScore" button.
# It is executed when the user clicks the button (Input) and it is given the values of every input
# box (States). Afterwards, there is a check to see that every input box has some value and if so,
# i create a dataframe with a single row (the values of the product). Then i load the model that we
# have already created using the classifier and just output the NutriScore.
@app.callback(Output('nutriscore-single-button-output','children'),
              Input('nutriscore-single-button','n_clicks'),
              State('input-kcal','value'), State('input-fat','value'), State('input-sat_fat','value'),
              State('input-proteins','value'), State('input-carbs','value'), State('input-fibers','value'),
              State('input-sugars','value'), State('input-salt','value'),)
def nutriscore_button_single (n_clicks, kcal, fat, sat_fat, proteins, carbs, fibers, sugars, salt):
    #for value in (kcal, fat, sat_fat, proteins, carbs, fibers, sugars, salt):
        if (kcal is None or fat is None or sat_fat is None or proteins is None or carbs is None or 
            fibers is None or sugars is None or salt is None):
            return html.Div('Please insert a number for every value')

        else:
            x_cols = ["energy-kcal_100g", "fat_100g", "saturated-fat_100g", "proteins_100g", 
                        "carbohydrates_100g", "fiber_100g", "sugars_100g", "salt_100g"]

            X_test = pd.DataFrame([ [kcal, fat, sat_fat, proteins, carbs, fibers, sugars, salt] ], 
                                        columns=list(x_cols))
            Y_test = pd.DataFrame([['e']], columns=list('A'))
            loaded_model = joblib.load('finalized_model.sav')
            Y_test = loaded_model.predict(X_test)
        
            return html.Div([
                    #html.H5('The NutriScore of your product is:'),
                    html.Img(src="assets/" + str(Y_test)[2] + ".png", style = {'height':150}),
                ], style = {'textAlign':'center'})

#Callback to make input boxes red/green based on user input.
for type in ('kcal', 'fat','sat_fat', 'proteins','carbs',
'fibers', 'sugars','salt'):

    @app.callback(Output('input-{}'.format(type), 'valid'),
                Output('input-{}'.format(type), 'invalid'),
                Input('input-{}'.format(type), 'value'), prevent_initial_call=True)
    def valid_input(value):
        if value>0:
            return True, False         
        else: 
            return False, True
#*********************************************************************************************
#*                              CALLBACKS FOR "ABOUT YOU"                                    *
#*********************************************************************************************
# Present the results of first CALORIE CALCULATION
@app.callback(
    Output('output-container-button', 'children'),
    Output(component_id='PAL_button', component_property='style'),
    Output('hidden-cal-container', 'children'),
    Input('calculateCal', 'n_clicks'),
    State('input_age', 'value'),
    State('input_weight', 'value'),
    State('input_height', 'value'),
    State('sex', 'value'))
def update_cal_output(n_clicks,input_age, input_weight, input_height, sex):
    if input_age and input_weight and input_height and sex is not None:
        if sex == 'female':
            x = int(655.1 + (9.6 * input_weight) + (1.8 * input_height) - (4.7 * input_age))
            info = [input_weight, input_height, x, 0.75*input_weight, 30]
            return html.Div([
                html.Div('You have a basal metabolic rate of {} kcal calories a day!'.format(x)),
                html.Div(info, id='store-user-info-input', style={'display':'None'}),
                html.Div(info, id='update-all', style={'display':'None'}),         
                html.Hr(),
                html.P("If you would like to determine a more precise calorie consumption:"),
            ]), show_style, x

        if sex == 'male':
            x = int(66.47 + (13.7 * input_weight) + (5 * input_height) - (6.8 * input_age))
            info = [input_weight, input_height, x, 0.75*input_weight, 30]
            return html.Div([
                html.Div('You have a basal metabolic rate of {} kcal calories a day!'.format(x)),
                html.Div(info, id='store-user-info-input', style={'display':'None'}),
                html.Div(info, id='update-all', style={'display':'None'}),
                html.Hr(),
                html.P("If you would like to determine a more precise calorie consumption:"),
            ]), show_style, x
        
        else:
            return 'You need to fill out every box', hide_style, 0

    else:
        return 'You need to fill out every box', hide_style, 0

#THIS CALLBACK JUST MAKES THE DETAILED PART OF CALORIE CALCULATOR VISIBLE
@app.callback(
    dash.dependencies.Output(component_id='PAL-values', component_property='style'),
    [dash.dependencies.Input('PAL_button', 'n_clicks')],)
def show_pal_entries(n_clicks):
    if n_clicks is not None:
        return show_style
    else: 
        return hide_style

# THIS CALLBACK IS FOR VALUE OUTPUT OF SLIDERS (cALORIE CALCULATOR)
@app.callback(
    dash.dependencies.Output('slider-output-sleep', 'children'),
    dash.dependencies.Output('slider-output-l-work', 'children'),
    dash.dependencies.Output('slider-output-m-work', 'children'),
    dash.dependencies.Output('slider-output-h-work', 'children'),
    dash.dependencies.Output('cal-output-container', 'children'),
    dash.dependencies.Output('hidden-hours-container', 'children'),
    [dash.dependencies.Input('PAL_button', 'n_clicks')],
    [dash.dependencies.Input('slider-sleep', 'value')],
    [dash.dependencies.Input('slider-l-work', 'value')],
    [dash.dependencies.Input('slider-m-work', 'value')],
    [dash.dependencies.Input('slider-h-work', 'value')],
    [dash.dependencies.State('hidden-cal-container', 'children')],
    )
def update_output(n_clicks, sleep, lwork, mwork, hwork, x):
    if x is not None:
        if x>0:
            x_new = int(x * (sleep * 0.95 + lwork * 1.45 + mwork * 1.7 + hwork * 2.2) / (sleep + lwork + mwork + hwork))
            piechart_values = sleep, lwork, mwork, hwork,
            print(piechart_values)
            return 'You are sleeping {} hours a day.'.format(sleep), 'You are light working {} hours a day.'.format(lwork), 'You are medium working {} hours a day.'.format(mwork), 'You are heavy working {} hours a day.'.format(hwork), html.Div('You have a basal metabolic rate of {} kcal calories a day!'.format(x_new)), piechart_values
    return 'You are sleeping {} hours a day.'.format(sleep), 'You are light working {} hours a day.'.format(lwork), 'You are medium working {} hours a day.'.format(mwork), 'You are heavy working {} hours a day.'.format(hwork), html.Div('You have a basal metabolic rate of zero kcal calories a day!'), [6, 6, 6 ,6]

#THIS CALLBACK IS FOR THE PIECHART, HOW HARD ARE YOU WORKING?(CALORIE CALCULATOR)
@app.callback(
    Output(component_id='piechart-calorie', component_property='figure'),
    [Input(component_id='PAL_button', component_property='n_clicks')],
    [Input(component_id='hidden-hours-container', component_property='children')],)
def update_piechart(n_clicks, piechart_values):
    
    if piechart_values is not None:
        piechart=px.pie(
                names=['sleep','light work (Office)','medium work (Hairstylist)','hard work (Builder)'],
                values=piechart_values,
                hole=.3,
                )
        return (piechart)
    else:
        return None

#*********************************************************************************************
#*                              CALLBACKS FOR STORING USER INFORMATION                       *
#*********************************************************************************************
# The 2 below callbacks handle the storing of the user data that appears on the table on the top of
# the page. The data that is stored within, is a table that has the values:
# [weight, height, kcal consumption/day, proteins/day, sugars/day]
@app.callback(Output('store-user-info', 'data'),
              Input('store-user-info-input', 'children'),
              State('store-user-info', 'data'))
def on_value(value, data):
    if value is None:
            # prevent the None callbacks is important with the store component.
            # you don't want to update the store for nothing.
            raise PreventUpdate

        #Give a default data dict with 0 clicks if there's no data.
    data = data or 0

    data = value

    return data

@app.callback(Output('store-user-info-value', 'children'),
                # Since we use the data prop in an output,
                # we cannot get the initial data on load with the data prop.
                # To counter this, you can use the modified_timestamp
                # as Input and the data as State.
                # This limitation is due to the initial None callbacks
                # https://github.com/plotly/dash-renderer/pull/81
                Input('store-user-info', 'modified_timestamp'),
                State('store-user-info', 'data'))
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate

    data = data or {}

    return data

# This callback uses the above stored data and updates the table with the user info. The if within
# serves an important purpose. When i call the store i check whether it was called in a "Div" that
# had "children" or not. If it did, that means that the user has changed the data and i need to 
# refresh the table with the new data. If the "Div" that called the store had no "children", that 
# means that the call happened while "loading" the page, so i need to refresh the table to 
# just "show" the values that are already stored.
@app.callback(Output('user-info','data'),
              Input('update-all','children'),
              State('store-user-info', 'data'))
def refresh_cal(children, data):
    if children is None:
        data1 = [{'Weight (kg)':data[0], 'Height (cm)':data[1], 'Cals/day (Kcal)':data[2],
                'Proteins/day (g)':data[3], 'Sugar/day (g)':data[4]}]
    else:
        data1 = [{'Weight (kg)':children[0], 'Height (cm)':children[1], 'Cals/day (Kcal)':children[2],
                'Proteins/day (g)':children[3], 'Sugar/day (g)':children[4]}]
        html.Div(children, id='store-user-info-input', style={'display':'None'})

    return data1

#*********************************************************************************************
#*                              CALLBACKS FOR "MY CALENDAR"                                  *
#*********************************************************************************************
# Callback for the button to reset the calendar. If we notice that the button has been clicked 3
# times, the value of the "clear_data" attribute of the Store that has the calendar, will be turned
# to "True". This way the calendar resets.
@app.callback(Output('store-calendar', 'clear_data'),
              Input ('calendar-reset', 'n_clicks'))
def reset_calendar(n_clicks):
    if n_clicks==3:
        return True

# Modal functionality of the "Reset Calendar" button.
@app.callback(
    Output("modal2", "is_open"),
    [Input("calendar-reset", "n_clicks"), Input("close2", "n_clicks")],
    [State("modal2", "is_open")],)
def toggle_modal(n1, n2, is_open):
    if n1<3 or n1>3:
        return is_open  
    else:     
        if n1 or n2:
            return not is_open
        return is_open

@app.callback(Output('day-remove-output', 'children'),
              Input ('day-remove', 'n_clicks'),
              State ('store-calendar', 'data'))
def remove_day(n_clicks, storedCalendar):
    if n_clicks==3:
        del storedCalendar[-1]
        return html.Div(storedCalendar, id='store-calendar-input')
        
# The 2 callbacks below are for the Store that has the calendar.
@app.callback(Output('store-calendar', 'data'),
              Input('store-calendar-input', 'children'),
              State('store-calendar', 'data'))
def on_value(value, data):
    
    if value is None:
            # prevent the None callbacks is important with the store component.
            # you don't want to update the store for nothing.
            raise PreventUpdate

        #Give a default data dict with 0 clicks if there's no data.
    data = data or 0
    
    data = value
    return data

@app.callback(Output('store-calendar-value', 'children'),
                # Since we use the data prop in an output,
                # we cannot get the initial data on load with the data prop.
                # To counter this, you can use the modified_timestamp
                # as Input and the data as State.
                # This limitation is due to the initial None callbacks
                # https://github.com/plotly/dash-renderer/pull/81
                Input('store-calendar', 'modified_timestamp'),
                State('store-calendar', 'data'))
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate

    data = data or {}
    return data

#*********************************************************************************************
#*                              CALLBACKS FOR "NEW DAY"                                      *
#*********************************************************************************************
# This callback has the functionality for the "Add Day" button. Depending on what the user has 
# inputted, a different "new day" is created and is then "appended" to the calendar. The only check
# that is happening is whether there is an existing calendar (so the first time that a day is created).
@app.callback(Output("calendar-div", "children"),
              Output('today-products','clear_data'),
              Output('day-total-cal','clear_data'),
              Output('day-total-prot','clear_data'),
              Output('day-total-sugar','clear_data'),
              Input ("add-day", "n_clicks"),
              State ('store-calendar', 'data'),
              State ('day-total-cal', 'data'), # #2 of user table
              State ('day-total-prot', 'data'), # #3 of user table 
              State ('day-total-sugar', 'data'), # #4 of user table
              State ('store-user-info', 'data'),
              State ('lastmonth', 'data'), prevent_initial_call=True)
def add_new_day (n_clicks, storedCalendar, totalcal, totalprot, totalsugar, userinfo, lastmonth):
    if n_clicks==1:
        if (totalprot>=userinfo[3] and totalsugar<=userinfo[4]): # Protein and Sugar values are normal
            if (abs(totalcal-userinfo[2])/userinfo[2]<=0.1):
                new_day = html.Div([ dbc.Card([
                
                                    dbc.CardBody ([
                                        html.H6(today.strftime("%d/%m/%Y"), className="card-title", style = {'textAlign':'center',}),
                                        html.P(['Calories: ' + str(totalcal), html.Br(), 
                                                'Proteins: '+ str(totalprot), html.Br(), 
                                                'Sugars: ' + str(totalsugar)], className = ('card-text'), 
                                                style = {'textAlign':'center', 
                                                        'font-size':'13px'})
                                    ])
                                ], id ='dayx', 
                                style = {'height':'130px', 'width':'130px'},
                                color="success", 
                                inverse=True, )

                        ], style={'display':'inline-block',})
            elif (abs(totalcal-userinfo[2])/userinfo[2]<=0.2):
                 new_day = html.Div([ dbc.Card([
                
                                    dbc.CardBody ([
                                        html.H6(today.strftime("%d/%m/%Y"), className="card-title", style = {'textAlign':'center',}),
                                        html.P(['Calories: ' + str(totalcal), html.Br(), 
                                                'Proteins: '+ str(totalprot), html.Br(), 
                                                'Sugars: ' + str(totalsugar)], className = ('card-text'), 
                                                style = {'textAlign':'center', 
                                                        'font-size':'13px'})
                                    ])
                                ], id ='dayx', 
                                style = {'height':'130px', 'width':'130px'},
                                color="#b6db81", 
                                inverse=True, )

                        ], style={'display':'inline-block',})
            elif (abs(totalcal-userinfo[2])/userinfo[2]<=0.3):
                 new_day = html.Div([ dbc.Card([
                
                                    dbc.CardBody ([
                                        html.H6(today.strftime("%d/%m/%Y"), className="card-title", style = {'textAlign':'center',}),
                                        html.P(['Calories: ' + str(totalcal), html.Br(), 
                                                'Proteins: '+ str(totalprot), html.Br(), 
                                                'Sugars: ' + str(totalsugar)], className = ('card-text'), 
                                                style = {'textAlign':'center', 
                                                        'font-size':'13px'})
                                    ])
                                ], id ='dayx', 
                                style = {'height':'130px', 'width':'130px'},
                                color="warning", 
                                inverse=True, )

                        ], style={'display':'inline-block',})
            elif (abs(totalcal-userinfo[2])/userinfo[2]<=0.5):
                new_day = html.Div([ dbc.Card([
                
                                    dbc.CardBody ([
                                        html.H6(today.strftime("%d/%m/%Y"), className="card-title", style = {'textAlign':'center',}),
                                       html.P(['Calories: ' + str(totalcal), html.Br(), 
                                                'Proteins: '+ str(totalprot), html.Br(), 
                                                'Sugars: ' + str(totalsugar)], className = ('card-text'), 
                                                style = {'textAlign':'center', 
                                                        'font-size':'13px'})
                                    ])
                                ], id ='dayx', 
                                style = {'height':'130px', 'width':'130px'},
                                color="#e89b02", 
                                inverse=True, )

                        ], style={'display':'inline-block',})
            else:         
                new_day = html.Div([ dbc.Card([
                
                                    dbc.CardBody ([
                                        html.H6(today.strftime("%d/%m/%Y"), className="card-title", style = {'textAlign':'center',}),
                                        html.P(['Calories: ' + str(totalcal), html.Br(), 
                                            'Proteins: '+ str(totalprot), html.Br(), 
                                            'Sugars: ' + str(totalsugar)], className = ('card-text'), 
                                            style = {'textAlign':'center', 
                                                     'font-size':'13px'})
                                    ])
                                ], id ='dayx', 
                                style = {'height':'130px', 'width':'130px'},
                                color="danger", 
                                inverse=True, )

                        ], style={'display':'inline-block',})           
        else:
            new_day = html.Div([ dbc.Card([
            
                                dbc.CardBody ([
                                    html.H6(today.strftime("%d/%m/%Y"), className="card-title", style = {'textAlign':'center',}),
                                    html.P(['Calories: ' + str(totalcal), html.Br(), 
                                            'Proteins: '+ str(totalprot), html.Br(), 
                                            'Sugars: ' + str(totalsugar)], className = ('card-text'), 
                                            style = {'textAlign':'center', 
                                                     'font-size':'13px'})
                                ])
                            ], id ='dayx', 
                            style = {'height':'130px', 'width':'130px'},
                            color="danger",
                            inverse=True, )

                    ], style={'display':'inline-block',})

        if storedCalendar is None:
            storedCalendar=[]
        
        if lastmonth is not None: # Check if user has at least one day in the calendar
            if (lastmonth != today.strftime("%m")): #If the last day was in a different month than today
                storedCalendar.append(html.Div(html.Hr()))
                storedCalendar.append(html.H1([today.strftime("%B")], style={'textAlign':'center'}))
        else:
            storedCalendar.append(html.H1([today.strftime("%B")], style={'textAlign':'center'}))
        
        storedCalendar.append(new_day)
        return html.Div([html.Div(storedCalendar, id='store-calendar-input'),
                         html.Div(today.strftime("%m"), id='lastmonth-input',  # When day is added, save the month
                                                        style={'display':'None'})]), True, True, True, True

# Callback for the functionality of the 2 buttons on the top of the "New Day" page. Depending on 
# what the user has clicked more recently, a different Div block is shown.
@app.callback(Output('buttons-choice-output', 'children'),
              Input('button-nutvalue', 'n_clicks'),
              Input('button-prodimage', 'n_clicks'))
def displayClick(btn1, btn2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'button-nutvalue' in changed_id:
        msg = html.Div([
                html.Div([
                    html.H6("Product Name (Optional)"),
                    html.Div([dbc.Input(
                                id= 'product-name',
                                placeholder='Enter name...',
                                type='text',
                                style={'width':'250px'}
                    )], style={'margin-left':'38%'}),
                ], style={'textAlign':'center'}),
                html.Div ([
                    html.Div([
                        html.H6("Kcal/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-kcal',
                            placeholder='Enter a value...',
                            type='number',
                            valid=False,
                            style={'borderRadius':'10px'}
                        ),
                    ], style = {'display':'inline-block', 'width':'20%'}),
                    html.Div([
                        html.H6("Fat/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-fat',
                            placeholder='Enter a value...',
                            type='number', 
                            style={'borderRadius':'10px'}
                        ),
                    ], style = {'display':'inline-block', 'margin-left':'40px', 'width':'20%'}),
                    html.Div([
                        html.H6("Saturated Fat/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-sat_fat',
                            placeholder='Enter a value...',
                            type='number',
                            style={'borderRadius':'10px'}
                        ),
                    ], style = {'display':'inline-block', 'margin-left':'40px', 'width':'20%'}),
                    html.Div([
                        html.H6("Proteins/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-proteins',
                            placeholder='Enter a value...',
                            type='number',        
                            style={'borderRadius':'10px'}       
                        ),
                    ], style = {'display':'inline-block', 'margin-left':'40px', 'width':'20%'}),
                    
                ], style = {'textAlign':'center', 'margin-top':'20px'}),

                html.Div ([
                    html.Div([
                        html.H6("Carbohydrates/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-carbs',
                            placeholder='Enter a value...',
                            type='number',
                            style={'borderRadius':'10px', }
                        ),
                    ], style = {'display':'inline-block', 'width':'20%'}),
                    html.Div([
                        html.H6("Fibers/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-fibers',
                            placeholder='Enter a value...',
                            type='number',
                            style={'borderRadius':'10px'}
                        ),
                    ], style = {'display':'inline-block', 'margin-left':'40px', 'width':'20%'}),
                    html.Div([
                        html.H6("Sugars/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-sugars',
                            placeholder='Enter a value...',
                            type='number',
                            style={'borderRadius':'10px'}
                        ),
                    ], style = {'display':'inline-block', 'margin-left':'40px', 'width':'20%'}),
                    html.Div([
                        html.H6("Salt/100g", style={'textAlign':'center'}),
                        dbc.Input(
                            id= 'input-salt',
                            placeholder='Enter a value...',
                            type='number',
                            style={'borderRadius':'10px'}
                        ),
                    ], style = {'display':'inline-block', 'margin-left':'40px', 'width':'20%'}),
                    
                ], style = {'textAlign':'center', 'margin-top':'40px'}),

                html.Div([
                    html.H6("Quantity consumed (in grams)"),
                    html.Div([dbc.Input(
                        id= 'quantity-consumed',
                        placeholder='Enter quantity...',
                        type='number',
                        style={'borderRadius':'10px', 'width':'250px'}
                    )], style={'margin-left':'38%'}),
                ], style={'textAlign':'center', 'margin-top':'20px'}),
                html.Div([
                    dbc.Button('Add Product to Day', id='myday-button2', n_clicks=0, style={'margin-top':'20px'}),
                ], style={'textAlign':'center', 'margin-top':'40px'})

            ])
    elif 'button-prodimage' in changed_id:
        msg = html.Div([
                #html.H2("Upload a photo of the product"),
                dcc.Upload(
                    id='upload-image-myday',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '50%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px',
                        'margin-left':'25%'
                    },
                    # Allow multiple files to be uploaded
                    multiple=False
                ),
                html.Div(id='output-image-myday', style={'margin-top':'30px'}),
            ], style={'textAlign':'center'})
    else:
        msg = html.Div([])
    return msg

# Callback for the image uploader within the button "Add with product image"
@app.callback(Output('output-image-myday', 'children'),
              Input('upload-image-myday', 'contents'))
def update_myday (contents):
    if contents is not None:
        children = [ parse_contents_myday(contents) ]
        return children

def parse_contents_myday (contents):
    b64_body = contents
    b64_body = contents.split(",")[1]
    decoded = base64.b64decode(b64_body)
    raw = io.BytesIO(decoded)
    img = Image.open(raw).convert("RGB")
    img = img.rotate(270)                                   
    id = iris.search(img)[0]      
    brand = iris.meta.loc[id, "brands"]
    product = iris.meta.loc[id, "product_name"]
    row = iris.meta.loc[id]

    return html.Div([
        html.Div([
            html.H5(brand + ' - ' + product, id='productinfo-input'),
            html.Img(src=contents, style={'height':300, }),
        
        ], style = {'width':'30%','display':'inline-block','textAlign':'center','verticalAlign':'top'}),

        html.Div([
            html.H5("Calories: " + str(round(row["energy-kcal_100g"], 1))),
            html.Div(row["energy-kcal_100g"], id='current_cal-input', style={'display':'None'}),
            html.H5("Protein: " + str(round(row["proteins_100g"], 1)) + "g"),
            html.Div(row["proteins_100g"], id='current_prot-input', style={'display':'None'}),
            html.H5("Carbs: " + str(round(row["carbohydrates_100g"], 1)) + "g"),
            html.Div(row["carbohydrates_100g"], id='current_carb-input', style={'display':'None'}),
            html.H5("Fat: " + str(round(row["fat_100g"], 1)) + "g"),
            html.Div(row["fat_100g"], id='current_fat-input', style={'display':'None'}),
            html.H5("Sugar: " + str(round(row["sugars_100g"], 1)) + "g"),
            html.Div(row["sugars_100g"], id='current_sugar-input', style={'display':'None'}),
            html.H5("Salt: " + str(round(row["salt_100g"], 3)) + "g"),
            html.Div(row["salt_100g"], id='current_salt-input', style={'display':'None'}),
            html.Div(row["fiber_100g"], id='current_fiber-input', style={'display':'None'}),
            html.Div(row["saturated-fat_100g"], id='current_sat_fat-input', style={'display':'None'}),

            html.Img(src="assets/" + row["nutriscore_grade"] + ".png", style={'height':100, 'width':200}),
        ], style = {'width':'30%','display':'inline-block','verticalAlign':'bottom','textAlign':'center'}),

        html.Div([
            html.H6("Amount of grams consumed"),
            dbc.Input(
                id= 'input-myday',
                placeholder='Enter a value...',
                type='number',
                value='',
                style={'borderRadius':'10px'}
            ),
            dbc.Button('Add Product to Day', id='myday-button', style={'verticalAlign':'bottom', 'width':200, 'height':40, "margin-top": "15px"}),
        ], style = {'width':'30%','display':'inline-block','verticalAlign':'center','textAlign':'center', "margin-top": "100px"}),

    ])

# Callback for the button to "Add product to day" that is hidden inside the "Add with product image"
# interface. If the button is clicked, the needed nutritional values of the product are stored and
# the product itself is stored as well on the "today products store" so that it can be shown until
# the day is finally added to the calendar.
@app.callback(Output('myday-button-output','children'),
              Input('myday-button', 'n_clicks'),
              State('input-myday', 'value'),
              State('today-products','data'),
              State('productinfo','data'),
              State('current_cal','data'), State('current_fat','data'), State('current_sat_fat','data'),
              State('current_prot','data'), State('current_carb','data'), State('current_fiber','data'),
              State('current_sugar','data'), State('current_salt', 'data'),)
def button_functionality(n_clicks, value, children, productinfo, currentcal, 
                        currentfat, currentsatfat,currentprot, currentcarb, currentfiber, 
                        currentsugar, currentsalt):
    if (value != '' and n_clicks<2):
        if children is None:
            children=[]

        new_consumed = html.Div ([
            html.H5(productinfo, style={'display':'inline-block'}),
            html.H5(": " + str(value) + "g ", style={'display':'inline-block'}),
            #html.Div(value, id='totalgrams-input', style={'display':'None'} ),
            html.Div(currentcal*value/100/2, id='day-total-cal-input', style={'display':'None'}),
            #html.Div(currentfat*value/100, id='total_fat-input', style={'display':'None'}),
            #html.Div(currentsatfat*value/100, id='total_sat_fat-input', style={'display':'None'}),
            html.Div(currentprot*value/100/2, id='day-total-prot-input', style={'display':'None'}),
            #html.Div(currentcarb*value/100, id='total_carb-input', style={'display':'None'}),
            #html.Div(currentfiber*value/100, id='total_fiber-input', style={'display':'None'}),
            html.Div(currentsugar*value/100/2, id='day-total-sugar-input', style={'display':'None'}),
            #html.Div(currentsalt*value/100, id='total_salt-input', style={'display':'None'}),
        ])
        children.append(new_consumed)
        
        return html.Div(children=children, id='today-products-input')
    else:
        raise PreventUpdate

# Same functionality as the above callback, but for the "Add product to day" button that is inside
# the "Add with nutrition values" interface.
@app.callback(Output('myday-button2-output','children'),
              Input('myday-button2', 'n_clicks'),
              State('quantity-consumed', 'value'),
              State('today-products','data'),
              State('product-name','value'),
              State('input-kcal','value'), State('input-fat','value'), State('input-sat_fat','value'),
              State('input-proteins','value'), State('input-carbs','value'), State('input-fibers','value'),
              State('input-sugars','value'), State('input-salt','value'))
def button_functionality(n_clicks, value, children, productname, kcal, fat, sat_fat, proteins,
                        carbs, fibers, sugars, salt,):
    if children is None:
        children=[]
    if n_clicks==0:
        raise PreventUpdate
    else:
        if (value and kcal and fat and sat_fat and proteins and carbs and fibers and sugars and salt) is not None:
            if (value>0 and kcal>0 and fat>0 and sat_fat>0 and proteins>0 and carbs>0 and fibers>0 and sugars>0 and salt>0):

                new_consumed = html.Div ([
                    html.H5(productname, style={'display':'inline-block'}),
                    html.H5(": " + str(value) + "g ", style={'display':'inline-block'}),
                    #html.Div(value, id='totalgrams-input', style={'display':'None'} ),
                    html.Div(kcal*value/100/2, id='day-total-cal-input', style={'display':'None'}), # THIS COULD USE FIXING (/2 Because executed 2 times)
                    #html.Div(currentfat*value/100, id='total_fat-input', style={'display':'None'}),
                    #html.Div(currentsatfat*value/100, id='total_sat_fat-input', style={'display':'None'}),
                    html.Div(proteins*value/100/2, id='day-total-prot-input', style={'display':'None'}),
                    #html.Div(currentcarb*value/100, id='total_carb-input', style={'display':'None'}),
                    #html.Div(currentfiber*value/100, id='total_fiber-input', style={'display':'None'}),
                    html.Div(sugars*value/100/2, id='day-total-sugar-input', style={'display':'None'}),
                    #html.Div(currentsalt*value/100, id='total_salt-input', style={'display':'None'}),
                ])
                children.append(new_consumed)
                
                return html.Div(children=children, id='today-products-input')

            else:
                raise PreventUpdate
        else:
            raise PreventUpdate

# The 2 callbacks below  are for the store that saves the products that have been consumed this day.
# The values within are reset when the "Add Day" button is clicked.
@app.callback(Output('today-products', 'data'),
              Input('today-products-input', 'children'),
              State('today-products', 'data'))
def on_value(value, data):
    if value is None:
            # prevent the None callbacks is important with the store component.
            # you don't want to update the store for nothing.
            raise PreventUpdate
        
        #Give a default data dict with 0 clicks if there's no data.

    data = data or 0
    data = value
    return data

@app.callback(Output('today-products-value', 'children'),
                # Since we use the data prop in an output,
                # we cannot get the initial data on load with the data prop.
                # To counter this, you can use the modified_timestamp
                # as Input and the data as State.
                # This limitation is due to the initial None callbacks
                # https://github.com/plotly/dash-renderer/pull/81
                Input('today-products', 'modified_timestamp'),
                State('today-products', 'data'))
def on_data(ts, data):

    if ts is None:
        raise PreventUpdate

    data = data or {}
    return data

# Store for saving the corresponding total nutrition values of this day.
for store in ('cal','prot','sugar'):

    @app.callback(Output('day-total-{}'.format(store), 'data'),
                Input('day-total-{}-input'.format(store), 'children'),
                State('day-total-{}'.format(store), 'data'),
                State('button-nutvalue', 'n_clicks'),
                State('button-prodimage', 'n_clicks'))
    def on_value(value, data, btn1, btn2):
    
        if ((value is None) or (btn1==0 and btn2==0)):
            # prevent the None callbacks is important with the store component.
            # you don't want to update the store for nothing.
            raise PreventUpdate

        data = data or 0

        data = data + value
        return data
        
    @app.callback(Output('day-total-{}-value'.format(store), 'children'),
                    # Since we use the data prop in an output,
                    # we cannot get the initial data on load with the data prop.
                    # To counter this, you can use the modified_timestamp
                    # as Input and the data as State.
                    # This limitation is due to the initial None callbacks
                    # https://github.com/plotly/dash-renderer/pull/81
                    Input('day-total-{}'.format(store), 'modified_timestamp'),
                    State('day-total-{}'.format(store), 'data'),)
    def on_data(ts, data,):
    
        if (ts is None):
            
            raise PreventUpdate

        data = data or {}
        return data

# Modal functionality of the "Add Day" button. Can't be clicked more than 1 time.
@app.callback(Output("modal", "is_open"),
            [Input("add-day", "n_clicks"), Input("close", "n_clicks")],
            [State("modal", "is_open")],)
def toggle_modal(n1, n2, is_open):
    if n1<2:
        if n1 or n2:
            return not is_open
        return is_open  

# This Store saves the current month.
@app.callback(Output('lastmonth','data'),
              Input ('lastmonth-input', 'children'),
              State ('lastmonth','data'))
def keep_month (value, data):
    if value is None:
            # prevent the None callbacks is important with the store component.
            # you don't want to update the store for nothing.
            raise PreventUpdate

    data = data or 0
    data = value
    return data

# Modal functionality of the "?" instruction buttons on every page.
@app.callback(Output("modal?", "is_open"),
            [Input("open?", "n_clicks"), Input("close?", "n_clicks")],
            [State("modal?", "is_open")],)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

def b64img2pil(self, b64):
        """Converts a Base64 image to PIL image"""
        b64_body = b64.split(",")[1]
        decoded = base64.b64decode(b64_body)
        raw = io.BytesIO(decoded)
        return Image.open(raw).convert("RGB")


if __name__ == "__main__":
    app.run_server(port=8888, debug=True)