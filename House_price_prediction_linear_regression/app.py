from bokeh.io import curdoc
from bokeh.layouts import column, Row
from bokeh.models import TextInput, Select, Button, ColumnDataSource, Div
from bokeh.plotting import figure
import pickle


# Load the model
with open("linear_regression_model.pkl", "rb") as f:
    reg = pickle.load(f)

# Create select widgets
a = total_rooms_input = TextInput(title="Total Rooms")
b = total_bedrooms_input = TextInput(title="Total Bedrooms")
c = population_input = TextInput(title="Population")
d = households_input = TextInput(title="Households")
e = ocean_proximity_select = Select(title="Ocean Proximity", options=["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"])

# Create a button
f = predict_button = Button(label="Predict", button_type="success")

# Create a div to display the prediction
g = prediction_div = Div(text="Prediction: ")

# Define a callback function
def predict_callback():
    if (total_rooms_input.value and total_bedrooms_input.value and 
        population_input.value and households_input.value and 
        ocean_proximity_select.value):
        total_rooms = int(total_rooms_input.value)
        total_bedrooms = int(total_bedrooms_input.value)
        population = int(population_input.value)
        households = int(households_input.value)
        
        # Create a new data point
        x = [total_rooms, total_bedrooms, population, households]
        
        # Convert ocean proximity to a numerical value
        ocean_proximity_dict = {"<1H OCEAN": 0, "INLAND": 1, "ISLAND": 2, "NEAR BAY": 3, "NEAR OCEAN": 4}
        x.append(ocean_proximity_dict[ocean_proximity_select.value])
        
        y = reg.predict([x])[0]
        
        # Update the prediction div
        prediction_div.text = f"Predicted house price: ${y:.2f}"
    else:
        prediction_div.text = "Please select all options"

# Add the callback function to the button
predict_button.on_click(predict_callback)

# Create a layout
layout = Row(
    total_rooms_input, 
    total_bedrooms_input, 
    population_input, 
    households_input, 
    ocean_proximity_select, 
    predict_button, 
    prediction_div, 
    sizing_mode="stretch_both", 
    max_width=800, 
    align="center",
    css_classes=["centered"]
)
# Add the layout to the current document

# Add custom CSS to center the content
custom_css = """
.centered {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    height: 100vh; /* Full viewport height */
}
"""

# Add the custom CSS to the document
curdoc().add_root(layout)
curdoc().template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Bokeh App</title>
    <style>
        {{ bokeh_css }}
        {{ custom_css }}
    </style>
    {{ bokeh_js }}
</head>
<body>
    {{ plot_div }}
</body>
</html>
"""
curdoc().template_variables["custom_css"] = custom_css