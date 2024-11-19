from fastapi import APIRouter, HTTPException, Depends, status
from models import UserRole
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy.exc import IntegrityError

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

@router.get("/user_roles")
def read_user_roles(db: Session = Depends(get_db)):
    user_role = db.query(UserRole.type_id,UserRole.role_name).all()
    role_list = [{"typeid":r.type_id,"rolename": r.role_name} for r in user_role]
    return role_list

@router.get("/user_roles_count")
def read_user_roles(db: Session = Depends(get_db)):
    user_role = db.query(UserRole.type_id,UserRole.role_name).all()
    role_list = [{"typeid":r.type_id,"rolename": r.role_name} for r in user_role]
    user_role_count = len(role_list)
    return user_role_count



@router.get("/user_roles/{role_name}")
def read_user_roles(role_name:str,db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.role_name==role_name).first()
    if not user_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid roleid: No such role exists")
    role_dict = {"typeid": user_role.type_id, "rolename": user_role.role_name}
    return role_dict

@router.post("/create-user-roles")
def create_user_roles(role_name: str, db: Session = Depends(get_db)):
    db_user_role = UserRole(role_name=role_name)
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)
    return db_user_role

@router.put("/update-user-role/{type_id}")
def update_user_role(type_id:int,role_name: Optional[str] = None, db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.type_id == type_id).first()
    if not user_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid roleid: No such role exists")
    if role_name is not None:
        user_role.role_name = role_name
    db.commit()
    return {
        "message": "User Role update successful",
        "userrole": {
            "typeid": user_role.type_id,
            "rolename": user_role.role_name
        }
    }

@router.delete("/delete-user-role/{type_id}")
def delete_user_role(type_id: int, db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.type_id == type_id).first()

    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role ID: No such role exists"
        )

    try:
        db.delete(user_role)
        db.commit()
        return {"Message": "User Role Deleted Successfully"}

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete role. It is referenced by other records."
        )

