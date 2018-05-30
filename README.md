#Dash Hudson Flask Demo API
A Flask todo demo app

##How to Run
```
git clone https://github.com/JPShee/dhDemo.git
cd dhDemo
. venv/bin/activate
pip install -r requirements.txt
```
Edit dbSetup.py line 5 and hello.py line 8 to ensure that the MySQL user information specified is correct for your machine and said user can create databases.

```
python dbSetup.py
python hello.py
```

###API
The API endpoints are as follows
/newList(POST)
Takes in the arguments "title" and "description" and creates a new todo list

/getLists(GET)
Takes in no arguments and returns all todo lists

/getAList/<int:id>(GET)
Takes in no arguments and returns a todo list specified by id

/deleteList/<int:id>(DELETE)
Takes in no arguments and deletes the todo list specified by id and removes and related todo items

/editListInfo<int:id>(PUT)
Takes in "title" and optionally "description" and changes those for the list specified by id

/getListItems<int:id>(GET)
Takes in no arguments and returns all todos assosciated with the list specified by id

/newTodoItem(POST)
Takes in "description" and "listId" and creates a new todo with the given description related to the list with the provided listId

/editTodoInfo<int:id>(PUT)
Takes in "description" and changes the description of the todo specified by id

/todoStatus<int:id>(PUT)
Toggles the status of the todo specified by id

/deleteTodo<int:id>(DELETE)
Deletes the todo specified by id
