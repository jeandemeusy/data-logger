from datetime import datetime
import getopt
import sys

from event_handler import EventHandler
from project_handler import ProjectHandler


def usage() -> None:
    print("Default usage")


def get_filename(pre: str = "", body: str = None, suf: str = ".json") -> str:
    body = datetime.now().strftime("%Y_%m_%d") if body == None else body
    filename = pre + body + suf
    return filename


def main(argv):
    try:
        opts, _ = getopt.getopt(
            argv, "hd:ta:", ["help", "delay=", "time", "add="])
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            usage()
        elif opt in ["-a", "--add"]:
            e_filename = get_filename(suf="_events.json")
            e_handler = EventHandler(file=e_filename, force=True)
            p_handler = ProjectHandler(file="projects.json")

            project = p_handler.find(arg)
            e_handler.add(project)

        elif opt in ["-t", "--time"]:
            e_filename = get_filename(suf="_events.json")
            e_handler = EventHandler(file=e_filename, force=False)
            if e_handler.exists:
                e_handler.time(display=True)
                e_handler.pause(display=True)

        elif opt in ["-d", "--delay"]:
            e_filename = get_filename(body=arg, suf="_events.json")
            e_handler = EventHandler(file=e_filename, force=False)
            if e_handler.exists:
                e_handler.time(display=True)
                e_handler.pause(display=True)


if __name__ == "__main__":
    main(sys.argv[1:])
