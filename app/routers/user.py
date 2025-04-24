from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import Field
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Bundle, load_only

from app.models.depends.uuid_depends import get_uuid_or_str
from app.models.user import User
from app.routers.auth import bcrypt_context, oauth2_scheme, get_current_user
from app.routers.config import root_api
from app.schemas.user import CreateUser, ShowUser
from app.backend.db_depends import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext
from datetime import datetime, timedelta


async def get_user_data_or_none(
        db: Annotated[AsyncSession, Depends(get_db)],
        id_or_username: Annotated[UUID | str, Field()],
        fields: Annotated[tuple | list, Field()]
) -> dict | None:
    user_values: tuple
    user_data: dict = {}
    if isinstance(id_or_username, UUID):
        # user = await db.scalar(select(User).where(User.id == id_or_username))
        user_values = (
            tuple(
                await db
                .scalar(
                    select(Bundle('user', *User.__table__.c[*fields])
                           )
                    .where(User.id == id_or_username)
                )))
    elif isinstance(id_or_username, str):
        user_values = (
            tuple(
                await db
                .scalar(
                    select(Bundle('user', *User.__table__.c[*fields])
                           )
                    .where(User.username == id_or_username)
                )))
        user_data.update(dict(zip(fields, user_values)))
    else:
        return None
    return user_data

async def get_user_or_none(
        db: Annotated[AsyncSession, Depends(get_db)],
        id_or_username: Annotated[UUID | str, Field()]
) -> User | None:
    user: User | None = None
    if isinstance(id_or_username, UUID):
        user = await db.scalar(select(User).where(User.id == id_or_username))
    elif isinstance(id_or_username, str):
        user = await db.scalar(select(User).where(User.username == id_or_username))
    return user

router = APIRouter(prefix=root_api+'/users', tags=['users'])

@router.post(path='/', status_code=status.HTTP_201_CREATED)
async def create_user(db: Annotated[AsyncSession, Depends(get_db)], new_user_raw: CreateUser):
    new_user_data: dict = new_user_raw.model_dump()
    new_user_data.pop('raw_password')
    new_user_data['password'] = bcrypt_context.hash(new_user_raw.raw_password)
    await db.execute(insert(User).values(**new_user_data))
    new_user: User | None = await db.scalar(select(User).where(User.username == new_user_raw.username))
    if not new_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this user doesn\'t exist")
    user_data: dict = new_user.__dict__
    user_data['role'] = new_user.role.value
    await db.commit()
    return {
        'user_data': ShowUser(**user_data),
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


#
# @router.get('/read_current_user')
# async def read_current_user(user: User = Depends(oauth2_scheme)):
#     return user

@router.get('/{id_or_username}')
async def show_user(
        db: Annotated[AsyncSession, Depends(get_db)],
        id_or_username: Annotated[UUID | str, Depends(get_uuid_or_str)]
):
    user: User | None = await get_user_or_none(db, id_or_username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this user doesn\'t exist")
    response = {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Successful',
        'item': ShowUser(**user.__dict__)
    }
    return response

@router.delete('/delete')
async def delete_user(
        db: Annotated[AsyncSession, Depends(get_db)],
        get_user: Annotated[dict, Depends(get_current_user)],
        user_id: UUID
):
    if not get_user.get('is_superuser'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have admin permission"
        )
    target_user = await db.scalar(select(User).where(User.id == user_id))
    if target_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You can't delete admin user"
        )
    if target_user.is_active:
        await db.execute(update(User).where(User.id == user_id).values(is_active=False))
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'detail': 'User is deleted'
        }
    else:
        return {
            'status_code': status.HTTP_200_OK,
            'detail': 'User already has been deleted'
        }
