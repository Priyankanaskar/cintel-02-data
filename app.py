
# import libraries

import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from palmerpenguins import load_penguins


# This package provides the Palmer Penguins dataset

from shiny import reactive, render, req
import seaborn as sns
import pandas as pd

# Use the built-in function to load the Palmer Penguins dataset

penguins_df = load_penguins()


# Add a Shiny UI sidebar for user interaction

ui.page_opts(title="Priyank's Penguin-Data", fillable=True)

# Use ui.input_selectize() to create a dropdown input to choose a column

with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize(
        "selected_attribute",
        "Select Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],)
    
    ui.input_checkbox_group(
        "selected_species_list",
        "Select Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True)
    
    
# Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 30)
    
    ui.input_slider( "seaborn_bin_count","Seaborn Bin Count",1,100,20,)
    
#Use ui.hr() to add a horizontal rule to the sidebar    
    ui.hr()

# Use ui.a() to add a hyperlink to the sidebar
    ui.a(
        "GitHub",
        href="https://github.com/priyankanaskar/cintel-02-data",
        target="_blank",
    )

with ui.accordion(id="acc", open="closed"):
    with ui.accordion_panel("Data Table"):
        @render.data_frame
        def penguin_datatable():
            return render.DataTable(penguins_df)

    with ui.accordion_panel("Data Grid"):
        @render.data_frame
        def penguin_datagrid():
            return render.DataGrid(penguins_df)


with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Plotly Histogram"):

        @render_plotly
        def plotly_histogram():
            plotly_hist = px.histogram(
                data_frame=penguins_df,
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
            ).update_layout(
                title="Plotly Penguins Data",
                xaxis_title="Selected Attribute",
                yaxis_title="Count",
            )
            return plotly_hist

    with ui.nav_panel("Seaborn Histogram"):

        @render.plot
        def seaborn_histogram():
            seaborn_hist = sns.histplot(
                data=penguins_df,
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
            )
            seaborn_hist.set_title("Seaborn Penguin Data")
            seaborn_hist.set_xlabel("Selected Attribute")
            seaborn_hist.set_ylabel("Count")

    with ui.nav_panel("Plotly Scatterplot"):
        ui.card_header("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            plotly_scatter = px.scatter(
                penguins_df,
                x="bill_depth_mm",
                y="bill_length_mm",
                color="species",
                size_max=8,
                labels={
                    "bill_depth_mm": "Bill Depth (mm)",
                    "bill_length_mm": "Bill Length(mm)",
                },
            )
            return plotly_scatter
