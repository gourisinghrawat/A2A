import pandas as pd
from pytrends.request import TrendReq
import time
import os

# # Initialize Pytrends with India settings
# pytrend = TrendReq(hl='en-IN', tz=330)  # Host language: English-India, Timezone: IST (+330 minutes)
# New: add timeout parameter
pytrend = TrendReq(hl='en-IN', tz=330, timeout=(10, 25))

# Map Product IDs to simplified product names for Trends queries and full names for merging
product_mapping = {
    'CLN001': {'search_name': 'Lizol Floor Cleaner', 'full_name': 'Lizol Floor Cleaner (Citrus) 2L'},
    'CLN002': {'search_name': 'Colin Glass Cleaner', 'full_name': 'Colin Glass Cleaner 500ml'},
    'CLN003': {'search_name': 'Vim Bar', 'full_name': 'Vim Bar (3x150g)'},
    'CLN004': {'search_name': 'Surf Excel Quick Wash', 'full_name': 'Surf Excel Quick Wash 2kg'},
    'CLN005': {'search_name': 'Harpic Toilet Cleaner', 'full_name': 'Harpic Toilet Cleaner 1L'},
    'CLN006': {'search_name': 'Dettol Antiseptic Liquid', 'full_name': 'Dettol Antiseptic Liquid 500ml'},
    'CLN007': {'search_name': 'Scotch-Brite Scrub Pad', 'full_name': 'Scotch-Brite Scrub Pad (5 pcs)'},
    'CLN008': {'search_name': 'Domex Floor Cleaner', 'full_name': 'Domex Disinfectant Floor Cleaner'},
    'CLN009': {'search_name': 'Pril Dishwash', 'full_name': 'Pril Liquid Dishwash 750ml'},
    'CLN010': {'search_name': 'Easy Off Bang', 'full_name': 'Easy Off Bang Bathroom Cleaner'},
    'CLN011': {'search_name': 'Surf Excel Matic Liquid', 'full_name': 'Surf Excel Matic Liquid 1L'},
    'CLN012': {'search_name': 'Dettol Disinfectant Spray', 'full_name': 'Dettol Surface Disinfectant Spray'},
    'CLN013': {'search_name': 'Lizol Floral Disinfectant', 'full_name': 'Lizol Floral Disinfectant 2L'},
    'CLN014': {'search_name': 'Nirma Washing Powder', 'full_name': 'Nirma Washing Powder 1kg'},
    'CLN015': {'search_name': 'Fabuloso Multi-Surface Cleaner', 'full_name': 'Fabuloso Multi-Surface Cleaner'},
    'CLN016': {'search_name': 'Tide Detergent Powder', 'full_name': 'Tide Detergent Powder 2kg'},
    'CLN017': {'search_name': 'Mr Muscle Kitchen Cleaner', 'full_name': 'Mr Muscle Kitchen Cleaner 500ml'},
    'CLN018': {'search_name': 'Himalaya Baby Wipes', 'full_name': 'Himalaya Gentle Baby Wipes (72)'},
    'CLN019': {'search_name': 'Savlon Disinfectant Spray', 'full_name': 'Savlon Surface Disinfectant Spray'},
    'CLN020': {'search_name': 'Vanish Oxi Action', 'full_name': 'Vanish Oxi Action Stain Remover 400g'},
    'CLN021': {'search_name': 'Lizol Lavender Disinfectant', 'full_name': 'Lizol Lavender Disinfectant 1L'},
    'CLN022': {'search_name': 'Colin Multipurpose Spray', 'full_name': 'Colin Multipurpose Spray 500ml'},
    'CLN023': {'search_name': 'Vim Liquid Gel', 'full_name': 'Vim Liquid Gel 500ml'},
    'CLN024': {'search_name': 'Tide Matic Front Load', 'full_name': 'Tide Matic Front Load 1kg'},
    'CLN025': {'search_name': 'Harpic Power Plus', 'full_name': 'Harpic Power Plus 500ml'},
    'CLN026': {'search_name': 'Dettol Hand Sanitizer', 'full_name': 'Dettol Hand Sanitizer 200ml'},
    'CLN027': {'search_name': 'Scotch-Brite Heavy Duty', 'full_name': '3M Scotch-Brite Heavy Duty'},
    'CLN028': {'search_name': 'Domex Toilet Cleaner', 'full_name': 'Domex Toilet Cleaner 1L'},
    'CLN029': {'search_name': 'Pril Lime Dishwash', 'full_name': 'Pril Lime Dishwash 500ml'},
    'CLN030': {'search_name': 'Mr Muscle Drain Cleaner', 'full_name': 'Mr Muscle Drain Cleaner 1L'},
    'CLN031': {'search_name': 'Surf Excel Easy Wash', 'full_name': 'Surf Excel Easy Wash 1kg'},
    'CLN032': {'search_name': 'Savlon Antiseptic Liquid', 'full_name': 'Savlon Antiseptic Liquid 500ml'},
    'CLN033': {'search_name': 'Dettol Hand Wash', 'full_name': 'Dettol Hand Wash 750ml'},
    'CLN034': {'search_name': 'Lizol Pine Disinfectant', 'full_name': 'Lizol Pine Disinfectant 2L'},
    'CLN035': {'search_name': 'Tide Plus Jasmine', 'full_name': 'Tide Plus Jasmine 1kg'},
    'CLN036': {'search_name': 'Easy Off Bang Degreaser', 'full_name': 'Easy Off Bang Degreaser 750ml'},
    'CLN037': {'search_name': 'Harpic Bathroom Cleaner', 'full_name': 'Harpic Bathroom Cleaner 500ml'},
    'CLN038': {'search_name': 'Nirma Detergent Cake', 'full_name': 'Nirma Detergent Cake 250g'},
    'CLN039': {'search_name': 'Fabuloso Citrus Cleaner', 'full_name': 'Fabuloso Citrus Multi-Cleaner'},
    'CLN040': {'search_name': 'Domex Surface Cleaner', 'full_name': 'Domex Surface Cleaner 1L'}
}

