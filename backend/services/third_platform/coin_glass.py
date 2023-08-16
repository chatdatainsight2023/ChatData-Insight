import requests
from core.config import Config

COIN_GLASS_API = Config.COIN_GLASS_API
import requests
import pandas as pd
import plotly.graph_objects as go
import json
import datetime
import random
import string
import os
import numpy as np

# Generate random string of length 8
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_liquidation_top(question):

    url = "https://open-api.coinglass.com/public/v2/liquidation_top?time_type=h12"

    headers = {
        "accept": "application/json",
        "coinglassSecret": COIN_GLASS_API
    }

    response = requests.get(url, headers=headers)

    data = json.loads(response.text)["data"]
    df = pd.DataFrame(data)
    
    # Convert columns to appropriate data types
    numerical_cols = ['number', 'amount', 'longVolUsd', 'shortVolUsd', 'totalVolUsd']
    for col in numerical_cols:
        df[col] = pd.to_numeric(df[col])

    # Sort the dataframe by the 'totalVolUsd' column in descending order
    df = df.sort_values(by='totalVolUsd', ascending=False)

    # Generate color based on 'longVolUsd' and 'shortVolUsd'
    df['color'] = df.apply(lambda row: 'Green' if row['shortVolUsd'] > row['longVolUsd'] else 'Red', axis=1)

    # Convert volume to millions
    df['longVolUsd'] = df['longVolUsd']/1000000
    df['shortVolUsd'] = df['shortVolUsd']/1000000
    df['totalVolUsd'] = df['totalVolUsd']/1000000

    # Generate labels for the treemap
    df['label'] = df['symbol'] + '<br>Total: ' + df['totalVolUsd'].round(2).astype(str) + ' M'
    df['label'] = np.where(df.index < 5, df['label'] + '<br>Long: ' + df['longVolUsd'].round(2).astype(str) + ' M<br>Short: ' + df['shortVolUsd'].round(2).astype(str) + ' M', df['label'])

    # Create a treemap
    fig = go.Figure(go.Treemap(
        labels=df['label'], 
        parents=['']*len(df),
        values=df['totalVolUsd'], 
        marker_colors=df['color'],
        textinfo="label"
    ))
    
    # Update layout
    fig.update_layout(title_text='12-Hour Mainstream Cryptocurrency Liquidation', title_x=0.5, width=1200, height=800)

    # Generate current time accurate to the hour
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H")

    # Generate a random string of length 8
    random_string = generate_random_string(8)

    # Include the current time and random string in the image name for differentiation
    image_filename = f"12h_liquidation_{current_time}_{random_string}.png"
    image_path_local = f"static/image/{image_filename}"

    # Add server address at the beginning of the image link
    server_address = "https://demo.chatdatainsight.com/api/"
    image_link = f"{server_address}{image_path_local}"

    # Save the chart to the specified file path and name
    if not os.path.exists('static/image'):
        os.makedirs('static/image')

    fig.write_image(image_path_local)

    # Only take the top 5 rows for the answer
    df_top_5 = df.head(5)
    for col in numerical_cols:
        df_top_5[col] = df_top_5[col].map('{:,.2f}'.format)

    ans_dict = {
        "question": question,
        "data": df_top_5.to_dict(orient='records'),
        "image": f"![12-Hour Mainstream Cryptocurrency Liquidation]({image_link})"
    }

    # Convert the dictionary to a JSON string
    ans_string = json.dumps(ans_dict)

    print("------ extracted data and image:",ans_string)

    result = ans_string
    return result


# get_liquidation_top("prompt:str")