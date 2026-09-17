# Import libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from pathlib import Path  # library to handle file paths

# Load the dataset
vehicles_df = pd.read_csv("vehicles_us.csv")

# Clean the dataset
vehicles_df["paint_color"] = vehicles_df["paint_color"].fillna(
    "Unknown"
)  # Replace missing values in 'paint_color' with 'Unknown'
vehicles_df["is_4wd"] = vehicles_df["is_4wd"].fillna(
    0
)  # Replace missing values in 'is_4wd' with 0
vehicles_df["is_4wd"] = vehicles_df["is_4wd"].astype(
    int
)  # Convert 'is_4wd' to integer type
vehicles_df["date_posted"] = pd.to_datetime(
    vehicles_df["date_posted"]
)  # Change the data type of 'date_posted' to datetime
vehicles_df["model"] = vehicles_df["model"].str.replace(
    "benze ", "", regex=False
)  # Remove 'benze' word from 'model' column
vehicles_df["type"] = vehicles_df["type"].str.lower()  # Convert 'type' in lower case
vehicles_df[["manufacturer", "model"]] = vehicles_df["model"].str.split(
    " ", n=1, expand=True
)  # Split Manufacturer and Model into separate columns

# Header
st.title("Exploratory Data Analysis (EDA) of Vehicles Dataset")
st.write("This is a simple Streamlit app to visualize the vehicles dataset.")

# Insert image
image_path = Path("vehicles_image.png")
if image_path.exists():
    st.image(str(image_path), caption="Vehicles Dataset")

st.subheader("Dataset Overview")

# Show table of the dataset
st.dataframe(vehicles_df, height=220)

# Show bar plot of vehicle types by manufacturer
manufacturer_type_counts = (
    vehicles_df.groupby(["manufacturer", "type"]).size().reset_index(name="count")
)

# Order manufacturers by total count
manufacturer_list = (
    manufacturer_type_counts.groupby("manufacturer")["count"]
    .sum()
    .sort_values(ascending=False)
    .index.to_list()
)

# Create a stacked bar chart using Plotly Express
fig = px.bar(
    manufacturer_type_counts,
    x="manufacturer",
    y="count",
    color="type",
    barmode="stack",
    category_orders={"manufacturer": manufacturer_list},
)

# Axis labels
fig.update_layout(
    xaxis_title="Manufacturer",
    yaxis_title="Count",
    legend_title="Vehicle Type",
)

# New line for spacing
st.write("")
st.write("")

# Show the bar plot for vehicle types by manufacturer
st.subheader("Vehicle Types by Manufacturer")
st.plotly_chart(fig, use_container_width=True)

# New line for spacing
st.write("")
st.write("")

st.subheader("Kilometers vs Price")

type_selected = st.selectbox(
    "Select Vehicle Type",
    options=vehicles_df["type"].unique(),
    key="vehicle_type",
    index=0,
)

# Kilometers vs Price scatter plot
fig = px.scatter(
    vehicles_df[
        vehicles_df["type"] == type_selected
    ],  # Filter outliers for better visualization
    x="odometer",
    y="price",
    title=f"Kilometers vs Price for {type_selected.capitalize()} Vehicles",
)

# Title and axis labels
fig.update_layout(
    xaxis_title="Odometer (km)",
    yaxis_title="Price ($)",
)


st.plotly_chart(fig, use_container_width=True)

# New line for spacing
st.write("")
st.write("")

st.subheader("Distribution of Vehicle Years")

# Checkbox to normalize the histogram
normalize_hist = st.checkbox("Normalize Histogram", value=False)

# Checkbox to overlay the bars
overlay_bars = st.checkbox("Overlay Bars", value=False)

# Histogram of model year by condition
fig = px.histogram(
    vehicles_df,
    x="model_year",
    color="condition",
    histnorm="probability density" if normalize_hist else None,
    barmode="overlay" if overlay_bars else "stack",
)

# Title and axis labels
fig.update_layout(
    xaxis_title="Model Year",
    # yaxis_title="Count",
)

st.plotly_chart(fig, use_container_width=True)


# New line for spacing
st.write("")
st.write("")

# Price distribution by fuel type
fig = px.box(vehicles_df, x="fuel", y="price")

# Change the y-axis range to focus on the main distribution and exclude extreme outliers
fig.update_yaxes(range=[0, 70000])

# Axis labels
fig.update_layout(
    xaxis_title="Fuel Type",
    yaxis_title="Price ($)",
)

st.subheader("Distribution of Vehicle Prices by Fuel Type")
st.plotly_chart(fig, use_container_width=True)

# New line for spacing
st.write("")
st.write("")

# Heatmap of correlation between numerical features
numerical_features = vehicles_df.select_dtypes(include=["float64", "int64"])
correlation_matrix = numerical_features.corr()

