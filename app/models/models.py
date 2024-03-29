import datetime
import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Define a relationship with the ChatRoom model
    rooms = relationship("ChatRoom", secondary="user_chat_room", overlaps="rooms")

    # Define a relationship with the Message model
    sent_messages = relationship(
        "Message", back_populates="sender", foreign_keys="[Message.sender_id]"
    )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


    def __repr__(self):
        return f"id={self.id}, user_name={self.username}, email={self.email}"


class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)

    # Define a relationship with the User model
    users = relationship("User", secondary="user_chat_room", overlaps="rooms")

    # Define a relationship with the Message model
    messages = relationship("Message", back_populates="room")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"id={self.id}, name={self.name}, users={self.users}"


class UserChatRoom(Base):
    __tablename__ = "user_chat_room"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    room_id = Column(String, ForeignKey("chat_rooms.id"), primary_key=True)


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    sender_id = Column(String, ForeignKey("users.id"), index=True)
    content = Column(String)
    username = Column(String, ForeignKey("users.username"), index=True)
    time = Column(String)
    room_id = Column(
        String, ForeignKey("chat_rooms.id"), default=lambda: str(uuid.uuid4())
    )

    # Define a relationship with the ChatRoom model
    room = relationship("ChatRoom", back_populates="messages")

    # Define a relationship with the User model
    sender = relationship(
        "User", back_populates="sent_messages", foreign_keys="[Message.sender_id]"
    )

    def __init__(
        self, sender_id, content, username, time=None, custom_uuid=None, room_id=None
    ):
        self.sender_id = sender_id
        self.username = username
        self.content = content
        self.time = time or datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self.uuid = custom_uuid or str(uuid.uuid4())
        self.room_id = room_id or str(uuid.uuid4())
