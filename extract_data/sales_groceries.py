import pandas as pd
from pytrends.request import TrendReq
from time import sleep
from math import ceil

# Load your product list
products_df = pd.read_csv('groceries.csv')

# Clean product names (keywords)
keywords = []

for name in products_df['Name'].tolist():
    # Remove anything after comma or '('
    clean_name = name.split(',')[0].split('(')[0].strip()
    # Split into words and take first two
    first_two_words = ' '.join(clean_name.split()[:2])
    keywords.append(first_two_words)

# Pytrends setup with increased timeout
pytrends = TrendReq(hl='en-IN', tz=330, timeout=(10, 30))

batch_size = 5
num_batches = ceil(len(keywords) / batch_size)

# Generate weekly periods for 2024: weekly frequency ends on Sunday
weeks = pd.date_range(start="2024-01-01", end="2024-12-31", freq='W-SUN').strftime("%Y-%m-%d").tolist()

sales_records = []

for batch_idx in range(num_batches):
    batch_keywords = keywords[batch_idx*batch_size : (batch_idx+1)*batch_size]

    try:
        pytrends.build_payload(batch_keywords, timeframe='2024-01-01 2024-12-31', geo='IN')
        trend_data = pytrends.interest_over_time()
        
        # For each keyword in batch, get weekly data
        for kw in batch_keywords:
            if kw in trend_data.columns:
                weekly_trend = trend_data[kw].resample('W-SUN').mean()
            else:
                weekly_trend = pd.Series([0]*len(weeks), index=pd.date_range('2024-01-07', periods=len(weeks), freq='W-SUN'))

            for week, value in zip(weeks, weekly_trend):
                search_interest = int(value) if not pd.isna(value) else 0
                prod_id = products_df.loc[products_df['Name'].str.contains(kw, case=False, na=False), 'Product ID'].values
                prod_id = prod_id[0] if len(prod_id) > 0 else 'UNKNOWN'

                base_sales = 7  # adjust base sales for weekly period
                units_sold = search_interest * base_sales

                sales_records.append({
                    'Product ID': prod_id,
                    'Week Ending': week,
                    'Search Interest': search_interest,
                    'Units Sold': units_sold
                })

    except Exception as e:
        print(f"Error fetching batch {batch_idx+1}: {e}")

    print(f"Processed batch {batch_idx+1}/{num_batches}")
    sleep(10)  # wait 10 seconds between batches

# Save to CSV
sales_df = pd.DataFrame(sales_records)
sales_df.to_csv('sales_data_weekly.csv', index=False)
