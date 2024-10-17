This web app allows users to scrape stock data from Screener.in and perform intrinsic valuation based on user inputs. The app also calculates the degree of overvaluation using a Growth-RoC DCF model with an explicit fade period.

**Features**:
**Stock Data Scraper**: Scrapes real-time stock data such as Stock P/E, Market Cap, FY23 Net Profit, and RoCE.

**Intrinsic PE Calculation**: Uses user inputs such as cost of capital, RoCE, growth rate, high growth period, fade period, and terminal growth rate to calculate intrinsic PE.

**Degree of Overvaluation**: Computes the degree of overvaluation based on either the current PE or FY23 PE.

**5-Year Median Pre-tax RoCE**: Calculates the 5-year median pre-tax RoCE from historical data.

**Dynamic Calculations**: The user can adjust financial factors, and the data updates dynamically without requiring a symbol reload.

**User Inputs**:

**Cost of Capital (%)**: The cost of capital used in the DCF model.

**RoCE (%)**: Return on Capital Employed.

**Growth During High Growth Period ($)**: Growth in absolute terms during the high growth period.

**High Growth Period (Years)**: Duration of the high growth period.

**Fade Period (Years)**: Duration of the fade period.

**Terminal Growth Rate (%)**: The terminal growth rate after the fade period.

**How It Works:**
The app scrapes stock data from Screener.in by entering the NSE/BSE symbol provided by the user.
After scraping the data, the user can enter inputs for calculating the intrinsic PE and degree of overvaluation.
The calculation uses the Growth-RoC DCF model, which projects cash flows during a high growth period followed by a fade period, then discounts them to present value.

**Example:**
If the user enters **NESTLEIND** as the stock symbol, the app scrapes the **current Stock P/E, Market Cap, FY23 Net Profit**, and **RoCE**.
Then, based on user-defined factors like cost of capital and growth, the app calculates intrinsic PE and displays the degree of overvaluation.

**Prerequisites:**
Python 3.x
Streamlit
BeautifulSoup4
Requests

**Installation:**
Clone the Repository:

**Terminal**
git clone https://github.com/yourusername/Stock-app.git
cd Stock-app
Install the Required Libraries: Open the terminal and run the following command to install dependencies:

**Terminal**
pip install streamlit beautifulsoup4 requests
Run the Application: After installing the necessary packages, you can run the app using Streamlit:

**Terminal**
streamlit run streamlit_app.py
Access the Application:

Once the app is running, Streamlit will provide a local or public URL to access the application.
Deployment:
This app is developed in GitHub Codespace. If you'd like to deploy it:

**Expose the Port**: In GitHub Codespace, ensure the port (8501) is exposed as Public in the Ports section of the Codespace window.

**Access the App:**

You can access the running app via the provided URL:
**Active link**: Stock Web App
**Note**: This URL might require a GitHub login to access.

**Code Repository**:
Link to the source code: GitHub Repository
Troubleshooting:
If you encounter issues such as missing modules or errors:

Ensure all required Python packages are installed correctly using pip install.
Verify that port 8501 is publicly accessible in GitHub Codespace.
