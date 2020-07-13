#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
from os import path, remove

PROJECT_DIRECTORY: str = path.realpath(path.curdir)


def remove_file(filepath: str) -> None:
    remove(path.join(PROJECT_DIRECTORY, filepath))


if __name__ == "__main__":

    if "Other" == "{{ cookiecutter.license }}":
        remove_file("LICENSE")

    from html import unescape as unescape_chars

    full_name: str = unescape_chars("{{ cookiecutter.full_name | escape }}")
    if '"' in full_name:
        import fileinput
        import sys

        with fileinput.input(
            path.join(PROJECT_DIRECTORY, "docs", "source", "conf.py"), inplace=True,
        ) as f:
            for line in f:
                sys.stdout.write(line.replace(f'"{full_name}"', f"'{full_name}'"))

        with fileinput.input(
            path.join(PROJECT_DIRECTORY, "setup.py"), inplace=True,
        ) as f:
            for line in f:
                sys.stdout.write(line.replace(f'"{full_name}"', f"'{full_name}'"))
