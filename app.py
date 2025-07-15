import os
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_KEY"))

from flask import Flask, render_template, request, redirect, url_for
from db import get_all_tasks, add_task, update_task, delete_task

from dotenv import load_dotenv
load_dotenv()  # Make sure environment variables load




app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "mysecretkey")

# 🏠 Home
@app.route("/")
def home():
    return render_template("index.html")

# 📋 Task Manager
@app.route("/task-manager")
def task_manager():
    try:
        tasks = get_all_tasks()
        return render_template("task_manager.html", tasks=tasks)
    except Exception as e:
        return f"❌ Internal Server Error: {str(e)}"

# ➕ Add Task
@app.route("/add-task", methods=["POST"])
def add_task_route():
    title = request.form.get("title")
    status = request.form.get("status")
    if title and status:
        add_task(title, status)
    return redirect(url_for("task_manager"))

# ✏️ Edit Task
@app.route("/edit-task/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    title = request.form.get("title")
    status = request.form.get("status")
    update_task(task_id, title, status)
    return redirect(url_for("task_manager"))

# ❌ Delete Task
@app.route("/delete-task/<int:task_id>")
def delete_task_route(task_id):
    delete_task(task_id)
    return redirect(url_for("task_manager"))

# 🤖 Generate Proposal (AI)
@app.route("/generate-proposal", methods=["GET", "POST"])
def generate_proposal():
    proposal = None

    if request.method == "POST":
        job_title = request.form.get("title")
        job_desc = request.form.get("description")

        prompt = f"""
You are an expert freelance proposal writer. Write a professional UpWork proposal
 based on the following job details:

Job Title: {job_title}

Job Description: {job_desc}

The proposal should be polite, confident, and convincing. Highlight relevant skills and past experience.
"""

        try:
            model = genai.GenerativeModel("gemini-pro-1.5")
            response = model.generate_content(prompt)
            proposal = response.text
        except Exception as e:
            proposal = f"❌ Error generating proposal: {str(e)}"

    return render_template("generate_proposal.html", proposal=proposal)

# 🚀 Run App
if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("APP_PORT", 5000)))
