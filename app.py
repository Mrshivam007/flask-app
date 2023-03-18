from flask import Flask, render_template, abort
import datetime
import yfinance as yf

app = Flask(__name__)


@app.route('/')
def index():
    # Define the ticker symbol
    tickerSymbol = '^NSEBANK'

    try:
        # Get data on this ticker
        tickerData = yf.Ticker(tickerSymbol)

        # Get the current price
        tickerPrice = tickerData.history(period='1d')['Close'][0]

        # Get the current date
        currentDate = datetime.date.today()

        # Get the day of the week corresponding to the current date
        dayOfWeek = currentDate.strftime("%A")

        # Get the value corresponding to the current day of the week
        dayValue = currentDate.weekday() + 1

        # Calculate the buy and sell prices for CE and PE options
        CE = (tickerPrice - ((tickerPrice % 100)))
        PE = (tickerPrice + (100 - (tickerPrice % 100)))
        buyCE_price = dayValue * 60
        buyPE_price = dayValue * 60
        sellCE_price = (dayValue * 60) + 100
        sellPE_price = (dayValue * 60) + 100
        sellingCE_price = (dayValue * 80)
        sellingPE_price = (dayValue * 80)

        # Render the HTML template and pass the data as variables
        return render_template('index.html', ticker=tickerSymbol, price=tickerPrice, date=currentDate,
                               day=dayOfWeek, value=dayValue, buyCE=CE, buyCE_price=buyCE_price, buyPE=PE,
                               buyPE_price=buyPE_price, sellCE=CE-100, sellCE_price=sellCE_price, sellPE=PE+100,
                               sellPE_price=sellPE_price, sellingCE_price=sellingCE_price, sellingPE_price=sellingPE_price)
    except:
        abort(500, "Failed to fetch data from Yahoo Finance")


if __name__ == '__main__':
    app.run(debug=True)
