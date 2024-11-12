from fastapi import FastAPI, HTTPException, Depends, status
from models import User,UserRole
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Optional

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

@app.get("/user_roles")
def read_user_roles(db: Session = Depends(get_db)):
    user_role = db.query(UserRole.type_id,UserRole.usertype).all()
    role_list = [{"type_id": r.type_id, "usertype":r.usertype} for r in user_role]
    return role_list

@app.get("/user")
def read_user(db: Session = Depends(get_db)):
    user = db.query(User.firstname, User.lastname, UserRole.usertype).join(UserRole, User.roleid == UserRole.type_id).all()
    user_list = [{"firstname": u.firstname, "lastname": u.lastname, "usertype": u.usertype} for u in user]
    return user_list

@app.get("/user_role_details/{id}")
def get_user(type_id:int,db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.type_id == type_id).first()
    if not user_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Role not found")
    return user_role

@app.get("/user_details/{id}")
def get_user(user_id:int,db: Session = Depends(get_db)):
    user = db.query(User.firstname, User.lastname, UserRole.usertype).join(UserRole, User.roleid == UserRole.type_id).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {
        "firstname": user.firstname,
        "lastname": user.lastname,
        "usertype": user.usertype
    }

@app.post("/create-user-roles/{type_id}")
def create_user_roles(type_id:int,usertype:str,db:Session = Depends(get_db)):
    existing_role = db.query(UserRole).filter(UserRole.type_id == type_id).first()
    if existing_role:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Role ID already exist")
    db_user_role=UserRole(type_id=type_id,usertype=usertype)
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)
    return db_user_role

@app.post("/create-user")
def create_user(user_id:int,firstname: str, lastname: str, roleid: int, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.user_id == user_id).first()
    if existing_user:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID already exist")
    user_role = db.query(UserRole).filter(UserRole.type_id == roleid).first()
    if not user_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid roleid: No such role exists")
    db_user = User(user_id=user_id,firstname=firstname, lastname=lastname, roleid=roleid)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/update-user-role/{type_id}")
def update_user_role(type_id:int, usertype: Optional[str] = None, db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.type_id == type_id).first()
    if not user_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid roleid: No such role exists")
    if usertype is not None:
        user_role.usertype = usertype
    db.commit()
    return {
       "message": "User Role update successful", 
       "user":{
           "type_id":user_role.type_id,
           "usertype":user_role.usertype
       }
    }

@app.put("/update-user/{user_id}")
def update_user(user_id:int, firstname: Optional[str]=None,lastname: Optional[str]=None,roleid: Optional[str]=None,db: Session = Depends(get_db)):
    user = db.query(User).join(UserRole,User.roleid==UserRole.type_id).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User_Id User not found")
    if firstname is not None:
        user.firstname = firstname
    if lastname is not None:
        user.lastname =lastname
    if roleid is not None:
        user_role = db.query(UserRole).filter(UserRole.type_id == roleid).first()
        if not user_role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid roleid: No such role exists")
        user.roleid = roleid
    db.commit()
    return {
        "message": "User update successful",
        "user": {
            "User_id": user.user_id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "roleid": user.roleid
        }
    }

@app.delete("/delete-user-role/{type_id}")
def delete_user_role(type_id:int,db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.type_id == type_id).first()
    if not user_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid roleid: No such role exists")
    db.delete(user_role)
    db.commit()
    return {"Message" : "User Role Deleted Successfully"}

@app.delete("/delete-user/{user_id}")
def delete_user(user_id:int,db: Session = Depends(get_db)):
    user = db.query(User).join(UserRole,User.roleid==UserRole.type_id).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User_Id User not found")
    db.delete(user)
    db.commit()
    return {"Message" : "User Deleted Successfully"}
    

    




    
    

