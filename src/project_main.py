from typing import List
import getopt
import sys

from project_handler import ProjectHandler


def usage() -> None:
    print("Default usage")


def main(argv: List[str]):
    handler = ProjectHandler(folder="data", file="projects.json")

    try:
        opts, _ = getopt.getopt(
            argv, "hla:r:", ["help", "list", "add=", "remove="])
    except getopt.GetoptError:
        usage()
    else:
        for opt, arg in opts:
            if opt in ["-h", "--help"]:
                usage()
            elif opt in ["-l", "--list"]:
                handler.show()
            elif opt in ["-a", "--add"]:
                handler.add(arg)
            elif opt in ["-r", "--remove"]:
                handler.remove(arg)


if __name__ == "__main__":
    main(sys.argv[1:])
