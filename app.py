from flask import Flask, render_template, request, redirect, url_for
from db import get_all_tasks, add_task, update_task, delete_task

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/task-manager")
def task_manager():
    try:
        tasks = get_all_tasks()
        return render_template("task_manager.html", tasks=tasks)
    except Exception as e:
        return f"❌ Internal Server Error: {str(e)}"

@app.route("/add-task", methods=["POST"])
def add_task_route():
    title = request.form.get("title")
    status = request.form.get("status")
    if title and status:
        add_task(title, status)
    return redirect(url_for("task_manager"))

@app.route("/edit-task/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    title = request.form.get("title")
    status = request.form.get("status")
    update_task(task_id, title, status)
    return redirect(url_for("task_manager"))

@app.route("/delete-task/<int:task_id>")
def delete_task_route(task_id):
    delete_task(task_id)
    return redirect(url_for("task_manager"))

if __name__ == "__main__":
    app.run(debug=True)
