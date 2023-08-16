
from requests import get, post
import pandas as pd
import time
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

from plotly.subplots import make_subplots
import os
import matplotlib.dates as mdates
import json

from core.config import Config
from services.helpers.chat_tools import data_summary_v2 as data_summary
from langchain.llms import OpenAI


MODEL_NAME = Config.MODEL_NAME
LLM = OpenAI(model_name=MODEL_NAME, temperature=0)  

API_KEY = Config.DUNE_API_KEY

HEADER = {"x-dune-api-key" : API_KEY}

BASE_URL = "https://api.dune.com/api/v1/"

def make_api_url(module, action, ID):
    """
    We shall use this function to generate a URL to call the API.
    """

    url = BASE_URL + module + "/" + ID + "/" + action

    return url

def execute_query(query_id):
    """
    Takes in the query ID.
    Calls the API to execute the query.
    Returns the execution ID of the instance which is executing the query.
    """

    url = make_api_url("query", "execute", query_id)
    response = post(url, headers=HEADER)

    print("post response:",response)
    execution_id = response.json()['execution_id']
    # print("post response:",execution_id)

    return execution_id


def get_query_status(execution_id):
    """
    Takes in an execution ID.
    Fetches the status of query execution using the API
    Returns the status response object
    """

    url = make_api_url("execution", "status", execution_id)
    response = get(url, headers=HEADER)

    return response


def get_query_results(execution_id):
    """
    Takes in an execution ID.
    Fetches the results returned from the query using the API
    Returns the results response object
    """

    url = make_api_url("execution", "results", execution_id)
    response = get(url, headers=HEADER)

    return response


def cancel_query_execution(execution_id):
    """
    Takes in an execution ID.
    Cancels the ongoing execution of the query.
    Returns the response object.
    """

    url = make_api_url("execution", "cancel", execution_id)
    response = get(url, headers=HEADER)

    return response


# 查询去中心化交易所近7天以及近24小时交易量
query_id = "4319"

def get_data_from_dune(query_id):
    execution_id = execute_query(query_id)
    response = get_query_status(execution_id)

    result_metadata = response.json()
    # print("response:", result_metadata)

    while result_metadata['state'] != 'QUERY_STATE_COMPLETED':
        time.sleep(1)  # 等待1秒钟
        response = get_query_status(execution_id)
        result_metadata = response.json()

    query_results = get_query_results(execution_id)
    data = pd.DataFrame(query_results.json()['result']['rows'])

    print("\nfetched data:\n", data)

    return data


# get_dex_volume(query_id)

# query total stablecoin supply
query_id = "14028"

# 查询去中心化交易所近7天以及近24小时交易量

import datetime
import secrets

# Function to generate a random string of specified length
def generate_random_string(length):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random_string = ''.join(secrets.choice(alphabet) for _ in range(length))
    return random_string


import plotly.graph_objects as go

