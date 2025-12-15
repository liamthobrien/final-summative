# Import libraries
from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score

# Load data
df = pd.read_csv("data/extracleaned_wheat_data.csv")
features = pd.read_csv("data/wheat_yield_country_features_with_clusters.csv")
wheat_long = pd.read_csv("data/wheat_yield_long_with_clusters.csv")

# Some processing of csv data
df = df[df["Area Code"] < 5000]
df.drop(columns=["Area Code"], inplace=True)
year_cols = [col for col in df.columns if col.startswith('Y')]
df_wide = wheat_long.pivot(index="Area", columns="Year", values="Yield")
features = features.set_index("Area")

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
                    ui.tags.li("Top 10 most volatile countries by relative variation(CV)"),
                    ui.tags.li("Wheat yield prediction modelling using regression")
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
                choices=sorted(wheat_long['Area'].unique()),
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

    # Prediction Modelling page
    ui.nav_panel(
        "Prediction Modelling",
        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("Wheat Yield Prediction using Regression Models"),
                ui.p("This section presents regression modelling to predict wheat yields based on historical data and cluster analysis."),
                ui.input_selectize(
                    "prediction_country_select",
                    "Select Country for Prediction",
                choices=sorted(wheat_long['Area'].unique()),
                selected=["China, mainland"],
                multiple=False
                )
            ),

            ui.h2("Wheat Yield Prediction Modelling"),
            ui.output_plot("prediction_plot"),
        )
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
        filtered_data = wheat_long[wheat_long['Area'].isin(selected)]

        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot each country 
        for country in selected:
            country_data = filtered_data[filtered_data['Area'] == country]
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
            country_df = wheat_long[wheat_long['Area'] == country]

            average = country_df['Yield'].mean()
            maximum = country_df['Yield'].max()
            minimum = country_df['Yield'].min()
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
        country_mean = df_wide.mean(axis=1).sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        country_mean.head(10).plot(kind="barh", ax=ax, color="steelblue")
        ax.set_xlabel("Mean Yield (kg/ha)")
        ax.set_ylabel("Country")
        ax.set_title("Top 10 Countries by Mean Yield")
        plt.tight_layout()
        return fig

    # Bottom 10 by mean yield 
    @output 
    @render.plot
    def bottom10_mean():
        country_mean = df_wide.mean(axis=1).sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        country_mean.tail(10).plot(kind="barh", ax=ax, color="coral")
        ax.set_xlabel("Mean Yield (kg/ha)")
        ax.set_ylabel("Country")
        ax.set_title("Bottom 10 Countries by Mean Yield")
        plt.tight_layout()
        return fig
                      

    # Percentage change
    @output 
    @render.plot
    def pct_change_plot():
        pct_df = df.copy()
        pct_df.set_index('Area', inplace=True)
        # Calculate percentage change from 1961 to 2023
        pct_change = ((pct_df['Y2023'] - pct_df['Y1961']) /pct_df['Y1961']) * 100
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
        all_yields = df[year_cols].values.flatten()
        fig,ax = plt.subplots(figsize=(8, 5))
        sns.histplot(all_yields, bins=50, kde=True, ax=ax)
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
        mean_yield = df[year_cols].mean(axis=1)
        std_yield  = df[year_cols].std(axis=1)
        cv = (std_yield / mean_yield)
        volatility = cv.sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        volatility.head(10).plot(kind="bar", ax=ax, color="orange")
        ax.set_ylabel("CV")
        ax.set_title("Top 10 Most Volatile Countries by relative variation(CV)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        return fig

    # Backend logic for prediction modelling
    @output
    @render.plot
    def prediction_plot():

        target_country = input.prediction_country_select()

        def make_country_dataset(target_country, train_end_year=2000):

            # Get cluster of the target and other members in the same cluster
            cluster_id = features.loc[target_country, "cluster"]
            cluster_members = features[features["cluster"] == cluster_id].index.tolist()
            other_members = [c for c in cluster_members if c != target_country]
    
            # Pivot to Year x Area wide format for all members of this cluster
            df_cluster = wheat_long[wheat_long["Area"].isin(cluster_members)]
            wide = df_cluster.pivot(index="Year", columns="Area", values="Yield").sort_index()
    
            # Target series
            y = wide[target_country]
    
            # Own lag
            X = pd.DataFrame(index=wide.index)
            X["y_lag1"] = y.shift(1)

            # Own lag -2
            X["y_lag2"] = y.shift(2)
    
            # Cluster mean lag (excluding the target)
            X["cluster_mean_lag1"] = wide[other_members].mean(axis=1).shift(1)
    
            # Add time trend
            X["Year"] = X.index
    
            # Combine with target and drop rows with missing lagged data
            data = pd.concat([X, y.rename("y")], axis=1).dropna()
    
            # Train/test split by time
            train_mask = data["Year"] <= train_end_year
            train = data[train_mask]
            test = data[~train_mask]
    
            X_train = train.drop(columns="y")
            y_train = train["y"]
            X_test = test.drop(columns="y")
            y_test = test["y"]
    
            return X_train, X_test, y_train, y_test, data

        # Generate dataset for the target country
        X_train, X_test, y_train, y_test, data_all = make_country_dataset(target_country, train_end_year=2000)

        def print_metrics(name, y_true, y_pred):
            rmse = root_mean_squared_error(y_true, y_pred)
            mae = mean_absolute_error(y_true, y_pred)
            r2 = r2_score(y_true, y_pred)
    
        y_pred_naive = X_test["y_lag1"]

        own_features = ["y_lag1", "y_lag2"]
        model_own = LinearRegression()
        model_own.fit(X_train[own_features], y_train)
        y_pred_own = model_own.predict(X_test[own_features])

        cluster_features = ["y_lag1", "cluster_mean_lag1", "Year"]
        model_cluster = LinearRegression()
        model_cluster.fit(X_train[cluster_features], y_train)
        y_pred_cluster = model_cluster.predict(X_test[cluster_features])

        test_years = X_test["Year"]

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.plot(test_years, y_test.values, marker="o", label="Actual")
        ax.plot(test_years, y_pred_naive.values, marker="o", linestyle="--", label="Naive (y_{t-1})")
        ax.plot(test_years, y_pred_own, marker="o", linestyle="--", label="Own-history LR")
        ax.plot(test_years, y_pred_cluster, marker="o", linestyle="--", label="Cluster-aug LR")

        ax.set_title(f"Actual vs predicted wheat yield for {target_country} (test period)")
        ax.set_xlabel("Year")
        ax.set_ylabel("Yield (tonnes/ha)")
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        return fig
        


app = App(app_ui, server)