import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from data import get_latest_treasury_rates
from curve import TreasuryCurve
from risk import calculate_risk_metric
from pricing import price_bond


#First let's create the User interface
st.set_page_config(page_title="Fixed Income Dashboard", layout="wide")
st.title(" Latest Treasury Yield & Analytics")
st.markdown("The purpose of this dashboard is to utilize FRED data to model the yield curve and price theortical bonds with relevant risk metrics")

#@st.cache_data(ttl=3600) # caches data for 1 hour
rates = get_latest_treasury_rates()

if rates is not None:
    curve_points = {}
    for t_str, yld in rates.items():
        #reusing same loop to ensure robustness
        yrs = int(t_str.replace('M', ''))/12 if 'M' in t_str else int(t_str.replace('Y',''))
        curve_points[yrs] = yld / 100.0 if yld > 1 else yld

    #call the treasurycurve with the curve points
    market_curve = TreasuryCurve(curve_points)
    
    #Desigining the sidebar that allows for dynamic inputs
    st.sidebar.header("Customizable Bond Cstharacteristics")
    target_tenor = st.sidebar.slider("Maturity Selection (Years, 1M - 30Y)",0.25, 30.0, 10.0, step=0.25)
    coupon_rate = st.sidebar.number_input("Coupon Rate (%)", min_value=0.0, max_value=20.0, value=5.0)
    par_value = 100

    # Using function from our previous modules we pull interpolated yield
    live_yield = market_curve.get_yield(target_tenor)

    # bring in risk metricks from our risk module
    metrics = calculate_risk_metric(par_value,coupon_rate,live_yield,target_tenor)


    #Finally we create the dashboard display

    col1, col2, col3, col4,col5 = st.columns(5)
    col1.metric("Interpolated Yield", f"{live_yield:.4%}")
    col2.metric("Calculated Bond Price", f"${metrics['price']:.2f}")
    col3.metric("DV01", f"{metrics['dv01']:.4f}")
    col4.metric("Modified Duration",f"{metrics['duration']:.4f}")
    col5.metric("Convexity", f"{metrics['convexity']:.2f}")

    st.divider()

    #Now for some visualization
    st.subheader("Market Snapshot")
    # Converts series to DataFrame for a clean table
    df_rates = pd.DataFrame(rates).reset_index()
    df_rates.columns = ['Tenor', 'Yield (%)']
    st.table(df_rates.set_index('Tenor').T)

    #Creating a sidebar for Scenario analysis /  fed movements
    st.sidebar.header("Stress Testing")
    bps_shock = st.sidebar.slider("Parallel Yield Shift (bps)", -100, 100, 0, 5)
    yield_shock = bps_shock / 10000.0

    #Calculation below will apply the bps impact onto the bond #instead of market_yield should be live_yield
    shocked_yield = live_yield + yield_shock #below could next to shocked_yield should be target_tenor
    shocked_price = price_bond(100, coupon_rate, shocked_yield,target_tenor)
    price_impact = shocked_price - metrics['price']

    # Calculating post shock risk metrics
    scenario_metrics =calculate_risk_metric(100,coupon_rate,shocked_yield,target_tenor)
    #calcuting raw number difference first
    dv01_impact = scenario_metrics['dv01'] - metrics['dv01']
    duration_impact = scenario_metrics['duration'] - metrics['duration']
    convexity_impact =  scenario_metrics['convexity'] - metrics['convexity']
    #Scenario metrics
    st.subheader(f"Scenario Impact: {bps_shock}bps {'Hike' if bps_shock >=0 else 'Cut'}")
    scol1, scol2,scol3,scol4,scol5= st.columns(5)
    scol1.metric("Scenario Price", f"${shocked_price:.2f}",  delta=f"{price_impact:.2f}")
    scol2.metric("Scenario Yield", f"{(shocked_yield *100):.4f}%",delta=f"{bps_shock} bps")
    if dv01_impact <0:
        dv01_deltra_str = f"-${abs(dv01_impact):.4f}"
    else:
        dv01_deltra_str = f"${dv01_impact:.4f}"
    scol3.metric("Scenario DV01", f"${scenario_metrics['dv01']:.4f}",delta=dv01_deltra_str)
    scol4.metric("Scenario Duration", f"{scenario_metrics['duration']:.4f}",delta=f"{duration_impact:.4f}")
    scol5.metric("Scenario Convexity", f"{scenario_metrics['convexity']:.2f}",delta=f"{convexity_impact:.2f}")     
    #col3.metric("DV01", f"{metrics['dv01']:.4f}")
    #col4.metric("Modified Duration",f"{metrics['duration']:.4f}")
    #col5.metric("Convexity", f"{metrics['convexity']:.2f}")
                  
    #simulating 100 points for a smooth curve using values 0.25 - 30 yrs
    plot_tenors = np.arange(0.25, 30.25,0.25)
    # # We then calculate yields for the original and shocked curved, put them them in a dataframe and then create a chart 
    # # also multiplying by 100 so the chart displays percentages
    chart_data = pd.DataFrame({
         'Tenor (Years)': plot_tenors,
         'Current Curve': [market_curve.get_yield(t) * 100 for t in plot_tenors],
         'Scenario Curve': [(market_curve.get_yield(t) + yield_shock) * 100 for t in plot_tenors]
     })


    # Using ploty for creative display
    fig = go.Figure()
    # Creating the current curve #darkslateblue
    fig.add_trace(go.Scatter(
        x=chart_data['Tenor (Years)'],
        y=chart_data['Current Curve'],
        mode='lines',
        name='Current Market Curve',
        line=dict(color='darkseagreen', width =2),
        hovertemplate='Tenor: %{x}Y<br>Yield: %{y:.4f}%' #Hover format
    ))
    #Scenario curve
    fig.add_trace(go.Scatter(
        x=chart_data['Tenor (Years)'],
        y=chart_data['Scenario Curve'],
        mode='lines',
        name=f'Scenario ({bps_shock} bps Shift)',
        line=dict(color='darkslateblue',width=2, dash='dash'),
        hovertemplate='Tenor: %{x}Y<br>Yield: %{y:.4f}'
    ))

    # creating a  vertical anchor to make it lockable
    fig.add_vline(
        x=target_tenor,
        line_width=2,
        line_dash="dot",
        line_color="orange",
        annotation_text=f"Selected: {target_tenor}Y",
        annotation_position="top left"

    )
    #Making the legend and axis labels
    fig.update_layout(
        title={
            'text': "Treasury Yield Curve: Current Market compared to Scenario",
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        # creating x axis
        xaxis_title="Time to Maturity (Years)",
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=2, #labels every 2 years keeps the axis clean
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)' #Creates dark theme
        ),

           #creating y axis
        yaxis_title="Yield (%)",
        yaxis=dict(
            ticksuffix="%", # Adds % sign to the axis number
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        ),
        legend=dict(
            orientation="h", # Horizontal legend
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=50, r=50, b=50, t=120),
        hovermode="x unified",
        template="plotly_dark"
       

        
       
        
    )

    # calling the chart using plotly
    st.plotly_chart(fig, use_container_width=True)





    #yield curve creation
    #st.subheader("Yield Curve Term Structure: Current vs. Scenario")

    #simulating 100 points for a smooth curve using values 0.25 - 30 yrs
    # tenors = np.linspace(0.25, 30,100)
    # # We then calculate yields for the original and shocked curved, put them them in a dataframe and then create a chart 
    # # also multiplying by 100 so the chart displays percentages
        #chart_data = pd.DataFrame({
         #'Tenor (Years)': tenors,
         #'Current Curve': [market_curve.get_yield(t) * 100 for t in tenors],
         #'Scenario Curve': [(market_curve.get_yield(t) + yield_shock) * 100 for t in tenors]
    # })
    # # Display the chart
    # st.line_chart(chart_data.set_index('Tenor (Years)'))
    # #this is a deterministic model remember