# Create directory for output CSVs
os.makedirs('trends_data_25', exist_ok=True)

# Batch products into groups of 5
all_trends = []
for i in range(0, len(product_mapping), 5):
    batch_ids = list(product_mapping.keys())[i:i+5]
    batch_keywords = [product_mapping[pid]['search_name'] for pid in batch_ids]
    print(f"Processing batch: {batch_keywords}")
    try:
        
        pytrend.build_payload(kw_list=batch_keywords, cat=0, timeframe='2025-01-01 2025-06-30', geo='IN')
        # Get interest over time
        df = pytrend.interest_over_time()
        if not df.empty:
            # Remove isPartial column if present
            if 'isPartial' in df.columns:
                df = df.drop(columns=['isPartial'])
            # Add ProductID column
            df['ProductID'] = None
            for pid, search_name in zip(batch_ids, batch_keywords):
                if search_name in df.columns:
                    df.loc[:, f'ProductID_{search_name}'] = pid
            all_trends.append(df)
            # Save batch to CSV
            df.to_csv(f'trends_data_25/trends_batch_{i}.csv')
    except Exception as e:
        print(f"Error processing batch {batch_keywords}: {e}")
    # Avoid rate limits
    time.sleep(20)

# Combine all batches
if all_trends:
    combined_trends = pd.concat(all_trends, axis=1)
    # Remove duplicate columns (e.g., date) if any
    combined_trends = combined_trends.loc[:, ~combined_trends.columns.duplicated()]
    combined_trends.to_csv('trends_data_25/combined_trends_2025.csv')
    print("Combined Trends data saved to 'trends_data_25/combined_trends_2025.csv'")

    # Reshape Trends data for merging
    trends_melted = combined_trends.reset_index().melt(id_vars=['date'], var_name='search_name', value_name='SearchInterest')
    # Map search names to full product names and Product IDs
    reverse_mapping = {v['search_name']: {'ProductID': k, 'ProductName': v['full_name']} for k, v in product_mapping.items()}
    trends_melted['ProductID'] = trends_melted['search_name'].map(lambda x: reverse_mapping.get(x, {}).get('ProductID'))
    trends_melted['Month'] = trends_melted['date']
    trends_melted = trends_melted[['ProductID', 'Month', 'SearchInterest']].dropna(subset=['ProductID'])
    trends_melted.to_csv('trends_data_25/trends_melted_2024.csv')

    # Merge with sales data (assuming cleaning_products_sales_2025.csv exists)
    try:
        sales_df = pd.read_csv('cleaning_products_sales_2025.csv')
        merged_df = pd.merge(sales_df, trends_melted, on=['ProductID', 'Month'], how='left')
        merged_df['SearchInterest'] = merged_df['SearchInterest'].fillna(0)  # Handle missing Trends data
        merged_df.to_csv('merged_sales_trends_2023.csv')
        print("Merged sales and Trends data saved to 'merged_sales_trends_2025.csv'")
    except FileNotFoundError:
        print("Sales data file 'cleaning_products_sales_2025.csv' not found. Trends data saved separately.")
else:
    print("No Trends data retrieved.")