def dune_dex_exchange_volume(question):
    query_id = "4319"

    data = get_data_from_dune(query_id)

    data = data.head(20)

    # Sort to ensure the chart displays in the order of Rank
    data = data.sort_values('Rank')

    # Define the colors for the bars
    bar_colors = ['#87CEEB', '#08519C']  # Light blue and dark blue colors

    # Create the bar trace for 24-hour trading volume
    trace_24_hours = go.Bar(
        x=data['Project'],
        y=data['24 Hours Volume'] / 1e6,
        name='24 Hours Volume',
        marker=dict(color=bar_colors[0])
    )

    # Create the bar trace for 7-day trading volume
    trace_7_days = go.Bar(
        x=data['Project'],
        y=data['7 Days Volume'] / 1e6,
        name='7 Days Volume',
        marker=dict(color=bar_colors[1])
    )

    # Create the layout for the chart
    layout = go.Layout(
        title=dict(
            text='Exchange Volume of Different DEX<br><sub>Volume (in millions USD)</sub>',
            x=0.5,  # This line ensures the title is centered
            font=dict(size=24)  # Larger, more professional title font size
        ),
        xaxis=dict(
            title='',
            tickangle=-45,
            tickfont=dict(size=12),  # Increase x-axis label font size
        ),
        yaxis=dict(
            title='',
            tickfont=dict(size=12),  # Increase y-axis label font size
        ),
        plot_bgcolor='#F0F0F0',  # Light gray plot background
        paper_bgcolor='rgba(255,255,255,1)',  # White surrounding
        margin=dict(l=75, r=50, t=100, b=75),  # Increased left and bottom margins to accommodate larger labels
        height=600,
        width=900,
        legend=dict(
            x=1,
            y=1,
            bgcolor='rgba(255, 255, 255, 0)',  # Transparent legend background
            xanchor='auto',
            yanchor='auto',
            font=dict(size=14)  # Larger, more professional legend font size
        ),
    )

    # Combine the traces and layout into a Figure object
    fig = go.Figure(data=[trace_24_hours, trace_7_days], layout=layout)

    # Generate current time accurate to the hour
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H")

    # Generate a random string of length 8
    random_string = generate_random_string(8)

    # Include the current time and random string in the image name for differentiation
    image_filename = f"dex_exchange_volume_or_market_share_chart_{current_time}_{random_string}.png"
    image_path_local = f"static/image/{image_filename}"

    # Add server address at the beginning of the image link
    server_address = "https://demo.chatdatainsight.com/api/"
    image_link = f"{server_address}{image_path_local}"

    # Save the chart to the specified file path and name
    fig.write_image(image_path_local)

    ans_dict = {
        "question": question,
        "data": data.to_dict(orient='records'),
        "image": f"![Exchange Volume of Different DEX Chart]({image_link})"
    }

    # Convert the dictionary to a JSON string
    ans_string = json.dumps(ans_dict)

    print("------ extracted data and image:",ans_string)

    result = ans_string
    return result


# 查询去中心化交易所在不同链上的表现

def dune_weekly_dex_exchange_volume_by_chain(question):

    query_id = "2180075"

    data = get_data_from_dune(query_id)

    # Convert column '_col1' to datetime format
    data['_col1'] = pd.to_datetime(data['_col1'])

    # Sort the data by blockchain and date
    data = data.sort_values(['blockchain', '_col1'])

    # Group by blockchain and calculate the total volume
    total_volume_by_chain = data.groupby('blockchain')['usd_volume'].sum()

    # Select the top 20 chains with the highest total volume
    top_20_chains = total_volume_by_chain.nlargest(10).index

    # Only keep the data for the top 20 chains
    data_top_20 = data[data['blockchain'].isin(top_20_chains)]

    # Define the colors for the lines
    color_palette = px.colors.qualitative.Plotly

    fig = go.Figure()

    # Draw a line for each chain
    for i, chain in enumerate(top_20_chains):
        chain_data = data_top_20[data_top_20['blockchain'] == chain]
        fig.add_trace(go.Scatter(x=chain_data['_col1'], y=chain_data['usd_volume'] / 1e6, 
                                 mode='lines', name=chain,
                                 line=dict(shape='spline', color=color_palette[i % len(color_palette)])))

    fig.update_layout(
        title=dict(
            text='Weekly DEX Exchange Volume by Chain<br><sub>Volume (in millions USD)</sub>',
            x=0.5, 
            font=dict(size=24)
        ),
        xaxis=dict(
            title='',
            tickfont=dict(size=12),
        ),
        yaxis=dict(
            title='',
            tickfont=dict(size=12),
        ),
        plot_bgcolor='#F0F0F0',
        paper_bgcolor='rgba(255,255,255,1)',
        margin=dict(l=75, r=50, t=100, b=75),
        height=600,
        width=900,
        legend=dict(
            x=0.98,
            y=1,
            bgcolor='rgba(255, 255, 255, 0)',
            xanchor='auto',
            yanchor='auto',
            font=dict(size=14)
        ),
    )

    # Generate current time accurate to the hour
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H")

    # Generate a random string of length 8
    random_string = generate_random_string(8)

    # Include the current time and random string in the image name for differentiation
    image_filename = f"weekly_dex_exchange_volume_by_chain_chart_{current_time}_{random_string}.png"
    image_path_local = f"static/image/{image_filename}"

    # Add server address at the beginning of the image link
    server_address = "https://demo.chatdatainsight.com/api/"
    image_link = f"{server_address}{image_path_local}"

    # Save the chart to the specified file path and name
    fig.write_image(image_path_local)

    # Find the latest date in the data
    latest_date = data_top_20['_col1'].max()

    # Calculate the date four weeks ago
    four_weeks_ago = latest_date - pd.DateOffset(weeks=4)

    # Filter the data to only include the last four weeks
    data_last_4_weeks = data_top_20[data_top_20['_col1'] >= four_weeks_ago]
    # Create a copy of the last 4 weeks of data
    data_last_4_weeks_copy = data_last_4_weeks.copy()

    # Convert the '_col1' column to string format before converting the DataFrame to dictionary
    data_last_4_weeks_copy['_col1'] = data_last_4_weeks_copy['_col1'].dt.strftime('%Y-%m-%d %H:%M:%S')

    ans_dict = {
        "question": question,
        "data": data_last_4_weeks_copy.to_dict(orient='records'),
        "image": f"'![DEX Exchange Volume by Chain Chart]({image_link})'"
    }

    # Convert the dictionary to a JSON string
    ans_string = json.dumps(ans_dict)

    print("------ extracted data and image:",ans_string)

    result = ans_string
    return result


