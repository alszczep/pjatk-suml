#!/usr/bin/env python
import os
import sys


def main():
    from dotenv import load_dotenv

    load_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

    from django.core.management.commands.runserver import Command as runserver

    runserver.default_port = os.environ["API_PORT"]
    runserver.default_addr = "0.0.0.0"

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
