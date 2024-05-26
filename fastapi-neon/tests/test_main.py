from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from fastapi_neon.main import app, get_session, TODOS, get_current_user
from fastapi_neon import settings

def test_home():
    client= TestClient(app=app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome To Our Website"}

def test_read_list_main():
    connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=3000)

    SQLModel.metadata.create_all(engine)  

    with Session(engine) as session:  
        def get_session_override():  
                return session  
        
        app.dependency_overrides[get_session] = get_session_override

        # Create a mock user for testing
        mock_user = {"username": "test_user", "user_id": 1}

        def get_current_user_override():
            return mock_user

        app.dependency_overrides[get_current_user] = get_current_user_override

        client = TestClient(app=app)
        response = client.get("/todos/")
        assert response.status_code == 200

def test_post_todo():
     connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")

     engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=3000)

     SQLModel.metadata.create_all(engine)

     with Session(engine) as session:  
       def get_session_override():  
               return session  
       app.dependency_overrides[get_session] = get_session_override 
       client = TestClient(app=app)
       todo_content = "buy bread"
       response = client.post("/todos",
           json={"content": todo_content}
       )
       data = response.json()
       print(data)
       assert response.status_code == 200
       assert data["content"] == todo_content

def test_update_todo_is_complete():
     connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")

     engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=3000)

     SQLModel.metadata.create_all(engine)

     with Session(engine) as session:  
       def get_session_override():  
               return session  
       app.dependency_overrides[get_session] = get_session_override 
       # Create a mock user for testing
       mock_user = {"username": "test_user", "user_id": 1}

       def get_current_user_override():
           return mock_user

       app.dependency_overrides[get_current_user] = get_current_user_override

       client = TestClient(app=app)

       todo_content = "Make Task True"
       create_response = client.post("/todos/", json={"content": todo_content, "is_complete": False})
       assert create_response.status_code == 200
       todo_id = create_response.json()["id"]

       update_todo = client.put(f"/todos/{todo_id}", json={'is_complete': True})
       response = update_todo.json()
       assert update_todo.status_code == 200
       assert response["is_complete"] == True

def test_update_todo_is_content():
     connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")

     engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=3000)

     SQLModel.metadata.create_all(engine)

     with Session(engine) as session:  
       def get_session_override():  
               return session  
       app.dependency_overrides[get_session] = get_session_override 
       # Create a mock user for testing
       mock_user = {"username": "test_user", "user_id": 1}

       def get_current_user_override():
            return mock_user

       app.dependency_overrides[get_current_user] = get_current_user_override


       client = TestClient(app=app)

       todo_content = "Change Me"
       create_response = client.post("/todos/", json={"content": todo_content, "is_complete": False})
       assert create_response.status_code == 200
       todo_id = create_response.json()["id"]
       

       update_todo = client.put(f"/todos/{todo_id}", json={'content': "Coding"})
       response = update_todo.json()
       assert update_todo.status_code == 200
       assert response["content"] == "Coding"

def test_delete_todo():
     connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")

     engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=3000)

     SQLModel.metadata.create_all(engine)

     with Session(engine) as session:
       def get_session_override():  
               return session  
       app.dependency_overrides[get_session] = get_session_override 
       # Create a mock user for testing
       mock_user = {"username": "test_user", "user_id": 1}

       def get_current_user_override():
            return mock_user

       app.dependency_overrides[get_current_user] = get_current_user_override
       client = TestClient(app=app)

       todo_content = "Delete Me"
       create_response = client.post("/todos/", json={"content": todo_content, "is_complete": False})
       assert create_response.status_code == 200
       todo_id = create_response.json()["id"]

       delete_todo = client.delete(f"/todos/{todo_id}")
       response = delete_todo.json()

       assert delete_todo.status_code == 200
       assert response["Message"] == "Todo deleted successfully"

def check_database_connection():
     connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")

     engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=3000)

     SQLModel.metadata.create_all(engine)

     with Session(engine) as session:
       todo_content = {"content": "Check Database", "is_complete": False}
       session.add(todo_content)
       session.commit()
       
       result = session.exec(select(TODOS).where(TODOS.content == "Check Database")).first()

       assert result.content == todo_content["content"]
       assert result.is_complete == todo_content["is_complete"]

     SQLModel.metadata.drop_all(engine)