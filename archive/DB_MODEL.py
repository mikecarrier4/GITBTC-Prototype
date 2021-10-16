from sqlalchemy import Table, Column, Integer, String, Date, Float, Boolean, ForeignKey, UniqueConstraint, DateTime, select
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from sqlalchemy.orm.relationships import foreign
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
import os


db_url = os.getenv('DB_STRING')
Base = declarative_base()

class Users(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    userpin = Column(String(255), nullable=False, unique=True)
    email = Column(String(255))
    phone = Column(String(10))
    f_name = Column(String(255))
    l_name = Column(String(255))
    created_on = Column(DateTime)
    
    def __repr__(self):
        return (
            "user_id:{},userpin:{},email:{},phone:{},f_name:{},l_name:{},created_on:{}"
        ).format(self.user_id, self.userpin)

class Running_Jobs(Base):

    __tablename__ = "running_jobs"

    job_id= Column(Integer,primary_key=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    running = Column(Boolean, unique=False, default=True)

    def __repr__(self):
        return (("job_id:{},user_id:{},start_time:{},end_time:{},running:{}").format(self.user_id, self.user_id, self.start_time, self.end_time, self.running))


class Database(object):

    def __init__ (self):
        self.engine = create_engine(
            'postgresql://qklkptqa:8hh34zpMJz6PfhrKw8NxCQbcYiY4knP2@chunee.db.elephantsql.com/qklkptqa:5432/postgres')


        self.Sessionmaker = scoped_session(
            sessionmaker(
                autoflush=False,
                autocommit=False,
                bind=self.engine
            )
        )

        self.TABLE_NAMES = {"users" : Users,
                            "running_jobs" : Running_Jobs}

    def test(self):
        with self.Sessionmaker() as session:
            query = select(Users).where(Users.user_id == 2)
            data = session.execute(query)
            return data

    
a = Database().test()
print(a)