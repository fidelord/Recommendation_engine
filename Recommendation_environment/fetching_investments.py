import pandas as pd
import numpy as np
import json

df= pd.read_csv('investment_products.csv')
# This is the server

# Open the JSON file
with open('cosine_similarities.json', 'r') as f:
    # Load the JSON data
    data = json.load(f)

# Now `data` is a Python object containing the data from the JSON file
cos = np.array(data)


def content_based_recommendations(title):
    
    # finding cosine similarity for the vectors

    cosine_similarities = cos
    
    # taking the title and book image link and store in new data frame called books
    investments = df['name']
    #Reverse mapping of the index
    indices = pd.Series(df.index, index = df['name']).drop_duplicates()
         
    idx = indices[title]
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:6]
    investment_products = [i[0] for i in sim_scores]
    recommend = investments.iloc[investment_products]
    return recommend.tolist()

def build_chart(categories, df=df, percentile=0.8, top_n=5):
    # Make a copy of the DataFrame
    dt = df.copy()
    # Initialize an empty list to store selected stocks
    selected_stocks = []

    # Calculate the score for all categories
    for category in categories:
        # Filter the DataFrame by the current category
        category_stocks = dt[dt['Category'] == category]
        # Check if there are stocks in the current category
        if len(category_stocks) > 0:
            # Calculate the mean of 'priceStock' for the current category
            C = category_stocks['priceStock'].mean()
            # Calculate the specified quantile of 'maximumCapital' for the current category
            m = category_stocks['maximumCapital'].quantile(percentile)
            # Calculate a score for each row in the current category using a specified formula
            dt.loc[dt['Category'] == category, 'score'] = category_stocks.apply(lambda x: (x['maximumCapital'] / (x['maximumCapital'] + m) *x['priceStock']) + (m / (m + x['maximumCapital'])*C), axis=1)

    # Iterate over each category provided
    for category in categories:
        # Filter the DataFrame by the current category
        category_stocks = dt[dt['Category'] == category]
        # Sort the DataFrame by the calculated scores in descending order and select the top stock
        top_stock = category_stocks.sort_values('score', ascending=False).head(1)
        # Add the name of the top stock from the current category to the selected stocks list
        selected_stocks.extend(list(top_stock['name']))

    # Calculate the remaining number of stocks needed to reach the cap
    remaining_slots = top_n - len(selected_stocks)
    # Initialize a set to keep track of selected categories
    selected_categories = set()

    # If there are remaining slots and categories, fill them with the top stocks from other categories
    while remaining_slots > 0 and len(selected_categories) < len(categories):
        # Iterate over each category provided
        for category in categories:
            # Check if the category has already been selected
            if category not in selected_categories:
                # Filter the DataFrame by the current category
                category_stocks = dt[dt['Category'] == category]
                # Exclude the stocks already selected
                category_stocks = category_stocks[~category_stocks['name'].isin(selected_stocks)]
                # If there are stocks available in the current category
                if len(category_stocks) > 0:
                    # Sort the DataFrame by the calculated scores in descending order and select the top stocks to fill the remaining slots
                    top_stocks = category_stocks.sort_values('score', ascending=False).head(remaining_slots)
                    # Extend the selected stocks list with the names of the top stocks from the current category
                    selected_stocks.extend(list(top_stocks['name']))
                    # Update the remaining number of slots
                    remaining_slots = top_n - len(selected_stocks)
                    # Add the selected category to the set of selected categories
                    selected_categories.add(category)
                    # If all slots are filled, break the loop
                    if remaining_slots <= 0:
                        break

    # Return the selected stocks, capped at the specified number
    return selected_stocks[:top_n]

