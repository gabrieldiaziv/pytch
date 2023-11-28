import os
import sys
import logging
import uuid

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
            
                
    def update_match(self, match_id: str, localization_url: str, label_url:str , match_url: str, thumbnail_url:str):
        query = """
        UPDATE GameMatch SET
            localization_video = %s,
            generated_video = %s,
            match_json = %s,
            thumbnail_url = %s
        WHERE
            match_id = %s
        """

        cursor = self._db.cursor()
        cursor.execute(query,
            [localization_url, label_url, match_url, thumbnail_url, match_id]
        )
        self._db.commit()
        cursor.close()

    def insert_viz(self, match_id: str, viz_name:str, viz_desc:str, viz_url: str):
        query ="""
        INSERT INTO Viz (viz_id, match_id, name, descr, url)
        VALUES
            (%s, %s, %s, %s, %s)
        """

        cursor=self._db.cursor()
        cursor.execute(query,
            [str(uuid.uuid4()), match_id, viz_name, viz_desc, viz_url]
        )
        self._db.commit()
        cursor.close()




