
def calculate_coupon(face_value, coupon_rate):
    return face_value * (coupon_rate / 100)

def calculate_pv(payment, market_rate, years):
    return payment / (1+ market_rate)**years

def price_bond(face_value,coupon_rate,market_rate, years_to_maturity):
    #creates a loop that prices a bond by summing the PV of all future cash flows
    total_price = 0
    annual_payout = calculate_coupon(face_value, coupon_rate)
    # this will check if the bonds maturity is less than a year
    if years_to_maturity <1:
         # due to the short time duration of front end rates we simply calculate the pv of the payout
         # face value + a fraction of the coupon
         payment =face_value + (annual_payout * years_to_maturity)
         total_price = calculate_pv(payment,market_rate,years_to_maturity)
    else:    
        for year in range(1,int (years_to_maturity) +1): # This loop handles full annual coupons, we create one below to handle fractiontional maturities
         total_price += calculate_pv(annual_payout, market_rate,year)

        total_price += calculate_pv(face_value,market_rate,years_to_maturity) # this allows whole numbers and fractional maturities as well.

    return total_price
    # remember annual payout uses the function we created, then it stores it in a variable that loops we then calculate the PV of that value
 
tenyr_bond = price_bond(100,5,0.042,10)
print(f"\nThis is the price of a euro bond : {tenyr_bond: .2f}")
   

def practice_model():
    
        face = 1000
        coupon = 5
        market = 5
        calculationcheck=calculate_coupon(face,coupon)
        print(calculationcheck)

        #we first price the first years bond #hardcoded
        year_1 = calculate_pv(50,5,1)
        year_2 = calculate_pv(1050,5,2)
        full_bond = year_1+year_2
        print(f"\nThis is the full bond price : {full_bond:.2f}")
if __name__=="__main__":
     #in order to run the practice model remove the comment line below under practice model
      #practice_model()
    pass


