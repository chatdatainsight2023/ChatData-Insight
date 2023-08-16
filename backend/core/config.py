from decouple import config

class Config:
         
    OPENAI_API_KEY = config("OPENAI_API_KEY", cast=str)
    PRIMARY_AGENT_OPENAI_API_KEY = config("PRIMARY_AGENT_OPENAI_API_KEY",cast=str)
    SECONDARY_AGNET_OPENAI_API_KEY = config("SECONDARY_AGNET_OPENAI_API_KEY",cast=str)
    

    MODEL_NAME = config("MODEL_NAME",cast=str)
    PROMPT_FILE = config("PROMPT_FILE", cast=str)
    COIN_SYMBOLS = config("COIN_SYMBOLS", cast=str)
    # PROMPT_FILE_KAHIN = config("PROMPT_FILE_KAHIN", cast=str)
    NEWS_API_KEY = config("NEWS_API_KEY", cast=str)
    QUICKNODE_ENDPOINT = config("QUICKNODE_ENDPOINT", cast=str)
    QUICKNODE_API_KEY = config("QUICKNODE_API_KEY", cast=str)

    JUDGEMENT_PROMPT = config("JUDGEMENT_PROMPT", cast=str)
    BINANCE_PROMPT = config("BINANCE_PROMPT", cast=str)
    NEWS_PROMPT = config("NEWS_PROMPT", cast=str)
    COIN_GLASS_API = config("COIN_GLASS_API", cast=str)
    
    # config verify database
    MYSQL_URL = config("MYSQL_URL",cast=str)
    # config JWT
    SECRET_KEY = config("SECRET_KEY", default="chatdata-insight-secret-key")
    ALGORITHM = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=60, cast=int)
    # aes key
    AES_KEY = config("AES_KEY", cast=str)
    
    DEFAULT_PASSWORD=config("DEFAULT_PASSWORD",cast=str)
    WEB_USER_TABLE=config("WEB_USER_TABLE",cast=str)
    WEB_USER_NAME = config("WEB_USER_NAME",cast=str)

    DUNE_API_KEY = config("DUNE_API_KEY",cast=str)
