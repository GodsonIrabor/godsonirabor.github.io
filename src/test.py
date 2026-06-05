
import textwrap
from curve import TreasuryCurve
from risk import calculate_risk_metric

#Stimulating the inverted curve data this will simply be the 2,10 and 30s curve
market_data = {
    2: 0.062,
    10: 0.038,
    30: 0.029
}
#initalize the curve object with market data essentially creating the curve using the function and marketdata as the argument 
curve = TreasuryCurve(market_data)
#Pricing a 16Y bond using the interpolated yield
tenor_to_test = 16
interpolated_yield = curve.get_yield(tenor_to_test)

print(f"--- Demonstration: {tenor_to_test}Y Tenor---")
print(f"Interpolated Yield: {interpolated_yield:.4%}")

# We now will run risk metrics using what we obtained from the curve derived yield
# In this example we will assume a 5% coupon and 100 face value
quick_metrics =calculate_risk_metric(100,5,interpolated_yield,16)

print(f"Price ${quick_metrics['price']:<9.2f}")
print(f"DV01 {quick_metrics['dv01']:<9.2f}")
print(f"Duration {quick_metrics['duration']:<9.2f}")
print(f"Convexity {quick_metrics['convexity']:<9.2f}")

elaboration = ("Some rates knowledge: here couple things to hone in on some of the FI fundamentals. With a price of 179.20 this indicates the bond is trading at a massive premium, this tracks with the coupon rate which is 5% is much higher than the current market rate. Moving on to other risk metrics, with Duration at 12.65 for a 16yr bond is feasible due to the fact that typically the duration will be much shorted than the actual maturity of the bond.With that in mind, the value also represents that if rates move by 1% or 100bp you can expect a drop or increase of 12.6% in either direction.Moving onto Convexity, a high positive convexity indicate that as rates move then price will increase more when rates fall than it will decrease when rates rise.")

  #print(f"{tenor:<8} |${results['price']:<9.2f} | {results['dv01']:<10.4f} | {results['duration']:<10.4f} | {results['convexity']:<10.4f} |")

elaboration_text = textwrap.fill(elaboration, width=35)
print(elaboration_text)