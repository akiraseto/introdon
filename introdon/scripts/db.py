from flask_script import Command

from introdon import db


class InitDB(Command):
    """create database"""

    def run(self):
        db.create_all()
