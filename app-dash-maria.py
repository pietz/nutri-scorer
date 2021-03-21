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
from math import isnan
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from iris import IRIS
from PIL import Image
from dash.exceptions import PreventUpdate
import pandas as pd
import base64
import io
import math
import random

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
                dbc.NavLink("Suggestions", href="/page-suggest", active="exact"),
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

    elif pathname == "/page-suggest": #SUGGESTION PAGE
        
        return html.Div([ 
            dcc.Store(id='sug_id'),
            html.H1("Suggestions", style={'textAlign':'center','fontWeight': 'bold','font-style':'italic','borderRadius': '5px','color': 'black'}),
            html.Hr( style={"background-color":"#dfd7cc",'borderStyle': 'bold','borderWidth': '3px'}),
            html.H5("Find healthier alternatives of your favorite products", style={'textAlign':'center','font-style':'italic'}),
            #info button in suggestions
            dbc.Button("Info", id="open",style={'margin-left':'90%',}),
            dbc.Modal([dbc.ModalHeader("Information for suggestion page"),dbc.ModalBody("In this page you upload an image of a product. "
                                                                                "The information of the product is displayed and the suggestion criteria menu appears. "
                                                                                "You click on a button to get suggestions for foods of similar categories to the uploaded product. "),
                        dbc.ModalFooter(dbc.Button("Close", id="close", className="ml-auto")),],id="modal"),

            dcc.Upload(
                id='upload-image-suggest',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files',style={'text-decoration':'underline'})
                ]),
                style={
                    'width': '40%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'borderColor': '#f0eae1',
                    'textAlign': 'center',
                    'margin': '10px',
                    'margin-left': '30%',
                    'background-color': '#f6f4f0',
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Hr(),
            html.Div(id='output-image-upload-suggest'),

        ])

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
#callback of info suggestions
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
#info suggestions
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

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
        children= [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
# CODE BLOCK FOR IMAGE UPLADING AUXILIARY END HERE ************************************************

#LOAD IRIS
def load_data():
    #df = pd.read_csv('csv_path')
    # return IRIS("iris_210118090818.feather") #ORIGINAL
     return IRIS("final.feather") #WITH CATEGORIES
    #return IRIS("iris_210316030945.feather")
iris = load_data()

#PARSE SUGGESTION
def parse_contents_suggest(contents, filename, date):
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
            html.H4(brand + " - "+ product),
            #html.H6(datetime.datetime.fromtimestamp(date)),
            html.Img(src=contents, style={'height':300, 'width':300}),
            html.Hr(),
        ],style={'width':'50%','display':'inline-block','textAlign': 'center','verticalAlign':'top'}),
        
        html.Div(children=id, id='sug_id_input', style={'display':'None'}),

        html.Div([ 
            html.H4("Product Information:",style={'font-style':'italic'}),  
            html.Hr(),
            html.H5("Calories: " + str(round(row["energy-kcal_100g"], 1))),
            html.H5("Protein: " + str(round(row["proteins_100g"], 1)) + "g"),
            html.H5("Carbs: " + str(round(row["carbohydrates_100g"], 1)) + "g"),
            html.H5("Fat: " + str(round(row["fat_100g"], 1)) + "g"),
            html.H5("Sugar: " + str(round(row["sugars_100g"], 1)) + "g"),
            html.H5("Salt: " + str(round(row["salt_100g"], 3)) + "g"),
            html.H5("Categories: " + str(row["categories_en"])),
            #html.H5("Category: " + str(row["categories_en"])),
            #html.Img("assets/" + row["nutriscore_grade"] + ".png", style={'height':100, 'width':150}),
        ],style={'width':'50%','display':'inline-block','textAlign': 'left'}),
        
        html.Div([   
            html.H5("Please select suggestion criteria:",style={'fontWeight': 'bold','font-style':'italic'}),
            dbc.DropdownMenu(label='Calories',children=[dbc.DropdownMenuItem("Less",id='btn-Calories-less'),dbc.DropdownMenuItem("More",id='btn-Calories-more')],style={'margin': '20px', 'width':'100px', 'display':'inline-block'}),
            dbc.DropdownMenu(label='Protein', children=[dbc.DropdownMenuItem("Less",id='btn-Protein-less'),dbc.DropdownMenuItem("More",id='btn-Protein-more')], style={ 'margin': '20px','width':'100px','display':'inline-block'}),
            dbc.DropdownMenu(label='Carbs', children=[dbc.DropdownMenuItem("Less",id='btn-Carbs-less'),dbc.DropdownMenuItem("More",id='btn-Carbs-more')], style={ 'margin': '20px','width':'100px','display':'inline-block'}),
            dbc.DropdownMenu(label='Fat', children=[dbc.DropdownMenuItem("Less",id='btn-Fat-less'),dbc.DropdownMenuItem("More",id='btn-Fat-more')], style={ 'margin': '20px','width':'100px','display':'inline-block'}),
            dbc.DropdownMenu(label='Sugar', children=[dbc.DropdownMenuItem("Less",id='btn-Sugar-less'),dbc.DropdownMenuItem("More",id='btn-Sugar-more')], style={ 'margin': '20px','width':'100px','display':'inline-block'}),
            dbc.DropdownMenu(label='Salt', children=[dbc.DropdownMenuItem("Less",id='btn-Salt-less'),dbc.DropdownMenuItem("More",id='btn-Salt-more')], style={ 'margin': '20px','width':'100px','display':'inline-block'}),
            html.Div(id='container-button-timestamp'),
            
         ], style={'textAlign':'center'})
   
    ])


