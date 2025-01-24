import os
import logging
from uuid import UUID, uuid4

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

MONGODB_CONNECTION_STRING = os.environ["MONGODB_CONNECTION_STRING"]

client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING, uuidRepresentation="standard")
db = client.todolist
todos = db.todos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for logging requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

class TodoItem(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    content: str

class TodoItemCreate(BaseModel):
    content: str

@app.post("/todos", response_model=TodoItem)
async def create_todo(item: TodoItemCreate):
    logger.info(f"Creating todo: {item.content}")
    new_todo = TodoItem(content=item.content)
    await todos.insert_one(new_todo.model_dump(by_alias=True))
    logger.info(f"Todo created with ID: {new_todo.id}")
    return new_todo

@app.get("/todos", response_model=list[TodoItem])
async def read_todos():
    return await todos.find().to_list(length=None)

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: UUID):
    logger.info(f"Attempting to delete todo with ID: {todo_id}")
    delete_result = await todos.delete_one({"_id": todo_id})
    if delete_result.deleted_count == 0:
        logger.error(f"Todo with ID {todo_id} not found")
        raise HTTPException(status_code=404, detail="Todo not found")
    logger.info(f"Todo with ID {todo_id} deleted successfully")
    return {"message": "Todo deleted successfully"}

if __name__ == "__main__":
    logger.info("Starting FastAPI application...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    logger.info("FastAPI application has stopped.")
