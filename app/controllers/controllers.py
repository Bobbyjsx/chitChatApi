# controllers.py
from pydantic import ValidationError
from sqlalchemy.orm import Session, joinedload, contains_eager
from app.models.models import Message, User, ChatRoom, UserChatRoom
from app.schema.schemas import (
    MessageCreate,
    UpdateMessageResponse,
    UserCreate,
    ChatRoomCreate,
    UserResponse,
    ChatRoomCreate,
    ChatRoomResponse,
    AllChatRoomResponse,
)
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from fastapi import status


def create_user(db, user):
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="User with this email or userName already exists"
        ) from e


def read_user(db: Session, email: str):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")


def get_user(db: Session, user_email: str):
    query = db.query(User).filter(User.email == user_email).first()
    if query:
        return {
            "uuid": query.id,
            "email": query.email,
            "userName": query.username,
            "rooms": query.rooms,
            "sentMessages": query.sent_messages,
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


def read_user_by_id(db: Session, user_id: str):
    query = db.query(User).filter(User.id == user_id)
    if query:
        return {
            "uuid": query.id,
            "email": query.email,
            "userName": query.username,
            "rooms": query.rooms,
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


def create_chat_room(db: Session, room: ChatRoomCreate):
    # Create ChatRoom instance
    db_room = ChatRoom(name=room.name)
    db.add(db_room)
    db.commit()

    # Fetch users by their IDs
    users = db.query(User).filter(User.id.in_(room.members)).all()

    # Add fetched users to the chat room
    db_room.users.extend(users)

    db.commit()
    db.refresh(db_room)

    # Build the response with members as UserResponse objects
    members = [
        UserResponse(id=user.id, username=user.username, email=user.email)
        for user in db_room.users
    ]

    return ChatRoomResponse(id=db_room.id, name=db_room.name, members=members)


def add_user_to_room(db: Session, user_id: str, room_id: str):
    db_user_room = UserChatRoom(user_id=user_id, room_id=room_id)
    db.add(db_user_room)
    db.commit()
    db.refresh(db_user_room)
    return db_user_room


def get_chat_room_by_id(db: Session, chat_room_id: str):
    return db.query(ChatRoom).filter(ChatRoom.id == chat_room_id).first()


def get_chat_rooms(db: Session, user_id: str):
    user_chat_rooms = (
        db.query(UserChatRoom.room_id).filter(UserChatRoom.user_id == user_id).all()
    )

    chat_rooms_response = []
    for user_chat_room in user_chat_rooms:
        chat_room = (
            db.query(ChatRoom).filter(ChatRoom.id == user_chat_room.room_id).first()
        )
        if chat_room:
            members = (
                db.query(User)
                .join(UserChatRoom)
                .filter(UserChatRoom.room_id == chat_room.id)
                .all()
            )
            members_data = [
                {"id": member.id, "username": member.username, "email": member.email}
                for member in members
            ]
            chat_rooms_response.append(
                {
                    "id": chat_room.id,
                    "name": chat_room.name,
                    "members": members_data,
                }
            )

    print(chat_rooms_response)
    return chat_rooms_response


def get_user_rooms(db: Session, user_id: str):
    user_chat_rooms = (
        db.query(UserChatRoom.room_id).filter(UserChatRoom.user_id == user_id).all()
    )

    chat_rooms_response = []
    for user_chat_room in user_chat_rooms:
        chat_room = (
            db.query(ChatRoom).filter(ChatRoom.id == user_chat_room.room_id).first()
        )
        if chat_room:
            members = (
                db.query(User)
                .join(UserChatRoom)
                .filter(UserChatRoom.room_id == chat_room.id)
                .all()
            )
            members_data = [
                {"id": member.id, "username": member.username, "email": member.email}
                for member in members
            ]
            chat_rooms_response.append(
                {
                    "id": chat_room.id,
                    "name": chat_room.name,
                    "members": members_data,
                }
            )

    print(chat_rooms_response)
    return chat_rooms_response


def create_message(db: Session, message_data: MessageCreate, room_id: str):
    sender_id = message_data.sender_id

    # Check if the sender_id exists in the User table
    sender = db.query(User).filter(User.id == sender_id).first()

    if not sender:
        # Handle the case where the sender_id doesn't exist
        raise ValueError(f"User with ID {sender_id} does not exist.")

    # Create the Message instance
    db_message = Message(**message_data.dict(), room_id=room_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages_by_room(db: Session, room_id: str, skip: int = 0, limit: int = 10):
    messages = (
        db.query(
            Message.id,
            Message.sender_id,
            Message.content,
            Message.time,
            Message.room_id,
        )
        .filter(Message.room_id == room_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Convert the query results to a list of dictionaries
    messages_list = [
        {
            "id": message.id,
            "sender_id": message.sender_id,
            "content": message.content,
            "time": message.time,
            "room_id": message.room_id,
        }
        for message in messages
    ]

    return messages_list


def get_messages(db: Session, skip: int = 0, limit: int = 10):
    messages = (
        db.query(
            Message.id,
            Message.sender_id,
            Message.content,
            Message.time,
            Message.room_id,
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    sender_ids = [message.sender_id for message in messages]

    # Fetch usernames corresponding to sender_ids
    usernames = (
        db.query(User.id, User.username)
        .filter(User.id.in_(sender_ids))
        .all()
    )
    
    # Create a mapping of sender_id to username
    username_mapping = {user.id: user.username for user in usernames}

    # Convert the query results to a list of dictionaries with appended usernames
    messages_list = [
        {
            "id": message.id,
            "sender_id": message.sender_id,
            "username": username_mapping.get(message.sender_id), 
            "content": message.content,
            "time": message.time,
            "room_id": message.room_id,
        }
        for message in messages
    ]
    return messages_list


def delete_message(db: Session, message_id: str):
    try:
        message = db.query(Message).filter(Message.id == message_id).first()

        if message:
            db.delete(message)
            db.commit()
            return {
                "id": message.id,
                "sender_id": message.sender_id,
                "content": message.content,
                "time": message.time,
                "room_id": message.room_id,
                "status": "success",
            }
        else:
            # Raise a 404 Not Found HTTPException
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
            )

    except IntegrityError as e:
        # Handle SQLAlchemy IntegrityError (e.g., foreign key constraint violation)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    except ValidationError as e:
        # Handle Pydantic ValidationError (if any)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors()
        )


def update_message(db: Session, message_id: str, new_message: UpdateMessageResponse):
    try:
        message = db.query(Message).filter(Message.id == message_id).first()

        if message:
            # Update the content of the message
            message.content = new_message.content

            # Commit the changes to the database
            db.commit()

            # Return the updated message
            return {
                "id": message.id,
                "sender_id": message.sender_id,
                "content": message.content,
                "time": message.time,
                "room_id": message.room_id,
            }
        else:
            # Return an error message if the message doesn't exist
            return {"message": "Message not found"}

    except IntegrityError as e:
        # Handle SQLAlchemy IntegrityError (e.g., foreign key constraint violation)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    except ValidationError as e:
        # Handle Pydantic ValidationError (if any)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors()
        )
