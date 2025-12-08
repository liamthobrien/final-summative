#Import libraries
from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt
import numpy as pd
import json 

# Load data

#UI
app_ui = ui.page_sidebar(

    # Sidebar with controls
    ui.sidebar(
        ui.h3("Time Series"),
        ui.p("Controls for time series will go here"),

        ui.hr()

        ui.h3("Data Simulation"),
        ui.p("Controls will go here"),

        ui.hr(),

        ui.p("Model info will go here")
    )
# Main panel 

# Server

# Run app 

app = App(app_ui, server)