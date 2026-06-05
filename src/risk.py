from pricing import price_bond

def calculate_risk_metric(face_value,coupon, market_yield,maturity):
    #this function will be used to calculate metrics using dynamic inputs, remember that market yield must be normalized 

    #base price of an example bond
    p_base = price_bond(face_value,coupon,market_yield,maturity)

    # we will now create a way to perform shock up and down to a bond used for risk calculations
    # 1bp is (0.0001) as the standard value
    h = 0.0001
    p_up = price_bond(face_value,coupon, market_yield +h, maturity)
    p_down = price_bond(face_value,coupon, market_yield -h ,maturity)

    # primary risk calculations

    # dollar value of a 1 bp move, average change for a 1bp move regardless of direction
    dv01 =((p_down-p_up) / 2 ) 
    #first linear approximation of price , an approximate % change in price for a 1%  (100bp) move in yield 
    # (h*100) turns 0.0001 into 0.01 representing 1%
    duration = (p_down -p_up) / (2 * p_base * h) #modified duration
    # second linear approximation of price, this metric measures the curvature/accerelation of price change
    # (h* 100) **2 scales the denomintaor to units squared
    convexity = (p_up+p_down - 2 * p_base) / (p_base * h**2)

    return {
        "price":p_base,
        "dv01": dv01,
        "duration": duration,
        "convexity":convexity
    }

# quick sandbox test
if __name__ =="__main__":
    test_data = [("10Y", 0.0446), ("30Y", 0.0463)]
    #once  congifured this data will come from data.py which pulls from fred
    # we use tuples to stimulate tenor and yield in the example

    print(f"{'Tenor':<8} | {'Price':<10} | {'DV01': <10} | {'Duration':<10} | {'Convexity':<10}")
    print("-" *45)

    for tenor, rate in test_data:
        # normalization if i get rate blocked again
        

        # pulls maturity from the string and turns into understandable format
        yrs = int(''.join(filter(str.isdigit, tenor)))
        results = calculate_risk_metric(100,5,rate, yrs)

        print(f"{tenor:<8} | ${results['price']:<9.2f} | {results['dv01']:<10.4f} | {results['duration']:<10.4f} | {results['convexity']:<10.4f} |")


       