from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from source.database.db import get_db
from source.repository import users as repository_users
from source.schemas.user import UserSchema, UserResponse

from source.models.models import Consumer#,Role
from source.services.auth import auth_service
# from source.services.roles import RoleAccess

router = APIRouter(prefix='/users', tags=['users'])


@router.get("/", response_model=list[UserResponse])
async def get_users(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                    db: AsyncSession = Depends(get_db), c_user: Consumer = Depends(auth_service.get_current_user)):
    users = await repository_users.get_users(limit, offset, db)
    return users

@router.get("/birth_date", response_model=list[UserResponse])
async def get_users_birth(limit: int = Query(7, ge=7, le=100),
                    db: AsyncSession = Depends(get_db), c_user: Consumer = Depends(auth_service.get_current_user)):
    users = await repository_users.get_users_birth(limit, db)
    return users

@router.get("/search_by", response_model=list[UserResponse])
async def get_users_by(first_name: str = Query(None, min_length=3, description="Frist name search query"), 
                       second_name: str = Query(None, min_length=3, description="Second name search query"),
                       email_add: str = Query(None, min_length=3, description="Email search query"),
                       db: AsyncSession = Depends(get_db), c_user: Consumer = Depends(auth_service.get_current_user)):
    users = await repository_users.get_users_by(first_name, second_name, email_add, db)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), c_user: Consumer = Depends(auth_service.get_current_user)):
    user = await repository_users.get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db), c_user: Consumer = Depends(auth_service.get_current_user)):
    user = await repository_users.create_user(body, db)
    return user


@router.put("/{user_id}")
async def update_user(body: UserSchema, user_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), c_user: Consumer = Depends(auth_service.get_current_user)):
    user = await repository_users.update_user(user_id, body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), c_user: Consumer = Depends(auth_service.get_current_user)):
    user = await repository_users.delete_user(user_id, db)
    return user
