from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from services.insight import chatdata_insight_v2 as chatdata_insight
from services.helpers.chat_tools import stream_output as output

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import create_engine, Table, MetaData, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import select
from sqlalchemy import TIMESTAMP
from sqlalchemy import Column, Integer, String, LargeBinary, Float, TIMESTAMP, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import update
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

import base64
import json
import uvicorn
import logging

from api.v1.helpers.encrypt_decrypt import decrypt_text
from api.v1.helpers.encrypt_decrypt import encrypt_text


from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str
    wallet_address: str = None
    username: str = None

from core.config import Config

DEFAULT_PASSWORD = Config.DEFAULT_PASSWORD

SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES

DATABASE_URL = Config.MYSQL_URL
engine = create_engine(DATABASE_URL)
metadata = MetaData()
# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 配置密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

Base = declarative_base()

class ChatRecord(Base):
    __tablename__ = 'chat_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    prompt = Column(LargeBinary, nullable=False)
    answer = Column(LargeBinary, nullable=True)
    ratings = Column(Integer, default=0)
    prompt_insert_time = Column(TIMESTAMP, default=datetime.utcnow())  # Changed to TIMESTAMP type
    answer_insert_time = Column(TIMESTAMP, default=datetime.utcnow())  # Changed to TIMESTAMP type

def create_chat_record_table(email: str):
    # Replacing '@' and '.' in the email with '_'
    table_name = f"{email.replace('@', '_').replace('.', '_')}_chat_records"

    # Creating a new MetaData instance to create the table
    metadata = MetaData()

    # Creating the ChatRecord table in the database, the fields include username+'_chat_records'
    table = Table(
        table_name, metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('email', String(255), nullable=False),
        Column('prompt', LargeBinary, nullable=False),
        Column('answer', LargeBinary, nullable=True),
        Column('ratings', Integer, default=0),
        Column('prompt_insert_time', TIMESTAMP, default=datetime.utcnow()), # Changed to TIMESTAMP type
        Column('answer_insert_time', TIMESTAMP, default=datetime.utcnow())  # Changed to TIMESTAMP type
    )

    # Checking if the table already exists
    inspector = Inspector.from_engine(engine)
    if not inspector.has_table(table_name):
        # If the table does not exist, create the table
        table.create(engine)
    else:
        print(f"The table {table_name} already exists.")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


router = APIRouter()

from cryptography.hazmat.primitives.asymmetric import rsa

# 生成私钥
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# 获取相应的公钥
public_key = private_key.public_key()


@router.get("/api/public_key")
def get_public_key():
    # serilize pubkey to pem
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return {"public_key": pem.decode()}


class LoginRequest(BaseModel):
    email: str
    password: str
    wallet_address: str = None
    username: str = None

@router.post("/api/v1/login", 
    response_description="List login response", responses={404: {"description": "Not found"}})
