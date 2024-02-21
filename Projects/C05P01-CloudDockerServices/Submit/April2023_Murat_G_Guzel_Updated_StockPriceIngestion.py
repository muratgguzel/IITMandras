import json
import boto3
import sys
import yfinance as yf

import time
import random
import datetime


# Your goal is to get per-hour stock price data for a time range for the ten stocks specified in the doc. 
# Further, you should call the static info api for the stocks to get their current 52WeekHigh and 52WeekLow values.
# You should craft individual data records with information about the stockid, price, price timestamp, 52WeekHigh and 52WeekLow values and push them individually on the Kinesis stream

def get_stock_52_week_high_low(ticker_symbol):
    
    # Create a Ticker object for the given symbol
    stock = yf.Ticker(ticker_symbol)
    
    # Retrieve stock information
    stock_info = stock.info
    
    # Extract the 52-week high and low
    fifty_two_week_high = stock_info['fiftyTwoWeekHigh']
    fifty_two_week_low = stock_info['fiftyTwoWeekLow']
    
    return fifty_two_week_high, fifty_two_week_low


def send_to_kinesis(stream_name,kinesis_client,stock_id, price, price_timestamp, week52_high, week52_low):
    """
    Pushes stock data to an Amazon Kinesis stream.

    Parameters:
    - stream_name: The name of the Kinesis stream.
    - stock_id: The stock ticker symbol.
    - price: The current price of the stock.
    - price_timestamp: The timestamp of the current price.
    - week52_high: The 52-week high price of the stock.
    - week52_low: The 52-week low price of the stock.
    """
    # Prepare the data record
    record = {
        "stockid": stock_id,
        "price": price,
        "price_timestamp": price_timestamp,
        "52WeekHigh": week52_high,
        "52WeekLow": week52_low
    }
        
    # Convert the record to a JSON string
    data = json.dumps(record)
    
    # Push the data to the Kinesis stream
    response = kinesis_client.put_record(
        StreamName=stream_name,
        Data=data,
        PartitionKey=stock_id  # Using stock ID as partition key
    )
    
    print(f"Pushed record to Kinesis: {response}")


def push_stock_data_to_kinesis(stream_name,kinesis_client,ticker_symbol,data,week52_high, week52_low):
        
    for date,row in dataMSFT.iterrows():
        price = row['Close'] 
        price_timestamp = date.strftime('%Y-%m-%d %H:%M:%S')

        # Send data to Kinesis
        response = send_to_kinesis(stream_name, kinesis_client, ticker_symbol, price, price_timestamp, week52_high, week52_low)
        print(f"Sent data for {ticker_symbol} at {price_timestamp}: {response}")


kinesis_client = boto3.client('kinesis', region_name = "us-east-1") #Modify this line of code according to your requirement.

today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(1)

## Add code to pull the data for the stocks specified in the doc

dataMSFT = yf.download("MSFT", start= yesterday, end= today, interval = '1h' )
print(dataMSFT)
ticker = "MSFT"
high_MSFT, low_MSFT = get_stock_52_week_high_low(ticker)
print(f"{ticker} 52-Week High: {high_MSFT}")
print(f"{ticker} 52-Week Low: {low_MSFT}")

push_stock_data_to_kinesis("Project5_Stream",kinesis_client,ticker,dataMSFT,high_MSFT,low_MSFT)



dataMVIS = yf.download("MVIS", start= yesterday, end= today, interval = '1h' )
print(dataMVIS)
ticker = "MVIS"
high_MVIS, low_MVIS = get_stock_52_week_high_low(ticker)
print(f"{ticker} 52-Week High: {high_MVIS}")
print(f"{ticker} 52-Week Low: {low_MVIS}")

push_stock_data_to_kinesis("Project5_Stream",kinesis_client,ticker,dataMVIS,high_MVIS,low_MVIS)

