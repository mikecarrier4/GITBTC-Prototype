from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Identity, DateTime, insert, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
import psycopg2
from sqlalchemy.sql.sqltypes import Date
from dotenv import load_dotenv
import os
db_url = 'postgresql://uelexskq:WjAIlGoAK7HsjRTu2uiwd5xUY_QyqsZt@fanny.db.elephantsql.com/uelexskq'
engine = create_engine(db_url, echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, Identity(start=1, cycle=True), primary_key=True)
    pin = Column('pin', String, unique=True )
    f_name = Column('first_name', String)
    l_name = Column('last_name', String)
    phone = Column('phone', String)
    email = Column('email', String)


class Jobs(Base):
    __tablename__ = 'running_jobs'

    job_id = Column('job_id', Integer, Identity(start=1, cycle=True), primary_key=True)
    pid = Column('pid', Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_time = Column('start_time', DateTime, non_nullable=True)
    heart_beat = Column('hear_beat', DateTime)
    end_time = Column('end_time', DateTime)
    stategy = Column('stategy', String)


class Database(object):

    def __init__ (self):
        self.engine = create_engine(
            db_url,
            pool_recycle = 3600,
            pool_size = 10,
            echo = True,
            pool_pre_ping=True
        )
        self.Sessionmaker = scoped_session(
            sessionmaker(
                autoflush=False,
                autocommit=False,
                bind=self.engine
            )

        )
        self.TABLE_NAMES = {
            "user": User,
            "running_jobs": Jobs
        }

    def insert_user(self):
        """Inser User"""
        with self.Sessionmaker() as session:
            query = select(User)
            session.execute(query)
            session.commit()


Database().insert_user()