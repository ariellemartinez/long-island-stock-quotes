import os
import pandas as pd
import finnhub
from itertools import batched
import time

finnhub_api_key = os.environ.get("FINNHUB_API_KEY")

public_companies_dataframe = pd.read_csv("csv/public-companies.csv")
public_companies = public_companies_dataframe.to_dict("records")

finnhub_client = finnhub.Client(api_key=finnhub_api_key)

quotes = []

for batch in batched(public_companies, 30):
	for public_company in list(batch):
		quote = finnhub_client.quote(public_company["symbol"])
		quote["Name"] = public_company["name"]
		quote["Symbol"] = public_company["symbol"]
		quotes.append(quote)
	time.sleep(1)

quotes_dataframe = pd.DataFrame(quotes)
quotes_dataframe = quotes_dataframe.rename(columns={"c": "Current price", "d": "Change", "dp": "Percent change", "h": "High price of the day", "l": "Low price of the day", "o": "Open price of the day", "pc": "Previous close price", "t": "UNIX seconds timestamp"})
quotes_dataframe["Date and time"] = pd.to_datetime(quotes_dataframe["UNIX seconds timestamp"], unit="s")
quotes_dataframe["Date and time"] = quotes_dataframe["Date and time"].dt.tz_localize("UTC").dt.tz_convert("US/Eastern").dt.strftime("%Y-%m-%d %H:%M:%S")
quotes_dataframe = quotes_dataframe[["Name", "Symbol", "Current price", "Change", "Percent change", "High price of the day", "Low price of the day", "Open price of the day", "Previous close price", "Date and time"]]
quotes_dataframe.to_csv("csv/stock-quotes.csv", index=False)