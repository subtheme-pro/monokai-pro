#!/usr/bin/env python3

import datetime
import os
import shutil
import sys

import jinja2
import yaml


def build_jetbrains(theme_path, build_path):
    for filename in os.listdir(os.path.join(theme_path, "colors")):
        with open(os.path.join(theme_path, "colors", filename), 'r') as f:
            data = yaml.safe_load(f)
            colors = {}
            for k,v in data["colors"].items():
                colors[k] = "#" + str(v).replace('x', '')
            data["colors"] = colors

        data["filename"] = filename[:-5]
        data["date"] = datetime.datetime.now().replace(microsecond=0).isoformat()

        templates_path = os.path.join(build_path, "templates", data["template"])
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=templates_path))

        scheme_template = env.get_template("scheme.xml")
        theme_template = env.get_template("theme.json")

        if not os.path.isdir(os.path.join(build_path, "src")):
            os.makedirs(os.path.join(build_path, "src"))

        with open(os.path.join(build_path, "src", "{id}.theme.json".format(id=filename[:-5])), "w") as f:
            f.write(theme_template.render(**data))

        if not os.path.isdir(os.path.join(build_path, "resources", "themes")):
            os.makedirs(os.path.join(build_path, "resources", "themes"))

        with open(os.path.join(build_path, "resources", "themes", "{id}.xml".format(id=filename[:-5])), "w") as f:
            f.write(scheme_template.render(**data))

        # shutil.rmtree(templates_path)


def build(path="."):
    for app in os.listdir(os.path.join(path, "apps")):
        app_path = os.path.join(path, "apps", app)
        if os.path.isdir(app_path):
            build_path = os.path.join(path, "build", app)

            if os.path.exists(build_path):
                shutil.rmtree(build_path)

            shutil.copytree(os.path.join(path, "apps", app), build_path)

            if app == "jetbrains":
                print("Building {}..".format(app))
                build_jetbrains(path, build_path)
            else:
                print("Invalid app: {}".format(app))
                sys.exit(0)

    print("Done")


build()
