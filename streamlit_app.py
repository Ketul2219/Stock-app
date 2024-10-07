import streamlit as st
import requests
from bs4 import BeautifulSoup

# Cache the scraping function to avoid repeated calls when user changes input values
@st.cache_data
def scrape_data(symbol):
    url = f"https://www.screener.in/company/{symbol}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Initialize data dictionary
    data = {}

    # Scrape Stock P/E
    li_tags = soup.find_all('li', class_="flex flex-space-between", attrs={"data-source": "default"})
    for li in li_tags:
        if 'Stock P/E' in li.find('span', class_='name').text:
            data['Stock P/E'] = li.find('span', class_='number').text.strip()
            break
    else:
        data['Stock P/E'] = "N/A"

    # Scrape Market Cap
    for li in li_tags:
        if 'Market Cap' in li.find('span', class_='name').text:
            market_cap_text = li.find('span', class_='number').text.strip()
            market_cap = float(market_cap_text.replace(',', ''))  # Convert to ₹
            data['Market Cap'] = market_cap
            break
    else:
        data['Market Cap'] = "N/A"
    
    # Scrape FY23 Net Profit by summing Mar, Jun, Sep, Dec 2023 values
    net_profit_table = soup.find('table', class_='data-table')
    if net_profit_table:
        headers = [header.text.strip() for header in net_profit_table.find('thead').find_all('th')]  # Get years
        rows = net_profit_table.find_all('tr')  # All data rows

        # We are looking for the row that contains 'Net Profit'
        for row in rows:
            if 'Net Profit' in row.text:
                net_profit_cells = row.find_all('td')[1:]  # Exclude first cell as it contains the label 'Net Profit'
                net_profit_values = [cell.text.strip().replace(',', '') for cell in net_profit_cells]

                # Calculate FY23 Net Profit by summing values for Mar, Jun, Sep, Dec 2023
                fy23_quarters = ['Mar 2023', 'Jun 2023', 'Sep 2023', 'Dec 2023']
                fy23_net_profit = 0
                for quarter in fy23_quarters:
                    if quarter in headers:
                        index = headers.index(quarter) - 1  # Adjust by -1 for the corresponding <td> index
                        fy23_net_profit += float(net_profit_values[index])

                data['FY23 Net Profit'] = f"{fy23_net_profit:.2f} Cr"
                break
    else:
        data['FY23 Net Profit'] = "N/A"

    # Scrape RoCE
    for li in li_tags:
        if 'ROCE' in li.find('span', class_='name').text:
            data['RoCE'] = li.find('span', class_='number').text.strip()
            break
    else:
        data['RoCE'] = "N/A"

    return data

# Function to calculate intrinsic PE and degree of overvaluation
def calculate_intrinsic_pe(current_pe, fy23_pe, cost_of_capital, roce, growth, high_growth_years, fade_years, terminal_growth_rate):
    # Calculate intrinsic PE using the DCF model
    tax_rate = 0.25
    total_value = 0
    
    # Calculate cash flows for the high growth period
    for year in range(high_growth_years):
        cash_flow = fy23_pe * (1 + growth) ** year * (1 - tax_rate)
        total_value += cash_flow / ((1 + cost_of_capital) ** (year + 1))
    
    # Calculate cash flows for the fade period
    for year in range(fade_years):
        growth_rate = (growth - terminal_growth_rate) * (1 - (year / fade_years)) + terminal_growth_rate
        cash_flow = fy23_pe * (1 + growth_rate) ** (high_growth_years) * (1 - tax_rate)
        total_value += cash_flow / ((1 + cost_of_capital) ** (high_growth_years + year + 1))
    
    intrinsic_pe = total_value / (fy23_pe * (1 - tax_rate))  # Adjust for tax
    
    return intrinsic_pe

# Streamlit app interface
st.title("Dynamic Stock Data and Intrinsic PE Calculator")

# Input for stock symbol
symbol = st.text_input("Enter the NSE/BSE Symbol:", "NESTLEIND")

# Scrape data dynamically when symbol is entered
if symbol:
    data = scrape_data(symbol)

    if data:
        st.write("### Stock Data")
        st.write(f"**Stock P/E**: {data['Stock P/E']}")
        st.write(f"**Market Cap**: ₹{data['Market Cap']:,} Cr")
        st.write(f"**FY23 Net Profit**: {data['FY23 Net Profit']}")
        st.write(f"**RoCE**: {data['RoCE']}%")

        # Inputs for intrinsic PE calculation
        st.subheader("Intrinsic PE Calculation")
        cost_of_capital = st.number_input("Cost of Capital (%)", min_value=0.0, value=10.0)
        roce = st.number_input("RoCE (%)", min_value=0.0, value=15.0)
        growth = st.number_input("Growth During High Growth Period (%)", min_value=0.0, value=10.0)
        high_growth_years = st.number_input("High Growth Period (Years)", min_value=1, value=15)
        fade_years = st.number_input("Fade Period (Years)", min_value=1, value=15)
        terminal_growth_rate = st.number_input("Terminal Growth Rate (%)", min_value=0.0, value=2.0)

        # Convert inputs from percentages to decimals
        cost_of_capital /= 100
        roce /= 100
        growth /= 100
        terminal_growth_rate /= 100
        
        # Calculate intrinsic PE
        if data['Stock P/E'] != "N/A" and data['FY23 Net Profit'] != "N/A":
            current_pe = float(data['Stock P/E'])
            fy23_pe = current_pe  # or calculate FY23 PE as needed
            
            intrinsic_pe = calculate_intrinsic_pe(current_pe, fy23_pe, cost_of_capital, roce, growth, high_growth_years, fade_years, terminal_growth_rate)
            st.write(f"**Intrinsic PE**: {intrinsic_pe:.2f}")
            
            # Calculate degree of overvaluation
            if current_pe < fy23_pe:
                degree_of_overvaluation = (current_pe / intrinsic_pe) - 1
            else:
                degree_of_overvaluation = (fy23_pe / intrinsic_pe) - 1
                
            st.write(f"**Degree of Overvaluation**: {degree_of_overvaluation:.2%}")
