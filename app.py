from flask import Flask, render_template, request, flash
import csv
from pathlib import Path

from stock_data import get_data, make_chart


# Create the Flask application
app = Flask(__name__)

app.secret_key = "development-secret-key"

# Read stock symbols from the CSV file
def load_stocks():

    csv_path = Path(__file__).parent / "stocks.csv"

    with open(csv_path, "r", newline="", encoding="utf-8-sig") as file:

        reader = csv.DictReader(file)

        stocks = []

        for row in reader:
            stocks.append({
                "symbol": row["Symbol"].strip(),
                "name": row["Name"].strip()
            })

    return stocks


# Create the homepage route
@app.route("/", methods=["GET", "POST"])
def index():

    stocks = load_stocks()

    submitted = None
    chart_data_uri = None

    # Check if the form was submitted
    if request.method == "POST":

        submitted = {
            "symbol": request.form.get("symbol"),
            "chart_type": request.form.get("chart_type"),
            "time_series": request.form.get("time_series"),
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date")
        }

        # Validate the dates
        from datetime import datetime

        try:
            start_date = datetime.strptime(
                submitted["start_date"], "%Y-%m-%d"
            ).date()

            end_date = datetime.strptime(
                submitted["end_date"], "%Y-%m-%d"
            ).date()

            if end_date < start_date:
                flash("End date must be after start date.")
                submitted = None

        except (ValueError, TypeError):
            flash("Please enter valid start and end dates.")
            submitted = None

        # Retrieve stock data and generate the chart
        if submitted is not None:

            data = get_data(
                submitted["symbol"],
                submitted["time_series"]
            )

            if data == "PREMIUM_REQUIRED":
                flash("Intraday data requires a premium Alpha Vantage subscription. Please select Daily, Weekly, or Monthly data.")

            elif data is None:
                flash("Unable to retrieve stock data. Check the symbol or API response.")

            else:
                chart_data_uri = make_chart(
                    submitted["symbol"],
                    data,
                    submitted["chart_type"],
                    start_date,
                    end_date
                )

                if chart_data_uri is None:
                    flash("No stock data was found for the selected dates.")

    return render_template(
        "index.html",
        stocks=stocks,
        submitted=submitted,
        chart_data_uri=chart_data_uri
    )

# Run the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