#THIS CALLBACK IS FOR THE SUGGESTION UPLOADER
@app.callback(Output('output-image-upload-suggest', 'children'),
              Input('upload-image-suggest', 'contents'),
              State('upload-image-suggest', 'filename'),
              State('upload-image-suggest', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents_suggest(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)
            ]
        return children


def calculate_suggestions(vrb1, id_photo,less):
    #id = iris.search(vrb1)[0]  
    row = iris.meta.loc[id_photo] 
    res=round(row[vrb1], 1)
    product = iris.meta.loc[id_photo, "product_name"]
    brand = iris.meta.loc[id_photo, "brands"]
    category = iris.meta.loc[id_photo, "categories_en"]
    catlist = category.split(",")
   
    i = 0
    n = random.randrange(1,26712)
    objects = []
    no_results=0;
    # csv_path="processed.csv.gz"
    # df = pd.read_csv(csv_path)
    # df = df[(df["product_name"] == product) & (df["brand"] ==brand)]
    # print(df)
    
    while True:
        if math.isnan(res):
            objects.append(html.Div([html.H3("!  The value is empty. Please select other suggestion criteria")], style={"color":'#FF0000'}))
            break
        row_test=iris.meta.loc[n]
        res_test=round(row_test[vrb1],1)
        category_test = iris.meta.loc[n, "categories_en"]
        catlist_test= category_test.split(",")
        common = list(set(catlist) & set(catlist_test))
        
        if res_test is not None:
            if less:
                kk= res_test<res
            else:
                kk=res_test>res
                
            if (kk and common != [] ):
                newone = dbc.Card(
                        [
                            dbc.CardImg(src=row_test["image_url"], style={'height':'200px'}, top=True),
                            dbc.CardBody(
                                [
                                    html.H4(str(iris.meta.loc[n,"brands"]) + ' - ' + str(iris.meta.loc[n,"product_name"]), className="card-title"),
                                    html.P(
                                        ["Calories:" + str(round(iris.meta.loc[n, "energy-kcal_100g"],1)), html.Br(),
                                        "Proteins:" + str(round(iris.meta.loc[n,'proteins_100g'],1))+ "g",html.Br(),
                                        "Carbs: " + str(round(iris.meta.loc[n,"carbohydrates_100g"], 1)) + "g",html.Br(),
                                        "Fat: " + str(round(iris.meta.loc[n,"fat_100g"], 1)) + "g",html.Br(),
                                        "Sugar: " + str(round(iris.meta.loc[n,"sugars_100g"], 1)) + "g",html.Br(),
                                        "Salt: " + str(round(iris.meta.loc[n,"salt_100g"], 3)) + "g",html.Br(),
                                        html.Hr(),
                                        dcc.Markdown('''**Keywords: **'''), str(common)[1:-1]
                                        ],
                                        className="card-text",
                                    ),
                                    #dbc.Button("Go somewhere", color="primary"),
                                ]
                            ),
                        ],
                        style={"width": "200px", 'display':'inline-block', 'margin-left':'20px', 'margin-top':'20px', 'verticalAlign':'top'},
                    )
                #objects.append(html.Div([html.Img(src=row_test["image_url"], height='250px'),
                                        #html.H5(common)]))
                objects.append(newone)
                #objects.append(n)
                i=i+1

        n=n+10
        if i==10:
            break
        if n>=26712:
            no_results+=1
            n=1
        if no_results==2:
            objects.append(html.Div([html.H3("!  No products were found matching this category. Please select another product.")], style={"color":'#FF0000'}))
            break
    return objects
       
#BUTTON SUGGESTIONS CALLBACK
@app.callback(Output('container-button-timestamp', 'children'),
              Input('btn-Calories-less', 'n_clicks'),Input('btn-Calories-more', 'n_clicks'),
              Input('btn-Protein-less', 'n_clicks'),Input('btn-Protein-more', 'n_clicks'),
              Input('btn-Carbs-less', 'n_clicks'),Input('btn-Carbs-more', 'n_clicks'),
              Input('btn-Fat-less', 'n_clicks'),Input('btn-Fat-more', 'n_clicks'),
              Input('btn-Sugar-less', 'n_clicks'),Input('btn-Sugar-more', 'n_clicks'),
              Input('btn-Salt-less', 'n_clicks'),Input('btn-Salt-more', 'n_clicks'),
              State('sug_id','data'),  prevent_initial_call=True)
def displayClick(btn11, btn12, btn21, btn22, btn31, btn32, btn41, btn42, btn51, btn52, btn61, btn62, id_photo):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-Calories-less' in changed_id:
        vrb="energy-kcal_100g"
        nn='less calories'
        less=True
    elif 'btn-Calories-more' in changed_id:
        vrb="energy-kcal_100g"
        nn='more calories'
        less=False   
    elif 'btn-Protein-less' in changed_id:
        vrb="proteins_100g"
        nn='less protein'
        less=True
    elif 'btn-Protein-more' in changed_id:
        vrb="proteins_100g"
        nn='more protein'
        less=False    
    elif 'btn-Carbs-less' in changed_id:
        vrb="carbohydrates_100g"
        nn='less carbs'
        less=True
    elif 'btn-Carbs-more' in changed_id:
        vrb="carbohydrates_100g"
        nn='more carbs'
        less=False    
    elif 'btn-Fat-less' in changed_id:
        vrb="fat_100g"
        nn='less fat'
        less=True
    elif 'btn-Fat-more' in changed_id:
        vrb="fat_100g"
        nn='more fat'
        less=False    
    elif 'btn-Sugar-less' in changed_id:
        vrb="sugars_100g"  
        nn='less sugar'
        less=True 
    elif 'btn-Sugar-more' in changed_id:
        vrb="sugars_100g"  
        nn='more sugar'
        less=False      
    elif 'btn-Salt-less' in changed_id:
        vrb="salt_100g"
        nn='less salt'
        less=True
    elif 'btn-Salt-more' in changed_id:
        vrb="salt_100g"
        nn='more salt'
        less=False    
    
    ch=calculate_suggestions(vrb,id_photo,less)
    ch=html.Div([html.H5('Similar products with ', style={'display':'inline-block'}),
                 html.H5(str(nn), style={'display':'inline-block', 'fontWeight':'bold','margin-left':'3px','margin-right':'3px'}),
                 html.H5(' are:', style={'display':'inline-block',}),
                html.Div(ch)])
    #print(ch)
    return ch
    #html.Div(ch,style={'fontWeight': 'bold','font-style':'italic'})                      

@app.callback(Output('sug_id', 'data'),
              Input('sug_id_input', 'children'),
              State('sug_id', 'data'))
def on_value(id, data):
    if id is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    #Give a default data dict with 0 clicks if there's no data.
    data = id

    return data

# Output callback of the above Store
@app.callback(Output('sug_id_value', 'children'),
                # Since we use the data prop in an output,
                # we cannot get the initial data on load with the data prop.
                # To counter this, you can use the modified_timestamp
                # as Input and the data as State.
                # This limitation is due to the initial None callbacks
                # https://github.com/plotly/dash-renderer/pull/81
                Input('sug_id', 'modified_timestamp'),
                State('sug_id', 'data'))
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate

    data = data or {}

    return data


if __name__ == "__main__":
    app.run_server(port=8888, debug=True)