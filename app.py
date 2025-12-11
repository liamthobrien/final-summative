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
        ui.h3("Time Series of Wheat Yield by Country"),
        ui.input_selectize(
            "countries_select",
            "Select Countries",
            choices=sorted(df['Country'].unique()),
            selected=["Afghanistan"],
            multiple=True
        ),
        
        ui.hr(),

        ui.h3("Simulation"),
        ui.p("Simulation controls coming soon...")
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
        selected = input.countries_select()
    
        if not selected:
            return None 
    
        # Filter
        filtered_data = df[df['Country'].isin(selected)]

        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot each country 
        for country in selected:
            country_data = filtered_data[filtered_data['Country'] == country]
            ax.plot(country_data['Year'], country_data['Yield'],
                    marker='o', label=country, linewidth=2, markersize=4)
                                
        ax.set_title('Wheat Yield: {country}')
        ax.set_xlabel('Year')
        ax.set_ylabel('Yield (kg/ha)')
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        return fig

    @output
    @render.text
    def yield_summary():
        selected = input.countries_select()

        if not selected:
            return 'Select countries to see statistics.'
    
        # Calculate stats 
        stats = []
        for country in selected:
            country_df = df[df['Country'] == country]
            average = country_df['Yield'].mean()
            maximum = country_df['Yield'].max()
            minimum = country_df['Yield'].min()

            stats.append(
                f'Average Yield {average:.2f} kg/ha | Max Yield {maximum:.2f} kg/ha| Min Yield {minimum:.2f} kg/ha'
        )
        return " | ".join(stats)
 
# Run app 

app = App(app_ui, server)