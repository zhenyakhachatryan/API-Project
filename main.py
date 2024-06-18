from fastapi import FastAPI,Request,Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import User, get_db
from sqlalchemy.exc import SQLAlchemyError

app=FastAPI()
templates=Jinja2Templates(directory='templates')

@app.get('/',response_class=HTMLResponse)
async def home_page(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})

@app.get('/view_user',response_class=HTMLResponse)
async def home_page(request:Request):
    return templates.TemplateResponse("view_user.html",{"request":request})

@app.get('/update_user',response_class=HTMLResponse)
async def home_page(request:Request):
    return templates.TemplateResponse("update_user.html",{"request":request})

@app.get('/delete_user',response_class=HTMLResponse)
async def home_page(request:Request):
    return templates.TemplateResponse("delete_user.html",{"request":request})




@app.post('/add_user',response_class=HTMLResponse)
async def add_user(request:Request,db:Session=Depends(get_db)):
    form= await request.form()
    name=form.get("name")
    email=form.get("email")
    age=form.get("age")
    print(name)
    print(email)
    print(age)

    if not name or not email or not age:
        return templates.TemplateResponse("home.html",{"request":request,"Error":"All fields should be filled up"})
    else:
        user=db.query(User).filter_by(email=email).first()
        if user:
            return templates.TemplateResponse("home.html", {"request":request,"Error": "User already exists"})
        else:
            new_user=User(name=name,email=email,age=int(age))
            db.add(new_user)
            db.commit()
            return templates.TemplateResponse("home.html", {"request":request,"Message": "User added successfully"})

@app.post('/view_user',response_class=HTMLResponse)
async  def view_user(request:Request,db:Session=Depends(get_db)):
    form=await request.form()
    user_id=form.get("user_id")

    if not user_id:
        return templates.TemplateResponse("view_user.html",{"request":request,"Error":"Field should be filled up"})
    else:
        user=db.query(User).filter_by(id=user_id).first()
        if not user:
            return templates.TemplateResponse("view_user.html", {"request":request,"Error": "User not found}"})
        else:
            return templates.TemplateResponse("view_user.html",{"request":request,"Message": f"ID:{user.id}, Name:{user.name},Email: {user.email}, Age:{user.age}"})

@app.post('/update_user',response_class=HTMLResponse)
async  def view_user(request:Request,db:Session=Depends(get_db)):
    form=await request.form()
    user_id=form.get("user_id")
    name = form.get("name")
    email = form.get("email")
    age = form.get("age")

    if not name or not email or not age:
        return templates.TemplateResponse("update_user.html",{"request":request,"Error":"All fields should be filled up"})

    else:
        user=db.query(User).filter_by(id=user_id).first()
        if not user:
            return templates.TemplateResponse("update_user.html", {"request":request,"Error": "User not found}"})
        else:
            user_email = db.query(User).filter_by(email=email).first()
            if user_email:
                return templates.TemplateResponse("update_user.html",{ "request":request,"Error": "User already exists"})
            try:
                user.name=name
                user.email=email
                user.age=int(age)
                db.commit()
                return templates.TemplateResponse("update_user.html", {"request":request,"Message": "User updated successfully"})
            except SQLAlchemyError:
                db.rollback()
                return templates.TemplateResponse("update_user.html", {"request":request,"Error": "Cannot update user"})

@app.post("/delete_user",response_class=HTMLResponse)
async  def view_user(request:Request,db:Session=Depends(get_db)):
    form = await request.form()
    user_id = form.get("user_id")

    if not user_id:
        return templates.TemplateResponse("delete_user.html",{"request":request,"Error": "Field should be filled up"})
    else:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return templates.TemplateResponse("delete_user.html", {"request":request,"Error": "User not found}"})
        else:
            try:
                db.delete(user)
                db.commit()
                return templates.TemplateResponse("delete_user.html", {"request":request,"Message": "User deleted successfully"})
            except SQLAlchemyError:
                db.rollback()
                return templates.TemplateResponse("delete_user.html", {"request":request,"Error": "Cannot update user"})







