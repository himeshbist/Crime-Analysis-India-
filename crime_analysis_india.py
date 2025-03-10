# -*- coding: utf-8 -*-
"""Crime-Analysis-India.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fYAOxrsgrYj0kX1oaVm-eQZqQ81R8JXx
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA

# Load the dataset
df = pd.read_csv("crime_dataset_india.csv")

# Step 1: Data Cleaning
# Convert Date column to datetime format
df['Date of Occurrence'] = pd.to_datetime(df['Date of Occurrence'], errors='coerce')
df = df.dropna(subset=['Date of Occurrence'])  # Remove missing dates

# Step 2: Resampling data to Monthly Level
df_resampled = df.groupby(['City', pd.Grouper(key='Date of Occurrence', freq='M')]).size().reset_index(name='Crime Count')

# Step 3: Trend Analysis using Moving Average
plt.figure(figsize=(12, 5))
top_cities = df['City'].value_counts().head(5).index  # Top 5 high-crime cities

for city in top_cities:
    city_data = df_resampled[df_resampled['City'] == city]
    plt.plot(city_data['Date of Occurrence'], city_data['Crime Count'].rolling(window=6).mean(), label=city)  # 6-month moving avg

plt.title("City-wise Crime Trend (Moving Average)")
plt.xlabel("Year")
plt.ylabel("Crime Count (6-month Avg)")
plt.legend()
plt.grid(True)
plt.show()

# Step 4: Forecasting Future Crime Trends using ARIMA
city_forecasts_final = {}
plt.figure(figsize=(12, 6))

for city in top_cities:
    city_data = df_resampled[df_resampled['City'] == city].set_index('Date of Occurrence')

    # Fit ARIMA model
    arima_model = ARIMA(city_data['Crime Count'], order=(3,1,2))  # Adjusted parameters
    arima_fit = arima_model.fit()

    # Forecast for next 24 months (2 years)
    future_forecast = arima_fit.forecast(steps=24)

    # Store forecasted values
    city_forecasts_final[city] = future_forecast.sum()

    # Plot the forecast
    plt.plot(pd.date_range(start=city_data.index[-1], periods=24, freq='M'), future_forecast, label=city)

# Graph settings
plt.title("Final City-wise Crime Prediction for Next 2 Years")
plt.xlabel("Year")
plt.ylabel("Predicted Crime Count (Monthly Basis)")
plt.legend()
plt.grid(True)
plt.show()


# Display refined numerical results
city_forecast_final_df = pd.DataFrame(city_forecasts_final.items(), columns=["City", "Predicted Crime Count (Next 2 Years)"])
print(city_forecast_final_df)

# Step 5: Gender-wise Crime Analysis (Corrected)

# Count the number of crimes targeting each gender
gender_counts = df['Victim Gender'].value_counts()

# Plot gender distribution
plt.figure(figsize=(8, 5))
sns.barplot(x=gender_counts.index, y=gender_counts.values, palette='coolwarm')
plt.title("Gender-wise Crime Distribution")
plt.xlabel("Gender")
plt.ylabel("Crime Count")
plt.grid(True)
plt.show()

# Display numerical gender distribution
gender_counts

# Step 6: Crime Type Analysis for Female Victims (Corrected)

# Filter dataset for Female victims
female_crimes = df[df['Victim Gender'] == 'F']

# Count the most common crimes against females
female_crime_counts = female_crimes['Crime Description'].value_counts().head(10)  # Top 10 crimes

# Plot the crime distribution for females
plt.figure(figsize=(10, 5))
sns.barplot(x=female_crime_counts.values, y=female_crime_counts.index, palette='Reds_r')
plt.title("Top Crimes Faced by Female Victims")
plt.xlabel("Number of Cases")
plt.ylabel("Crime Type")
plt.grid(True)
plt.show()

# Display numerical results
female_crime_counts

# Step 7: Age-wise Crime Analysis

# Creating age groups
bins = [0, 12, 18, 30, 50, 100]  # Age ranges
labels = ['Child (0-12)', 'Teen (13-18)', 'Young Adult (19-30)', 'Adult (31-50)', 'Senior (51+)']
df['Age Group'] = pd.cut(df['Victim Age'], bins=bins, labels=labels, right=False)

# Count the number of crimes per age group
age_group_counts = df['Age Group'].value_counts().sort_index()

# Plot age group distribution
plt.figure(figsize=(8, 5))
sns.barplot(x=age_group_counts.index, y=age_group_counts.values, palette='viridis')
plt.title("Age-wise Crime Distribution")
plt.xlabel("Age Group")
plt.ylabel("Crime Count")
plt.grid(True)
plt.show()

# Display numerical results
age_group_counts