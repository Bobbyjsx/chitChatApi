from typing import List
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: str


class SignIn(BaseModel):
    email: str


class SignInResponse(BaseModel):
    id: str
    username: str
    email: str
    password: str


class ChatRoomCreate(BaseModel):
    name: str
    members: List[str]  # List of user IDs


class ChatRoomResponse(BaseModel):
    id: str
    name: str
    members: List[UserResponse]


class AllChatRoomResponse(BaseModel):
    id: str
    name: str
    members: List[UserResponse]


class UserChatRoomResponse(BaseModel):
    user_id: str
    room_id: str


class MessageCreate(BaseModel):
    content: str
    sender_id: str


class GetMessageResponse(BaseModel):
    id: str
    sender_id: str
    content: str
    time: str
    room_id: str
    username: str

class MessageResponse(BaseModel):
    id: str
    sender_id: str
    content: str
    time: str
    room_id: str


class DeleteMessageResponse(BaseModel):
    id: str
    sender_id: str
    content: str
    time: str
    room_id: str
    status: str


class UpdateMessage(BaseModel):
    content: str


class UpdateMessageResponse(BaseModel):
    id: str
    sender_id: str
    content: str
    time: str
    room_id: str
    username: str


class Config:
    from_attributes = True
