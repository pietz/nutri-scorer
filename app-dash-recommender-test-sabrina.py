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
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# DEFINE DATA FRAME
df = pd.read_csv('processed.csv.gz')
df_product = df['product_name'].head(100)
df_head = df.head(100)

# NEW START
allergens = [
        {'label':"eggs",'value':"eggs"},
        {'label':"flour",'value':"flour"},
        {'label':"fish",'value':"fish"},
        {'label':"gluten",'value':"gluten"},
        {'label':"milk",'value':"milk"},
        {'label':"mustard",'value':"mustard"},
        {'label':"nuts",'value':"nuts"},
        {'label':"pork",'value':"pork"},
        {'label':"sesame",'value':"sesame"},
        {'label':"soy",'value':"soy"},
        {'label':"wheat",'value':"wheat"},
        {'label':"yeast",'value':"yeast"},
]
# NEW END
content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# THIS CALLBACK IS FOR THE SIDEBAR
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div( # inside html.Div, we create the layout of the page
            [
            html.H1("Food recommender", style={'textAlign':'center'}),
            html.Hr(),
            # NEW START
            html.H3("Do you have any allergies?"),
            html.Br(),
            html.H5("Please select any food alergies we should be aware of"),
            dcc.Dropdown(
                id='allergen-dropdown',
                options= allergens,
                placeholder="Select your allergens",
                multi=True, #Multi select
            ),
            html.Br(),
            # NEW END
            html.H3("What are the nutrition facts of your food?"),
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
            # html.Div([
            #     html.H5("Check out this alternative:"),
            #     html.Div(id='alternative-recommendation' , style = {'width':'50%', 'display':'inline-block', 'textAlign':'left'}),
            # ]),
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
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

#THIS CALLBACK IS FOR THE SINGLE PRODUCT
@app.callback(
            Output('data-container', 'children'),
            [Input('allergen-dropdown', 'value')],
            [Input('dropdown-value', 'value')])

def display_table(allergen, product):
    if product is not None:
        # SELECT SUBSET OF CSV AS DATAFRAME
        # 'df_head' is defined in row 71. I only extracted the first 100 products to prevent long loading times
        df_data = df_head
        # SELECT PRODUCT DATA BASED ON SELECTION IN DROPDOWN 
        data = df_data[df_data['product_name'] == product]
        product_name = data['product_name']
        data_url = data['image_small_url'].values[0] 
        # # Determine product category (not working properly, please ignore)
        # cat = data['categories_en'].values[0]
        # print(cat)
        # cat_list = cat.split(",")
        # prod_cat = str(cat_list[0])
        # print(prod_cat)
        # Select comparison value as basis for the recommended alternative
        prod_cal = data['energy-kcal_100g'].values[0]

        # SELECT PRODUCT ALTERNATIE
        # NEW START
        if allergen is not None:
            # Create a new dataframe which excludes all products that include the selected allergens
            allergen_df = df 
            for allergen in allergen:
                print(allergen)
                allergen_df = allergen_df[allergen_df['allergens'].str.lower().str.contains(allergen) == False]
                print(allergen_df.shape)
        # NEW END
            # Select alternative
            # # Filter on products that include the first of the categories included in the selected product from above (not working properly, please ignore)
            # allergen_df['categories_en'] = allergen_df.categories_en.str.split(',').tolist()
            # category_df = allergen_df[allergen_df['categories_en'].str.contains(prod_cat) == True]
            # print(category_df.shape)
            # df_alternative = category_df[category_df['energy-kcal_100g'] < prod_cal]
            # Filter on products with a calorie value lower than the selected product from above
            df_alternative = allergen_df[allergen_df['energy-kcal_100g'] < prod_cal]
            # Sort the new dataframe based on the calories from highest to lowest
            final_df = df_alternative.sort_values(by=['energy-kcal_100g'], ascending=False)
            # Select first row of new dataframe as the product to display as an alternative
            data_alternative = final_df.head(1)
            product_alter = data_alternative['product_name']
            alter_url = data_alternative['image_small_url'].values[0]
            print(product_alter)
        else:
            return None
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
                    html.H5("Protein: " + str(round(data["proteins_100g"].values[0], 1)) + " g"),
                    html.H5("Carbs: " + str(round(data["carbohydrates_100g"].values[0], 1)) + " g"),
                    html.H5("Fat: " + str(round(data["fat_100g"].values[0], 1)) + " g"),
                    html.H5("Sugar: " + str(round(data["sugars_100g"].values[0], 1)) + " g"),
                    html.H5("Salt: " + str(round(data["salt_100g"].values[0], 3)) + " g"),
                    html.H5("Nutriscore: " + str(data["nutrition-score-fr_100g"].values[0]))
                ],style={'width':'50%','display':'inline-block','textAlign': 'left'}),
            ]),
            html.Div([
                html.H3("Check out this alternative: "),
                html.H4(product_alter),
                ]),
            html.Div([ 
                html.Br(),
                html.H5("Product Information:",style={'font-style':'italic'}),
                html.Div([
                    html.Img(src=alter_url, style={'height':200, 'width':200}),
                    html.Hr(),
                ],style={'width':'50%','display':'inline-block','textAlign': 'center','verticalAlign':'top'}),
                html.Div([
                    html.H5("Calories: " + str(round(data_alternative["energy-kcal_100g"].values[0], 1))),
                    html.H5("Protein: " + str(round(data_alternative["proteins_100g"].values[0], 1)) + " g"),
                    html.H5("Carbs: " + str(round(data_alternative["carbohydrates_100g"].values[0], 1)) + " g"),
                    html.H5("Fat: " + str(round(data_alternative["fat_100g"].values[0], 1)) + " g"),
                    html.H5("Sugar: " + str(round(data_alternative["sugars_100g"].values[0], 1)) + " g"),
                    html.H5("Salt: " + str(round(data_alternative["salt_100g"].values[0], 3)) + " g"),
                    html.H5("Nutriscore: " + str(data_alternative["nutrition-score-fr_100g"].values[0]))
                ],style={'width':'50%','display':'inline-block','textAlign': 'left'}),
                ]),   
        ])
    else:
        return None #, None


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

if __name__ == "__main__":
    app.run_server(port=8888, debug=True)