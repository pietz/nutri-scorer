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
import plotly
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.express as px
import plotly.io as pio
#from iris import IRIS
from PIL import Image
import pandas as pd
import numpy as np

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

hide_style = {
                    'display': 'none'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

global_df = pd.read_csv('processed.csv.gz', nrows=10) #x rows for faster processing
global_df["allergens"].replace(np.nan, "", regex=True, inplace=True)
df = global_df.drop(columns=['brands','main_category_en', 'categories_en', 'countries_en', 'nutrition-score-fr_100g', 'carbon-footprint_100g'])
product_list = df["product_name"].tolist() #for single selection in dropdown

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Open Food Facts Explorer/ Working with a dataframe"),
    html.Hr(),
    html.Div([
        html.H2("Just the dataframe + Filter"),
        dcc.Dropdown(
            id='allergen-dropdown',
            options= allergens,
            placeholder="Select your allergens",
            multi=True, #Multi select
        ),
        dash_table.DataTable(
            id='show-dataframe',
            columns=[{"name": i, "id": i} for i in df.columns],
            #data=df.to_dict('records'),
        ),
    ]),
    html.Div([
        html.Hr(),
        html.H2("Single Selection + Piechart"),
        dcc.Dropdown(
            id='single-product-dropdown',
            options= [{'label': product, 'value': product} for product in product_list],
            placeholder="Select your product",
        ),
        html.Div(id='output-container-single')
    ]),
])

@app.callback(
    dash.dependencies.Output('show-dataframe', 'data'),
    [dash.dependencies.Input('allergen-dropdown', 'value')],
)

def filter_dataframe(allergen):
    if allergen is not None:
        allergen_df = df 
        for allergen in allergen:
            print(allergen)
            allergen_df = allergen_df[allergen_df["allergens"].str.lower().str.contains(allergen) == False]  
        return allergen_df.to_dict('records')
    else:
        return df.to_dict('records')

@app.callback(
    dash.dependencies.Output('output-container-single', 'children'),
    [dash.dependencies.Input('single-product-dropdown', 'value')],    
)
#
def show_single_selection(product):
    if product is not None:
        print(product)
        single_df = df
        single_df = single_df[single_df["product_name"] == product]
        single_list = [item for sublist in single_df.values.tolist() for item in sublist]
        print(single_list)
        # Just return values, if product was found
        if len(single_list) > 0:
            content_url = single_list[1]
            composition_values_piechart = single_list[3:8]
            single_df = single_df.drop(columns=['image_small_url'])
            print(composition_values_piechart)       
            return html.Div(
            [   
                #Table / Dataframe
                html.Div([
                    dash_table.DataTable(
                        id='show-single-product',
                        columns=[{"name": i, "id": i} for i in single_df.columns],
                        data=single_df.to_dict('records'),
                        ),
                ]),
                #Picture + Piechart
                html.Div([
                    # Picture
                    html.Div([
                        html.H5(" "),
                        html.Img(src=content_url, style={'height':300, 'width':300}),    
                    ],style={'width': '33%', 'display': 'inline-block','vertical-align': 'middle',}),
                    # Values           
                    html.Div([
                        html.P("Calories: " + str(single_list[2])),
                        html.P("Protein: " + str(single_list[3]) + "g"),
                        html.P("Carbs: " + str(single_list[4]) + "g"),
                        html.P("Fat: " + str(single_list[5]) + "g"), 
                        html.P("Sugar: " + str(single_list[6]) + "g"),
                        html.P("Salt: " + str(single_list[7]) + "g"),
                    ],style={'width': '33%', 'display': 'inline-block','vertical-align': 'top',}),
                    # Piechart
                    html.Div([
                        dcc.Graph(figure = px.pie(
                            names=['protein','fat','carbohydrates','sugars', 'salt'],
                            values = composition_values_piechart,
                            hole=.3,
                        ))
                    ],style={'width': '33%', 'display': 'inline-block','vertical-align': 'top',}),
                ])
            ])
        else:
            return "Product not found, select an other one"
    else: 
        return "Select a product"

# Updating the Piechart for single products
# @app.callback(
#     Output(component_id='piechart-single-product', component_property='figure'),
#     [Input(component_id='hidden-single-composition-container', component_property='children')],    
# )

# def update_piechart_single_product(composition_values_piechart):
    
#     if composition_values_piechart is not None:
#         piechart_single_prodct=px.pie(
#                 names=['protein','fat','carbohydrates','sugars', 'salt'],
#                 values = composition_values_piechart,
#                 hole=.3,
#                 )
#         return (piechart_single_prodct)
#     else:
#         return None 

if __name__ == '__main__':
    app.run_server(debug=False)#, use_reloader = True)