# dune_weekly_dex_exchange_volume_by_chain("question")


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
import json

def dune_daily_dex_exchange_volume(question):
    query_id = "4388"
    data = get_data_from_dune(query_id)
    data = data.rename(columns={"_col1": "Date", "project": "Dex Name", "usd_volume": "USD Volume (Millions)"})
    data['Date'] = pd.to_datetime(data['Date'])
    data['USD Volume (Millions)'] = data['USD Volume (Millions)'] / 1e6
    data_grouped = data.groupby(['Dex Name', 'Date']).sum().reset_index()
    top_10_projects = data_grouped.groupby('Dex Name')['USD Volume (Millions)'].sum().nlargest(10).index
    data_top_10 = data_grouped[data_grouped['Dex Name'].isin(top_10_projects)]
    color_palette = px.colors.qualitative.Plotly
    fig = go.Figure()
    
    # Draw a line chart for each project
    for i, project in enumerate(top_10_projects):
        project_data = data_top_10[data_top_10['Dex Name'] == project]
        fig.add_trace(go.Scatter(x=project_data['Date'], y=project_data['USD Volume (Millions)'], 
                                 mode='lines', name=project,
                                 line=dict(color=color_palette[i % len(color_palette)], 
                                           shape='spline', 
                                           smoothing=0.5)))

    fig.update_layout(
        title=dict(
            text='Daily DEX Exchange Volume<br><sub>USD Volume (Millions)</sub>',
            x=0.5,
            y=0.9,
            font=dict(size=20)
        ),
        xaxis_title='',
        yaxis_title='',
        plot_bgcolor='#F0F0F0',
        paper_bgcolor='rgba(255,255,255,1)',
        height=600,
        width=900,
        legend=dict(
            x=1,
            y=1,
            bgcolor='rgba(255, 255, 255, 0)',
            xanchor='auto',
            yanchor='auto',
            font=dict(size=14)
        ),
    )

    # Generate current time accurate to the hour
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H")

    # Generate a random string of length 8
    random_string = generate_random_string(8)

    # Include the current time and random string in the image name for differentiation
    image_filename = f"dex_daily_trading_volume_chart_{current_time}_{random_string}.png"
    image_path_local = f"static/image/{image_filename}"

    # Add server address at the beginning of the image link
    server_address = "https://demo.chatdatainsight.com/api/"
    image_link = f"{server_address}{image_path_local}"
    
    # Save the chart as a .png file
    fig.write_image(image_path_local)

    # Slice the data_top_10 to 1/3 length
    data_top_10_sliced = data_top_10[:len(data_top_10)//10]

    # Convert 'Date' to string
    data_top_10_sliced['Date'] = data_top_10_sliced['Date'].astype(str)

    # Convert DataFrame to dictionary
    data_dict = data_top_10_sliced.to_dict(orient='records')

    ans_dict = {
        "question": question,
        "data": data_dict,
        "image": f"'![Dex Daily Trading Volume Chart]({image_link})'"
    }

    # Convert the dictionary to a JSON string
    ans_string = json.dumps(ans_dict)

    print("------ extracted data and image:", ans_string)

    result = ans_string
    return result


# dune_daily_dex_exchange_volume("question")


# Ensure the use of the correct engine for image generation
pio.kaleido.scope.default_format = "png"

def stablecoin_supply_and_growth(question):

    query_id = "1652031"

    df = get_data_from_dune(query_id)
    
    # Convert the total_supply to billions and round it to two decimal places
    df['total_supply'] = df['total_supply'] / 1e9
    df['total_supply'] = df['total_supply'].round(2)

    # Exclude negative values
    df = df[df['total_supply'] > 0]

    # Sort df by total_supply and get the top 5
    top_4_df = df.sort_values('total_supply', ascending=False).head(4)

    # Remaining
    remaining_total_supply = df.loc[~df.index.isin(top_4_df.index), 'total_supply'].sum()
    remaining_df = pd.DataFrame([['Others', remaining_total_supply]], columns=['name', 'total_supply'])
    
    # Concatenate the top 5 df with the remaining df
    final_df = pd.concat([top_4_df, remaining_df])

    # Calculate the percentage
    final_df['percentage'] = final_df['total_supply'] / final_df['total_supply'].sum() * 100

    # Create a pie chart for the 'percentage' column
    fig = go.Figure(data=[go.Pie(labels=final_df['name'], 
                                 values=final_df['total_supply'], 
                                 hole=.6,  # Increase hole size
                                 pull=[0, 0, 0.1, 0],
                                 insidetextorientation='radial')])  # Make text inside the pie chart appear radially

    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20)
    fig.update_layout(
        title={
            'text': "Market Share of Different Stablecoins (Top 4 and Others)<br><sub>In Billions of Dollars</sub>",  # Add subtitle to the title
            'y':0.91,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        height=600,
        width=900,
        legend=dict(
            x=0.8,
            y=0.9,
            bgcolor='rgba(255, 255, 255, 0)',
            font=dict(size=14)
        ),
        margin=dict(l=20, r=20, t=70, b=60)
    )
    
    # Generate current time accurate to the hour
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H")

    # Generate a random string of length 8
    random_string = generate_random_string(8)

    # Include the current time and random string in the image name for differentiation
    image_filename = f"stablecoin_market_share_chart_{current_time}_{random_string}.png"
    image_path_local = f"static/image/{image_filename}"

    # Save the image to the local file system
    fig.write_image(image_path_local)

    # Add server address at the beginning of the image link
    server_address = "https://demo.chatdatainsight.com/api/"
    image_link = f"{server_address}{image_path_local}"

    ans_dict = {
        "question": question,
        "data": final_df.to_dict(orient='records'),
        "image": f"'![Market Share of Different Stablecoins Chart]({image_link})'"
    }

    # Convert the dictionary to a JSON string
    ans_string = json.dumps(ans_dict)

    print("------ extracted data and image:",ans_string)

    result = ans_string

    return result

# stablecoin_supply_and_growth("question")
# dune_dex_exchange_volume("question")