from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.orm import sessionmaker
import  os

base_dir=os.path.abspath(os.path.dirname(__file__))
db_path=os.path.join(base_dir,"User.db")

SQLALCHEMY_DATABASE_URL="sqlite:///"+db_path

Base=declarative_base()

engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,index=True)
    email=Column(String,unique=True,index=True)
    age=Column(Integer,index=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:

        yield db
    finally:
        db.close()