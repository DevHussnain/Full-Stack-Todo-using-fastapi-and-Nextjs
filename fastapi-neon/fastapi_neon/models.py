from typing import Optional
from sqlmodel import Field, SQLModel
    
class USERS(SQLModel, table=True):
  id : Optional[int] = Field(default=None, primary_key=True)
  username: str = Field(unique=True)
  hashed_password: str