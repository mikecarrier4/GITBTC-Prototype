from flask import Flask, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from src import DB
import subprocess
import os
import signal

app = Flask(__name__, template_folder='templates')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
#app.config['SQLALCHEMY_DATABASE_URI'] = 


@app.route('/')
def test ():
    return render_template('/index.html')


@app.route('/login',  methods = ['GET', 'POST'])
def login ():
    if request.method == 'GET':
        return 'hello'
    if request.method == 'POST':
        x = request.form
        session['pin'] = x['pin']
        session['fn'] , session['ln'], session['user_id'] = DB.User().check_pin(session['pin'])
        print('first name', session['fn'])
        current_status = DB.Running_Jobs().find_job(session['user_id']) #Grab PIN and Pdid
        print('the current status is ', current_status)
        if type(current_status) == tuple and len(current_status) == 1:
            return redirect(url_for('charts'))
        elif type(current_status) == tuple and len(current_status) > 1:
            pass #have serious issue page here
        else:
            return redirect(url_for('strategy'))


@app.route('/strategy')
def strategy():
    return render_template('/strategy.html', **locals())


@app.route('/strategy_vector', methods = ['GET', 'POST'])
def strategy_vector():
    if request.method == 'GET':
        return f'url/form'
    if request.method == 'POST':
        try:
            x = request.form
            session['Crypto']  = x['crypto']
            session['Strategy'] = x['pstrategy']
            session['Duration'] = x['sstrategy']
            return redirect(url_for('robinhood'))
        except:
            pass # have error page here


@app.route('/robinhood')
def robinhood():
    return render_template('/robinhood.html', **locals())


@app.route('/driver', methods = ['POST'])
def driver():
    if request.method == 'POST':
        x = request.form
        session['a'] = x['rhuserid']
        session['b'] = x['rhpwd']
        session['c'] = x['mfa']
        session['d'] = x['amount']
        subprocess.Popen(["python", "src/main.py", str(session)])
        x = None
        for i in ['a', 'b', 'c', 'd']:
            session.pop(i)

    return redirect(url_for('charts'))


@app.route('/charts')
def charts():
    """search for the username and display a job"""
    """display pics and details"""
    return render_template('/charts.html')


@app.route('/kill', methods = ['POST'])
def kill():
    if request.method == 'POST':
        x = request.form
        if x['kill'] == 'kill':
            job_id = DB.Running_Jobs().find_job(session['user_id'])
            print('the job id is ' ,job_id)
            os.kill(job_id[0], signal.SIGTERM)
            DB.Running_Jobs().kill_time(job_id[0])
            return redirect(url_for('charts'))
        else:
            pass # spit out html to kill
            
    return redirect(url_for('charts'))


@app.route('/about')
def about():
    return render_template('/about.html')


@app.route('/form')
def hello_form():
    return render_template('/form.html')


if __name__ == "__main__":
    app.run()
