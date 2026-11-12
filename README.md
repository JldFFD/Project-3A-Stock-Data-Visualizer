# Stock Data Visualization Web Application

## Overview
This project is a web-based stock data visualization application built with Python and Flask. It allows users to pick a stock from a dropdown box with the information in the stocks.csv file, choose a chart type and time series, select a date range, and generate a visual representation of the stock's historical data.
Stock information is retrieved through the Alpha Vantage API, and charts are generated using Pygal.

## Features
- Select stocks from a dropdown populated by `stocks.csv`.
- Choose between bar charts and line charts.
- Select a time series: Intraday, Daily, Weekly, or Monthly.
- Chose a start date and end date for the chart.
- Validates date selections.
- Display the selected stock information and generated chart.
- Run locally using Flask or in a Docker container.

## Programs and functions Used
- Python
- Flask
- HTML and internal CSS
- Alpha Vantage API
- Pygal
- Requests
- Python-dotenv
- Docker and Docker Compose

### Requirements
- Python 3
- An Alpha Vantage API key
- Docker Desktop (for containerized deployment)

### Environment Variables
Create a `.env` file in the project root directory for the Alpha Vantage API key:

### Run Locally
1. Create and activate a Python virtual environment.
2. Install the required packages:
3. Start the Flask application:
4. Open the application in your browser:

## Run with Docker
Build the Docker image:
Start the application:
Open the application in a website:
--http://localhost:5000

## Issue I had when trying to select Intraday from the free Alpha Vantage API key
The application includes an Intraday option but during testing, the Alpha Vantage API returned a message indicating that the Intraday endpoint requires a premium subscription.
This was identified as an API access restriction rather than an application coding error. The application handles this response and displays a message informing the user that Intraday data requires a premium Alpha Vantage subscription.
Daily, Weekly, and Monthly data were successfully tested.

## Project Files
- `app.py` — Flask application and web routes.
- `stock_data.py` — Retrieves stock data and generates charts.
- `templates/index.html` — Application interface and form.
- `stocks.csv` — Stock symbols, company names, and sectors.
- `requirements.txt` — Python dependencies.
- `Dockerfile` — Instructions for building the Docker image.
- `docker-compose.yml` — Docker Compose configuration.
- `.dockerignore` — Files excluded from the Docker build context.
- `.gitignore` — Files excluded from Git tracking.