print(">>> SCRIPT IS RUNNING <<<")
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os 
import requests


def get_latest_treasury_rates():
    # creating human to machince mapping for fred data
    cache_file = "treasury_cache.csv"
    symbols = {
        '1M' : 'DGS1MO', '3M': 'DGS3MO', '6M': 'DGS6MO',
        '1Y' : 'DGS1', '2Y': 'DGS2','3Y': 'DGS3',
        '5Y' : 'DGS5','7Y':  'DGS7', '10Y': 'DGS10',
        '20Y' : 'DGS20','30Y' : 'DGS30'
    }
    #check if data was fetched today
    if os.path.exists(cache_file):
         file_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
         if file_time.date() ==datetime.now().date():
          print(">>> Using local Cache (No network call needed doesnt require fred)<<<")
          return pd.read_csv(cache_file, index_col=0).iloc[:,0]
    
    try:
        # creating the time window (to 10 days for safety for when delayed quotes happen)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=10)
        
        #Creates a user agent to bypass bot filters
        session  = requests.Session()
        session.headers.update({
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # this next line pulls data from fred
        df = web.DataReader(list(symbols.values()),'fred', start_date, end_date, session=session)
        # clean the data (use forward fill to prevent lagged data recording, so the model can still fetch)
        latest_row  = df.ffill().iloc[-1]

        # invert the mapping to rename ids (dgs) to tenors, this is done by dictionary inverison and mapping the keys to values
        id_to_tenor = {v: k for k, v in symbols.items()}
        latest_row.index = [id_to_tenor[idx] for idx in latest_row.index]

        latest_row.to_csv(cache_file)


        return latest_row

    except Exception as e:
        print(f"Error: {e}")
        
        print(">>> In this instance: We are using Cache Rates <<<")
        fallback_rates=pd.Series({'1M': 3.71, '3M': 3.78, '6M': 3.78, 
            '1Y': 3.84, '2Y': 4.08, '3Y': 4.14, 
            '5Y': 4.21, '7Y': 4.34, '10Y': 4.49, 
             '20Y': 5.00, '30Y': 4.99
             
        })
    fallback_rates.to_csv(cache_file)

    return fallback_rates


if __name__ == "__main__":
        rates = get_latest_treasury_rates()
        print("Fetched Treasury Rates: Successfully called data from fred")
        print(rates)
        if rates is not None:
             # we now create spread relationships and multiple by 100 to get bp
             spread_2y10y = (rates['10Y'] - rates['2Y']) * 100
             print(f"\n10Y-2Y Spread: {spread_2y10y: .2f} bps")
             frontend_spread = (rates['3M'] - rates['1M']) *100
             print(f"3M-M front-end relationship: {frontend_spread:.2f}bps")

        if rates is not None:
             plt.figure(figsize=(12,6))

             # Solid line with markers for each data point rates.index and rates.values are series related terms
             plt.plot(rates.index, rates.values, marker='o', linestyle='-', linewidth=2, color='#008080')

             # marks every tenor with a tick
             plt.xticks(ticks=range(len(rates.index)), labels=rates.index, rotation=45)
             
             # preparing the data and create the table 
             cell_text = [[f"{v:.2f}%"] for v in rates.values]
             plt.table(cellText=cell_text, rowLabels=rates.index, colLabels=['Yield'],
                       loc='right', bbox=[1.05, 0, 0.2, 1])
             
             plt.title("US Treasury Yield Curve", fontsize=17.5)
             plt.xlabel("Tenor (Time to Maturity)", fontsize=11.5)
             plt.ylabel("Yield (%)",fontsize=11.5)
             plt.grid(True, which='both', linestyle='--', alpha=0.5)

             # using tight layout so labels do not get cut off
             plt.tight_layout()
             plt.show()




