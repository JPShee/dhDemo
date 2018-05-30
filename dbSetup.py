import sqlalchemy
from datetime import datetime
from hello import db, TodoList, TodoItem

engine = sqlalchemy.create_engine('mysql+pymysql://root:Password@localhost')
engine.execute("CREATE DATABASE dhDemo_db")

db.create_all()

todolist1 = TodoList(title='TestTitle1', description="This is the first test list",
	updatedAt=datetime.utcnow())
db.session.add(todolist1)

todolist2 = TodoList(title='TestTitle2', description="This is the second test list",
	updatedAt=datetime.utcnow())
db.session.add(todolist2)

todolist3 = TodoList(title='TestTitle3', description="This is the third test list",
	updatedAt=datetime.utcnow())
db.session.add(todolist3)

todolist4 = TodoList(title='TestTitle4', description="This is the fourth test list",
	updatedAt=datetime.utcnow())
db.session.add(todolist4)

todoitem1 = TodoItem(description="This is the first test item for list 1", listId=1, 
	updatedAt=datetime.utcnow())
db.session.add(todoitem1)

todoitem2 = TodoItem(description="This is the second test item for list 1", listId=1, 
	updatedAt=datetime.utcnow())
db.session.add(todoitem2)

todoitem3 = TodoItem(description="This is the first test item for list 2", listId=2, 
	updatedAt=datetime.utcnow())
db.session.add(todoitem3)

todoitem4= TodoItem(description="This is the second test item for list 2", listId=2, 
	updatedAt=datetime.utcnow())
db.session.add(todoitem4)

todoitem5 = TodoItem(description="This is the first test item for list 3", listId=3, 
	updatedAt=datetime.utcnow())
db.session.add(todoitem5)

todoitem6 = TodoItem(description="This is the second test item for list 3", listId=3, 
	updatedAt=datetime.utcnow())
db.session.add(todoitem6)

todoitem7 = TodoItem(description="This is the first test item for list 4", listId=4, 
	updatedAt=datetime.utcnow())
db.session.add(todoitem7)

todoitem8 = TodoItem(description="This is the second test item for list 4", listId=4, 
	updatedAt=datetime.utcnow())
db.session.add(todoitem8)

todoitem9 = TodoItem(description="This is the third test item for list 1", complete= True, listId=1, 
	updatedAt=datetime.utcnow())
db.session.add(todoitem9)

db.session.commit()