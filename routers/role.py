from fastapi import APIRouter, HTTPException, Depends, status
from models import UserRole
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

@router.get("/user_roles")
def read_user_roles(db: Session = Depends(get_db)):
    user_role = db.query(UserRole.type_id, UserRole.usertype).all()
    role_list = [{"type_id": r.type_id, "usertype": r.usertype} for r in user_role]
    return role_list

@router.get("/user_role_details/{id}")
def get_user_role(type_id: int, db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.type_id == type_id).first()
    if not user_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Role not found")
    return user_role

@router.post("/create-user-roles/{type_id}")
def create_user_roles(type_id: int, usertype: str, db: Session = Depends(get_db)):
    existing_role = db.query(UserRole).filter(UserRole.type_id == type_id).first()
    if existing_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Role ID already exists")
    db_user_role = UserRole(type_id=type_id, usertype=usertype)
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)
    return db_user_role

@router.put("/update-user-role/{type_id}")
def update_user_role(type_id: int, usertype: Optional[str] = None, db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.type_id == type_id).first()
    if not user_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid roleid: No such role exists")
    if usertype is not None:
        user_role.usertype = usertype
    db.commit()
    return {
        "message": "User Role update successful",
        "user_role": {
            "type_id": user_role.type_id,
            "usertype": user_role.usertype
        }
    }

@router.delete("/delete-user-role/{type_id}")
def delete_user_role(type_id: int, db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.type_id == type_id).first()
    if not user_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid roleid: No such role exists")
    db.delete(user_role)
    db.commit()
    return {"Message": "User Role Deleted Successfully"}


