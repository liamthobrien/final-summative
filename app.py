# Import libraries
from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load data
df = pd.read_csv("crop_yield_countries_only.csv")

#UI
app_ui = ui.page_navbar(

    # Home page 
    ui.nav_panel(
        "Home",
        ui.layout_column_wrap(
            ui.card(
                ui.card_header("Wheat Yield Dashboard"),
                ui.h3("Explore Wheat Yield Data by Country and Year"), 
                ui.hr(),

                #Project Description
                ui.h4("About The Project"),
                ui.p( "This dashboard allows users to explore wheat yield data from 1961 to 2023 across all wheat producing countries."
                ),
                ui.hr(),

                # Features
                ui.h4("Features"),
                ui.tags.ul(
                    ui.tags.li("Historical yield trend analysis"),
                    ui.tags.li("Top 10 countries by mean yield"),
                    ui.tags.li("Bottom 10 countries by mean yield"),
                    ui.tags.li("Top 15 countries by percentage change"),
                    ui.tags.li("Top 10 most volatile countries")
                ),                        
                ui.hr(),

                # Team
                ui.h4("Team Members"),
                ui.tags.ul(
                    ui.tags.li("Ella - Dashboard Development & UI Design"),
                    ui.tags.li("Mason - Simulation Logic and Data Integration"),
                    ui.tags.li("Liam - Data Analysis and Visualisation"),
                    ui.tags.li("Digby - Regression Modelling and Predictions")
               ),

            ui.p("London Interdisciplinary School - Data Science Summative Project 2"),
        
            ui.hr(),

            # Start Button
                ui.input_action_button(
                    "start_button",
                    "Get Started",
                    class_="btn-primary btn-lg",
                    width = "100%"  
                )
        ),
        width="800px"
    )
),

# Time series panel
    ui.nav_panel(
        "Time Series",
        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("Time Series of Wheat Yield by Country"),
                ui.input_selectize(
                    "countries_select",
                    "Select Countries",
                choices=sorted(df['Country'].unique()),
                selected=["Afghanistan"],
                multiple=True
                )
            ),

            ui.h2("Wheat Yield Trends Over Time"),
            ui.output_plot('yield_plot'),
            ui.output_text("yield_summary")
        )
    ),
    
    # Main yield page 
    ui.nav_panel(
        "Mean Yield",
        ui.h2("Top 10 Countries by Mean Yield"),
        ui.output_plot("top10_mean"),
        ui.hr(),
        ui.h2("Bottom 10 Countries by Mean Yield"),
        ui.output_plot("bottom10_mean"),
    ),

    # Percentage change page
    ui.nav_panel(
        "Percentage Change",
        ui.h2("Top 15 Countries by Percentage Increase (1961-2023)"),
        ui.output_plot("pct_change_plot"),
    ),

    # Distribution page
    ui.nav_panel(
        "Distribution",
        ui.h2("Distribution of Wheat Yields (1961-2023)"),
        ui.output_plot("yield_histogram"),
    ),

    # Volatility page
    ui.nav_panel(
            "Volatility",
        ui.h2("Top 10 Volatile Countries"),
        ui.output_plot("volatility_plot"),
    ),

    title="Wheat Yield Dashboard"
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
                                
        ax.set_title('Wheat Yield Trends Over Time')
        ax.set_xlabel('Year')
        ax.set_ylabel('Yield (kg/ha)')
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        return fig

    # Summary statistics
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
            
            average = country_df["Yield"].mean()
            maximum = country_df["Yield"].max()
            minimum = country_df["Yield"].min()
            stats.append(
                f"{country}: "
                f"Average Yield: {average:.2f} kg/ha |"
                f"Max Yield: {maximum:.2f} kg/ha |"
                f"Min Yield: {minimum:.2f} kg/ha"
            )
        return " | ".join(stats)
 
    # Top 10 by mean yield 
    @output 
    @render.plot
    def top10_mean():
        df_wide = df.pivot(index="Country", columns="Year", values="Yield")
        country_mean = df_wide.mean(axis=1).sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        country_mean.head(10).plot(kind="barh", ax=ax, color="steelblue")
        ax.set_xlabel("Mean Yield (kg/ha)")
        ax.set_title("Top 10 Countries by Mean Yield")
        plt.tight_layout()
        return fig

    # Bottom 10 by mean yield 
    @output 
    @render.plot
    def bottom10_mean():
        df_wide = df.pivot(index="Country", columns="Year", values="Yield")
        country_mean = df_wide.mean(axis=1).sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        country_mean.tail(10).plot(kind="barh", ax=ax, color="coral")
        ax.set_xlabel("Mean Yield (kg/ha)")
        ax.set_title("Bottom 10 Countries by Mean Yield")
        plt.tight_layout()
        return fig
                      

    # Percentage change
    @output 
    @render.plot
    def pct_change_plot():
        df_wide = df.pivot(index="Country", columns="Year", values="Yield")

        # Calculate percentage change from 1961 to 2023
        pct_change = ((df_wide[2023] - df_wide[1961]) /df_wide[1961]) * 100
        pct_change_sorted = pct_change.sort_values(ascending=False)

        # Remove infinite values
        pct_change_sorted = pct_change_sorted.replace([np.inf, -np.inf], np.nan).dropna()
        
        # Remove China if present
        if "China" in pct_change_sorted.index:
            pct_change_sorted = pct_change_sorted.drop("China")

        # Plot
        fig = plt.figure()
        pct_change_sorted.head(15).plot(kind="bar")
        plt.ylabel("Percentage change in yield (1962-2023)")
        plt.title("Top 15 countries by percentage increase in wheat yield(1961 to 2023)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        return fig

    # Yield histogram
    @output
    @render.plot
    def yield_histogram():
        fig,ax = plt.subplots(figsize=(10, 6))
        sns.histplot(df["Yield"], bins=50, kde=True, ax=ax)
        ax.set_title("Distribution of Wheat Yields (1961-2023)")
        ax.set_xlabel("Yield (kg/ha)")
        ax.set_ylabel("Frequency")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

 # Volatility
    @output 
    @render.plot
    def volatility_plot():
        df_wide = df.pivot(index="Country", columns="Year", values="Yield")
        volatility = df_wide.std(axis=1).sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        volatility.head(10).plot(kind="bar", ax=ax, color="orange")
        ax.set_ylabel("Standard Deviation (kg/ha)")
        ax.set_title("Top 10 Most Volatile Countries")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        return fig
                      

app = App(app_ui, server)