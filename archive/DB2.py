from sqlalchemy import create_engine
from sqlalchmey.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
import os

db_url = os.getenv('DB_STRING')


class Database(object):


    def __init__(self):
        self.engine = create_engine(
            db_url,
            pool_recycle=3600,
            pool_size=10,
            echo=False,
            pool_pre_ping=True
        )

        self.Sessionmaker = scoped_session(
            sessionmaker(
                autoflush=False,
                autocommit=False,
                bind=self.engine
            )
        )

        self.TABLE_NAMES = {"users" : Users,
                            "running_jobs" : Running_Jobs}