dataGOOG = yf.download("GOOG", start= yesterday, end= today, interval = '1h' )
print(dataGOOG)
ticker = "GOOG"
high_GOOG, low_GOOG = get_stock_52_week_high_low(ticker)
print(f"{ticker} 52-Week High: {high_GOOG}")
print(f"{ticker} 52-Week Low: {low_GOOG}")

push_stock_data_to_kinesis("Project5_Stream",kinesis_client,ticker,dataGOOG,high_GOOG,low_GOOG)

dataSPOT = yf.download("SPOT", start= yesterday, end= today, interval = '1h' )
print(dataSPOT)
ticker = "SPOT"
high_SPOT, low_SPOT = get_stock_52_week_high_low(ticker)
print(f"{ticker} 52-Week High: {high_SPOT}")
print(f"{ticker} 52-Week Low: {low_SPOT}")

push_stock_data_to_kinesis("Project5_Stream",kinesis_client,ticker,dataSPOT,high_SPOT,low_SPOT)


dataINO =  yf.download("INO", start= yesterday, end= today, interval = '1h' )
print(dataINO)
ticker = "INO"
high_INO, low_INO = get_stock_52_week_high_low(ticker)
print(f"{ticker} 52-Week High: {high_SPOT}")
print(f"{ticker} 52-Week Low: {low_SPOT}")

push_stock_data_to_kinesis("Project5_Stream",kinesis_client,ticker,dataINO,high_INO,low_INO)


dataOCGN = yf.download("OCGN", start= yesterday, end= today, interval = '1h' )
print(dataOCGN)
ticker = "OCGN"
high_OCGN, low_OCGN = get_stock_52_week_high_low(ticker)
print(f"{ticker} 52-Week High: {high_OCGN}")
print(f"{ticker} 52-Week Low: {low_OCGN}")

push_stock_data_to_kinesis("Project5_Stream",kinesis_client,ticker,dataOCGN,high_OCGN,low_OCGN)


dataABML = yf.download("AAPL", start= yesterday, end= today, interval = '1h' )
print(dataABML)
ticker = "AAPL"
high_AAPL, low_AAPL = get_stock_52_week_high_low(ticker)
print(f"{ticker} 52-Week High: {high_AAPL}")
print(f"{ticker} 52-Week Low: {low_AAPL}")

push_stock_data_to_kinesis("Project5_Stream",kinesis_client,ticker,dataABML,high_AAPL,low_AAPL)

dataRLLCF = yf.download("RLLCF", start= yesterday, end= today, interval = '1h' )
print(dataRLLCF)
ticker = "RLLCF"
high_RLLCF, low_RLLCF = get_stock_52_week_high_low(ticker)
print(f"{ticker} 52-Week High: {high_RLLCF}")
print(f"{ticker} 52-Week Low: {low_RLLCF}")

push_stock_data_to_kinesis("Project5_Stream",kinesis_client,ticker,dataABML,high_RLLCF,low_RLLCF)

dataJNJ =  yf.download("JNJ", start= yesterday, end= today, interval = '1h' )
print(dataJNJ)
ticker = "JNJ"
high_JNJ, low_JNJ = get_stock_52_week_high_low(ticker)
print(f"{ticker} 52-Week High: {high_JNJ}")
print(f"{ticker} 52-Week Low: {low_JNJ}")

push_stock_data_to_kinesis("Project5_Stream",kinesis_client,ticker,dataJNJ,high_JNJ,low_JNJ)


dataPSFE = yf.download("PSFE", start= yesterday, end= today, interval = '1h' )
print(dataPSFE)
ticker = "PSFE"
high_PSFE, low_PSFE = get_stock_52_week_high_low(ticker)
print(f"{ticker} 52-Week High: {high_PSFE}")
print(f"{ticker} 52-Week Low: {low_PSFE}")

push_stock_data_to_kinesis("Project5_Stream",kinesis_client,ticker,dataPSFE,high_PSFE,low_PSFE)