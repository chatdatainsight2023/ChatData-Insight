
from services.third_platform.binance import get_token_price_trend

def cex_agent(question):

    result = get_token_price_trend(question)

    return result
