from fastapi import APIRouter,Depends
from fastapi.responses import StreamingResponse

from services.insight import chatdata_insight_v2 as chatdata_insight
from services.helpers.chat_tools import stream_output as output
import json

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta

from core.config import Config

from api.v1.helpers.encrypt_decrypt import decrypt_text
from api.v1.helpers.encrypt_decrypt import encrypt_text

WEB_USER_TABLE = Config.WEB_USER_TABLE
WEB_USER_NAME = Config.WEB_USER_NAME

DATABASE_URL = Config.MYSQL_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

NO_PROMPT_RETURN = '''To assist you more effectively, 
I need to understand the specific details of your question.
Could you please tell me what exactly you would like to ask?'''


NO_ANSWER_RETURN = '''
I'm sorry, but I'm currently unable to answer your question. 
My expertise lies in the fields of blockchain and web3. 
Feel free to ask me any questions related to these domains.
'''

router = APIRouter()

@router.get(    
    "/api/v1/insight", 
    response_description="List prompt response",
    responses={404: {"description": "Not found"}}
)
def get_insight(prompt: str,db: Session = Depends(get_db)):
    # Check if the prompt is None or empty, and return a predefined response if it is
    if prompt is None or prompt == "":
        
        res = {"content": NO_PROMPT_RETURN}

    else:

        # Encrypt the prompt using the AES encryption algorithm
        encrypted_prompt = encrypt_text(prompt)
        # Get the current time
        now = datetime.now()
        # Convert the current time to a timestamp
        prompt_insert_time = now.strftime('%Y-%m-%d %H:%M:%S')

        # Retrieve the answer corresponding to the prompt
        answer = chatdata_insight(prompt)

        # Check if the answer is None or empty, and return a predefined response if it is
        if answer is None or answer == "":
            encrypted_answer = encrypt_text("")
            res = {"content": NO_ANSWER_RETURN}
        else:
            # Encrypt the answer using the AES encryption algorithm
            encrypted_answer = encrypt_text(answer)
            res = {"content": answer}
        try:
            # Get the current time
            now = datetime.now()
            # Convert the current time to a timestamp
            answer_insert_time = now.strftime('%Y-%m-%d %H:%M:%S')
            persist_web_query(encrypted_prompt,encrypted_answer,prompt_insert_time,answer_insert_time,db)
        except Exception as e:
            print(f"ERROR:     Error occurred during store web query: {e}")
            
    print("-----response", res)

    return StreamingResponse(output(json.dumps(res)), media_type='text/event-stream')
    # return res # The return value for testing

def persist_web_query(encrypted_prompt:str, encrypted_answer:str, prompt_insert_time, answer_insert_time,db):

    # Insert the encrypted prompt, answer, and timestamps into the database
    email = WEB_USER_NAME
    table_name = WEB_USER_TABLE
    table = Table(table_name, metadata, autoload_with=engine)
    record = table.insert().values(email=email, prompt=encrypted_prompt, answer=encrypted_answer,
                                    prompt_insert_time=prompt_insert_time, answer_insert_time=answer_insert_time)
    db.execute(record)
    db.commit()

    