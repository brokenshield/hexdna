# encoding: utf-8
__version__ = "2.1.50"
__author__ = "Gunnar Roxen <gunnar@brokenshield.net>"

from json import dump, load, loads
from character_dataclasses import (
    BSCMConfig,
    # NodeMap,
    # BaseModel,
    # PlayerModel,
    # CharacterModel,
    # LiveCharacterModel,
    # SpecialStats,
    # BreedTemplates,
)
import sqlite3
import logging
import os
from json import dumps
from textwrap import wrap

logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(filename='app.log', filemode='w', format='%(message)s')


class UtilityMethods:
    """The UtilityMethods class provides some general purpose utility methods used by CharacterMethods and
    DeleteMethods. CharacterMethods extends UtilityMethods."""

    def __init__(self, **kwargs):
        super(UtilityMethods, self).__init__(**kwargs)

        bscm = BSCMConfig()
        self.bscm = bscm
        self.pc_types = bscm.pc_types
        self.pc_tables = bscm.pc_tables
        self.valid_char_types = bscm.valid_char_types
        self.gamedata_db = bscm.gamedata_db
        self.chardata_db = bscm.chardata_db
        self.char_save_file_tail = bscm.char_save_file_tail
        self.live_char_save_file_tail = bscm.live_char_save_file_tail

        # Custom Colours for CLI Logging output
        colour = {
            "g": "\x1b[32m",
            "r": "\x1b[31m",
            "y": "\x1b[33m",
            "w": "\x1b[37m",
            "m": "\x1b[35m",
            "b": "\x1b[34m",
            "c": "\x1b[36m",
        }
        self.col = colour
        # Easier to add these here rather than repeating ad nauseam in the code!
        self.chk = f"{self.col['w']}[{self.col['g']}✓{self.col['w']}]"
        self.cross = f"{self.col['w']}[{self.col['r']}X{self.col['w']}]"
        self.info = f"{self.col['w']}[{self.col['m']}i{self.col['w']}]"
        self.test_text = (
            f"{self.col['y']}TEST:{self.col['w']}  "  # Extra spaces are for alignment
        )
        self.sql_txt = f"{self.col['b']}SQLite:{self.col['w']}"
        self.py_txt = f"{self.col['c']}Python:{self.col['w']}"
        self.util_txt = f"{self.col['y']}Utility:{self.col['w']}"
        self.err_txt = (
            f"{self.col['r']}ERROR:{self.col['w']} "  # Extra space for alignment
        )
        self.fail_txt = f"{self.col['r']}FAILED{self.col['w']}"
        #  All the spaces below are for formatting logging output:
        self.l_break = (
            f"\n{self.col['c']}    _____________________________________________________________________"
            f"{self.col['w']}\n          "
        )

        self.l_break_no_indent = (
            f"\n{self.col['c']}    _____________________________________________________________________"
            f"{self.col['w']}\n    "
        )
        # Indents available in multiple sizes!
        self.ind4 = self._indent(i=26)
        self.ind3 = self._indent(i=20)
        self.ind2 = self._indent(i=12)
        self.ind1 = self._indent(i=6)
        self.ind0 = self._indent(i=5)

        db_write_count = 0
        self.db_write_count = db_write_count
        db_cached_write_count = 0
        self.db_cached_write_count = db_cached_write_count
        db_read_count = 0
        self.db_read_count = db_read_count

        current_sql_write_query = ""
        self.current_sql_write_query = current_sql_write_query
        current_sql_data_tuple = ()
        self.current_sql_data_tuple = current_sql_data_tuple

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def db_fetch(
        self,
        db: str,
        db_path: str,
        fetch_sql: str,
        sql_data_tuple: tuple = (),
        allow_edit: bool = False,
        lower_case: bool = False,
    ) -> dict:
        """
        Requires db (string), db_path (string), fetch_sql (string); returns dict.
        This method performs a simple SELECT query on the specified database and returns it as a dict.
        For database protections will error out if any other type of SQL query is sent (such as INSERT or DELETE)
        and will return an empty dict.
        Available Options:
        db: name of DB
        db_path: string of DB path
        fetch_sql: SQL to be performed. Unless allow_edit = True this must be a SELECT query
        sql_data_tuple: arbitrary list of data to be included in SQL query
        allow_edit: prevents any queries except SELECT unless set to True
        """
        conn = sqlite3.connect(db_path + db)
        cursor = conn.cursor()
        logging.debug(
            f"{self.chk} {self.sql_txt} Connecting to "
            f"db:{self.col['y']}{db_path}{db}{self.col['w']}."
        )

        # Check this is a SELECT query only and not trying to spoof us
        if allow_edit:
            if len(sql_data_tuple) > 0:
                logging.debug(
                    f"{self.chk} {self.sql_txt} Executing "
                    f"{self.col['g']}INSERT or UPDATE{self.col['w']} query: "
                )
                logging.debug(
                    f"{self.col['g']}{fetch_sql} {sql_data_tuple}{self.col['w']}"
                )

                self.db_write_count += 1
                logging.info(
                    f"{self.chk} {self.sql_txt} {self.col['m']}!!!!! DB WRITE COUNT = "
                    f"{self.db_write_count} !!!!!{self.col['w']}\n"
                    f"{fetch_sql}"
                )
                self.current_sql_write_query = fetch_sql
                self.current_sql_data_tuple = sql_data_tuple
                cursor.execute(fetch_sql, sql_data_tuple)
            else:
                logging.info(
                    f"{self.chk} {self.sql_txt} Executing "
                    f"{self.col['g']}INSERT or UPDATE{self.col['w']} query: "
                    f"{self.col['g']}{fetch_sql} {self.col['w']}"
                )
                logging.info(
                    f"{self.chk} {self.sql_txt} {self.col['c']}!!!!! DB READ COUNT = "
                    f"{self.db_read_count} !!!!!{self.col['w']}"
                )

                self.db_write_count += 1
                logging.info(
                    f"{self.chk} {self.sql_txt} {self.col['m']}!!!!! DB WRITE COUNT = "
                    f"{self.db_write_count} !!!!!{self.col['w']}\n"
                    f"{fetch_sql}"
                )

                self.current_sql_write_query = fetch_sql
                cursor.execute(fetch_sql)

            select_data = cursor.fetchall()
            return_data = dict(select_data)

        else:
            if "SELECT" in fetch_sql:
                self.db_read_count += 1
                logging.debug(
                    f"{self.chk} {self.sql_txt} Executing {self.col['g']}SELECT{self.col['w']} "
                    f"query: "
                )
                logging.debug(f"{self.col['g']}{fetch_sql}{self.col['w']}")
                if lower_case:
                    fetch_sql = fetch_sql.replace("WHERE", "WHERE LOWER(")
                    fetch_sql = fetch_sql.replace("=", ")=")
                    # Really need to mke the search term lower case too with a regex...
                cursor.execute(fetch_sql)
                select_data = cursor.fetchall()
                data_count = len(select_data)
                logging.debug(
                    f"{self.chk} {self.sql_txt} {self.col['g']}DATABASE SELECT QUERY SUCCEEDED."
                    f"{self.col['w']} Good job!"
                )
                logging.info(
                    f"{self.chk} {self.sql_txt} Number of records found: "
                    f"{self.col['g']}{data_count}{self.col['w']}"
                )
                logging.info(
                    f"{self.chk} {self.sql_txt} {self.col['c']}!!!!! DB READ COUNT = "
                    f"{self.db_read_count} !!!!!{self.col['w']}"
                )
                return_data = select_data

            else:
                logging.error(
                    f"{self.cross} {self.err_txt} {self.col['r']}INCORRECT SQL QUERY SUBMITTED."
                    f"{self.col['w']}\n"
                    f"                      -> Only {self.col['g']}SELECT{self.col['w']}"
                    f" queries are accepted."
                )
                logging.error(
                    f"{self.cross} {self.err_txt} You submitted: "
                    f"{self.col['r']}{fetch_sql}{self.col['w']}.\n"
                    f"                      -> Please try again."
                )
                return_data = {0: 0}

        conn.commit()
        conn.close()
        logging.debug(f"{self.chk} {self.sql_txt} Connection closed.")

        return return_data

    def fetch_next_id(self, id_type: str = "player") -> int:
        """Requires id_type (string); returns int.
        We need to fetch the next available ID from the DB to use with the PlayerModel, CharacterModel or
        LiveCharacterModel dataclasses.
        Available Options:
        id_type = 'player', 'char', or 'live_char"""
        logging.info(f"{self.chk} {self.col['y']}[fetch_next_id]{self.col['w']}")

        logging.info(
            f"{self.chk} {self.sql_txt} Retrieving next available "
            f"{self.col['y']}'{id_type}'{self.col['w']}."
        )

        match id_type:
            case "player":
                logging.info(
                    f"{self.chk} {self.sql_txt} {self.col['g']}'player'{self.col['w']} "
                    f"selected."
                )
                fetch_sql = (
                    f"SELECT player_id FROM players ORDER BY player_id DESC LIMIT 1"
                )
            case "char":
                logging.info(
                    f"{self.chk} {self.sql_txt} {self.col['g']}'character'{self.col['w']} "
                    f"selected."
                )
                fetch_sql = (
                    f"SELECT char_id FROM characters ORDER BY char_id DESC LIMIT 1"
                )
            case "live_char":
                logging.info(
                    f"{self.chk} {self.sql_txt} {self.col['g']}'live_character'{self.col['w']} "
                    f"selected."
                )
                fetch_sql = f"SELECT live_char_id FROM live_characters ORDER BY live_char_id DESC LIMIT 1"
            case _:
                logging.warning(
                    f"{self.cross} {self.sql_txt} {self.err_txt} No id_type selected."
                )
                return False

        last_id = self.db_fetch(
            self.chardata_db["db"], self.chardata_db["db_path"], fetch_sql
        )

        if not last_id:
            next_id = 0
        else:
            last_id = int(last_id[0][0])
            next_id = last_id + 1

        return next_id

    def query_exists_in_db(
        self, query_id: int, query_table: str = "characters", id_label: str = "player"
    ) -> bool:
        """Requires query_id (int), query_table (string), id_label (string); returns bool.
        This method does a quick query to see if an id already exists in a certain table and DB.
        Available Options:
        query_table = 'gamedata', 'characters', 'players', or 'live_characters'
        id_label = 'gamedata', 'player', 'char', or 'live_char'"""
        logging.info(f"{self.chk} {self.col['y']}[query_exists_in_db]{self.col['w']}")

        logging.info(
            f"{self.chk} {self.sql_txt} Querying {self.col['y']}'{query_table}'{self.col['w']} "
            f"table to see if {id_label}_id:{self.col['y']}{query_id}{self.col['w']} "
            f"exists..."
        )

        if query_table == "gamedata":
            id_type = "mod_id"

            db = self.gamedata_db["db"]
            db_path = self.gamedata_db["db_path"]
        else:
            if id_label in self.pc_types:
                id_type = id_label + "_id"

                db = self.chardata_db["db"]
                db_path = self.chardata_db["db_path"]
            else:
                logging.error(
                    f"{self.cross} {self.err_txt} Database query failed. Please call query_exists_in_db "
                    f"method with correct query_id and either correct query_table"
                )
                return False

        logging.info(
            f"{self.chk} {self.sql_txt} Checking to see if '{id_type} = {query_id}' exists in '{query_table}' "
            f"table in '{db}' DB?"
        )

        # This is the variable SELECT SQL statement:
        fetch_sql = f"SELECT * FROM {query_table} WHERE {id_type}={query_id} LIMIT 1"
        query_return = self.db_fetch(
            db, db_path, fetch_sql
        )  # Returns dict if True, empty dict if False.

        if query_return:
            # We found a record with that ID number, so return True
            logging.info(
                f"{self.chk} {self.sql_txt} ID {query_id} {self.col['r']}DOES EXIST{self.col['w']}"
                f" in table '{query_table}'. It IS NOT available for use. Use the 'UPDATE' statement."
            )
            logging.debug(f"{self.chk} {self.sql_txt} Query returned: {query_return}")

            return True
        else:
            # We did not find a record with that ID number, so return False
            logging.info(
                f"{self.chk} {self.sql_txt} ID {query_id} "
                f"{self.col['g']}DOES NOT EXIST{self.col['w']}"
                f" in table '{query_table}'. It IS available for use. Use the 'INSERT' statement."
            )
            logging.debug(f"{self.chk} {self.sql_txt} Query returned: {query_return}")
            return False

    def insert_update_db(self, write_id: int, write_type: str = "player") -> bool:
        """Requires: write_id (int), write_type (string); returns bool.
        Here we check if we are INSERTING into the DB table or UPDATING the DB table
        Available Options:
        write_type = 'player','char','live_char'"""
        logging.info(f"{self.chk} {self.col['y']}[insert_update_db]{self.col['w']}")

        logging.info(
            f"{self.chk} {self.sql_txt} Querying whether we need to INSERT or UPDATE {write_type } ID {write_id}"
        )
        insert_update = False

        match write_type:
            case "player":
                check_player = self.query_exists_in_db(
                    write_id, query_table="players", id_label="player"
                )

                if not check_player:
                    insert_update = True
            case "char":
                check_character = self.query_exists_in_db(
                    write_id, query_table="characters", id_label="char"
                )

                if not check_character:
                    insert_update = True
            case "live_char":
                check_live_character = self.query_exists_in_db(
                    write_id, query_table="live_characters", id_label="live_char"
                )

                if not check_live_character:
                    insert_update = True
            case _:
                insert_update = False

        if insert_update:
            logging.info(
                f"{self.chk} {self.sql_txt} You must {self.col['g']}INSERT{self.col['w']} "
                f"as a {self.col['g']}NEW{self.col['w']} record."
            )
        else:
            logging.info(
                f"{self.chk} {self.sql_txt} You must {self.col['y']}UPDATE{self.col['w']}  an "
                f"{self.col['y']}EXISTING{self.col['w']} record."
            )

        return insert_update

    def string_safe(
        self,
        input_string: str,
        input_name: str = "text field",
        to_lower: bool = False,
        allow_hash: bool = False,
        parenthesis: bool = False,
        allow_hyphen: bool = False,
        allow_at: bool = False,
    ) -> str:
        """This helper method takes an unsafe string and replaces/deletes disallowed character and outputs a
        safe string.
        Available Options:
        input_text: incoming string to be made safe
        input_name: Purely for the logs, a name for the string
        to_lower: True/False set string to lower case
        allow_hash: True/False allow the # character
        parenthesis: True/False replace colons with parenthesis
        allow_hyphen: True/False allow the - character
        allow_at: True/False allow the @ character"""
        logging.info(
            f"{self.chk} {self.util_txt} Making "
            f"{self.col['y']}{input_name}{self.col['w']} string "
            f"{self.col['y']}'{input_string}'{self.col['w']} safe."
        )

        safe_string = str(input_string)
        if parenthesis:
            logging.info(f"{self.chk} {self.util_txt} replacing ':' with parenthesis")
            if ": " in safe_string:
                safe_string = safe_string.replace(": ", " (")
            elif ":_" in safe_string:
                safe_string = safe_string.replace(":_", "_(")

        if allow_hyphen:
            logging.info(
                f"{self.chk} {self.util_txt} '-' character "
                f"{self.col['g']}ALLOWED{self.col['w']} in {input_name}."
            )
            pass
        else:
            safe_string = safe_string.replace("-", "_")

        if "(" in safe_string:
            if ")" in safe_string:
                pass
            else:
                safe_string = safe_string + ")"

        replace_string = (
            ("?", ""),
            (" ", "_"),
            ("'", ""),
            ("!", ""),
            (",", ""),
            ("/", ""),
            (":", ""),
            ("__", ""),
            (";", ""),
        )
        funcs = [str.replace for x in replace_string]
        count = 0

        for x in funcs:
            safe_string = x(
                safe_string,
                str(replace_string[count][0]),
                str(replace_string[count][1]),
            )
            count += 1

        if allow_hash:
            logging.info(
                f"{self.chk} {self.util_txt} '#' character "
                f"{self.col['g']}ALLOWED{self.col['w']} in {input_name}."
            )
            pass
        else:
            safe_string = safe_string.replace("#", "")

        if allow_at:
            logging.info(
                f"{self.chk} {self.util_txt} '@' character "
                f"{self.col['g']}ALLOWED{self.col['w']} in {input_name}."
            )
            logging.info(
                f"{self.chk} {self.util_txt} '.' character "
                f"{self.col['g']}ALLOWED{self.col['w']} in {input_name}."
            )

            pass
        else:
            safe_string = safe_string.replace("@", "")
            safe_string = safe_string.replace(".", "")

        if to_lower:
            logging.info(f"{self.chk} {self.util_txt} String to lower case requested.")
            safe_string = safe_string.lower()

        logging.info(
            f"{self.chk} {self.util_txt} Cleaned/safe output string is: "
            f"{self.col['g']}'{safe_string}'{self.col['w']}"
        )

        return safe_string

    def string_pretty(
        self, input_text: str, input_name: str = "input string", title_case: bool = True
    ) -> str:
        """This is a helper method to prettify a safe string into title case and replace underscores with spaces.
        Available Options:
        input_text: incoming string to be made pretty
        input_name: Purely for the logs, a name for the string"""
        logging.info(
            f"{self.chk} {self.util_txt} Making "
            f"{self.col['y']}{input_name}{self.col['w']}string "
            f"'{self.col['y']}{input_text}'{self.col['w']} pretty."
        )
        input_text = str(input_text)
        input_text = input_text.replace("_", " ")

        if title_case:
            pretty_text = input_text.title()
        else:
            pretty_text = input_text

        logging.info(
            f"{self.chk} {self.util_txt} Output prettified string is: "
            f"'{self.col['y']}{pretty_text}{self.col['w']}'"
        )

        return pretty_text

    def string_wrap(
        self, input_string: str, width: int = 55, indent: int = 20, lvl: int = 1
    ) -> str:
        """Simple method for wrapping blocks of text"""

        dumped_text = dumps(input_string, ensure_ascii=False, indent=4)
        cleaned_text = dumped_text.replace('"', "").replace("\\n", "").replace("\\", "")
        ind = self._indent(i=indent)

        match lvl:
            case 3:
                shrink_ind = indent - lvl - 13
                lvl_ind = ind + self._indent(i=shrink_ind)
                width_mod = 6
            case 2:
                shrink_ind = indent - lvl - 3
                lvl_ind = ind + self._indent(i=shrink_ind)
                width_mod = 16
            case _:
                lvl_ind = ind + " "
                width_mod = 0

        total_width = width - width_mod
        text_list = wrap(cleaned_text, width=total_width)
        wrapped_text: str = ""

        for line in text_list:
            if not wrapped_text:
                wrapped_text = f"{line}"
            else:
                wrapped_text = f"{wrapped_text}\n{lvl_ind}{line}"

        return wrapped_text

    @staticmethod
    def convert_db_str_to_dict(db_str: str) -> dict:
        """Requires: str; returns JSON dict.
        Simple utility method for cleaning up returned strings that should be dicts from DB."""

        # JSON elements are required to be encased in double quotes and not single quotes
        double_quoted_str = str.replace(db_str, "'", '"')
        # It turns out you need to encase True and False in quotes
        # replace_true = str.replace(double_quoted_str, "True", '"True"')
        # replace_false = str.replace(replace_true, "False", '"False"')
        if "'" in double_quoted_str:
            logging.error(f"Single quote found!")
        output_dict = loads(double_quoted_str)

        return output_dict

    @staticmethod
    def _str_strip(input_str: str):
        output_str = (
            input_str.strip("[")
            .strip('"')
            .strip("]")
            .strip('"')
            .strip("'")
            .replace(" ", "")
            .replace('"', "")
            .replace("]", "")
        )
        return output_str

    @staticmethod
    def _indent(i: int = 20):
        ind: str = ""
        count: int = 0
        while count <= i:
            ind = f"{ind} "
            count += 1
        return ind

    @staticmethod
    def _strindent(input_str: str, i: int = 16):
        len_str = len(input_str) + 1
        corrected_ind = i - len_str
        ind: str = ""
        count: int = 0
        while count < corrected_ind:
            if ind:
                ind = f"{ind} "
            else:
                ind = f" "
            count += 1
        return ind

    @staticmethod
    def split_string_list_to_true_list(string_list: str = "") -> list:
        """Requires string_list (str); returns list.
        A simple method to convert lists returned as strings from a DB etc. back to true lists."""
        string_list = string_list.replace('"', "")
        true_list = string_list.strip("][").split(", ")
        return true_list

    def open_json(
        self,
        readfile: str,
        directory: str = "import",
        cli_print: bool = False,
    ) -> dict:
        """Static method to open a json file"""
        logging.debug(f"{self.chk} {self.util_txt} Action is: read from JSON file")
        # All the card data and user history data is stored in a JSON

        if directory == "import":
            save_path = f"./{self.bscm.load_dir}"
        else:
            save_path = f"./{directory}"

        data: dict = {}

        # This file is writeable to so need to check it out
        openfile = f"{readfile}.json"
        file_save_path = f"{save_path}/{openfile}"
        try:
            if os.path.isfile(file_save_path):
                # Check the file exists
                if os.stat(file_save_path).st_size != 0:
                    # Check the file is not 0 byte sized
                    with open(file_save_path, "r") as json_file:
                        data = load(json_file)
                        logging.info(
                            f"{self.chk} {self.util_txt} {self.col['g']}{file_save_path}{self.col['w']} was "
                            f"successfully read."
                        )
                        if cli_print:
                            print(
                                f"{self.chk} {self.col['g']}{file_save_path}{self.col['w']} was "
                                f"successfully read."
                            )
                else:
                    logging.debug(
                        f"{self.chk} {self.util_txt} {self.col['y']}{file_save_path}{self.col['w']} is empty, "
                        f"creating file..."
                    )
                    if cli_print:
                        print(
                            f"{self.chk} {self.col['y']}{file_save_path}{self.col['w']} is empty, "
                            f"creating file..."
                        )
                    data = self.write_json(data=data, writefile=readfile)
            else:
                logging.debug(
                    f"{self.chk} {self.util_txt} {self.col['y']}{file_save_path}{self.col['w']} "
                    f"is empty, creating file..."
                )
                data = self.write_json(data=data, writefile=readfile)
        except ValueError:
            # Uh-oh, something broke badly!
            logging.error(
                f"{self.chk} {self.util_txt} {self.err_txt }Exception: {self.col['r']}{file_save_path} "
                f"{self.col['w']} does not exist!"
            )
            if cli_print:
                print(
                    f"{self.cross} {self.col['w']}{file_save_path}{self.col['r']} is empty, "
                    f"creating file..."
                )
            data = self.write_json(data=data, writefile=readfile)

        return data

    def write_json(
        self,
        data: dict,
        writefile: str,
        mode: str = "w",
        directory: str = "export",
        cli_print: bool = False,
    ) -> dict:
        """Static method to safely write to the user's history json file"""
        logging.info(f"{self.chk} {self.util_txt} Action is: write to JSON file")

        # This method dumps the current info as a json
        mode = self.string_safe(mode, to_lower=True)

        match mode:
            case "w" | "a":
                if type(data) is dict:
                    if directory == "export":
                        save_path = f"./{self.bscm.save_dir}"
                    else:
                        directory = self.string_safe(
                            directory, parenthesis=True, allow_hyphen=True
                        )
                        save_path = f"./{directory}"

                    writefile = self.string_safe(
                        writefile, parenthesis=True, allow_hyphen=True
                    )
                    openfile = f"{writefile}.json"
                    file_save_path = f"{save_path}/{openfile}"

                    try:
                        with open(file_save_path, mode) as outfile:
                            dump(data, outfile, indent=4, default=str)
                            logging.info(
                                f"{self.chk} {self.util_txt} File:{self.col['g']}{save_path}/{writefile}.json"
                                f"{self.col['w']} was successfully saved."
                            )
                            if cli_print:
                                print(
                                    f"\n{self.chk} {self.col['g']}File:{self.col['w']}{save_path}/{writefile}.json"
                                    f"{self.col['g']} was successfully saved."
                                )
                    except ValueError:
                        logging.error(
                            f"{self.chk} {self.util_txt} {self.err_txt }Exception: "
                            f"{self.col['y']}{save_path}/{writefile}.json {self.col['r']}CANNOT be written!"
                            f"{self.col['w']}"
                        )
                    return data
                else:
                    logging.error(
                        f"{self.chk} {self.util_txt} {self.err_txt}Exception: "
                        f"{self.col['r']}data to be written must be in the form of a dictionary.{self.col['w']}"
                    )
                    return data
            case _:
                logging.error(
                    f"{self.chk} {self.util_txt} {self.err_txt}Exception: "
                    f"{self.col['r']}incorrect write mode specified, must be 'w' or 'a' be written.{self.col['w']}"
                )
                return data
