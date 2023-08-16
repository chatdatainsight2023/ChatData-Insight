

# ChatdataInsight APP

Application built with FastAPI, React, and MongoDB. 

You need a mongodb account. 

## Setup MongoDB connection

``` 
    -> Create a .env file and add the following lines: 

    DB_URL = "mongodb+srv://<name>:<password>@..."
    DB_NAME = "PolarDashApp"
    COLLECTION_NAME = "polardash"

```

## Setup backend

In the backend folder
```
    -> Create a new env. with python3 -m venv polardash-backend-env
    -> Activate the virtual env. with source polardash-backend-env/bin/activate 
    -> Install dependencies with <b>pip install -r requirements.txt</b>
    -> Activate the backend with python main.py

```

## Setup frontend

In the frontend folder 
```
    -> Create a new env. with python3 -m venv polardash-frontend-env
    -> Activate the virtual env. with source polardash-frontend-env/bin/activate
    -> Install react app with npm install 
    -> npm install react-router-dom

    -> Run the app with npm start
```

# API Examples

Below is a detailed description of the APIs

## 1 Web App API

### GET /api/v1/insight

This endpoint is used to fetch insights.

**Parameters:**

- prompt: String. The prompt provided by the user.

**Request Example:**

```
https://demo.chatdatainsight.com/api/v1/insight?prompt="who are you?"
```

**Response **

StreamingOutput

## 2 Mobile App API

### POST /api/v1/login

This endpoint is used to log in.

**Parameters:**

- username: String. The username of the user.
- password: String. The password of the user.

**Request Example:**

```
https://demo.chatdatainsight.com/api/v1/login?username=xxxn@outlook.com&password=xxx
```

**Response Example:**

```
{
    "token_type": "bearer",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqaWFucXVhbnFpbkBvdXRsb29rLmNvbSIsImV4cCI6MTY5MTA0MTMwMn0.uemSIGo9zrtptE9Ps_Zgfg009Cq1MZTLNfJICqe18QY"
}
```

### GET /api/v1/mobile_insight

This endpoint is used to fetch insights.

**Parameters:**

- prompt: String. The prompt provided by the user.

**Headers:**

- key: Authorization
- value: Bearer access_token

**Request Example:**

```
https://demo.chatdatainsight.com/api/v1/mobile_insight?prompt=who are you?
```

**Response **

StreamingOutput

### GET /api/v1/record

This endpoint is used to fetch the chat records of a user.

**Parameters:**

- username: String. The username of the user.

**Headers:**

- key: Authorization
- value: Bearer access_token

**Request Example:**

```
https://demo.chatdatainsight.com/api/v1/record?username=xxx@outlook.com
```

**Response Example:**

```
[
    {
        "record_id": 1,
        "prompt": "who are you?",
        "answer": "",
        "ratings": null,
        "prompt_insert_time": 1691050000.0,
        "answer_insert_time": 1691050000.0
    }
]
```

# Test questions

## 1 Query on-chain information

```
1.1 Can you help me examine the details of this contract: 0xf2A22B900dde3ba18Ec2AeF67D4c8C1a0DAB6aAC?
```

## 2 Query cex data

```
What's the recent price trend of BTC over the last few hours?
```

## 3 Query dex

```
3.1 Could you please check the market share of decentralized exchanges?
3.2 Can you help me check the trading volumes of exchanges on various blockchains?
3.3 What is the daily trading volume of dex?
```
## 4 Query Stablecoin info

```
4.1 Can you help me check the market share of stablecoin?
```

## 5 Query certain project info

```
5.1 Which stablecoins are available on Moonbeam?
```

