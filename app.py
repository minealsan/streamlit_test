import streamlit as st
import pandas as pd


# task 1
# write headline as header "Worldwide Analysis of Quality of Life and Economic Factors"
# write subtitle "This app enables you to explore the relationships between poverty,
#            life expectancy, and GDP across various countries and years.
#            Use the panels to select options and interact with the data."
# use the whole width of the page
# create 3 tabs called "Global Overview", "Country Deep Dive", "Data Explorer"

# Set the page to use wide mode (must be the first Streamlit command)
st.set_page_config(layout="wide")

# Write headline and subtitle
st.title("Worldwide Analysis of Quality of Life and Economic Factors")
st.markdown(
    "### This app enables you to explore the relationships between poverty, life expectancy, and GDP across various countries and years. Use the panels to select options and interact with the data."
)

# create 3 tabs called "Global Overview", "Country Deep Dive", "Data Explorer"
tab1, tab2, tab3 = st.tabs(["Global Overview", "Country Deep Dive", "Data Explorer"])

# task 2 in tab 3
# use global_development_data.csv to be found here: https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv

# which is a cleaned merge of those 3 datasets

# poverty_url = 'https://raw.githubusercontent.com/owid/poverty-data/main/datasets/pip_dataset.csv'
# life_exp_url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Healthy%20Life%20Expectancy%20-%20IHME/Healthy%20Life%20Expectancy%20-%20IHME.csv"
# gdp_url = 'https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Maddison%20Project%20Database%202020%20(Bolt%20and%20van%20Zanden%20(2020))/Maddison%20Project%20Database%202020%20(Bolt%20and%20van%20Zanden%20(2020)).csv'

# show the dataset in the 3rd tab
# read in the dataset and show it
# include a multiselectbox to select the country names
# include a slider to select the year range
# make the filtered dataset downloadable

# show the dataset in the 3rd tab
with tab3:
    st.header("Data Explorer")

    # Read the dataset
    @st.cache_data  # This will cache the data to make it load faster
    def load_data():
        url = "https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv"
        return pd.read_csv(url)

    # Load the data
    df = load_data()

    # Create country selection
    countries = sorted(df["country"].unique().tolist())
    selected_countries = st.multiselect(
        "Select Countries",
        options=countries,
        default=countries[:5],  # Default to first 5 countries
    )

    # Create year range slider
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    year_range = st.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),  # Default to full range
    )

    # Filter and display the data
    if selected_countries:
        filtered_df = df[
            (df["country"].isin(selected_countries))
            & (df["year"].between(year_range[0], year_range[1]))
        ]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        filtered_df = df[df["year"].between(year_range[0], year_range[1])]
        st.dataframe(filtered_df, use_container_width=True)

    # Add download button for filtered data
    if not filtered_df.empty:
        st.download_button(
            label="Download filtered data as CSV",
            data=filtered_df.to_csv(index=False),
            file_name="filtered_global_development_data.csv",
            mime="text/csv",
        )

# task 3: deployment: deploy the app on streamlit cloud (see readme: create own github repo with practical.py file and requirements.txt, connect the github to streamlit cloud)
