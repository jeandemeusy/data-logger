from datetime import datetime
from flask import Flask, render_template
from event import Event

from event_handler import EventHandler, Type
from project_handler import ProjectHandler

import os

app = Flask(__name__)


def get_filename(pre: str = "", body: str = None, suf: str = ".json") -> str:
    body = datetime.now().strftime("%Y_%m_%d") if body == None else body
    filename = pre + body + suf
    return filename


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/add_project")
def add_project():
    return projects()


@app.route("/remove_project")
def remove_project():
    return projects()


@app.route("/activites")
def activites():
    e_filename = get_filename(suf="_events.json")
    e_handler = EventHandler(file=e_filename)
    p_handler = ProjectHandler(file="projects.json")
    activities_list = []

    last_e = Event("_", "_")
    for e in e_handler.list:
        if last_e.type == Type.START.value and e.type == Type.END.value:
            project = p_handler.find(e.project).name
            date = datetime.strptime(last_e.time, e.format).strftime("%H:%M")
            duration = e - last_e
            activities_list.append((project, date, duration))
        last_e = e

    work = sum([a[2] for a in activities_list])
    total_hour_min = [work // 60, work % 60]
    pause = e_handler.pause(display=False)[1]
    pause_hour_min = [pause // 60, pause % 60]

    return render_template("activites.html", events=activities_list, total_hour_min=total_hour_min, pause_hour_min=pause_hour_min)


@ app.route("/projects")
def projects():
    folder = "data"
    project_file = "projects.json"

    files = os.listdir(folder)

    if "projects.json" in files:
        files.remove(project_file)

    p_handler = ProjectHandler(folder=folder, file=project_file)
    p_names = [p.name for p in p_handler.list]

    data = dict((name, []) for name in p_names)

    for file in files:
        e_handler = EventHandler(folder=folder, file=file)

        found_names = []
        temp_times = e_handler.time()

        if len(temp_times) != 0:
            for uid, time in temp_times.items():
                name = p_handler.find(uid).name
                data[name].append(time)
                found_names.append(name)

            for name in p_names:
                if name not in found_names:
                    data[name].append(0)

    names = [key for key, _ in data.items()]
    times = [val for _, val in data.items()]

    return render_template("projects.html", projects=names, times=times)


if __name__ == "__main__":
    app.run(debug=True)
