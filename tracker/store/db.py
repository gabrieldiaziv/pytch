import os
import sys
import logging
from datetime import datetime

import mysql.connector as sql

ENV_DB_HOST = 'MYSQL_HOST'
ENV_DB_USER = 'MYSQL_USER'
ENV_DB_NAME = 'MYSQL_NAME'
ENV_DB_PASS = 'MYSQL_PASS'

class PytchDB:
    def __init__(self):
        host = os.getenv(ENV_DB_HOST)
        user = os.getenv(ENV_DB_USER)
        name = os.getenv(ENV_DB_NAME)
        pswd = os.getenv(ENV_DB_PASS)

        if host and user and name and pswd:
            self._db = sql.connect(
                host=host,
                user=user,
                database=name,
                password=pswd,
            )
        else:
            logging.fatal("could not connect to db")
            sys.exit(1)
            
                
    def insert_match(self, match_id: str, user_id: str, team_home: str, team_away: str, data: datetime):

