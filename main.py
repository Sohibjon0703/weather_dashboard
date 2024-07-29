import requests
import streamlit
from datetime import date
import calendar
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math

# Handling forecast days

month_names = calendar.month_name
today = date.today()
today_month_name = month_names[today.month]
today_day= today.day
year = today.year


API_KEY = "4462dc246d6f0f995f8e3b49abf608ec"

def get_current_weather_data(place):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}'
    data = requests.get(url=url).json()
    temperature = round(data['main']['temp'] - 273.15, 2)
    humidity = round(data['main']['humidity'], 1)
    sea_level = round(data['main']['sea_level'], 1)
    return {
        "temperature": temperature,
        "humidity": humidity,
        "sea_level": sea_level
    }

def get_historical_weather_data(place):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}'
    data = requests.get(url).json()
    filtered_data = []
    for i in data["list"]:
        filtered_data.append(i["main"]["temp"])
    block_size = 8
    block_means = []
    for m in range(0, len(filtered_data), block_size):
        block = filtered_data[m:m+block_size]
        block_mean = round(sum(block) / len(block) - 273.15, 2)
        block_means.append(block_mean)
    return block_means

streamlit.title("Weather Dashboard")

input_value = streamlit.text_input("Enter city name:", key="input_field").lower().title()
if streamlit.button("Submit"):
    print(input_value)
    streamlit.header(f"Current weather information in {input_value} in {today_day} of {today_month_name}, {year}:")

    ext_data = get_current_weather_data(input_value)
    temp = ext_data["temperature"]
    hum = ext_data["humidity"]
    sea_level = ext_data["sea_level"]

    table_data = {
        "Current conditions": ["Temperature (in Celcius)", "Humidity", "Sea level"],
        "Measurement": [temp, hum, sea_level]
    }
    streamlit.table(table_data)

    streamlit.header(f"5 day's weather information in {input_value} in {year} until {today_day} of {today_month_name}:")

    x_axis = [int(today_day), int(today_day) - 1, int(today_day) - 2, int(today_day) - 3, int(today_day - 4)]
    y_axis = get_historical_weather_data(place=input_value)

    chart_data = pd.DataFrame({
        'x': x_axis,
        'y': y_axis
    })

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(chart_data['x'], chart_data['y'])
    ax.set_xticks(chart_data['x'])
    ax.set_xticklabels(chart_data['x'])
    ax.set_xlabel('Days')
    ax.set_ylabel('Temperature in Celcius')
    ax.set_title(f'The line grapf of weather information in {input_value}')

    streamlit.pyplot(fig)
