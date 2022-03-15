"""
db_user.py
    - contains functions for database operations relating to the user table
    - functions from here are called by user-related CRUD endpoints
"""

from backend import schemas
from sqlalchemy.orm.session import Session
from .models import DbUser
from .hash import Hash


def create_user(db: Session, request: schemas.UserRequest):
    print('creating new user')
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.encrypt(request.password)
     )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_user_data(db: Session):
    return db.query(DbUser).all()


def get_user_data(db: Session, username: str):
    return db.query(DbUser).filter(DbUser.username == username).first()


def update_user_data(db: Session, username: str, request: schemas.UserRequest):
    user = db.query(DbUser).filter(DbUser.username == username)
    user.update({
        DbUser.username: request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.encrypt(request.password)
    })
    db.commit()
    return{'success': True, 'message': f'Updated user: {username}'}


def delete_user_data(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    db.delete(user)
    db.commit()
    return{'success': True, 'message': f'Deleted user: {username}'}


def check_duplicates(db: Session, username: str, email: str):
    if db.query(DbUser).filter(DbUser.username == username).first() or db.query(DbUser).filter(DbUser.email == email).first():
        return True
    return False