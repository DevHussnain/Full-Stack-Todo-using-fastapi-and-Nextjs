from contextlib import asynccontextmanager
from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel, Field, select
from starlette import status
from fastapi_neon import settings
from passlib.context import CryptContext
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi_neon.models import USERS

db_url = str(settings.DATABASE_URL).replace(
   "postgresql" , "postgresql+psycopg"
)

engine = create_engine(db_url, connect_args={"sslmode": "require"},  pool_recycle=300)

def create_table():
  SQLModel.metadata.create_all(engine)  # Call this to create the table

@asynccontextmanager
async def call_table():
    create_table()

router = APIRouter(
    prefix='/auth',
    tags=["auth"],
)

SECRET_KEY = "ceafd143bd34e1d484ee933c57fe75c6aac371c5938509252c38c499fb252851"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_barrer = OAuth2PasswordBearer(tokenUrl='auth/token')
                                     

class CreateUserRequest(BaseModel):
    username: str
    password: str

class SinginRequst(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_highest_id(session):
        result = session.query(USERS).order_by(USERS.id.desc()).first()
        return result.id if result else 0  # Return 0 if no todos exist

def get_session():
    with Session(engine) as session:
        yield session

db_dependency = Annotated[Session, Depends(get_session)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(session: db_dependency, create_user_request: CreateUserRequest):
    get_id=get_highest_id(session)
    create_user_model = USERS(
        id=get_id+1,
        username = create_user_request.username,
        hashed_password = bcrypt_context.hash(create_user_request.password)
    )

    session.add(create_user_model)

    session.commit()

    return {"name":create_user_model.username, "password":create_user_model.hashed_password}

@router.post('/token', response_model=Token)
async def login_to_acess_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could Not vailde User')
    
    token = create_acess_token(user.username, user.id , timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

@router.delete("/")
async def delete_user(session: db_dependency, user_id: int):
    user =  session.get(USERS, user_id)
    if user:
        session.delete(user)
        session.commit()
        return {"Message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

def authenticate_user(username:str, password:str, db):
    user = db.query(USERS).filter(USERS.username == username).first()

    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user

def create_acess_token(username:str, user_id: int , expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}

    expires = datetime.utcnow() + expires_delta

    encode.update({'exp': expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_barrer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')

        user_id = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'Could Not Validate User!'})
        
        return {'username': username, 'user_id': user_id}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'Could Not Validate User!'})