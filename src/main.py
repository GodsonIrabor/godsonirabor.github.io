from data import get_latest_treasury_rates
from pricing import price_bond

def main():
    # pulls live data from fred (using the data module we built)
    rates = get_latest_treasury_rates()

    if rates is not None:
#  creating a float dictionary for curve.py this is required so data that flows into main.py can handle float (values with decimals)
        curve_points = {}
        for t_str, yld in rates.items():
            yrs = int(t_str.replace('M',''))/12 if 'M' in t_str else int(t_str.replace('Y',''))
            curve_points[yrs] = yld / 100.0 # this normalizes to decimal

            from curve import TreasuryCurve
            market_curve = TreasuryCurve(curve_points)
        # tenors from data py (important to use all including front end for risk free rate)
        #full_tenors = ['1M', '3M', '1Y','2Y','3Y','5Y','7Y','10Y','15Y','20Y','30Y']
        target_tenor = 10
        yield_at_tenor = market_curve.get_yield(target_tenor)
        print(f"Tenor: {target_tenor} Yield: {yield_at_tenor:.4%}")
        #print(f"{'Tenor':<8} | {'Yield':<8} | {'Price':<10}")
        #print("-" * 35)
        
        #results = {} # creates an empty dicitionary so all prices can be saved
        #for tenor in full_tenors:
            #if tenor in rates:
                #market_yield = rates[tenor]
                # this will convert tenor string into to numerical years so 3m becomes -> 0.2
                #if 'M' in tenor:
                    #maturity_in_years = int(tenor.replace('M', '')) /12
                #else:
                    #maturity_in_years =int(tenor.replace('Y', ''))
                # the price function will now be able to handle front end rates as well as long dated tenors

                #normalizing for when using hardcoded data and not data from fred
                #adj_yield = market_yield / 100 if market_yield > 1 else market_yield
                #price = price_bond(100,5,adj_yield,maturity_in_years)
                #results[tenor] = price #saves price in dictionary
                
                #par_price = price_bond(100, market_yield,market_yield, maturity_in_years)
                #results[tenor] = price # saves price in a dictionary
                #print(f"{tenor:<8} | {market_yield:>6.2f}% | ${par_price:>8.2f}")
                
    #ten_year_yield = rates['10Y']
    #ten_year_yield_price = price_bond(100, 5, ten_year_yield,10)
    #print(f"The price of a 10Y bond with a 5% coupon is: {ten_year_yield_price:.2f}")
    #spread_between_30yrand10yr = (rates['30Y'] - rates['10Y']) * 100 
    #print(f"The 10yrs and 30srs relationship is: {spread_between_30yrand10yr:.2f}")    
if __name__=="__main__":
    main()
