#!venv/bin/python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration for SQLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SQLALCHEMY_TRACK_MODIFICATION = True
