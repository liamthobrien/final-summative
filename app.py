# Import libraries
from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("crop_yield_data.csv")

#UI
app_ui = ui.page_sidebar(

    # Sidebar with controls
    ui.sidebar(
        ui.h3("Select Country"),
        ui.input_select(
            "country_selector",
            "Country",
            choices=sorted(df['Country'].unique())
        )
    ),
    ui.h1("Wheat Yield Dashboard"),
    ui.output_plot("yield_plot"),
    ui.output_text("yield_summary")
)

# Server
def server(input, output, session):

    @output
    @render.plot
    def yield_plot():
        country = input.country_selector()
    
        if not country:
            return None 
    
        # Filter
        country_data = df[df['Country'] == country]

        # Plot
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(country_data['Year'], country_data['Yield'], marker='o')
        ax.set_title(f'Wheat Yield: {country}')
        ax.set_xlabel('Year')
        ax.set_ylabel('Yield (kg/ha)')
        ax.grid(True)
        plt.tight_layout()
        return fig

    @output
    @render.text
    def yield_summary():
        country = input.country_selector()

        if not country:
            return 'Select a country to see statistics.'
    
        # Calculate stats 
        country_df = df[df['Country'] == country]
        average = country_df['Yield'].mean()
        maximum = country_df['Yield'].max()
        minimum = country_df['Yield'].min()

        return f'Average Yield {average:.2f} kg/ha | Max Yield {maximum:.2f} kg/ha| Min Yield {minimum:.2f} kg/ha'
 
# Run app 

app = App(app_ui, server)