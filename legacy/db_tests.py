# encoding: utf-8
__version__ = "0.1"

import json
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)


class DBTests:
    """This script reads gamedata.xlsx and exports ut to gamedata.json"""

    def __init__(self, **kwargs):
        super(DBTests, self).__init__(**kwargs)

    def fetch_mod_info(
        self,
        db="broken_shield_gamedata.sqlite",
        gamedata="gamedata",
        db_path="./gamedata/",
        etsb="edge",
        mod_type="pkc",
        mod_id="e_grit",
    ):

        conn = sqlite3.connect(db_path + db)
        cursor = conn.cursor()
        logging.info(f"\n----------\n")
        logging.info(f"[  ] SQLite: connecting to db '{db_path}{db}'")

        fetch_sql = (
            f"SELECT * FROM {gamedata} WHERE category='{etsb}' AND type='{mod_type}'"
        )

        """
        logging.info(
            f"[  ] SQLite: fetching '{etsb}':'{mod_type}' data from table '{gamedata}'"
        )
        """
        cursor.execute(fetch_sql)
        data = cursor.fetchall()
        data_count = len(data)

        """
        logging.info(
            f"[  ] SQLite: fetched {data_count} records from table '{gamedata}' from category '{etsb}' "
            f"and type '{mod_type}'"
        )
        """
        fetch_sql2 = f"SELECT * FROM {gamedata} WHERE mod_id='{mod_id}'"

        logging.info(
            f"[  ] SQLite: fetching mod data for mod '{mod_id}' data from table '{gamedata}'"
        )
        cursor.execute(fetch_sql2)
        data2 = cursor.fetchall()
        data_count2 = len(data2)

        print("data: " + str(data2[0]))

        logging.info(
            f"[  ] SQLite: fetched {data_count2} records from table '{gamedata}' from where mod_id is '{mod_id}'"
        )
        logging.info(f"\n----------\n")

        conn.commit()
        conn.close()

        logging.info(f"\n----------\n")
        # print(str(data))

        logging.info(f"\n----------\n")
        # print(str(data2))

        logging.info(f"\n----------\n")

        for i in data2:
            print(i)
            count = 0
            for j in i:
                print(str(count) + ": " + str(j))
                count += 1

        print(data2[0][12])
        return data


test_db = DBTests()
test_db.fetch_mod_info()
