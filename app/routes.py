from flask import (
    Flask,
    request,
    render_template
)
import requests 
app = Flask(__name__)
BACKEND_URL = "http://127.0.0.1:5000/tasks"

#example
@app.get("/")
def index():
    return render_template("index.html")

@app.get("/about")
def about_me():
    me = {
        "first_name": "Dorothy",
        "last_name": "Schwark",
        "hobbies": "Chickens",
        "bio": "loves chickens"
    }
    return render_template("about.html", user=me)

@app.get("/tasks")
def task_list():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        task_list = response.json().get("tasks")
        return render_template("list.html", tasks=task_list)
    return(
        render_template("error.html", err=response.status_code),
        response.status_code
    )

@app.get("/tasks/edit/<int:pk>")
def edit_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        task_data = response.json().get("task")
        return render_template("edit.html", task=task_data),
    return(
        render_template("error.html", err=response.status_code),
    )

@app.post("/tasks/edit/<int:pk>")
def edit_task_req(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    task_data =request.form
    response = requests.put(url, json=task_data)
    if response.status_code ==204:
        return render_template("success.html")
    return(
        render_template("error.html", response.status_code),
        response.status_code
    )

@app.post("/tasks/add")
def new_task():
    url = "%s/%s" % (BACKEND_URL)
    new_task =request.form
    task_data={
        "summary":new_task.get("summary"),
        "description":new_task.get("description")
    }
    response = requests.put(url, json=task_data)
    if response.status_code ==204:
        return render_template("success.html")
    return(
        render_template("error.html", response.status_code),
        response.status_code
    )
@app.get("/tasks/add")
def new_task_form():
    #url = "%s/%s" % (BACKEND_URL)
    #response = requests.get(url)
    #form = create_task()
    #if response.status_code ==204:
    return render_template("create.html")
    # return(
    #     render_template("error.html", response.status_code),
    #     response.status_code
    # )