# Create a heatmap using Plotly Express
fig = px.imshow(
    correlation_matrix,
    labels=dict(x="Features", y="Features", color="Correlation"),
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    color_continuous_scale="RdBu",
    range_color=[-1, 1],
)

st.subheader("Correlation Matrix")
st.plotly_chart(fig, use_container_width=True)

# New line for spacing
st.write("")
st.write("")

st.subheader("Price Distribution")

# Slider for number of bins in the histogram
nbins = st.slider("Number of Bins", min_value=10, max_value=400, value=376)

# Slider for price range
price_range = st.slider("Price Range ($)", min_value=0, max_value=400000, value=100000)

# Histogram of price
fig = px.histogram(vehicles_df, x="price", nbins=nbins)

# Axis labels
fig.update_layout(
    xaxis_title="Price ($)",
    yaxis_title="Count",
)

fig.update_xaxes(range=[0, price_range])  # Set the x-axis range based on the selected

st.plotly_chart(fig, use_container_width=True)


# New line for spacing
st.write("")
st.write("")

st.subheader("Price Distribution by Condition")

# Sort button by median
sort_condition = st.button("Sort by Median Price")

if sort_condition:
    condition_order = (
        vehicles_df.groupby("condition")["price"]
        .median()
        .sort_values(ascending=False)
        .index.to_list()
    )
    fig = px.box(
        vehicles_df,
        x="condition",
        y="price",
        category_orders={"condition": condition_order},
    )
else:
    # Box plot of price by condition
    fig = px.box(vehicles_df, x="condition", y="price")

# Update axis labels
fig.update_layout(
    xaxis_title="Condition",
    yaxis_title="Price ($)",
)

# Range of y-axis to focus on the main distribution and exclude extreme outliers
fig.update_yaxes(range=[0, 85000])
st.plotly_chart(fig, use_container_width=True)

# New line for spacing
st.write("")
st.write("")

st.subheader("Price vs Year Model")

# Scatter plot of price vs year model
fig = px.scatter(vehicles_df, x="model_year", y="price")

# Update axis labels
fig.update_layout(
    xaxis_title="Year Model",
    yaxis_title="Price ($)",
)
st.plotly_chart(fig, use_container_width=True)

# New line for spacing
st.write("")
st.write("")

st.subheader("Average Price by Type")

# Bar plot of average price by type
avg_price_by_type = (
    vehicles_df.groupby("type")["price"].mean().sort_values(ascending=False)
)

fig = px.bar(x=avg_price_by_type.index, y=avg_price_by_type.values)
fig.update_layout(
    xaxis_title="Type",
    yaxis_title="Average Price ($)",
)

st.plotly_chart(fig, use_container_width=True)

# New line for spacing
st.write("")
st.write("")

st.subheader("Conclusions")
"""
    The exploratory data analysis provided valuable insights into the used **vehicle market** represented in the dataset.

- Vehicle listings are concentrated among a **limited number of manufacturers**, with brands such as Ford, Chevrolet, Toyota, and Jeep accounting for a significant share of the market. **Trucks, pickups, SUVs, and sedans** were the most common vehicle types.

- A **negative relationship** was observed between vehicle mileage (**odometer**) and **price.** In general, vehicles with higher mileage tended to have lower market values, although some variability exists depending on vehicle type and condition.

- The correlation analysis for sedan vehicles confirmed that **mileage** is one of the factors most strongly associated with **price depreciation.** Vehicles with lower mileage generally command higher prices.

- Vehicle condition has a noticeable impact on price. Listings categorized as *excellent*, *like new*, or *new* typically show higher prices than those classified as *good*, *fair*, or *salvage*.

- **Model year** is positively related to vehicle price. Newer vehicles tend to have **higher prices**, while older vehicles generally experience lower market values due to depreciation.

- Fuel type also influences pricing. **Hybrid and diesel** vehicles often exhibit different price distributions compared to traditional **gasoline-powered** vehicles, likely reflecting differences in efficiency, demand, and vehicle characteristics.

- The correlation heatmap suggests that **model year** and **odometer reading** are among the most influential numerical variables affecting vehicle prices. Newer vehicles with lower mileage tend to be listed at higher prices.

- The **price distribution is right-skewed**, indicating that most vehicles fall within a moderate price range while a smaller number of high-value vehicles create a long upper tail.

- **Average prices** vary considerably across vehicle types. **Trucks, pickups, and larger SUVs** generally achieve **higher** average **prices**, whereas sedans and compact vehicles tend to be more affordable.

Overall, the analysis indicates that **vehicle age, mileage, condition, fuel type, and vehicle category are the primary factors influencing vehicle prices**. These findings provide a strong foundation for the interactive Streamlit application, allowing users to explore market trends and relationships within the dataset.
"""
