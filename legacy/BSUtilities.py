# encoding: utf-8
__version__ = "1.1.1"

from json import load, dump
import os
import logging
import sqlite3
from timer import Timer

logging.basicConfig(level=logging.INFO)


class BrokenShieldUtilities:
    """This is a class of utilities shared by the various BrokenShield App elements."""

    card_delete = ""
    file_size = ""
    last_history = []
    current_selection = []
    user_history = []
    history_message = ""
    t = Timer()

    def __init__(self, **kwargs):
        super(BrokenShieldUtilities, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def open_json(self, readfile="bci", directory="user_settings"):
        """Static method to open a json file"""
        logging.debug("Utility: Action is read from JSON file")
        # All the card data and user history data is stored in a JSON
        user_settings = Broken_Shield_Companion()

        if directory == "user_settings":
            save_path = user_settings.get_user_data_dir()
        else:
            save_path = str(directory)

        if readfile == "user_history":
            # This file is writeable to so need to check it out
            openfile = str(readfile + ".json")
            file_save_path = str(save_path + "/" + openfile)
            try:
                if os.path.isfile(file_save_path):
                    # Check the file exists
                    if os.stat(file_save_path).st_size != 0:
                        # Check the file is not 0 byte sized
                        with open(file_save_path, "r") as json_file:
                            data = load(json_file)
                            logging.info(
                                "Utility: " + file_save_path + " was successfully read"
                            )
                    else:
                        # Write a blank file with []
                        logging.debug(
                            "Utility: " + file_save_path + " is empty, creating file"
                        )
                        data = []
                        self.write_json(data)
                else:
                    # Write a blank file with []
                    logging.debug(
                        "Utility: " + file_save_path + " is empty, creating file"
                    )
                    data = []
                    self.write_json(data)
            except ValueError:
                # Uh-oh, something broke badly!
                logging.error("Exception: " + file_save_path + " does not exist")
                data = []

        else:
            # This is much more straightforward as the other json files are read only
            openfile = str(directory + "/" + readfile + ".json")
            try:
                if os.stat(openfile).st_size != 0:
                    with open(openfile, "r") as json_file:
                        data = load(json_file)
                        logging.debug(
                            "Utility: " + openfile + ".json was successfully read"
                        )
                else:
                    logging.debug("Utility: " + openfile + ".json is empty")
                    data = []
            except ValueError:
                logging.error("Exception: " + openfile + ".json does not exist")
                data = []

        return data

    @staticmethod
    def write_json(data, writefile="user_history", mode="w", directory="user_settings"):
        """Static method to safely write to the user's history json file"""
        logging.debug("Utility: Action is write to JSON file")

        # This method dumps the current info as a json
        user_settings = Broken_Shield_Companion()
        if directory == "user_settings":
            save_path = user_settings.get_user_data_dir()
        else:
            save_path = str(directory)

        openfile = str(writefile + ".json")
        file_save_path = str(save_path + "/" + openfile)

        try:
            with open(file_save_path, mode) as outfile:
                dump(data, outfile, indent=4)
                logging.debug(
                    "Utility: "
                    + save_path
                    + "/"
                    + writefile
                    + ".json was successfully updated"
                )
        except ValueError:
            logging.error(
                "Exception: " + save_path + "/" + writefile + ".json cannot be written"
            )
        return data

    def update_user_history(self, new_results):
        """Method to update user history when a new card is pulled or skill test is made"""
        logging.debug("Utility: Action is update user history")
        # Take history, add in new results, and then save it back to history
        count = 0

        # Open and read current history
        user_history = self.open_json("user_history")
        if len(user_history) != 0:
            count = len(user_history)
            logging.debug("Utility: The user history has a length of " + str(count))
        else:
            count = 0
            logging.debug(
                "Utility: The user history is empty, therefore length is " + str(count)
            )

        # Add current count to the beginning of new_results
        new_results = {"count": count, **new_results}
        # Append new_results to user_history
        user_history.append(new_results)

        # Write updated user_history to file
        self.write_json(user_history)

    def history_file_size(self, filename="user_history"):
        """Static method to check file size of user history - will create empty history file if one doesn't
        exist"""
        logging.debug("Utility: Action is display card history file size")

        user_settings = Broken_Shield_Companion()
        save_path = user_settings.get_user_data_dir()
        openfile = str(filename + ".json")
        file_save_path = str(save_path + "/" + openfile)
        try:
            if os.path.isfile(file_save_path):
                # Check the file exists
                if os.stat(file_save_path).st_size != 0:
                    # Check the file is not 0 byte sized
                    with open(file_save_path, "r") as json_file:
                        data = load(json_file)
                        file_size = str(
                            round(os.path.getsize(file_save_path) / 1024, 2)
                        )
                        logging.debug(
                            "Utility: The user history file size is "
                            + str(file_size)
                            + "KB"
                        )
                else:
                    # file doesn't exist - create empty file to prevent crash
                    # Write a blank file with []
                    logging.debug(
                        "Utility: " + file_save_path + " is empty, creating file"
                    )
                    data = []
                    self.write_json(data)
                    file_size = str(round(os.path.getsize(file_save_path) / 1024, 2))
                    logging.debug(
                        "Utility: The user history file size is "
                        + str(file_size)
                        + "KB"
                    )
            else:
                # file doesn't exist - create empty file to prevent crash
                # Write a blank file with []
                logging.debug("Utility: " + file_save_path + " is empty, creating file")
                data = []
                self.write_json(data)
                file_size = str(round(os.path.getsize(file_save_path) / 1024, 2))
                logging.debug(
                    "Utility: The user history file size is " + str(file_size) + "KB"
                )
        except ValueError:
            # Uh-oh, something broke badly!
            logging.error("Exception: " + file_save_path + " does not exist")

        return file_size

    def show_user_history(self):
        """Method to show user's card and skilltest history"""
        logging.debug("Utility: Action is show user history")
        user_history = {}
        self.last_history = []
        new_row = []
        compiled_row_info = ""

        rv_key = 0

        # Open and read current history
        user_history = self.open_json("user_history")
        count = len(user_history)

        # Format those cards and turn them into text
        for item in user_history:

            if item["history_type"] == "card":

                card_pulled = str(item["name"])

                if item["type"] == "boost":
                    deck_type = "Boost"
                    description = (
                        "[color="
                        + str(item["color"])
                        + "]Minor:[/color] "
                        + str(item["minor"])
                        + "; [color="
                        + str(item["color"])
                        + "]Major:[/color] "
                        + str(item["major"])
                    )

                elif item["type"] == "complication":
                    deck_type = "Complication"
                    description = (
                        "[color="
                        + str(item["color"])
                        + "]Minor:[/color] "
                        + str(item["minor"])
                        + "; [color="
                        + str(item["color"])
                        + "]Major:[/color] "
                        + str(item["major"])
                        + "; [color="
                        + str(item["color"])
                        + "]Catastrophic:[/color] "
                        + str(item["catastrophic"])
                    )
                else:
                    deck_type = str.capitalize(item["deck"]) + " Injury"
                    description = str(item["description"])

                # Clean up the text, remove line breaks ad then compile all the entries into a single label
                stripped_description = description.replace("\n", "")
                compiled_row_info = (
                    str(count)
                    + ". [color="
                    + str(item["color"])
                    + "]"
                    + str(card_pulled)
                    + " ("
                    + str(deck_type)
                    + "):[/color] "
                    + stripped_description
                    + "\n"
                )

            elif item["history_type"] == "skilltest":
                description = str(item["description"])
                compiled_row_info = str(count) + ". " + description + "\n"
            else:
                compiled_row_info = "0. Empty History.\n"

            new_row = [
                dict(text=compiled_row_info, rv_key=item["count"]),
            ]

            self.last_history.extend(new_row)

            count = count - 1  # counting down as we will reverse the list order...
            rv_key = rv_key + 1

        # Reverse the list because you want newest at the top
        self.last_history.reverse()

        logging.debug(
            "Utility: The last_history in user history are: \n" + str(self.last_history)
        )

        return self.last_history

    def select_row(self, rv_key, active):
        """Required method to display the card history with one card per row"""
        logging.debug("Utility: List action is select row")
        if active and rv_key not in self.current_selection:
            logging.debug(
                "Utility: List action is append, active: "
                + str(active)
                + ", rv_key: "
                + str(rv_key)
            )
            self.delete_row_from_history(rv_key)

        elif not active and rv_key in self.current_selection:
            logging.debug(
                "Utility: List action is delete, active: "
                + str(active)
                + ", rv_key: "
                + str(rv_key)
            )

    def delete_row_from_history(self, row_id):
        """Method to delete an individual card from the history"""
        logging.debug("Utility: Action is delete card(s) from card history")

        # Read card_history and delete entry entries where 'count' == card_id
        self.user_history = self.open_json("user_history")

        logging.debug("Utility: Deleting selected entry: count: " + str(row_id))

        # Search card_history for entry to delete
        for i in range(len(self.user_history)):
            if self.user_history[i]["count"] == int(row_id):
                self.user_history.pop(i)
                break

        self.write_json(self.user_history)
        self.show_user_history()

        return self.user_history

    def delete_user_history(self):
        """Method to delete entire card and skilltest history"""
        logging.debug("Utility: Action is delete user history")
        # Simple method for wiping the contents of the user_history.json file
        data = []
        self.write_json(data)
        logging.debug(
            "Utility: The user history file has been deleted and replaced with "
            + str(data)
        )
        feedback = "User history deleted!"
        return feedback

    def character_db(
        self,
        live_character,
        username_input,
        db_name="character.db",
        table_name="characters",
        just_fetch=False,
    ):
        """This method is used to save, update and grab character info from the character.db SQLite3 database and
        characters table by default"""

        output = {}

        # SQLite3 DB info: Put database in same directory as this script
        # make_string_safe(input_text, lower=False, allow_hash=True, parenthesis=False, hyphen=False):
        username = self.make_string_safe(str(username_input), allow_hash=False)
        db = self.make_string_safe(str(db_name), allow_hash=False)
        table = self.make_string_safe(str(table_name), allow_hash=False)

        # Establish a connection to the DB
        logging.info("SQLite: connecting to db = " + db)
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # get stored object from database
        logging.info(
            "SQLite: SELECT * FROM " + table + ' WHERE username = "' + username + '"'
        )
        sql = "SELECT * FROM " + table + " WHERE username = ?"
        cursor.execute(sql, [username])
        data = cursor.fetchall()
        data_count = len(data)
        logging.info(
            "SQLite: Fetched data is: " + str(data) + ", Length: " + str(data_count)
        )

        # This DB script expects any input to be in the form of a big JSON object which it then needs to iterate
        # through. These are the top level sections:
        character_sections = (
            "info",
            "career",
            "points",
            "nodes",
            "stats",
            "live_stats",
            "edges",
            "traits",
            "sliverware",
            "breeds",
        )

        """
        if just_fetch:
            output = data
        else:
            if len(data) == 0:
                # if object does not exist, create it. Leave data set unaltered.
                logging.info('SQLite: "INSERT INTO ' + table + ' VALUES (' + str(username) + ', ' + str(rerollable_dice)
                             + ', ' + str(dl) + ', ' + str(successes) + ', ' + str(drama_result))
                sql = 'INSERT INTO ' + table + ' VALUES (?, ?, ?, ?, ?, 1, 1)'
                cursor.execute(sql, [username, rerollable_dice, dl, successes, drama_result])
                output = data
            else:
                # if stored object exists we need update it. Update returned data set
                logging.info('SQLite: UPDATE ' + table + ' SET rerollable_dice = ' + str(rerollable_dice) + ', dl = '
                             + str(dl) + ', successes = ' + str(successes) + ', drama_result = "' + str(drama_result)
                             + '", allow_one = ' + str(set_allow_one) + ', allow_two = ' + str(set_allow_two)
                             + ' WHERE username = "' + str(username) + '"')
                sql = 'UPDATE ' + table + ' SET rerollable_dice = ?, dl = ?, successes = ?, drama_result = ?, allow_one = ?, allow_two = ? WHERE username = ?'
                cursor.execute(sql, [rerollable_dice, dl, successes, drama_result, set_allow_one, set_allow_two, username])
                output = [username, rerollable_dice, dl, successes, drama_result, set_allow_one, set_allow_two]
        """

        # close database connection
        conn.commit()
        conn.close()

        return output

    def fetch_update_sqlite_util(
        self,
        just_fetch=False,
        username="",
        rerollable_dice=0,
        dl=0,
        successes=0,
        drama_result="",
        allow_one=True,
        allow_two=True,
        db_name="user_rerolls.db",
        table="rerolls",
    ):
        # Create the SQLite3 DB file user_rerolls.db in the same folder as this script

        # Dice Roll User and info
        username = str(username)
        rerollable_dice = int(rerollable_dice)
        dl = int(dl)
        successes = int(successes)
        drama_result = str(drama_result)

        # SQLite3 DB info
        db_name = str(db_name)
        table = str(table)

        """
        CREATE TABLE rerolls (
            username VARCHAR NOT NULL PRIMARY KEY,
            rerollable_dice INTEGER,
            dl INTEGER,
            successes INTEGER,
            drama_result VARCHAR,
            allow_one INTEGER DEFAULT 1,
            allow_two INTEGER DEFAULT 1
        );    
        """

        # Establish a connection to the DB
        logging.info("SQLite: connecting to db = " + db_name)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # get stored object from database

        logging.info(
            "SQLite: SELECT * FROM " + table + ' WHERE username = "' + username + '"'
        )
        sql = "SELECT * FROM " + table + " WHERE username = ?"
        cursor.execute(sql, [username])
        data = cursor.fetchall()
        data_count = len(data)
        logging.info(
            "SQLite: Fetched data is: " + str(data) + ", Length: " + str(data_count)
        )

        if just_fetch:
            output = data
        else:
            if len(data) == 0:
                # if object does not exist, create it. Leave data set unaltered.
                logging.info(
                    'SQLite: "INSERT INTO '
                    + table
                    + " VALUES ("
                    + str(username)
                    + ", "
                    + str(rerollable_dice)
                    + ", "
                    + str(dl)
                    + ", "
                    + str(successes)
                    + ", "
                    + str(drama_result)
                )
                sql = "INSERT INTO " + table + " VALUES (?, ?, ?, ?, ?, 1, 1)"
                cursor.execute(
                    sql, [username, rerollable_dice, dl, successes, drama_result]
                )
                output = data
            else:
                # Has 1 success been added to the test?
                if allow_one:
                    set_allow_one = 1
                else:
                    set_allow_one = 0

                # have 2 dice been added to the test
                if allow_two:
                    set_allow_two = 1
                else:
                    set_allow_two = 0

                # if stored object exists we need update it. Update returned data set
                logging.info(
                    "SQLite: UPDATE "
                    + table
                    + " SET rerollable_dice = "
                    + str(rerollable_dice)
                    + ", dl = "
                    + str(dl)
                    + ", successes = "
                    + str(successes)
                    + ', drama_result = "'
                    + str(drama_result)
                    + '", allow_one = '
                    + str(set_allow_one)
                    + ", allow_two = "
                    + str(set_allow_two)
                    + ' WHERE username = "'
                    + str(username)
                    + '"'
                )
                sql = (
                    "UPDATE "
                    + table
                    + " SET rerollable_dice = ?, dl = ?, successes = ?, drama_result = ?, allow_one = ?, allow_two = ? WHERE username = ?"
                )
                cursor.execute(
                    sql,
                    [
                        rerollable_dice,
                        dl,
                        successes,
                        drama_result,
                        set_allow_one,
                        set_allow_two,
                        username,
                    ],
                )
                output = [
                    username,
                    rerollable_dice,
                    dl,
                    successes,
                    drama_result,
                    set_allow_one,
                    set_allow_two,
                ]

        # close database connection
        conn.commit()
        conn.close()

        return output

    @staticmethod
    def make_string_safe(
        input_text, lower=False, allow_hash=True, parenthesis=False, hyphen=False
    ):
        """This functional programming method does multiple string replaces and outputs a safe name."""
        logging.debug('BSU: Input String is: "' + str(input_text) + '"')
        input_text = str(input_text)
        if parenthesis:
            if ": " in input_text:
                input_text = input_text.replace(": ", " (")
            elif ":_" in input_text:
                input_text = input_text.replace(":_", "_(")

        if hyphen:
            pass
        else:
            input_text = input_text.replace("-", "_")

        if "(" in input_text:
            if ")" in input_text:
                pass
            else:
                input_text = input_text + ")"

        replace_string = (
            (".", ""),
            ("?", ""),
            (" ", "_"),
            ("'", ""),
            ("!", ""),
            (",", ""),
            ("/", "_"),
            (":", "_"),
            ("__", "_"),
        )
        funcs = [str.replace for x in replace_string]
        count = 0

        for x in funcs:
            input_text = x(
                input_text, str(replace_string[count][0]), str(replace_string[count][1])
            )
            count += 1

        if allow_hash:
            pass
        else:
            input_text = input_text.replace("#", "")

        if lower:
            input_text = input_text.lower()

        logging.debug('BSU: Output String is: "' + str(input_text) + '"')

        return input_text

    @staticmethod
    def make_string_pretty(input_text):
        logging.debug('BSU: Input String is: "' + str(input_text) + '"')
        input_text = str(input_text)
        input_text = input_text.replace("_", " ")
        input_text = input_text.title()

        logging.debug('BSU: Output String is: "' + str(input_text) + '"')

        return input_text

    def write_character_to_db(
        self, live_character, db_name="character.db", table="characters"
    ):

        """DB Schema:
        CREATE TABLE characters (
            username VARCHAR NOT NULL PRIMARY KEY,
            character_name VARCHAR NOT NULL,
            character_json JSON,
            last_character_json JSON,
            date_created dt datetime default current_timestamp,
            date_modified dt datetime default current_timestamp
        );
        """
        # SQLite3 DB info
        # make_string_safe(input_text, lower=False, allow_hash=True, parenthesis=False, hyphen=False):
        db_name = self.make_string_safe(db_name, lower=True, allow_hash=False)
        table = self.make_string_safe(table, lower=True, allow_hash=False)
        username = self.make_string_safe(
            live_character["info"]["player_name"],
            lower=True,
            allow_hash=False,
            hyphen=True,
        )
        character_name = self.make_string_safe(
            live_character["info"]["safe_name"],
            lower=True,
            allow_hash=False,
            hyphen=True,
        )

        # Establish a connection to the DB
        logging.info("SQLite: connecting to db = " + db_name)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # get stored object from database

        logging.info(
            "SQLite: SELECT * FROM " + table + ' WHERE username = "' + username + '"'
        )
        sql = "SELECT * FROM " + table + " WHERE username = ?"
        cursor.execute(sql, [username])
        data = cursor.fetchall()
        data_count = len(data)
        logging.info(
            "SQLite: Fetched data is: " + str(data) + ", Length: " + str(data_count)
        )
        """
        if just_fetch:
            output = data
        else:
            if len(data) == 0:
                # if object does not exist, create it. Leave data set unaltered.
                logging.info('SQLite: "INSERT INTO ' + table + ' VALUES (' + str(username) + ', ' + str(rerollable_dice)
                             + ', ' + str(dl) + ', ' + str(successes) + ', ' + str(drama_result))
                sql = 'INSERT INTO ' + table + ' VALUES (?, ?, ?, ?, ?, 1, 1)'
                cursor.execute(sql, [username, rerollable_dice, dl, successes, drama_result])
                output = data
            else:

                # if stored object exists we need update it. Update returned data set
                logging.info('SQLite: UPDATE ' + table + ' SET rerollable_dice = ' + str(rerollable_dice) + ', dl = '
                             + str(dl) + ', successes = ' + str(successes) + ', drama_result = "' + str(drama_result)
                             + '", allow_one = ' + str(set_allow_one) + ', allow_two = ' + str(set_allow_two)
                             + ' WHERE username = "' + str(username) + '"')
                sql = 'UPDATE ' + table + ' SET rerollable_dice = ?, dl = ?, successes = ?, drama_result = ?, allow_one = ?, allow_two = ? WHERE username = ?'
                cursor.execute(sql, [rerollable_dice, dl, successes, drama_result, set_allow_one, set_allow_two, username])
                output = [username, rerollable_dice, dl, successes, drama_result, set_allow_one, set_allow_two]

        # close database connection
        conn.commit()
        conn.close()
        """
        # return output


class _UserSettings:
    """DON'T USE THIS CLASS! Use Broken_Shield_Companion, immediately below, because for some reason the user save
    file directory
    is named after the class name (in lower case)"""

    @staticmethod
    def get_user_data_dir():
        # save_dir = self.user_data_dir
        save_dir = "./save"
        return save_dir


# noinspection PyPep8Naming
class Broken_Shield_Companion(_UserSettings):
    """CALL THIS CLASS! Sets the correct name for the user save file directory"""

    pass
