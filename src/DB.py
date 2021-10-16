import os 
import psycopg2
import urllib.parse as up
from dotenv import load_dotenv
import datetime


class Cursor:
    def __init__ (self):
        """ Initalize Connection"""
        self.conn = psycopg2.connect('postgres://qklkptqa:8hh34zpMJz6PfhrKw8NxCQbcYiY4knP2@chunee.db.elephantsql.com/qklkptqa')
        self.cursor = self.conn.cursor()
        return None


class User(Cursor):
    """For all Table SQL Statments that deal with the USER table"""

    def insert_user (self, *args):
        """ userpin, email, phone, fname, lname"""
        try:
            self.current_time = datetime.datetime.now()
            self.args = args
            sql_statment = """
            INSERT INTO users
            (userpin, email, phone, f_name, l_name, created_on)
            VALUES
            ('{}', '{}', '{}', '{}', '{}', '{}')
            """.format(self.args[0], self.args[1], self.args[2], self.args[3], self.args[4], self.current_time)
            self.cursor.execute(sql_statment)
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            print(args)
        except:
            self.cursor.close()
            self.conn.close()
            return 'Check Arguments, Error'

    def check_pin (self, pin):
        """check for login credentials"""
        try:
            self.pin = pin
            sql_statment = """
            SELECT f_name, l_name, user_id FROM users WHERE userpin = '{}'
            """.format(pin)
            self.cursor.execute(sql_statment)
            a = (self.cursor.fetchone())
            self.cursor.close()
            self.conn.close()
            return a[0], a[1], a[2]
        except:
            return 'Login Failed'

    def user_phone (self, pin):
        try:
            self.pin = pin
            sql_statment = """
            SELECT phone FROM users WHERE userpin = '{}'
            """.format(self.pin)
            self.cursor.execute(sql_statment)
            a = self.cursor.fetchone()
            print(a)
            self.cursor.close()
            self.conn.close()
            return "".join(a)
        except:
            return 'USER retrival Failed'

    def user_id (self, pin):
        
        self.pin = pin
        sql_statment = """
        SELECT user_id FROM users WHERE userpin = '{}'
        """.format(self.pin)
        self.cursor.execute(sql_statment)
        a = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return a[0]

        
class Running_Jobs(Cursor):
    
    def insert_job (self, job_id, strategy, user_id):
        """job_id, user_id, start_time, end_time, status"""
        self.job_id = job_id
        self.user_id = user_id
        self.current_time = datetime.datetime.now()
        self.strategy = strategy
        sql_statment = """
        INSERT INTO running_jobs
        (pdid, user_id, strategy, start_time)
        VALUES
        ('{}', '{}', '{}', '{}')
        """.format(self.job_id, self.user_id, self.strategy, self.current_time)
        self.cursor.execute(sql_statment)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def find_job (self, user_id):
        """find job with user id that is running"""
        self.user_id = user_id
        sql_statment = """
        SELECT pdid 
        FROM running_jobs 
        WHERE user_id = {} and end_time is NULL
        """.format(self.user_id)
        self.cursor.execute(sql_statment)
        job = self.cursor.fetchone()
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return job

    #TODO Update this for heartbeat 
    def update_time (self, job_id):
        self.job_id = job_id
        sql_statment = """
        UPDATE running_jobs
        SET status = '{}'
        WHERE job_id = {}
        """.format(True, job_id)
        self.cursor.execute(sql_statment)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    
 
    def kill_time (self, pdid):
        self.pdid = pdid
        self.time = datetime.datetime.now()
        sql_statment = """
        UPDATE running_jobs
        SET end_time = '{}'
        WHERE pdid = {}
        """.format(self.time, pdid)
        self.cursor.execute(sql_statment)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        

"""
a = Running_Jobs().find_job(1)
print(a)
print(type(a))
print(a[0])
"""

sql_1 = """
CREATE TABLE IF NOT EXISTS users (
   user_id serial PRIMARY KEY,
   userpin VARCHAR (50) UNIQUE NOT NULL,
   email VARCHAR (50), 
   phone VARCHAR (10),
   f_name VARCHAR (50),
   l_name VARCHAR (50),
   created_on TIMESTAMP NOT NULL
);

"""

sql_2 = """
CREATE TABLE IF NOT EXISTS running_jobs (
    job_id serial PRIMAY KEY,
    user_id INT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status BOOLEAN,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);
"""
sql_3 = """
DROP TABLE IF EXISTS running_jobs;

CREATE TABLE running_jobs (
    job_id serial PRIMArY KEY,
    pdid INT,
    user_id INT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    heart_beat TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
    strategy VARCHAR (15)
);

"""

sql_4 = """
DROP TABLE IF EXISTS users

CREATE TABLE IF NOT EXISTS users (
   user_id serial PRIMARY KEY,
   userpin VARCHAR (50) UNIQUE NOT NULL,
   email VARCHAR (50), 
   phone VARCHAR (10),
   f_name VARCHAR (50),
   l_name VARCHAR (50),
   created_on TIMESTAMP NOT NULL,
   profile_pic BYTEA,
   activate_pic BYTEA
   )
   """