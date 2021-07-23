from datetime import datetime


class Event:
    """
    Class to store all informations about a given log entry.
    """

    def __init__(self, project: str, type: str, time: str = None):
        """
        Initialisation of the class.
        """

        if time == None:
            time = self.get_time()

        self.time = time
        self.project = project
        self.type = type

    @property
    def format(self):
        """
        Date and time format for logs.
        """

        return "%d/%m/%Y %H:%M:%S"

    def get_time(self) -> str:
        """
        Return current time with given format.
        """

        return datetime.now().strftime(self.format)

    def __str__(self):
        """
        String representation of an event.
        """

        return f"<{__name__}.{self.__class__.__name__} object: {self.__dict__}>"

    def __lt__(self, other):
        """
        Event to event comparison logic. 
        """

        time1 = datetime.strptime(self.time, self.format)
        time2 = datetime.strptime(other.time, self.format)
        return time1 < time2

    def __sub__(self, other):
        """
        Event to event substraction.
        """

        time1 = datetime.strptime(self.time, self.format)
        time2 = datetime.strptime(other.time, self.format)
        diff = time1 - time2

        return diff.seconds // 60
