#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from databases import createDatabase


def main():
    dbconstructor()
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def dbconstructor():
    db = createDatabase()
    db.dbCreate()
    a = ["income", "expenses", "items"]
    for i in a: db.createTable(i)
    db.importData(table = "income", amount = 150, contributor = "Emma", source = "Medlemavgift", date = "20210303")
        

if __name__ == '__main__':
    main()
