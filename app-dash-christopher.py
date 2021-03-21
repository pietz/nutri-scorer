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
#NEED TO ADD FUNCTION TO THE UPLOADER

#html.Div: inside here we create the layout of the page. (Text, buttons, images) children need []!!!
import datetime
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from iris import IRIS
from PIL import Image
import pandas as pd
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

#hide_style, show_style, cal_slider_text, cal_slider_reset for styling of calorie calculation page
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

sidebar = html.Div(
    [
        html.H2("Nutri Scorer", className="display-4"),
        html.Hr(),
        html.P(
            "A simple app for your healthy-eating needs", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Single Product", href="/", active="exact"),
                dbc.NavLink("Comparison", href="/page-1", active="exact"),
                dbc.NavLink("Custom Recipe", href="/page-2", active="exact"),
                dbc.NavLink("Calorie Calculator", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# THIS CALLBACK IS FOR THE SIDEBAR
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/": # THIS IS WHAT HAPPENS ON THE SINGLE PRODUCT PAGE
        return html.Div( # inside html.Div, we create the layout of the page
            [
            html.H1("Single Product", style={'textAlign':'center'}),
            html.Hr(),
            html.H2("Upload a photo of the product"),
            dcc.Upload(
                id='upload-image-1',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='output-image-upload-1'),
            
        ])
    elif pathname == "/page-1": # THIS IS WHAT HAPPENS ON THE COMPARISON PAGE 
        return html.Div([
            html.H1("Comparison", style={'textAlign':'center'}),
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
            ], style = {'width':'45%', 'display':'inline-block'}),

            html.Div(id='output-image-upload-1' , style = {'width':'45%', 'display':'inline-block', 'textAlign':'center'}),
            html.Div(id='output-image-upload-2' , style = {'width':'45%', 'display':'inline-block', 'textAlign':'center'}),

        ])
    elif pathname == "/page-2": # THIS IS WHAT HAPPENS ON THE CUSTOM RECIPE PAGE

        return html.Div(
            [
                html.H1("Custom Recipe", style={'textAlign':'center'}),
                html.Hr(),
            ]
        )
    elif pathname == "/page-3": # THIS IS WHAT HAPPENS ON THE CALORIE CALCULATOR PAGE

        return html.Div(
            [   
                html.H1("Calorie Calculator", style={'textAlign':'center'}),
                html.Hr(),
                html.H2("Enter your your paramters:"),
                html.Hr(),
                # Box with four boxes (inline) inside
                html.Div(
                    [
                        html.Div(
                            [
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
                        html.Div(
                            [                            
                                html.H4("Enter your Age"),
                                html.Div(dcc.Input(id='input_age', type='number', placeholder='Age in years', min=1, style={'width': '180px', 'height': '35px'},)),                                
                            ],style={'width': '24%', 'display': 'inline-block','vertical-align': 'top'}),
                        html.Div(
                            [                      
                                html.H4("Enter your weight"),
                                html.Div(dcc.Input(id='input_weight', type='number', placeholder='Weight in kg', min=1, style={'width': '180px', 'height': '35px'},)),                                
                            ],style={'width': '24%', 'display': 'inline-block','vertical-align': 'top'}),
                        html.Div(
                            [   
                                html.H4("Enter your height"),
                                dcc.Input(id='input_height', type='number', placeholder='Height in cm', min=1, style={'width': '180px', 'height': '35px'},),
                                #html.P("cm", style={'width': '12%', 'verticalAlign': 'mid', 'display': 'inline-block'})
                            ],style={'width': '24%', 'display': 'inline-block','vertical-align': 'top'}),
                    ]),
                html.Div(
                    [
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
    #,'border':'2px black solid' for seeing the borders of a div
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# CODE BLOCK FOR IMAGE UPLADING AUXILIARY STARTS HERE *********************************************
def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents, style={'height':300, 'width':300}),
        html.Hr(),
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
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
# CODE BLOCK FOR IMAGE UPLADING AUXILIARY END HERE ************************************************

# Present the results of first CALORIE CALCULATION
@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    dash.dependencies.Output(component_id='PAL_button', component_property='style'),
    dash.dependencies.Output('hidden-cal-container', 'children'),
    [dash.dependencies.Input('input_age', 'value')],
    [dash.dependencies.Input('input_weight', 'value')],
    [dash.dependencies.Input('input_height', 'value')],
    [dash.dependencies.Input('sex', 'value')],
    )
def update_cal_output(input_age, input_weight, input_height, sex):
    if input_age and input_weight and input_height and sex is not None:
        if sex == 'female':
            x = int(655.1 + (9.6 * input_weight) + (1.8 * input_height) - (4.7 * input_age))
            return html.Div([
                html.Div('You have a basal metabolic rate of {} kcal calories a day!'.format(x)),
                html.Hr(),
                html.P("If you would like to determine a more precise calorie consumption:"),
            ]), show_style, x

        if sex == 'male':
            x = int(66.47 + (13.7 * input_weight) + (5 * input_height) - (6.8 * input_age))
            return html.Div([
                html.Div('You have a basal metabolic rate of {} kcal calories a day!'.format(x)),
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
    [dash.dependencies.Input('PAL_button', 'n_clicks')],
)
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
    [Input(component_id='hidden-hours-container', component_property='children')],    
)

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

if __name__ == "__main__":
    app.run_server(debug=False, port=8888)