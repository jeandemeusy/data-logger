
from typing import List
from os import path, mkdir
import json

from project import Project


class ProjectHandler():
    """
    Class to handle projects.
    """

    def __init__(self, folder: str = "data", file: str = "projects.json"):
        """
        Initisalisation of the class.
        """

        self.filename: str = folder + "/" + file
        if not path.exists(folder):
            mkdir(folder)
        if not path.exists(self.filename):
            open(self.filename, 'w').close()

        self.list: List[Project] = self.load()

    def show(self) -> None:
        """
        Shows all existing projets.
        """
        self.save()
        for project in self.list:
            print(project)

    def save(self) -> None:
        """
        Save the project list by replacing the existing file.
        """

        self.list.sort()
        with open(self.filename, 'w') as f:
            json.dump([ob.__dict__ for ob in self.list], f)

    def load(self) -> List[Project]:
        """
        Load the project list from the file.
        """

        with open(self.filename, 'r') as f:
            try:
                list = json.load(f)
            except:
                list = []

        return [Project(p["name"], p["uid"]) for p in list]

    def add(self, string: str) -> None:
        """
        Adds a project to the list. It checks that the uid and the name are not already in the list.
        """

        project_data = string.split("-")

        existing_names = [p.name for p in self.list]
        existing_uids = [p.uid for p in self.list]

        assert len(project_data) == 2, \
            "Missing information, either project uid or name."

        name: str = project_data[1].strip()
        uid: str = project_data[0].strip()

        assert name not in existing_names, "Project name already exists."
        assert uid not in existing_uids, "Project uid already exists."
        assert len(name) != 0, "Name is empty"
        assert len(uid) != 0, "uid is empty"

        self.list.append(Project(name, uid))
        self.save()
        print(f"Project '{name}' ({uid}) has been added.")

    def remove(self, string: str) -> None:
        """
        Removes a project iditified by a string from the list. The string may correspond to the uid or the name of the aimed project.
        """

        project = self.find(string)
        self.list.remove(project)
        self.save()

        print(f"Project '{project.name}' removed.")

    def find(self, string: str) -> Project:
        """
        Find a project identified by a string from the list. The string may correspond to the uid or the name of the aimed project.
        """

        projects_uids = [p.uid for p in self.list]
        projects_names = [p.name for p in self.list]

        if string in projects_uids:
            return self.list[projects_uids.index(string)]

        if string in projects_names:
            return self.list[projects_names.index(string)]
