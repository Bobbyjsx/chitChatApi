from typing import List
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class SignIn(BaseModel):
    email: str


class SignInResponse(BaseModel):
    id: int
    username: str
    email: str
    password: str


class ChatRoomCreate(BaseModel):
    name: str
    members: List[int]  # List of user IDs


class ChatRoomResponse(BaseModel):
    id: str
    name: str
    members: List[UserResponse]


class AllChatRoomResponse(BaseModel):
    id: str
    name: str
    members: List[UserResponse]


class UserChatRoomResponse(BaseModel):
    user_id: int
    room_id: str


class MessageCreate(BaseModel):
    content: str
    sender_id: int


class MessageResponse(BaseModel):
    id: str
    sender_id: int
    content: str
    time: str
    room_id: str


class DeleteMessageResponse(BaseModel):
    id: str
    sender_id: int
    content: str
    time: str
    room_id: str
    status: str


class UpdateMessage(BaseModel):
    content: str


class UpdateMessageResponse(BaseModel):
    id: str
    sender_id: int
    content: str
    time: str
    room_id: str


class Config:
    from_attributes = True
