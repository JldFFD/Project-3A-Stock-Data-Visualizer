import os
import time
import requests
import pygal

from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


def get_data(symbol, function):
    """Ask Alpha Vantage for the stock data and return it as a dictionary."""

    api_key = os.environ.get("API_KEY")

    if api_key is None:
        print("No API key found. Put it in your .env file.")
        return None

    url = "https://www.alphavantage.co/query"

    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "full",
    }

    # Needs an interval; the other functions do not
    if function == "TIME_SERIES_INTRADAY":
        params["interval"] = "60min"

    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
        print("API RESPONSE:", data)

    except Exception:
        print("Could not get data from Alpha Vantage. Check your internet.")
        return None

    # Check for API errors
    if "Error Message" in data:
        print("Symbol not found. Check the stock symbol.")
        return None

    # Try compact data if the API does not allow full data
    if "Information" in data and params["outputsize"] == "full":
        params["outputsize"] = "compact"
        time.sleep(2)

        try:
            response = requests.get(url, params=params, timeout=15)
            data = response.json()

        except Exception:
            print("Could not get data from Alpha Vantage. Check your internet.")
            return None

    if "Note" in data or "Information" in data:
        api_message = data.get("Note") or data.get("Information")
        print("The API gave a message:")
        print(api_message)

        if "premium" in api_message.lower():
            return "PREMIUM_REQUIRED"

        return None

    # Find and return the time series data
    for key in data:
        if "Time Series" in key:
            return data[key]

    print("No time series data in the response.")
    return None


def make_chart(symbol, data, chart_type, start, end):
    """Create a Pygal chart for the selected stock and date range."""

    dates = []
    opens = []
    highs = []
    lows = []
    closes = []

    # Go oldest to newest so the chart reads left to right
    for date in sorted(data.keys()):

        day = datetime.strptime(date[:10], "%Y-%m-%d").date()

        if start <= day <= end:
            dates.append(date)
            opens.append(float(data[date]["1. open"]))
            highs.append(float(data[date]["2. high"]))
            lows.append(float(data[date]["3. low"]))
            closes.append(float(data[date]["4. close"]))

    if len(dates) == 0:
        print("No data for those dates.")
        return None

    # Select the chart type
    if chart_type == "bar":
        chart = pygal.Bar(x_label_rotation=45)
    else:
        chart = pygal.Line(x_label_rotation=45)

    chart.title = (
        "Stock Data for " + symbol + ": "
        + str(start) + " to " + str(end)
    )

    chart.x_labels = dates
    chart.x_labels_major_count = 10
    chart.show_minor_x_labels = False

    chart.add("Open", opens)
    chart.add("High", highs)
    chart.add("Low", lows)
    chart.add("Close", closes)

    # Return the chart as an SVG data URI for Flask
    return chart.render_data_uri()


