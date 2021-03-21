import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from iris import IRIS
import joblib
import pandas as pd
from iris import IRIS

app = dash.Dash(__name__, suppress_callback_exceptions=True)

def load_data():
     #df = pd.read_csv(csv_path)
     return IRIS("E:\TechLabs\TechLabs_Group1\iris_210118090818.feather")

iris = load_data()

x_cols = [
    "energy-kcal_100g",
    "fat_100g",
    "saturated-fat_100g",
    "proteins_100g",
    "carbohydrates_100g",
    "fiber_100g",
    "sugars_100g",
    "salt_100g"
]
y_col = "nutriscore_grade"

X_test = pd.DataFrame([[369,1.1,0.6,8.4,51,8.7,25,0.44]], columns=list(x_cols))

Y_test = pd.DataFrame([['e']], columns=list('A'))

loaded_model = joblib.load('finalized_model.sav')
Y_test = loaded_model.predict(X_test)

app.layout = html.Div([
    html.Div('NutriScore: ' + Y_test)
])


if __name__ == '__main__':
    app.run_server(debug=True)