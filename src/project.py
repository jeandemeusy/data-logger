class Project:
    """
    Class to store all informations about a given project.
    """

    def __init__(self, name: str, uid: str):
        """
        Initialisation of the class.
        """

        self.uid = uid
        self.name = name

    def __str__(self):
        """
        String representation of a project.
        """

        return f"<{__name__}.{self.__class__.__name__} object: {self.__dict__}>"

    def __lt__(self, other):
        """
        Project to project comparison logic. 
        """

        return int(self.uid) < int(other.uid)
