
from typing import Dict, List, Tuple
from os import path, mkdir
from enum import Enum
import json
from time import sleep

from event import Event
from project import Project


class Type(Enum):
    """
    Enum for work-logs types.
    """

    START = "start"
    END = "end"
    NDEF = "ndef"


class EventHandler():
    """
    Class to handle all existing and future work-logs.
    """

    def __init__(self, folder: str = "data", file: str = "events.json", force: bool = True):
        """
        Initialisation of the class. Set destination folder to store .json files, and the name of the file to look at and to store data to.
        The function handles the creation of the folder.
        """

        self.filename: str = folder + "/" + file
        self.list: List[Event] or None = None

        if force:
            if not path.exists(folder):
                mkdir(folder)
            if not path.exists(self.filename):
                open(self.filename, 'w').close()

        if path.exists(self.filename):
            self.list = self.load()
        else:
            print("File does not exist")

        self.exists = self.list != None

    def show(self) -> None:
        """
        Shows the content of the work-log list.
        """

        for project in self.list:
            print(project)

    def save(self) -> None:
        """
        Save the work-log list by replacing the existing file.
        """

        with open(self.filename, 'w') as f:
            json.dump([ob.__dict__ for ob in self.list], f)

    def load(self) -> List[Event]:
        """
        Load the work-log list from the file.
        """

        with open(self.filename, 'r') as f:
            try:
                list = json.load(f)
            except:
                list = []

        return [Event(e["project"], e["type"], e["time"]) for e in list]

    def add(self, project: Project) -> None:
        """
        Adds a log to the list. It autonamtically detects if it is a "start" or an "end" log.
        If a start-log is added after an other start-log, the corresponding end-log is added between them.
        """

        assert isinstance(project, Project), f"Project not found."

        last_e = self.list[-1] if self.list else Event("_", "_")

        if last_e.project != project.uid:
            type = Type.START
            if last_e.type == Type.START.value:
                self.__append(last_e.project, Type.END)
                sleep(1)
        else:
            type = Type.END if last_e.type == Type.START.value else Type.START

        self.__append(project.uid, type)
        self.save()

    def time(self, display: bool = False) -> Dict[str, str]:
        """
        Sum work times by project. 
        """

        last_e = Event("_", "_")
        if len(self.list) == 0:
            return []

        if self.list[-1].type == Type.START.value:
            print("Current work not finished. Showing only partial work-time.")

        conseq: List[Tuple[int, str]] = []
        for e in self.list:
            if last_e.type == Type.START.value and e.type == Type.END.value:
                conseq.append((e - last_e, e.project))
            last_e = e

        times = {}
        unique_projects = set([tup[1] for tup in conseq])
        for p in unique_projects:
            times[p] = sum([tup[0] for tup in conseq if tup[1] == p])

        if display:
            for p, time in times.items():
                self.__print_time(f"Project '{p}'", time)

        return times

    def pause(self, display: bool = False) -> Tuple[str, int]:
        """
        Sum pause times.
        """

        last_e = Event("_", "_")

        conseq_times: List[int] = []
        for e in self.list:
            if last_e.type == Type.END.value and e.type == Type.START.value:
                conseq_times.append(e - last_e)
            last_e = e

        time = sum(conseq_times)
        if display:
            self.__print_time("Pause", time)

        return ("Pause", time)

    def __print_time(self, string: str, time: int) -> None:
        """
        Default project print format.
        """

        print(f"{string}: {time//60:0>2}h{time%60:0>2}")

    def __append(self, project: str, type: Type) -> None:
        """
        Append a project and its event type to the log-list.
        """
        self.list.append(Event(project, type.value))

        if type == Type.START:
            print(f"Work on '{project}' started.")
        elif type == Type.END:
            print(f"Work on '{project}' finished.")
        else:
            print(f"Unexpected state for '{project}'.")
