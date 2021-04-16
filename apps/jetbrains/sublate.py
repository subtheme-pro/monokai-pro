import datetime
import shutil

SUBLATE = {
    "exclude": "templates"
}

DATE = datetime.datetime.now().replace(microsecond=0).isoformat()


def post():
    shutil.rmtree('templates')
    print("Finished jetbrains")
