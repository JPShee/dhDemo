import os
from datetime import  datetime
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password@localhost/dhDemo_db'
db = SQLAlchemy(app)

##MODELS FOR DATABASE##

class TodoList(db.Model):
	__tablename__ = "todolists"
	id = db.Column('id', db.Integer, primary_key=True)
	title = db.Column('title', db.Text)
	description = db.Column('description', db.Text)
	createdAt = db.Column('createdAt', db.DateTime, index=True, default=datetime.utcnow())
	updateAt = db.Column('updatedAt', db.DateTime)	
	todoitems = db.relationship('TodoItem', cascade='all, delete-orphan')

class TodoItem(db.Model):
	__tablename__ = 'todoitems'
	id = db.Column('id', db.Integer, primary_key=True)
	description = db.Column('description', db.Text)
	complete = db.Column('complete', db.Boolean, default=False)
	listId = db.Column('listId', db.ForeignKey('todolists.id'), nullable=False)
	createdAt = db.Column('createdAt', db.DateTime, index=True, default=datetime.utcnow())
	updateAt = db.Column('updatedAt', db.DateTime)	

##Handle JSON responses to more easily return##
##There may have been a better way to do this##
def serialize_list(data):
	return {
		"id": data.id,
		"title": data.title,
		"description": data.description
	}

def serialize_items(data):
	if data.complete == False:
		completed = "Not Complete"
	else:
		completed = "Complete"
	return {
		"Parent List Id": data.listId,
		"description": data.description,
		"Status": completed
	}


##API ROUTES##
@app.route("/")
def hello():
	return "Hello World"

##Create a new list##
@app.route('/newList', methods=['POST'])
def newList():
	data = request.get_json() or {}
	if 'title' not in data:
		abort(400)
	todolist = TodoList(title=data['title'], description=['description'], 
		updateAt=datetime.utcnow())
	db.session.add(todolist)
	db.session.commit()
	return jsonify({"message": todolist.id })

##Return all lists##
@app.route("/getLists", methods=['GET'])
def getLists():
	retrievedLists = [serialize_list(x) for x in TodoList.query.order_by(TodoList.createdAt)]
	if retrievedLists:
		return jsonify({"Todo Lists": retrievedLists})
	else:
		abort(400)

##Return a specific list##
@app.route("/getAList/<int:id>", methods=['GET'])
def getAList(id):
	check = serialize_list(Todolist.query.get(id))
	if check:
		return jsonify({"Requested Todo List": check})
	else:
		abort(400)

##Delete a provided list and the accompanying todo items##
@app.route("/deleteList/<int:id>", methods=['DELETE'])
def deleteList(id):
	check = TodoList.query.get(id)
	if check:
		db.session.delete(check)
		db.session.commit()
		return jsonify({"message": "entry deleted"})
	else:
		abort(400)

##Edit the title and description for a list##
@app.route("/editListInfo/<int:id>", methods=['PUT'])
def editListInfo(id):
	data = request.get_json() or {}
	if 'title' not in data:
		abort(400)
	todolist = TodoList.query.get(id)
	if todolist:
		todolist.title = data['title']
		todolist.updateAt = datetime.utcnow()
		if 'description' not in data:
			db.session.commit()
			return jsonify({"message": todolist.id})
		db.session.commit()
		return jsonify({"message": todolist.id})
	else:
		abort(400)

##Return the items on a specific list##
@app.route("/getListItems/<int:id>", methods=['GET'])
def getListItems(id):
	queryStr = TodoItem.query.filter_by(listId=id).order_by(TodoItem.createdAt)
	retrievedItems = [serialize_items(x) for x in queryStr]
	if retrievedItems:
		return jsonify({"List Items": retrievedItems})
	else:
		abort(400)

##Add a new todo item to a list##
@app.route("/newTodoItem", methods=['POST'])
def newTodoItem():
	data = request.get_json() or {}
	if 'description' not in data or 'listId' not in data:
		abort(400)
	check = TodoList.query.get(data['listId'])
	if check:
		todoitem = TodoItem(description=['description'], listId=data['listId'])
		db.session.add(todoitem)
		db.session.commit()
		return jsonify({"message": "todo list item added"})
	else:
		abort(400)

##Edit the description of a provided todo item##
@app.route("/editTodoInfo/<int:id>", methods=['PUT'])
def editTodoInfo(id):
	data = request.get_json() or {}
	if 'description' not in data:
		abort(400)
	todoitem = TodoItem.query.get(id)
	if todoitem:
		todoitem.description = data['description']
		todoitem.updateAt = datetime.utcnow()
		db.session.commit()
		return jsonify({"message": "todo list item updated"})
	else:
		abort(400)

##Toggles the completed status of a provided todo item##
@app.route("/todoStatus/<int:id>", methods=['PUT'])
def todoStatus(id):
	todoitem = TodoItem.query.get(id)
	if todoitem:
		if todoitem.complete == True:
			todoitem.complete = False
		else:
			todoitem.complete = True
		todoitem.updateAt = datetime.utcnow()
		db.session.commit()
		return jsonify({"message": "todo status updated"})
	else:
		abort(400)

##Deletes a given todo item##
@app.route("/deleteTodo/<int:id>", methods=['DELETE'])
def deleteTodo(id):
	todoitem = TodoItem.query.get(id)
	if todoitem:
		db.session.delete(todoitem)
		db.session.commit()
		return jsonify({"message": "todo succesfully deleted"})
	else:
		abort(400)


if __name__ == "__main__":
    app.run(debug=True)

