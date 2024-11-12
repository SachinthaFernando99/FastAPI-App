from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, UserRole
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/user")
def read_user(db: Session = Depends(get_db)):
    user = db.query(User.firstname, User.lastname, UserRole.usertype).join(UserRole, User.roleid == UserRole.type_id).all()
    user_list = [{"firstname": u.firstname, "lastname": u.lastname, "usertype": u.usertype} for u in user]
    return user_list

@router.get("/user_details/{id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User.firstname, User.lastname, UserRole.usertype).join(UserRole, User.roleid == UserRole.type_id).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {
        "first_name": user.firstname,
        "last_name": user.lastname,
        "user_type": user.usertype
    }

@router.post("/create-user")
def create_user(user_id: int, firstname: str, lastname: str, roleid: int, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.user_id == user_id).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID already exists")
    user_role = db.query(UserRole).filter(UserRole.type_id == roleid).first()
    if not user_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid roleid: No such role exists")
    db_user = User(user_id=user_id, firstname=firstname, lastname=lastname, roleid=roleid)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "user_id": db_user.user_id,
        "firs_tname": db_user.firstname,
        "last_name": db_user.lastname,
        "role_id": db_user.roleid
    }

@router.put("/update-user/{user_id}")
def update_user(user_id: int, firstname: Optional[str] = None, lastname: Optional[str] = None, roleid: Optional[int] = None, db: Session = Depends(get_db)):
    user = db.query(User).join(UserRole, User.roleid == UserRole.type_id).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User_ID: User not found")
    if firstname is not None:
        user.firstname = firstname
    if lastname is not None:
        user.lastname = lastname
    if roleid is not None:
        user_role = db.query(UserRole).filter(UserRole.type_id == roleid).first()
        if not user_role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid roleid: No such role exists")
        user.roleid = roleid
    db.commit()
    return {
        "message": "User update successful",
        "user": {
            "User_id": user.user_id,
            "first_name": user.firstname,
            "last_name": user.lastname,
            "role_id": user.roleid
        }
    }

@router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).join(UserRole, User.roleid == UserRole.type_id).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User_ID: User not found")
    db.delete(user)
    db.commit()
    return {"Message": "User Deleted Successfully"}
