# routers.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers.controllers import (
    create_message,
    get_messages,
    get_messages_by_room,
    delete_message,
    get_user,
    read_user_by_id,
    update_message,
    create_chat_room,
    add_user_to_room,
    create_user,
    get_chat_rooms,
    read_user,
)
from app.schema.schemas import (
    MessageCreate,
    MessageResponse,
    UpdateMessage,
    UpdateMessageResponse,
    UserResponse,
    ChatRoomCreate,
    UserCreate,
    ChatRoomResponse,
    UserChatRoomResponse,
    AllChatRoomResponse,
    SignInResponse,
    SignIn,
)
from app.database import get_db
from app.schema.schemas import DeleteMessageResponse

router = APIRouter()


@router.post("/auth/sign-up", response_model=UserResponse)
def create_users(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/auth/sign-in/{email}", response_model=SignInResponse)
def read_users(email: str, db: Session = Depends(get_db)):
    return read_user(db, email)


@router.get("/user/{email}")
def get_current_user(email: str, db: Session = Depends(get_db)):
    return get_user(db, email)


@router.get("/user/{id}")
def read_user_by_id(id: str , db: Session = Depends(get_db)):
    return read_user_by_id(db, id)


@router.post("/chat-room", response_model=ChatRoomResponse)
def create_chat_rooms(room: ChatRoomCreate, db: Session = Depends(get_db)):
    return create_chat_room(db, room)


@router.post("/users/{user_id}/rooms/{room_id}", response_model=UserChatRoomResponse)
def add_user_to_rooms(user_id: str, room_id: str, db: Session = Depends(get_db)):
    return add_user_to_room(db, user_id, room_id)


@router.post("/messages/{room_id}", response_model=MessageResponse)
def create_messages(
    message: MessageCreate, room_id: str, db: Session = Depends(get_db)
):
    return create_message(db, message, room_id)


@router.get("/user/rooms/{user_id}", response_model=List[AllChatRoomResponse])
def get_chat_room(user_id: str, db: Session = Depends(get_db)):
    return get_chat_rooms(db, user_id)


@router.get("/messages/{room_id}", response_model=List[MessageResponse])
def read_messages(
    room_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return get_messages_by_room(db, room_id, skip=skip, limit=limit)


@router.get("/messages/", response_model=list[MessageResponse])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_messages(db, skip=skip, limit=limit)


@router.delete("/messages/{message_id}", response_model=DeleteMessageResponse)
def delete_messages(message_id: str, db: Session = Depends(get_db)):
    return delete_message(db, message_id)


@router.put("/messages/{message_id}", response_model=UpdateMessageResponse)
def edit_message(
    message_id: str, new_message: UpdateMessage, db: Session = Depends(get_db)
):
    return update_message(db, message_id, new_message)
