from application import app
from flask import render_template, request, redirect, flash, url_for

from bson import ObjectId

from .forms import TodoForm
from application import db
from datetime import datetime


@app.route("/")
def get_todos():
    todos = []
    for todo in db.todos_flask.find():
        todo["_id"] = str(todo["_id"])
        #todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M:%S")
        todos.append(todo)

    return render_template("view_todos.html", todos = todos)
    
@app.route("/add_todo", methods = ['POST', 'GET'])
def add_todo():
    if request.method == "POST":
        form = TodoForm(request.form)
        name = form.name.data
        print(name)
        book_name = form.book_name.data
        usn = form.usn.data
        pending_fine= form.pending_fine.data

        db.todos_flask.insert_one({
            "name": name,
            "book_name": book_name,
            "usn": usn,
            "pending_fine": pending_fine
        })
        flash("book successfully added", "success")
        return redirect("/")
    else:
        form = TodoForm()
    return render_template("add_todo.html", form = form)


@app.route("/delete_todo/<id>")
def delete_todo(id):
    print(id)
    db.todos_flask.find_one_and_delete({"_id": ObjectId(id)})
    flash("book successfully deleted", "success")
    return redirect("/")


@app.route("/update_todo/<id>", methods = ['POST', 'GET'])
def update_todo(id):
    if request.method == "POST":
        form = TodoForm(request.form)
        name = form.name.data
        print(name)
        book_name = form.book_name.data
        usn = form.usn.data
        pending_fine= form.pending_fine.data
        print(ObjectId(id))
        db.todos_flask.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": name,
            "book_name": book_name,
            "usn": usn,
            "pending_fine": pending_fine
            
        }})
        flash(" book successfully updated", "success")
        return redirect("/")
    else:
        form = TodoForm()

        todo = db.todos_flask.find_one({"_id": ObjectId(id)})
        print(todo)
        form.name.data = todo.get("name", None)
        form.book_name.data = todo.get("book_name", None)
        form.usn.data = todo.get("usn", None)
        form.pending_fine.data = todo.get("pending_fine", None)


    return render_template("add_todo.html", form = form)