def login(request: LoginRequest, db: Session = Depends(get_db), ):

    email = request.email
    password = request.password
    wallet_address = request.wallet_address
    username = request.username

    # Base64 decode the encrypted email and password
    encrypted_email_bytes = base64.b64decode(email)
    encrypted_password_bytes = base64.b64decode(password)

    # Decrypt using the private key
    decrypted_email = private_key.decrypt(encrypted_email_bytes, padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None)).decode()
    decrypted_password = private_key.decrypt(encrypted_password_bytes, padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None)).decode()

    # Create user table
    users = Table('user', metadata, autoload_with=engine)

    try:
        # Verify user

        result = db.execute(select(users.c.password).where(users.c.email == decrypted_email))
        user = result.fetchone()

        # If the user does not exist, register a new user
        if not user:
            hashed_password = pwd_context.hash(decrypted_password)
            # Get the current time
            now = datetime.now()
            # Convert the current time to a timestamp
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
            ins = users.insert().values(email=decrypted_email, wallet_name=wallet_address, username=username, password=hashed_password, balance=0, limitation=20, balance_update_time=timestamp, limitation_update_time=timestamp)

            # Insert the new user record
            db.execute(ins)
            db.commit()

            # Create a user record table
            create_chat_record_table(decrypted_email)

        # Validate password
        elif not pwd_context.verify(decrypted_password, user.password):
            
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        # Create access token
        access_token = create_access_token(data={"sub": decrypted_email})

        # Return access token and key
        return {"token_type": "bearer", "access_token": access_token}

    except HTTPException as e:
        # If the raised exception is an HTTPException, re-raise it without modifying the status code or details
        raise
    except Exception as e:
        # If any other exception is raised, log the error information and return a 500 Internal Server Error
        logging.error("Failed to login user: %s", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to login user")

class UpdateRequest(BaseModel):
    wallet_address: str = None
    username: str = None
    password: str=None

@router.post("/api/v1/update_info",
    response_description="List login response",
    responses={404: {"description": "Not found"}})
def update_info(request: UpdateRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    wallet_address = request.wallet_address
    username = request.username
    password = request.password

    # verify token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # update data
    table_name = "user"
    table = Table(table_name, metadata, autoload_with=engine)
    stmt = table.update().where(table.c.email == email)

    if wallet_address is not None:
        stmt = stmt.values(wallet_name=wallet_address)
    if username is not None:
        stmt = stmt.values(username=username)
    if password is not None:
        hashed_password = pwd_context.hash(password)
        stmt = stmt.values(password=hashed_password)

    db.execute(stmt)
    db.commit()

    # return user and update result
    return {"username": email,"update_result": "success"}


def persist_mobile_query(email:str, encrypted_prompt:str, encrypted_answer:str, prompt_insert_time, answer_insert_time, db):
    # Insert the encrypted prompt, answer, and timestamps into the database
    table_name = f"{email.replace('@', '_').replace('.', '_')}_chat_records"
    table = Table(table_name, metadata, autoload_with=engine)
    record = table.insert().values(email=email, prompt=encrypted_prompt, answer=encrypted_answer,
                                prompt_insert_time=prompt_insert_time, answer_insert_time=answer_insert_time)
    db.execute(record)
    db.commit()

NO_PROMPT_RETURN = '''To assist you more effectively, 
I need to understand the specific details of your question.
Could you please tell me what exactly you would like to ask?'''


NO_ANSWER_RETURN = '''
I'm sorry, but I'm currently unable to answer your question. 
My expertise lies in the fields of blockchain and web3. 
Feel free to ask me any questions related to these domains.
'''

@router.get("/api/v1/mobile_insight",
    response_description="List prompt response",
    responses={404: {"description": "Not found"}})
def get_insight(prompt: str, token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # check membership
    table_name = "user"
    table = Table(table_name, metadata, autoload_with=engine)

    # select membership_level and limitation_update_time
    stmt = select(table.c.membership_level, table.c.limitation_update_time, table.c.limitation).where(table.c.email == email)

    result = db.execute(stmt).first()

    if result:
        membership_level, limitation_update_time, limitation = result

        if membership_level == 'basic':
            current_time = datetime.now()
            midnight_today = datetime(current_time.year, current_time.month, current_time.day)

            # 如果limitation_update_time是空的，或者在今天的00点之前
            if limitation_update_time is None or limitation_update_time < midnight_today:
                update_stmt = update(table).where(table.c.email == email).values(
                    limitation=19,
                    limitation_update_time=current_time
                )
                db.execute(update_stmt)
            else:
                # 如果还在当天，则limitation减1
                if limitation > 0:
                    update_stmt = update(table).where(table.c.email == email).values(limitation=limitation-1)
                    db.execute(update_stmt)
                else:
                    raise HTTPException(status_code=402, detail="Reached the daily usage limit")
            
            db.commit()  # 提交事务
    else:
        raise HTTPException(status_code=404, detail="User not found")


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
            persist_mobile_query(email, encrypted_prompt,encrypted_answer,prompt_insert_time,answer_insert_time,db)
        
        except Exception as e:
            print(f"ERROR:     Error occurred during store mobile query: {e}")
    
    print("-----response", res)

    return StreamingResponse(output(json.dumps(res)), media_type='text/event-stream')
    # return res # The return value for testing


@router.get("/api/v1/record",
    response_description="List record response",
    responses={404: {"description": "Not found"}})
def get_record(username: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        current_user = payload.get("sub")
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 组合提供的用户名与 'chat_records' 来获取数据表名
    table_name = f"{username.replace('@', '_').replace('.', '_')}_chat_records"

    print("table name:",table_name)

    # 获取数据库中的表对象，并使用别名
    chat_records_table = Table(table_name, metadata, autoload_with=engine)

    # 别名对象
    record = chat_records_table.alias("record")

    # 构建查询语句
    query = select(
        record.c.id,
        record.c.email,
        record.c.prompt,
        record.c.answer,
        record.c.ratings,
        record.c.prompt_insert_time,
        record.c.answer_insert_time
    )

    # 执行查询语句并获取结果
    result = db.execute(query)

    # 解密 prompt 和 answer 字段，并将记录存储在列表中
    decrypted_records = []
    for record in result:
        decrypted_prompt = decrypt_text(record.prompt)
        decrypted_answer = decrypt_text(record.answer)
        decrypted_record = {
            "record_id": record.id,
            "prompt": decrypted_prompt,
            "answer": decrypted_answer,
            "ratings": record.ratings,
            "prompt_insert_time": record.prompt_insert_time,
            "answer_insert_time": record.answer_insert_time
        }
        decrypted_records.append(decrypted_record)

    return decrypted_records