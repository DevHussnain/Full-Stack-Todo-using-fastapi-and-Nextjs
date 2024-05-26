from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import SQLModel, create_engine, Field, Session, select
from pydantic import BaseModel
from typing import Annotated, Optional
from fastapi_neon import settings
from fastapi_neon import auth
from fastapi_neon.auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware

class TODOS(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  content: str | None = Field(index=True)
  is_complete: bool = Field(default=False)
  userid: Optional[int] = Field(default=None, foreign_key="users.id")


class USER_DATA(BaseModel):
  content: str
  is_complete: bool = False

class UPDATE_USER_DATA(BaseModel):
  content: Optional[str] = None
  is_complete: bool = False

db_url = str(settings.DATABASE_URL).replace(
   "postgresql" , "postgresql+psycopg"
)

engine = create_engine(db_url, connect_args={"sslmode": "require"},  pool_recycle=300)

def get_highest_id(session):
        result = session.query(TODOS).order_by(TODOS.id.desc()).first()
        return result.id if result else 0  # Return 0 if no todos exist

def create_table():
  SQLModel.metadata.create_all(engine)  # Call this to create the table

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_table()
    yield

app = FastAPI(lifespan=lifespan,title="Todo List API", 
    version="0.0.1",
    servers=[
        {
            "url": "http://localhost:8000/", # This is localhost URL
            "description": "Development Server"
        },
        {
            "url": "https://related-strangely-stork.ngrok-free.app", # This is NGROK URL
            "description": "Production Server"
        },
        ])

app.include_router(auth.router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_session():
    with Session(engine) as session:
        yield session
  
@app.get('/')
async def read_home():
   return {"Message": "Welcome To Our Website"}

@app.get('/todos')
async def get_todos(session: Annotated[Session, Depends(get_session)],user: Annotated[dict, Depends(get_current_user)]):
     todos = session.exec(select(TODOS).where(TODOS.userid == user["user_id"])).all()  # Fetch all TODOS objects
     if not user:
          return {'Meassage': "Please Login First"}
     return todos
    
@app.get('/todos/{todo_id}')
async def get_todos_by_id(user: Annotated[dict, Depends(get_current_user)], todo_id: int , session: Annotated[Session, Depends(get_session)]):
   todos = session.get(TODOS, todo_id)
   if not user:
          return {'Meassage': "Please Login First"}
   if todos and todos.userid == user["user_id"]:
      return todos
   else:
      raise HTTPException(status_code=404, detail="Todo not found")
    
@app.post('/todos')
async def add_todos(user: Annotated[dict, Depends(get_current_user)], user_data: USER_DATA, session: Annotated[Session, Depends(get_session)]):
    if not user:
          return {'Meassage': "Please Login First"}
    if user and user_data.content.strip():
          highest_id = get_highest_id(session)
          new_todo = TODOS(content=user_data.content, is_complete=user_data.is_complete , id=highest_id + 1, userid=user["user_id"])
          session.add(new_todo)
          session.commit()
          session.refresh(new_todo)
          return {
                    "id": new_todo.id,
                    "content": new_todo.content,
                    "is_complete": new_todo.is_complete 
                  }
    else:
        raise HTTPException(status_code=400, detail="Please Fill The Todo Field")


@app.put('/todos/{todo_id}')
async def update_todo(user: Annotated[dict, Depends(get_current_user)], todo_id: int, user_data: UPDATE_USER_DATA, session: Annotated[Session, Depends(get_session)]):
    todo = session.get(TODOS, todo_id)
    if not user:
          return {'Meassage': "Please Login First"}
    if user and todo and todo.userid == user["user_id"]:
        if user_data.content != todo.content and user_data.content != None:  # Update content if different
            todo.content = user_data.content
            session.add(todo)
        if user_data.is_complete != todo.is_complete:  # Update is_complete if different
            todo.is_complete = user_data.is_complete
            session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.delete('/todos/{todo_id}')
async def delete_todo(user: Annotated[dict, Depends(get_current_user)], todo_id: int, session: Annotated[Session, Depends(get_session)]):
    todo = session.get(TODOS, todo_id)
    if not user:
          return {'Meassage': "Please Login First"}
    if user and todo and todo.userid == user["user_id"]:
        session.delete(todo)
        session.commit()
        return {"Message": "Todo deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
