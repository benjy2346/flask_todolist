from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://tao1808039546:WN9iLSs67Kwevzzh@cluster0.fbq8qf5.mongodb.net/myDB?retryWrites=true&w=majority'
mongo = PyMongo(app)
todos = mongo.db.todo

@app.route('/')
def index():
    saved_todos = todos.find() 
    return render_template('index.html', todos=saved_todos)

@app.route('/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo')
    if new_todo == "":
        return redirect(url_for('index'))
    todos.insert_one({'text' : new_todo, 'complete' : False})
    return redirect(url_for('index'))

@app.route('/complete/<oid>')
def complete(oid):
    todo_item = todos.find_one({'_id': ObjectId(oid)})
   
    if todo_item['complete'] == False :
        todos.insert_one( {'text' : todo_item['text'] + ' done', 'complete' : True})
        todos.delete_one(todo_item)
    return redirect(url_for('index'))

@app.route('/delete_completed')
def delete_completed():
    todos.delete_many({'complete' : True})
    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all():
    todos.delete_many({})
    return redirect(url_for('index'))