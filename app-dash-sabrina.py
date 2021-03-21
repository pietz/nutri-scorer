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
import dash_daq as daq
import dash_table
from iris import IRIS
from PIL import Image
import pandas as pd

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#fed8b1",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Nutri Scorer", className="display-4"),
        html.Hr(),
        html.P(
            "How healthy is your nutrition?", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Single Product", href="/", active="exact"),
                dbc.NavLink("Comparison", href="/page-1", active="exact"),
                dbc.NavLink("Custom Recipe", href="/page-2", active="exact"),
                dbc.NavLink("BMI Calculator", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# STYLING OF BMI CALCULATION PAGE
cal_slider_text = {
                      'width': '10%',
                      'verticalAlign': 'top',
                      'display': 'inline-block',
                      }

cal_slider_rest = {
                      'width': '80%',
                      'verticalAlign': 'top',
                      'display': 'inline-block',
                      }   

# DEFINE DATA FRAME
df = pd.read_csv('processed.csv.gz')
df_product = df['product_name'].head(100)
df_head = df.head(100)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# THIS CALLBACK IS FOR THE SIDEBAR
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div( # inside html.Div, we create the layout of the page
            [
            html.H1("Nutri Score Calculator", style={'textAlign':'center'}),
            html.Hr(),
            html.H3("Do you have any allergies?"),
            html.Br(),
            html.H5("Please select any food alergies we should be aware of"),
            dcc.Checklist(
                id = 'allergen-selection',
                options=[
                    {'label': ' Eggs', 'value': 'E'},
                    {'label': ' Fish', 'value': 'F'},
                    {'label': ' Milk', 'value': 'M'},
                    {'label': ' Peanuts', 'value': 'P'},
                    {'label': ' Shellfish', 'value': 'SH'},
                    {'label': ' Soybeans', 'value': 'SO'},
                    {'label': ' Tree nuts', 'value': 'T'},
                    {'label': ' Wheat', 'value': 'W'},
                ],
                labelStyle = dict(display='block')
            ),
            html.Br(),
            html.H3("What is the Nutri Score of your product?"),
            html.Div([
             html.P([
             html.Label("Choose a product"),
             html.Div(dcc.Dropdown(
                 id='dropdown-value', 
                 options=[
                    {'label': i, 'value': i} for i in df_product
                    ], 
                #multi=True, 
                placeholder='Select a product...')),
                #html.Div(id='dropdown-output'),
            ]),
            html.Div([
                html.Div(id='data-container' , style = {'width':'50%', 'display':'inline-block', 'textAlign':'left'}),
            ]),
            html.Br(),
            ]),
            # LEFT HAND SIDE
            # html.Div([
            #     html.H5("Please upload a photo of your product"),
            #     dcc.Upload(
            #     id='upload-image-1',
            #     children=html.Div([
            #         'Drag and Drop or ',
            #         html.A('Select Files')
            #     ]),
            #     style={
            #         'width': '90%',
            #         'height': '60px',
            #         'lineHeight': '60px',
            #         'borderWidth': '1px',
            #         'borderStyle': 'dashed',
            #         'borderRadius': '5px',
            #         'textAlign': 'center',
            #         'margin': '10px',
            #     },
            #     # Allow multiple files to be uploaded
            #     multiple=True
            # ),
            # #html.Div(id='output-image-upload-1'),
            # ], style = {'width':'45%', 'display':'inline-block'}),
            # RIGHT HAND SIDE
            html.Div([
                html.H5("Check out this alternative:"),
                dcc.Markdown(
                id='alternative-recommendation',
                children=[],
                style={
                    'width': '90%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                }),
            ], style = {'width':'45%', 'display':'inline-block'}),

            #html.Div(id='output-image-upload-1' , style = {'width':'45%', 'display':'inline-block', 'textAlign':'center'}),
            html.Div(id='alternative-recommendation' , style = {'width':'45%', 'display':'inline-block', 'textAlign':'center'}),
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
             ])
    elif pathname == "/page-3": # THIS IS WHAT HAPPENS ON THE BMI CALCULATOR PAGE
        return html.Div(
            [
                html.Div(
                    [
                        html.H1("BMI Calculator", style={'textAlign':'center'}),
                        html.Hr(),
                        html.H3("Please enter your parameters:"),
                        html.H5("Please select your gender:"),
                         dcc.Dropdown(
                             id='input_gender',
                             options=[
                                 {'label': 'female', 'value': 'female'},
                                 {'label': 'male', 'value': 'male'},
                             ],
                             value='gender',
                             style={'width': '35%'}
                         ),
                     ]),
                 html.Div(
                     [
                        html.Hr(),
                        html.H5("Please enter your age:"),
                        html.Div(dcc.Input(id='input_age', type='number', placeholder='Age in years', style={'width': '20%'})),
                    ]),
                html.Div(
                    [
                        html.Hr(),
                        html.H5('Please select your height in cm'),
                        html.Br(),
                        html.Br(),
                        html.Div([
                            html.P('Height'),],
                            style=cal_slider_text),
                        html.Div([
                            daq.Slider(id='input_height',min=140,max=200,step=1.0,
                             marks={
                                140: '140 cm',
                                200: '200 cm'
                            },
                            handleLabel={"showCurrentValue": True,"label": "VALUE"},
                            value=175,),
                        ], style=cal_slider_rest),
                        html.Div(id='slider-output-height'),
                ]),
                html.Div(
                    [
                        html.Hr(),
                        html.H5('Please select your weight in kg'),
                        html.Br(),
                        html.Br(),
                        html.Div([
                            html.P('Weight'),
                        ], style = cal_slider_text),
                        html.Div([
                            daq.Slider(id='input_weight', min=20, max=200, step=0.5, 
                            marks={
                                20: '20 kg',
                                200: '200 kg'
                            },
                            handleLabel={"showCurrentValue": True,"label": "VALUE"},
                            value=70),
                        ], style = cal_slider_rest),
                        html.Div(id='slider-output-weight'),
                        ]),

            #Button for showing the sliders for a detailed calorie calculation
                html.Div([
                    html.Br(),
                    html.Hr(),
                    html.Button('BMI button', id='BMI_button'),
                    html.Hr(),
                    html.Div(id='BMI_result')
                    ]),
            ])
      
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

#THIS CALLBACK IS FOR THE SINGLE PRODUCT
@app.callback(dash.dependencies.Output('data-container', 'children'),
            [dash.dependencies.Input('dropdown-value', 'value')],
            [dash.dependencies.Input('allergen-selection', 'value')])


def display_table(dropdown_value, allergen_selection):
    if dropdown_value is not None:
        # SELECT SUBSET OF CSV AS DATAFRAME
        df_data = df_head
        # Select data for selection in dropdown
        data = df_data[df_data['product_name'] == dropdown_value]
        product = data['product_name']
        data_url = data['image_small_url'].values[0]

        return html.Div([
            html.Div([
                html.H4(product),
                ]),
            html.Div([ 
                html.Br(),
                html.H5("Product Information:",style={'font-style':'italic'}),
                html.Div([
                    html.Img(src=data_url, style={'height':200, 'width':200}),
                    html.Hr(),
                ],style={'width':'50%','display':'inline-block','textAlign': 'center','verticalAlign':'top'}),
                html.Div([
                    html.H5("Calories: " + str(round(data["energy-kcal_100g"].values[0], 1))),
                    html.H5("Protein: " + str(round(data["proteins_100g"].values[0], 1)) + "g"),
                    html.H5("Carbs: " + str(round(data["carbohydrates_100g"].values[0], 1)) + "g"),
                    html.H5("Fat: " + str(round(data["fat_100g"].values[0], 1)) + "g"),
                    html.H5("Sugar: " + str(round(data["sugars_100g"].values[0], 1)) + "g"),
                    html.H5("Salt: " + str(round(data["salt_100g"].values[0], 3)) + "g"),
                    #html.H5("Category: " + str(data["categories_en"].values[0])),
                    html.H5("Nutriscore: " + str(data["nutrition-score-fr_100g"].values[0]))
                    #html.Img("assets/" + data["nutriscore_grade"] + ".png", style={'height':100, 'width':150}),
                ],style={'width':'50%','display':'inline-block','textAlign': 'left'}),
            ]),
        ])
    else:
        return "Please select a product."


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

# THIS CALLBACK IS FOR THE SLIDER
@app.callback(
    dash.dependencies.Output('slider-output-height', 'children'),
    dash.dependencies.Output('slider-output-weight', 'children'),
    [dash.dependencies.Input('input_weight', 'value')],
    [dash.dependencies.Input('input_height', 'value')],)

def update_output_height(input_weight, input_height):
    if input_weight and input_height is not None:
        return 'You have selected {} cm'.format(input_height), 'You have selected {} kg'.format(input_weight)
    else:
        return None, None

# THIS CALLBACK IS FOR THE BMI CALCULATOR
@app.callback(
     dash.dependencies.Output('BMI_result', 'children'),
     [dash.dependencies.Input('BMI_button', 'n_clicks')],
     [dash.dependencies.Input('input_weight', 'value')],
     [dash.dependencies.Input('input_height', 'value')],     
     [dash.dependencies.Input('input_age', 'value')],)

def update_bmi_output(n_clicks, input_weight, input_height, input_age):
    if input_height and input_weight and input_age and n_clicks is not None:
        if input_age >= 18:
            x = int(input_weight / ((input_height/100)**2))
            if x < 16:
                y = 'Severe Thinness'
            if 16 >= x < 17:
                y = 'Moderate Thinness'
            if 17 >= x < 18.5:
                y = 'Mild Thinness'
            if 18.5 >= x < 25:
                y = 'Normal'
            if 25 >= x < 30:
                y = 'Overweight'
            if 30 >= x < 35:
                y = 'Obese Class I'
            if 35 >= x < 40:
                y = 'Obese Class II'
            else:
                y = 'Obese Class III'
            return html.Div([
                html.Div('Your BMI is {}!'.format(x)),
                html.Div('According to the he World Health Organization recommended your BMI value belongs to the following category: {}'.format(y)),
            ])
        
        if input_age < 18:
            return 'No reliable information can be given'

        else:
            return 'Information missing'
    else: 
        return 'Information missing'

if __name__ == "__main__":
    app.run_server(port=8888, debug=True)