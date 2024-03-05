# ###################################################################################################
#  # Business Problem
# ##################################################################################################

# Gezinomi uses some features of its sales to make level-based sales.
# To create new sales definitions and create segments according to their definitions and create new segments based on these segments.
# How much money can prospective customers bring to the company on average?


# ###################################################################################################
# gezinomi.xlsx Dataset
# ##################################################################################################

# gezinomi.xlsx data set shows the prices of sales made by Gezinomi company and contains information about sales.
# The data set consists of records created in each sales transaction is occurring.
# This means the table is not deduplicated. In other words the customer may have made more than one purchase.

# ###################################################################################################
# # Variables
# ##################################################################################################

# SaleId: Sales ID
# SaleDate: Sale Date
# Price: Amount paid for the sale
# ConceptName: Information about the hotel concept
# SaleCityName: Information about the city where the hotel is located
# CheckInDate: Customer's hotel check-in date
# CInDay: Customer's day of hotel check-in
# SaleCheckInDayDiff: Difference in days between check-in and sale date
# Season: Information about the season on the hotel check-in date


# importing libraries and adjusting some settings
import pandas as pd
pd.set_option('display.max_column', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', '{:.2f}'.format)

# Read gezinomi.xlsx file to start working on the data set and have a quick look

df = pd.read_excel('datasets/gezinomi.xlsx')
df.info()

# Sort the output of the City-Concept-Season breakdown according to PRICE.
# Save the output you get as agg_df.

agg_df = df.groupby(['SaleCityName', 'ConceptName', 'Seasons']).agg({'Price': 'mean'}).sort_values(by='Price', ascending=False)

# Column names becomes index, so we need to fix the indexes
agg_df = agg_df.reset_index()

# Define new level-based customers (personas).

agg_df['Sales_Level_Based'] = agg_df[['SaleCityName', 'ConceptName', 'Seasons']].agg(lambda x: '_'.join(x).upper(), axis=1)

# Divide new personas into 4 segments according to PRICE.

agg_df['Segment'] = pd.qcut(df['Price'], 4, labels=['D', 'C', 'B', 'A'])

# Drop unnecessary columns
agg_df = agg_df[['Sales_Level_Based', 'Segment', 'Price']]

# Classify new customers and estimate how much revenue they can bring
# for example:

new_user = 'ANTALYA_HERŞEY DAHIL_HIGH'
agg_df[agg_df['Sales_Level_Based'] == new_user]

new_user2 = 'GIRNE_YARIM PANSIYON_LOW'
agg_df[agg_df['Sales_Level_Based'] == new_user2]

new_user3 = 'İZMIR_HERŞEY DAHIL_HIGH'
agg_df[agg_df['Sales_Level_Based'] == new_user3]

