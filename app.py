# app.py

# Import packages / modules
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import math

# Init flask
app = Flask(__name__)

# Configs
app.config.from_object('config')
app.config.from_pyfile('config.py')


# Init SQLAlchemy
db = SQLAlchemy(app)

# Models
class Task(db.Model):
	__tablename__ = 'tasks'
	idTask = db.Column('idTask', db.Integer, primary_key = True)
	task = db.Column('task', db.String)
	status = db.Column('status', db.String, default = 'uncomplete')
	creation_date = db.Column('creation_date', db.DateTime, default = datetime.utcnow())

	def __init__(self, task):
		self.task = task

# Routes
allTasks = []

# Generate a random integer based on current time in UTC format
def IDgenerator():
	return math.floor((datetime.utcnow() - datetime(1970,1,1)).total_seconds())

# Home page
@app.route('/')
def index():
	all_tasks = Task.query.all()
	return render_template('index.html', t = all_tasks)

# Create a new task
@app.route('/task', methods=['POST'])
def tasks():
	new_task = Task(request.form['task'])
	db.session.add(new_task)
	db.session.commit()
	return redirect('/', 302)
	
# Read a specific task
@app.route('/task/<id>', methods=['GET'])
def getTask(id):
	return id

# Update a task
@app.route('/updatetask/<taskID>', methods=['GET'])
def updateTask(taskID):
	the_task = Task.query.filter_by(idTask = taskID).first()

	return render_template('update.html', task = the_task)

@app.route('/do_updatetask', methods=['POST'])
def do_updatetask():
	update_task = Task.query.filter_by(idTask = request.form['taskID']).first()
	update_task.task = request.form['task']
	db.session.commit()

	return redirect('/', 302)

# Delete a task
@app.route('/deletetask/<taskID>', methods=['GET'])
def deleteTask(taskID):
	
	delete_task = Task.query.filter_by(idTask=taskID).first()
	db.session.delete(delete_task)
	db.session.commit()

	# redirect to homepage
	return redirect('/', 302)

@app.route('/complete/<taskID>')
def complete(taskID):

	complete_task = Task.query.filter_by(idTask = taskID).first()
	complete_task.status = 'complete'
	db.session.commit()

	# Redirect to the homepage
	return redirect('/', 302)

@app.route('/uncomplete/<taskID>')
def uncomplete(taskID):

	uncomplete_task = Task.query.filter_by(idTask = taskID).first()
	uncomplete_task.status = 'uncomplete'
	db.session.commit()

	# Redirect to the homepage
	return redirect('/', 302)

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
