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
    user = db.query(User.first_name, User.last_name, UserRole.role_name).join(UserRole, User.role_id == UserRole.type_id).all()
    user_list = [{"firstname": u.first_name, "lastname": u.last_name, "rolename": u.role_name} for u in user]
    return user_list



@router.post("/create-user")
def create_user(first_name: str, last_name: str, role_id: int, db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.type_id == role_id).first()
    if not user_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid roleid: No such role exists")
    db_user = User(first_name=first_name, last_name=last_name, role_id=role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "userid": db_user.user_id,
        "firstname": db_user.first_name,
        "lastname": db_user.last_name,
        "roleid": db_user.role_id
    }

@router.put("/update-user/{user_id}")
def update_user(user_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None, role_id: Optional[int] = None, db: Session = Depends(get_db)):
    user = db.query(User).join(UserRole, User.role_id == UserRole.type_id).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User_ID: User not found")
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if role_id is not None:
        user_role = db.query(UserRole).filter(UserRole.type_id == role_id).first()
        if not user_role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid roleid: No such role exists")
        user.role_id = role_id
    db.commit()
    return {
        "message": "User update successful",
        "user": {
            "Userid": user.user_id,
            "firstname": user.first_name,
            "lastname": user.last_name,
            "roleid": user.role_id
        }
    }

@router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).join(UserRole, User.role_id == UserRole.type_id).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User_ID: User not found")
    db.delete(user)
    db.commit()
    return {"Message": "User Deleted Successfully"}
