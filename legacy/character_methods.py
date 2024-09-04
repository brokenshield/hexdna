# encoding: utf-8
__version__ = "2.1.50"
__author__ = "Gunnar Roxen <gunnar@brokenshield.net>"

from character_dataclasses import (
    NodeMap,
    BaseModel,
    BSCMConfig,
    PlayerModel,
    CharacterModel,
    LiveCharacterModel,
    SpecialStats,
    BreedTemplates,
)
from datetime import datetime, timezone
from utility_methods import UtilityMethods
from json import dumps, loads
import textwrap
import logging

logging.basicConfig(level=logging.WARNING)


class CharacterMethods(UtilityMethods):
    """This is the class with the actions for adding, removing, calculating character values.
    Tests for all these methods are in test_character_methods.py which extends this class. CharacterMethods extends
    UtilityMethods and is extended by DeleteMethods"""

    def __init__(self, **kwargs):
        super(CharacterMethods, self).__init__(**kwargs)

        # Set pydantic dataclass models
        player = PlayerModel
        self.player = player

        char = CharacterModel
        self.char = char

        live_char = LiveCharacterModel
        self.live_char = live_char

        bscm = BSCMConfig()
        self.bscm = bscm
        tp_zero_mods = bscm.tp_no_change
        tp_bonus_mods = bscm.tp_bonus
        tp_cost_mods = bscm.tp_cost
        # All Mod types
        all_mod_types = set(tp_zero_mods + tp_bonus_mods + tp_cost_mods)

        valid_edge_types = bscm.valid_edge_types
        node_map_types = bscm.node_map_types

        nm = NodeMap()
        nm_dict = nm.dict()
        self.nm = nm
        self.nm_dict = nm_dict

        ss = SpecialStats()
        self.ss = ss

        # Set as class variables
        self.tp_zero_mods = tp_zero_mods
        self.tp_bonus_mods = tp_bonus_mods
        self.tp_cost_mods = tp_cost_mods
        self.all_mod_types = all_mod_types
        self.valid_edge_types = valid_edge_types
        self.node_map_types = node_map_types

        bt = BreedTemplates()
        self.bt = bt
        breeds_list = bt.breeds_list
        self.breeds_options = breeds_list

        self.lifestyle_mod_id = ""

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def create_new_player(
        self,
        player_name: str,
        player_real_name: str = "",
        player_email: str = "",
    ) -> PlayerModel:
        """START HERE! Use this method when creating a NEW PlayerModel and save it to the DB.
        Requires: player_name (str), player_real_name (str), player_email (str); returns PlayerModel"""
        logging.info(f"{self.chk} {self.col['y']}[create_new_player]{self.col['w']}")

        safe_player_name = self.string_safe(
            player_name,
            input_name="player_name",
            to_lower=False,
        )

        safe_player_real_name = self.string_safe(
            player_real_name,
            input_name="player_real_name",
            to_lower=False,
            allow_hyphen=True,
        )

        safe_player_email = self.string_safe(
            player_email,
            input_name="player_email",
            to_lower=True,
            allow_hash=True,
            allow_hyphen=True,
            allow_at=True,
        )

        logging.info(
            f"{self.chk} {self.sql_txt} Creating a {self.col['g']}NEW PLAYER{self.col['w']} "
            f"called '{self.col['g']}{safe_player_name}{self.col['w']}'."
        )

        player = self.new_or_update_player(
            player_name=safe_player_name,
            player_real_name=safe_player_real_name,
            player_email=safe_player_email,
            deleted=False,
            write_to_db=True,
        )

        self.player = player
        return player

    def create_new_char(
        self,
        char_name: str,
        player_id: int,
        char_archetype: str = "",
        char_type: str = "",
        breed: str = "",
        **mods_dict,
    ) -> CharacterModel:
        """START HERE! Use this method when creating a NEW CharacterModel a new LiveCharacterModel and save it to
        the DB.
        Requires: char_name (str), player_id (int), char_archetype (str), char_type (str), breed (str), **mods_dict
        (dict); returns CharacterModel.
        NOTE ON **mods_dict:
        This is a method to process a dictionary of mod_locations: mod_ids, for example:
        control_edge_n0= "e_brave" etc.
        This is especially useful when you need to quickly feed a set of mods into a CharacterModel.
        To set override or replacement text, submit the mod_id as:
        control_edge_n0= {"mod_id":"e_brave", "over":True, "text":"Fish Fingers"}
        NOTE: 'over' and 'text' fields both optional, just use the ones you need"""
        logging.warning(f"{self.chk} {self.col['y']}[create_new_char]{self.col['w']}")

        player_exists = self.pc_exists_by_id(int(player_id))
        if player_exists:
            safe_char_name = self.string_safe(
                char_name,
                input_name="char_name",
                to_lower=False,
                allow_hash=True,
                allow_hyphen=True,
            )

            if char_archetype:
                safe_title = self.string_safe(
                    char_archetype,
                    input_name="char_archetype",
                    to_lower=False,
                    allow_hash=True,
                    allow_hyphen=True,
                )
            else:
                safe_title = ""

            if char_type:
                safe_char_type_intermediate = self.string_safe(
                    char_type,
                    input_name="char_type",
                    to_lower=True,
                )
                if safe_char_type_intermediate in self.bscm.valid_char_types:
                    safe_char_type = char_type
                else:
                    safe_char_type = "character"
            else:
                safe_char_type = "character"

            if breed:
                safe_breed = self.string_safe(
                    breed,
                    input_name="breed",
                    to_lower=True,
                )

                # Apply Breed to Character
                if safe_breed in self.bt.breeds_list:
                    char_breed = safe_breed
                else:
                    char_breed = "human"
            else:
                char_breed = "human"

            logging.warning(
                f"{self.chk} {self.sql_txt} Creating a {self.col['g']}NEW {safe_char_type.upper()}{self.col['w']} "
                f"called '{self.col['g']}{safe_char_name}{self.col['w']}' of breed:'{self.col['g']}{char_breed}"
                f"{self.col['w']}'."
            )

            # Create Character (this also creates a LiveCharacterModel for the CharacterModel)
            char = self.new_or_update_char(
                char_name=safe_char_name,
                player_id=player_id,
                char_archetype=safe_title,
                char_type=safe_char_type,
                deleted=False,
                write_to_db=True,
            )

            # Apply Breed
            char = self.apply_breed_template_to_char(breed=char_breed, char=char)

            # Apply Multiple Mods to Char (**mods_dict)
            char = self.apply_multiple_mods_to_char(char=char, **mods_dict)

            # Save char to self.char
            self.char = char
            return char
        else:
            logging.error(
                f"{self.cross} {self.err_txt} {self.col['r']} Creating a new character FAILED{self.col['w']}"
            )

    def new_or_update_player(
        self,
        player_name: str,
        player_real_name: str,
        player_email: str,
        deleted: bool = False,
        player: PlayerModel = None,
        write_to_db: bool = True,
    ) -> PlayerModel:
        """Requires: player_name; Returns PlayerModel.
        Here we create a new player or update an existing player and save them in the db.
        Available Options:
        player_name: string
        player_real_name: string
        player_email: string
        deleted: bool
        """
        logging.info(f"{self.chk} {self.col['y']}[new_or_update_player]{self.col['w']}")

        if player:
            logging.info(
                f"{self.chk} {self.sql_txt} PlayerModel for "
                f"{self.col['g']}{player.player_name}{self.col['w']} already exists, "
                f"so {self.col['y']}UPDATING{self.col['w']} player save file."
            )
            safe_player_name = player.player_name
            safe_player_real_name = player.player_real_name
            safe_player_email = player.player_email
            next_player_id = player.player_id
            insert_update = False
        else:
            # Make sure all submitted strings from user are made safe
            safe_player_name = self.string_safe(
                player_name,
                input_name="player_name",
                to_lower=True,
            )

            safe_player_real_name = ""
            safe_player_email = ""

            if player_real_name:
                safe_player_real_name = self.string_safe(
                    player_real_name,
                    input_name="player_real_name",
                    allow_hash=True,
                    allow_hyphen=True,
                    allow_at=True,
                )
            if player_email:
                safe_player_email = self.string_safe(
                    player_email,
                    input_name="player_email",
                    to_lower=True,
                    allow_at=True,
                    allow_hyphen=True,
                )

            logging.info(
                f"{self.chk} {self.sql_txt} Creating a {self.col['g']}NEW{self.col['w']} player "
                f"or {self.col['y']}UPDATING{self.col['w']} an existing player "
                f"called {self.col['g']}'{safe_player_name}'{self.col['w']}."
            )

            # Does player already exist in DB?
            player_exists = self.pc_exists_by_name(
                safe_player_name, is_deleted=deleted, lower_case=True
            )

            # If player exists we don't want to assign them a new player_id, but just use an existing one
            # We don't want to make a new player record if the player already exists
            if player_exists:
                # Player exists so UPDATE
                next_player_id = int(player_exists[0][0])
                insert_update = False
                # If values are not supplied, use the existing values in the DB
                if not player_real_name:
                    safe_player_real_name = player_exists[0][2]
                if not player_email:
                    safe_player_email = player_exists[0][3]
            else:
                # Player doesn't exist so INSERT
                next_player_id = self.fetch_next_id("player")
                insert_update = self.insert_update_db(
                    write_id=next_player_id, write_type="player"
                )

            # Instantiate pydantic dataclass model for PlayerModel to save as json dump in DB
            player = PlayerModel(
                player_id=next_player_id,
                player_name=safe_player_name,
                player_real_name=safe_player_real_name,
                player_email=safe_player_email,
                deleted=deleted,
            )

        # We convert the PlayerModel into a JSON object for saving to the DB
        player_json = self._convert_model_to_dict(
            model=player, logging_name=safe_player_name
        )

        if write_to_db:
            if insert_update:
                # INSERT into table
                write_sql = (
                    f"INSERT INTO players (player_id, player_name, player_real_name, player_email, player_json, "
                    f"deleted) VALUES (?, ?, ?, ?, ?, ?)"
                )
                logging.info(
                    f"{self.chk} {self.sql_txt} Player doesn't exist, so "
                    f"{self.col['g']}INSERTING{self.col['w']} new DB entry for "
                    f"{self.col['g']}{safe_player_name}{self.col['w']}."
                )
                self.db_fetch(
                    self.chardata_db["db"],
                    self.chardata_db["db_path"],
                    write_sql,
                    sql_data_tuple=(
                        int(next_player_id),
                        safe_player_name,
                        safe_player_real_name,
                        safe_player_email,
                        str(player_json),
                        deleted,
                    ),
                    allow_edit=True,
                )

            else:
                # UPDATE table
                logging.info(
                    f"{self.chk} {self.sql_txt} Player {self.col['g']}{safe_player_name}"
                    f"{self.col['w']} already exists with "
                    f"{self.col['y']}player_id:{next_player_id}{self.col['w']} so "
                    f"{self.col['y']}UPDATING{self.col['w']} DB entry."
                )
                write_sql = (
                    f"UPDATE players SET player_real_name = ?, player_email = ?, player_json = ? "
                    f"WHERE player_id={next_player_id}"
                )

                self.db_fetch(
                    self.chardata_db["db"],
                    self.chardata_db["db_path"],
                    write_sql,
                    sql_data_tuple=(
                        safe_player_real_name,
                        safe_player_email,
                        str(player_json),
                    ),
                    allow_edit=True,
                )

        if self._pc_exists_feedback(safe_player_name, deleted, "player"):
            self.player = player
            return player

    def new_or_update_char(
        self,
        char_name: str,
        player_id: int,
        char_archetype: str = "",
        char_type: str = "character",
        deleted: bool = False,
        char: CharacterModel = None,
        write_to_db: bool = False,
        cli_print: bool = False,
        import_char: bool = False,
    ) -> CharacterModel:
        """Requires: char_name (str), player_id (str), char_archetype (str), char_type (str), deleted (bool),
        char (CharacterModel); returns CharacterModel.
        Here we create a new character or update an existing character and save them in the db.
        """
        logging.info(f"{self.chk} {self.col['y']}[new_or_update_char]{self.col['w']}")
        next_char_id: int
        player_id: int

        if cli_print:
            print(
                f"{self.l_break}"
                f"            {self.col['w']}CREATING/UPDATING CHARACTER!{self.col['w']}\n"
                f"{self.l_break}"
            )

        # Make sure all submitted strings from user are made safe
        if char and type(char) == CharacterModel:
            logging.info(
                f"{self.chk} {self.sql_txt} CharacterModel for "
                f"{self.col['g']}{char.char_name.title()}{self.col['w']} provided, "
                f"so {self.col['y']}UPDATING{self.col['w']} character save file."
            )
            if cli_print:
                print(
                    f"{self.chk} {self.col['y']}CharacterModel for "
                    f"{self.col['w']}{char.char_name.title()}{self.col['y']} provided. {self.col['w']}"
                )
            if import_char:
                next_char_id = self.fetch_next_id(id_type="char")
                safe_player_id = player_id
            else:
                next_char_id = char.char_id
            safe_char_name = char.char_name
            safe_char_archetype = char.char_archetype
            safe_char_type = char.char_type
            insert_update = False
            self.char = char
        else:
            safe_char_name = self.string_safe(
                char_name,
                input_name="char_name",
                to_lower=False,
                allow_hash=True,
                allow_hyphen=True,
            )
            logging.info(
                f"{self.chk} {self.sql_txt} CharacterModel for "
                f"{self.col['g']}{safe_char_name.title()}{self.col['w']} not provided, "
                f"so {self.col['y']}INSERTING or UPDATING{self.col['w']} character save file."
            )

            safe_char_archetype = ""
            safe_char_type = ""

            if char_archetype:
                safe_char_archetype = self.string_safe(
                    char_archetype,
                    input_name="char_archetype",
                    allow_hash=True,
                    allow_hyphen=True,
                    allow_at=True,
                )
            if char_type:
                safe_char_type_intermediate = self.string_safe(
                    char_type,
                    input_name="char_type",
                    to_lower=True,
                )
                if safe_char_type_intermediate in self.bscm.valid_char_types:
                    safe_char_type = safe_char_type_intermediate
                else:
                    safe_char_type = "character"

            # Search for player by player_id
            player_exists = self.pc_exists_by_id(int(player_id))
            if player_exists:
                safe_player_id = player_id
                logging.info(
                    f"{self.chk} {self.sql_txt} Creating a {self.col['g']}NEW{self.col['w']} "
                    f"character or {self.col['y']}UPDATING{self.col['w']} an existing character "
                    f"called '{safe_char_name}'."
                )
                # We want to search for character by char_id AND player_id
                char_exists = self.pc_exists_by_name(
                    search_name=safe_char_name,
                    is_deleted=deleted,
                    pc="char",
                    player_id=safe_player_id,
                    lower_case=True,
                )

                # If char exists we don't want to assign them a new char_id, but just use an existing one
                # We don't want to make a new char record if the char already exists
                if char_exists:
                    # Player exists so UPDATE
                    logging.info(
                        f"{self.chk} {self.sql_txt} {self.col['m']}CHARACTER EXISTS, UPDATING...{self.col['w']}"
                    )
                    if cli_print:
                        print(
                            f"{self.chk} {self.col['g']}UPDATING{self.col['y']} the CharacterModel for "
                            f"{self.col['w']}{safe_char_name}{self.col['y']}...{self.col['w']}"
                        )
                    next_char_id = int(char_exists[0][0])
                    insert_update = False
                    # If values are not supplied, use the existing values in the DB
                    if not char_archetype:
                        safe_char_archetype = char_exists[0][2]
                    if not char_type:
                        safe_char_type = char_exists[0][5]

                    # We retrieve the CharacterModel
                    char = self.load_char(char_id=next_char_id, feedback=True)

                    # Update/Add any missing nodes:
                    char = self._update_char_nodes(char=char)

                    modified_datetime: datetime = datetime.now()
                    setattr(char, "char_modified", f"{modified_datetime}")
                    self.char = char
                else:
                    # Player doesn't exist so INSERT
                    logging.info(
                        f"{self.chk} {self.sql_txt} {self.col['m']}CHARACTER DOESN'T EXIST, INSERTING...{self.col['w']}"
                    )
                    if cli_print:
                        print(
                            f"{self.chk} {self.col['g']}CREATING{self.col['y']} a new CharacterModel for "
                            f"{self.col['w']}{safe_char_name}{self.col['y']}...{self.col['w']}"
                        )

                    next_char_id = self.fetch_next_id(id_type="char")
                    insert_update = True

                    # Instantiate pydantic dataclass model for CharacterModel to save as json dump in DB
                    char = CharacterModel(
                        char_id=next_char_id,
                        char_name=safe_char_name,
                        char_archetype=safe_char_archetype,
                        player_id=safe_player_id,
                        char_type=safe_char_type,
                        deleted=deleted,
                    )

                    modified_datetime: datetime = datetime.now()
                    setattr(char, "char_created", f"{modified_datetime}")
                    setattr(char, "char_modified", f"{modified_datetime}")

                    self.char = char

            else:
                logging.error(
                    f"{self.cross} {self.err_txt} {self.col['r']} All player_ids must be integers.{self.col['w']}"
                )
                if cli_print:
                    print(
                        f"{self.cross} {self.err_txt} {self.col['r']} All player_ids must be integers.{self.col['w']}"
                    )
                return char

        if char:
            # We convert the CharacterModel into a JSON object for saving to the DB
            char_json = self._convert_model_to_dict(
                model=char, logging_name=safe_char_name
            )

            if import_char:
                insert_update = True

            if write_to_db:
                if insert_update:
                    # INSERT into table
                    write_sql = (
                        f"INSERT INTO characters (char_id, char_name, char_archetype, player_id, char_type, char_json, "
                        f"deleted) VALUES (?, ?, ?, ?, ?, ?, ?)"
                    )
                    logging.info(
                        f"{self.chk} {self.sql_txt} Character doesn't exist, so "
                        f"{self.col['g']}INSERTING{self.col['w']} new DB entry for "
                        f"{self.col['g']}{safe_char_name}{self.col['w']}."
                    )

                    self.db_fetch(
                        self.chardata_db["db"],
                        self.chardata_db["db_path"],
                        write_sql,
                        sql_data_tuple=(
                            int(next_char_id),
                            safe_char_name,
                            safe_char_archetype,
                            int(safe_player_id),
                            safe_char_type,
                            str(char_json),
                            deleted,
                        ),
                        allow_edit=True,
                    )

                    # Also make a new live_character profile for the new character
                    logging.info(
                        f"{self.chk} {self.sql_txt} Making LiveCharacter for "
                        f"{self.col['g']}{safe_char_name}{self.col['w']} with values: "
                        f"char_id={next_char_id}, player_id={safe_player_id}, deleted={deleted}"
                    )
                    if cli_print:
                        print(
                            f"{self.chk} {self.col['y']}Generating the Live Character play information from the "
                            f"{self.col['g']}NEW{self.col['y']} "
                            f"CharacterModel for {self.col['g']}{safe_char_name}{self.col['y']} with values: \n"
                            f"{self.ind0}{self.col['y']}-{self.col['g']} Character ID{self.col['y']} = "
                            f"{self.col['w']}{next_char_id}\n"
                            f"{self.ind0}{self.col['y']}-{self.col['g']} Player ID{self.col['y']} = "
                            f"{self.col['w']}{safe_player_id}\n"
                        )

                    live_char = self.new_or_update_live_char(
                        char_id=next_char_id, player_id=safe_player_id, deleted=deleted
                    )

                    modified_datetime: datetime = datetime.now()
                    setattr(live_char, "char_created", f"{modified_datetime}")
                    setattr(live_char, "char_modified", f"{modified_datetime}")
                else:
                    # UPDATE table
                    logging.info(
                        f"{self.chk} {self.sql_txt} Character {self.col['g']}{safe_char_name}"
                        f"{self.col['w']} already exists with "
                        f"{self.col['y']}char_id:{next_char_id}{self.col['w']} so "
                        f"{self.col['y']}UPDATING{self.col['w']} DB entry."
                    )
                    if cli_print:
                        print(
                            f"{self.chk} {self.col['y']}Regenerating the Live Character play information from the "
                            f"{self.col['g']}EXISTING{self.col['y']} "
                            f"CharacterModel for {self.col['g']}{safe_char_name}{self.col['y']} with values: \n"
                            f"{self.ind0}{self.col['y']}-{self.col['g']}Character ID{self.col['y']} = "
                            f"{self.col['w']}{next_char_id}\n"
                            f"{self.ind0}{self.col['y']}-{self.col['g']}Player ID{self.col['y']} = "
                            f"{self.col['w']}{safe_player_id}\n"
                        )
                    write_sql = (
                        f"UPDATE characters SET char_name = ?, char_archetype = ?, char_type = ?, char_json = ? "
                        f"WHERE char_id={next_char_id}"
                    )

                    self.db_fetch(
                        self.chardata_db["db"],
                        self.chardata_db["db_path"],
                        write_sql,
                        sql_data_tuple=(
                            safe_char_name,
                            safe_char_archetype,
                            safe_char_type,
                            str(char_json),
                        ),
                        allow_edit=True,
                    )

                    live_char = self.load_live_character(
                        char_id=next_char_id, feedback=True
                    )
                    modified_datetime: datetime = datetime.now()
                    setattr(char, "char_modified", f"{modified_datetime}")

                # Save live_char to self.live_char
                self.live_char = live_char

            # Process basic character model stuff:
            char = self.process_char(char=char)

            if cli_print:
                print(
                    f"{self.chk} {self.col['y']}Core character file for {self.col['w']}{char.char_name.title()} "
                    f"{self.col['g']}SUCCESSFULLY{self.col['y']} processed! Good job! \n{self.col['w']}"
                )

            self.char = char
            return char

    def new_or_update_live_char(
        self,
        char_id: int,
        player_id: int,
        deleted: bool = False,
        live_char: LiveCharacterModel = None,
        write_to_db: bool = True,
    ) -> LiveCharacterModel:
        """Requires: char_id; Returns LiveCharacterModel.
        Here we create a new character or updating an existing character and save them in the db.
        """
        logging.info(
            f"{self.chk} {self.col['y']}[new_or_update_live_char]{self.col['w']}"
        )
        insert_update: bool = True
        next_live_char_id: int = -1

        # LiveCharacterModel supplied
        if live_char and type(live_char) == LiveCharacterModel:
            logging.info(
                f"{self.chk} {self.sql_txt} LiveCharacterModel for "
                f"{self.col['g']}{live_char.char_name}{self.col['w']} supplied so, "
                f"so {self.col['y']}UPDATING{self.col['w']} character save file."
            )
            safe_char_name = live_char.char_name
            next_live_char_id = live_char.char_id
            player_id = live_char.player_id
            insert_update = False

        else:
            # Use the existing character information to discover the character's name and player_id
            char_exists = self.pc_exists_by_id(char_id, is_deleted=False, pc="char")
            safe_char_name = char_exists[0][1]

            # Do a quick check that the player exists as we need both character and player to exist
            player_check = self.pc_exists_by_id(
                player_id, is_deleted=False, pc="player"
            )
            if player_check:
                player_name = player_check[0][1]
                if char_exists:
                    logging.info(
                        f"{self.chk} {self.sql_txt} Creating a {self.col['g']}NEW{self.col['w']} "
                        f"live_character or {self.col['y']}UPDATING{self.col['w']} an "
                        f"existing live_character for the character called '{safe_char_name}'."
                    )

                    # We have to search the live_Characters table by char_id to see if a live_character already exists
                    # This is a more complicated search as each player could potentially have the same character
                    live_char_sql = f"SELECT * FROM live_characters WHERE char_id={char_id} AND player_id={player_id}"
                    live_char_exists = self.db_fetch(
                        self.chardata_db["db"],
                        self.chardata_db["db_path"],
                        live_char_sql,
                    )

                    if live_char_exists:
                        # If live_char exists we don't want to assign them a new live_char_id, but just use an
                        # existing one
                        # We don't want to make a new live_char record if the char already exists
                        # live_character exists so UPDATE
                        logging.info(
                            f"{self.chk} {self.sql_txt}LIVE CHARACTER EXISTS, UPDATING...{self.col['w']}"
                        )

                        next_live_char_id = int(live_char_exists[0][0])
                        insert_update = False
                        # We retrieve the CharacterModel
                        live_char = self.load_live_character(
                            char_id=next_live_char_id, feedback=True
                        )
                    else:
                        # live_character doesn't exist so INSERT
                        logging.info(
                            f"{self.chk} {self.sql_txt}LIVE CHARACTER DOESN'T EXIST, INSERTING...{self.col['w']}"
                        )

                        next_live_char_id = self.fetch_next_id("live_char")
                        insert_update = self.insert_update_db(
                            write_id=next_live_char_id, write_type="live_char"
                        )

                        # Instantiate pydantic dataclass model for LiveCharacterModel to save as json dump in DB
                        live_char = LiveCharacterModel(
                            live_char_id=next_live_char_id,
                            char_id=char_id,
                            char_name=safe_char_name,
                            player_id=player_id,
                            player_name=player_name,
                            deleted=deleted,
                        )
                else:
                    logging.error(
                        f"{self.cross} {self.err_txt} {self.col['r']} All live_characters "
                        f"must be assigned to an existing char_id.{self.col['w']}"
                    )
            else:
                logging.error(
                    f"{self.cross} {self.err_txt} {self.col['r']} All Live_characters "
                    f"must be assigned to an existing player_id.{self.col['w']}"
                )
        # We convert the LiveCharacterModel into a JSON object for saving to the DB
        char_json = self._convert_model_to_dict(
            model=live_char, logging_name="live_character"
        )

        if write_to_db and next_live_char_id > -1:
            if insert_update:
                # INSERT into table
                write_sql = (
                    f"INSERT INTO live_characters (live_char_id, char_id, player_id, char_name, live_char_json, "
                    f"deleted) VALUES (?, ?, ?, ?, ?, ?)"
                )
                logging.info(
                    f"{self.chk} {self.sql_txt} Live_Character doesn't exist, so "
                    f"{self.col['g']}INSERTING{self.col['w']} new DB entry for "
                    f"{self.col['g']}{safe_char_name}{self.col['w']}."
                )
                self.db_fetch(
                    self.chardata_db["db"],
                    self.chardata_db["db_path"],
                    write_sql,
                    sql_data_tuple=(
                        int(next_live_char_id),
                        int(char_id),
                        int(player_id),
                        safe_char_name,
                        str(char_json),
                        deleted,
                    ),
                    allow_edit=True,
                )

            else:
                # UPDATE table
                # Housekeeping - working out all the derived stuff, sliverware, languages, initiative, WTs, AVs,
                # skill min
                live_char = self.housekeeping(live_char=live_char)

                logging.info(
                    f"{self.chk} {self.sql_txt} Live_Character {self.col['g']}{safe_char_name}"
                    f"{self.col['w']} already exists with "
                    f"{self.col['y']}live_char_id:{next_live_char_id}{self.col['w']} so "
                    f"{self.col['y']}UPDATING{self.col['w']} DB entry."
                )
                write_sql = (
                    f"UPDATE live_characters SET char_id = ?, char_name = ?, live_char_json = ? "
                    f"WHERE live_char_id={next_live_char_id}"
                )

                self.db_fetch(
                    self.chardata_db["db"],
                    self.chardata_db["db_path"],
                    write_sql,
                    sql_data_tuple=(
                        char_id,
                        safe_char_name,
                        str(char_json),
                    ),
                    allow_edit=True,
                )

        if self._pc_exists_feedback(safe_char_name, deleted, "live_char"):
            self.live_char = live_char
        return live_char

    def save_player(
        self, player: PlayerModel = None, write_to_db: bool = True
    ) -> PlayerModel:
        """Requires: player (PlayerModel); returns PlayerModel.
        This is a simpler front end for new_or_update_live_char and ONLY requires PlayerModel."""
        logging.info(f"{self.chk} {self.col['y']}[save_player]{self.col['w']}")

        logging.info(f"{self.chk} {self.py_txt} Saving PlayerModel to DB...")
        if not player:
            player = self.player

        self.new_or_update_player(
            player_name=player.player_name,
            player_real_name=player.player_real_name,
            player_email=player.player_email,
            deleted=player.deleted,
            player=player,
            write_to_db=write_to_db,
        )

        return player

    def save_char(
        self, char: CharacterModel = None, write_to_db: bool = True
    ) -> CharacterModel:
        """Requires: char (CharacterModel); returns CharacterModel.
        This is a simpler front end for new_or_update_char and ONLY requires CharacterModel.
        """
        logging.info(f"{self.chk} {self.col['y']}[save_char]{self.col['w']}")

        logging.info(f"{self.chk} {self.py_txt} Saving CharacterModel to DB...")
        if not char:
            char = self.char

        self.new_or_update_char(
            char_name=char.char_name,
            player_id=char.player_id,
            char_archetype=char.char_archetype,
            char_type=char.char_type,
            deleted=char.deleted,
            char=char,
            write_to_db=write_to_db,
        )

        return char

    def save_live_char(
        self, live_char: LiveCharacterModel = None, write_to_db: bool = True
    ) -> LiveCharacterModel:
        """Requires: live_char (LiveCharacterModel); returns LiveCharacterModel.
        This is a simpler front end for new_or_update_live_char and ONLY requires LiveCharacterModel."""
        logging.info(f"{self.chk} {self.col['y']}[save_live_char]{self.col['w']}")

        logging.info(f"{self.chk} {self.py_txt} Saving LiveCharacterModel to DB...")
        if not live_char:
            live_char = self.live_char

        self.new_or_update_live_char(
            char_id=live_char.char_id,
            player_id=live_char.player_id,
            deleted=live_char.deleted,
            live_char=live_char,
            write_to_db=write_to_db,
        )

        return live_char

    def save_complete_character(
        self, char: CharacterModel = None, live_char: LiveCharacterModel = None
    ) -> None:
        """Method for saving complete character (CharacterModel and LiveCharacterModel) to DB."""
        logging.info(f"{self.chk} {self.col['y']}[save_character]{self.col['w']}")

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['g']}SAVING ENTIRE CHARACTER "
            f"(CharacterModel AND LiveCharacterModel) TO DB...{self.col['w']}"
        )
        if not char:
            char = self.char
        if not live_char:
            live_char = self.live_char

        char = self.save_char(char=char, write_to_db=True)
        live_char = self.save_live_char(live_char=live_char, write_to_db=True)

        self.char = char
        self.live_char = live_char

    def load_player(self, player_id: int, feedback: bool = True) -> PlayerModel:
        """Requires: player_id; returns PlayerModel.
        Here we retrieve the player information from the DB and load it dynamically into the PlayerModel."""
        logging.info(f"{self.chk} {self.col['y']}[load_player]{self.col['w']}")

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['g']}Retrieving player with player_id:{player_id} "
            f"from DB...{self.col['w']}"
        )

        player_exists = self.pc_exists_by_id(search_id=player_id, pc="player")

        if player_exists:
            retrieve_sql = f"SELECT * FROM players WHERE player_id={player_id}"
            player_retrieve = self.db_fetch(
                self.chardata_db["db"], self.chardata_db["db_path"], retrieve_sql
            )
            player_dict = self.convert_db_str_to_dict(player_retrieve[0][4])

            # Load returned dict dynamically into PlayerModel
            player = PlayerModel.parse_obj(player_dict)

            logging.info(
                f"{self.chk} {self.py_txt} Player "
                f"{self.col['g']}SUCCESSFULLY{self.col['w']} retrieved from DB:"
            )
            if feedback:
                logging.info(
                    f"{self.chk} {self.py_txt} {self.col['c']}>>>>> PLAYER DUMP:\n"
                    f"{dumps(player_dict, indent=4, default=str)}{self.col['w']}"
                )

            self.player = player
            return player
        else:
            logging.info(
                f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} "
                f"Player with player_id:{player_id} not found in DB.{self.col['w']}"
            )

    def load_player_by_name(
        self, player_name: str, feedback: bool = True
    ) -> PlayerModel:
        """Requires: player_name; returns PlayerModel.
        Here we retrieve the player information from the DB and load it dynamically into the PlayerModel."""
        logging.info(f"{self.chk} {self.col['y']}[load_player_by_name]{self.col['w']}")

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['g']}Retrieving player with player_name:{player_name} "
            f"from DB...{self.col['w']}"
        )

        player_exists = self.pc_exists_by_name(search_name=player_name, pc="player")

        if player_exists:
            retrieve_sql = f"SELECT * FROM players WHERE player_name='{player_name}'"
            player_retrieve = self.db_fetch(
                self.chardata_db["db"], self.chardata_db["db_path"], retrieve_sql
            )
            player_dict = self.convert_db_str_to_dict(player_retrieve[0][4])

            # Load returned dict dynamically into PlayerModel
            player = PlayerModel.parse_obj(player_dict)

            logging.info(
                f"{self.chk} {self.py_txt} Player "
                f"{self.col['g']}SUCCESSFULLY{self.col['w']} retrieved from DB:"
            )
            if feedback:
                logging.info(
                    f"{self.chk} {self.py_txt} {self.col['c']}>>>>> PLAYER DUMP:\n"
                    f"{dumps(player_dict, indent=4, default=str)}{self.col['w']}"
                )

            self.player = player
            return player
        else:
            logging.info(
                f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} "
                f"Player with player_name:{player_name} not found in DB.{self.col['w']}"
            )

    def load_complete_character(self, char_id: int) -> tuple:
        """This method loads the COMPLETE character, both the CharacterModel, the LiveCharacterModel and the
        PlayerModel and loads all three into their class variables.
        Returns a tuple of CharacterModel, LiveCharacterModel"""
        logging.info(
            f"{self.chk} {self.col['y']}[load_complete_character]{self.col['w']}"
        )

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['g']}Retrieving {self.col['g']}COMPLETE{self.col['g']} character "
            f"with char_id:{self.col['g']}{char_id}{self.col['w']} "
            f"(CharacterModel and LiveCharacterModel) from DB...{self.col['w']}"
        )

        char = self.load_char(char_id=char_id)
        live_char = self.load_live_character(char_id=char_id)
        player = self.load_player(player_id=char.player_id)

        self.char = char
        self.live_char = live_char
        self.player = player

        return char, live_char

    def export_character(
        self, char_id: int, cli_print: bool = False, export_dir: str = "export"
    ) -> None:
        """This method exports a character and live_character json save file by loading both from the DB."""
        logging.info(f"{self.chk} {self.col['y']}[export_character]{self.col['w']}")

        char_lc = self.load_complete_character(char_id=char_id)
        char = char_lc[0].dict()
        live_char = char_lc[1].dict()

        filename = f"{char['char_name'].lower()}{self.char_save_file_tail}"
        filename2 = f"{char['char_name'].lower()}{self.live_char_save_file_tail}"
        directory = export_dir

        logging.info(
            f"{self.chk} {self.py_txt} Exporting JSON save file for character:"
            f"{self.col['g']}{char['char_name']}{self.col['w']} as "
            f"{self.col['y']}'{filename}.json'{self.col['w']} and "
            f"{self.col['y']}'{filename2}.json'{self.col['w']} to the "
            f"directory {self.col['y']}'./{directory}'{self.col['w']}"
        )

        if cli_print:
            print(
                f"\n{self.chk} {self.col['g']}Exporting JSON save file for character:"
                f"{self.col['w']}{char['char_name']}{self.col['g']} as "
                f"{self.col['w']}'{filename}.json'{self.col['g']} and "
                f"{self.col['w']}'{filename2}.json'{self.col['g']} to the "
                f"directory {self.col['y']}'./{directory}'{self.col['w']}"
            )

        self.write_json(
            data=char, writefile=filename, directory=directory, cli_print=True
        )
        self.write_json(
            data=live_char, writefile=filename2, directory=directory, cli_print=True
        )

    def _check_mod_fail(self, nodes_dict: dict, cli_print: bool = False) -> list:
        """Requires: nodes_dict (dict), cli_print (bool); returns list.
        This method quickly checks a dict of mod_ids in nodes and returns a list of all the mod_ids that DON'T
        EXIST."""
        logging.info(f"{self.chk} {self.col['y']}[_check_mod_fail]{self.col['w']}")
        # We need to check all the mod_ids are valid and exist and throw an error if they don't
        failed_mods: list = []
        for node in nodes_dict:
            if nodes_dict[node]:
                check = self.check_mod_exists(mod_id=nodes_dict[node])
                if not check:
                    if cli_print:
                        print(
                            f"\n{self.cross} {self.col['r']}ERROR: Mod ID:{self.col['w']}{nodes_dict[node]}"
                            f"{self.col['r']} DOESN'T EXIST!"
                        )
                    failed_mods.append(nodes_dict[node])

        return failed_mods

    def import_character(
        self,
        char_id: int,
        char_name: str,
        cli_print: bool = False,
        import_dir: str = "export",
    ) -> CharacterModel:
        """This method imports a character from a save file and either updates an existing character or
        adds a new character to the DB."""
        logging.info(f"{self.chk} {self.col['y']}[Import_character]{self.col['w']}")

        filename = f"{char_name.lower()}{self.char_save_file_tail}"
        directory = import_dir

        logging.info(
            f"{self.chk} {self.py_txt} Importing JSON save file for character:"
            f"{self.col['g']}{char_name}{self.col['w']} as "
            f"{self.col['y']}'{filename}.json'{self.col['w']} from the "
            f"directory {self.col['y']}'./{directory}'{self.col['w']}"
        )
        if cli_print:
            print(
                f"{self.chk} Importing JSON save file for character:"
                f"{self.col['g']}{char_name}{self.col['w']} as "
                f"{self.col['y']}'{filename}.json'{self.col['w']} from the "
                f"directory {self.col['y']}'./{directory}'{self.col['w']}"
            )

        # Load file into a dictionary
        char_dict = self.open_json(readfile=filename, directory=directory)

        # We need to check all the mod_ids are valid and exist and throw an error if they don't
        nodes_dict = char_dict["nodes"]

        failed_mods = self._check_mod_fail(nodes_dict=nodes_dict, cli_print=cli_print)

        if not failed_mods:
            logging.info(
                f"\n{self.chk} {self.col['y']}All mods in the import file are {self.col['g']}VALID{self.col['y']}"
                f". Proceeding...{self.col['w']} "
            )
            if cli_print:
                print(
                    f"\n{self.chk} {self.col['y']}All mods in the import file are {self.col['g']}VALID{self.col['y']}"
                    f". Proceeding...{self.col['w']} "
                )
            # Pass that dictionary as **kwargs to the CharacterModel
            char = CharacterModel(**char_dict)

            # Check player_id exists
            player_check: dict = self.pc_exists_by_id(
                search_id=char.player_id, pc="player"
            )

            if cli_print:
                print(
                    f"\n{self.col['y']}Player Information =\n"
                    f"{player_check}{self.col['w']}"
                )
            existing_player_id: int = player_check[0][0]
            character_check: dict = self.pc_exists_by_id(
                search_id=char.char_id, pc="char"
            )

            if player_check:
                if existing_player_id == char.player_id:
                    if character_check:
                        logging.info(
                            f"{self.chk} {self.py_txt} Player AND Character {self.col['g']}EXIST{self.col['w']} so "
                            f"updating character in DB."
                        )
                        if cli_print:
                            print(
                                f"{self.chk} Player AND Character {self.col['g']}EXIST{self.col['w']} so "
                                f"updating character in DB."
                            )
                    else:
                        logging.info(
                            f"{self.chk} {self.py_txt} Player ONLY {self.col['g']}EXISTS{self.col['w']} so ADDING "
                            f"character to DB."
                        )
                        if cli_print:
                            print(
                                f"{self.chk} Player ONLY {self.col['g']}EXISTS{self.col['w']} so ADDING "
                                f"character to DB."
                            )

                    # Update the saves character in the DB or add a new character
                    char = self.new_or_update_char(
                        char_name=char.char_name,
                        player_id=char.player_id,
                        char_archetype=char.char_archetype,
                        char_type=char.char_type,
                        char=char,
                        write_to_db=True,
                        import_char=True,
                    )

                    # Save char to self.char
                    self.char = char
                else:
                    logging.error(
                        f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} "
                        f"Current player_id:{self.player.player_id} is NOT the same as the loaded "
                        f"player_id:{char.player_id} not found in DB{self.col['w']}. Do you need to make a new player?"
                    )
                    self.list_pc(cli_print=True)
            else:
                logging.error(
                    f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} "
                    f"Player with player_id:{char.player_id} not found in DB.{self.col['w']}. Do you need to make a new"
                    f"player?"
                )
                self.list_pc(cli_print=True)

            return char

        else:
            logging.error(
                f"\n{self.cross} {self.sql_txt} {self.col['r']} ERROR: One mods in the import file are "
                f"{self.col['g']}INVALID{self.col['r']}. The failed Mod_IDs were: \n"
                f"{self.col['w']}{failed_mods}{self.col['r']} "
                f"\nPlease check the save file and "
                f"try again...{self.col['w']} "
            )
            if cli_print:
                print(
                    f"\n{self.cross} {self.col['r']} ERROR: One mods in the import file are {self.col['g']}INVALID"
                    f"{self.col['r']}. The failed Mod_IDs were: \n"
                    f"{self.col['w']}{failed_mods}{self.col['r']} "
                    f"\nPlease check the save file and "
                    f"try again...{self.col['w']} "
                )

    def load_char(self, char_id: int, feedback: bool = True) -> CharacterModel:
        """Requires: char_id; returns CharacterModel.
        Here we retrieve the character information from the DB and load it dynamically into the CharacterModel."""
        logging.info(f"{self.chk} {self.col['y']}[load_character]{self.col['w']}")

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['g']}Retrieving {self.col['g']}CharacterModel{self.col['w']} with "
            f"char_id:{self.col['g']}{char_id}{self.col['w']} from DB...{self.col['w']}"
        )

        char_exists = self.pc_exists_by_id(search_id=char_id, pc="char")

        if char_exists:
            retrieve_sql = f"SELECT * FROM characters WHERE char_id={char_id}"
            char_retrieve = self.db_fetch(
                self.chardata_db["db"], self.chardata_db["db_path"], retrieve_sql
            )
            char_dict = self.convert_db_str_to_dict(char_retrieve[0][5])

            # Load returned dict dynamically into CharacterModel
            char = CharacterModel.parse_obj(char_dict)

            logging.info(
                f"{self.chk} {self.py_txt} Character "
                f"{self.col['g']}SUCCESSFULLY{self.col['w']} retrieved from DB:"
            )
            if feedback:
                logging.info(
                    f"{self.chk} {self.py_txt} {self.col['y']}>>>>> CHARACTER DUMP:\n"
                    f"{dumps(char_dict, indent=4, default=str)}"
                    f"{self.col['w']}"
                )

            # Update/Add any missing nodes:
            char = self._update_char_nodes(char=char)

            self.char = char
            return char
        else:
            logging.error(
                f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} "
                f"Character with char_id:{char_id} not found in DB.{self.col['w']}"
            )

    def load_char_by_name(
        self, char_name: str, feedback: bool = True
    ) -> CharacterModel:
        """Requires: char_id; returns CharacterModel.
        Here we retrieve the character information from the DB and load it dynamically into the CharacterModel."""
        logging.info(
            f"{self.chk} {self.col['y']}[load_character_by_name]{self.col['w']}"
        )

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['g']}Retrieving {self.col['g']}CharacterModel{self.col['w']} with "
            f"char_name:{self.col['g']}{char_name}{self.col['w']} from DB...{self.col['w']}"
        )

        char_exists = self.pc_exists_by_name(search_name=char_name, pc="char")

        if char_exists:
            retrieve_sql = f"SELECT * FROM characters WHERE char_name='{char_name}'"
            char_retrieve = self.db_fetch(
                self.chardata_db["db"], self.chardata_db["db_path"], retrieve_sql
            )
            char_dict = self.convert_db_str_to_dict(char_retrieve[0][5])

            # Load returned dict dynamically into CharacterModel
            char = CharacterModel.parse_obj(char_dict)

            logging.info(
                f"{self.chk} {self.py_txt} Character "
                f"{self.col['g']}SUCCESSFULLY{self.col['w']} retrieved from DB:"
            )
            if feedback:
                logging.info(
                    f"{self.chk} {self.py_txt} {self.col['y']}>>>>> CHARACTER DUMP:\n"
                    f"{dumps(char_dict, indent=4, default=str)}"
                    f"{self.col['w']}"
                )

            # Update/Add any missing nodes:
            char = self._update_char_nodes(char=char)

            self.char = char
            return char
        else:
            logging.error(
                f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} "
                f"Character with char_name:{char_name} not found in DB.{self.col['w']}"
            )

    def load_live_character(
        self, char_id: int, feedback: bool = True
    ) -> LiveCharacterModel:
        """Requires: char_id; returns LiveCharacterModel.
        Here we retrieve the live_character information from the DB and load it dynamically into the
        LiveCharacterModel."""
        logging.info(f"{self.chk} {self.col['y']}[load_live_character]{self.col['w']}")

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['g']}Retrieving {self.col['g']}LiveCharacterModel{self.col['w']} with "
            f"char_id:{self.col['g']}{char_id}{self.col['w']} from DB...{self.col['w']}"
        )

        char_exists = self.pc_exists_by_id(search_id=char_id, pc="char")

        if char_exists:
            lc = self.pc_exists_by_id(char_id, pc="live_char", lc=True)
            lc_id = lc[0][0]
            logging.debug(f"{self.chk} {self.sql_txt} live_char_id:{lc_id}")
            retrieve_sql = f"SELECT * FROM live_characters WHERE live_char_id={lc_id}"
            live_char_retrieve = self.db_fetch(
                self.chardata_db["db"], self.chardata_db["db_path"], retrieve_sql
            )
            live_char_dict = self.convert_db_str_to_dict(live_char_retrieve[0][4])

            # Load returned dict dynamically into LiveCharacterModel
            live_char = LiveCharacterModel.parse_obj(live_char_dict)

            logging.info(
                f"{self.chk} {self.py_txt} {self.col['g']}Live_Character information "
                f"SUCCESSFULLY{self.col['w']} retrieved from DB:"
            )

            if feedback:
                logging.info(
                    f"{self.chk} {self.py_txt} {self.col['g']}>>>>> LIVE_CHARACTER DUMP:\n"
                    f"{dumps(live_char_dict, indent=4, default=str)}{self.col['w']}"
                )

            self.live_char = live_char
            return live_char
        else:
            logging.error(
                f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} "
                f"Character with char_id:{char_id} not found in DB.{self.col['w']}"
            )

    def print_player_model(self, player: PlayerModel = None) -> None:
        """Requires: player (PlayerModel); returns nothing.
        Prints the current PlayerModel in memory."""
        logging.info(f"{self.chk} {self.col['y']}[print_player_model]{self.col['w']}")

        if not player:
            player = self.player

        player_dict = player.dict()
        print(
            f"{self.chk} {self.py_txt} Current {self.col['m']}PlayerModel{self.col['w']}:"
            f" \n{self.col['m']}{dumps(player_dict, indent=4, default=str)}{self.col['w']}"
        )

    def print_complete_character(
        self, char: CharacterModel = None, live_char: LiveCharacterModel = None
    ) -> None:
        """This method simply prints the entire character, both CharacterModel and LiveCharacterModel to log."""
        logging.info(
            f"{self.chk} {self.col['y']}[print_complete_character]{self.col['w']}"
        )

        if not char:
            char = self.char
        if not live_char:
            live_char = self.live_char

        self.print_char_model(char=char)
        self.print_live_char_model(live_char=live_char)

    def print_char_model(self, char: CharacterModel = None) -> None:
        """Requires: char (CharacterModel); returns nothing.
        Prints the current CharacterModel in memory."""
        logging.info(f"{self.chk} {self.col['y']}[print_char_model]{self.col['w']}")

        if not char:
            char = self.char

        char_dict = char.dict()
        print(
            f"{self.chk} {self.py_txt} Current {self.col['m']}CharacterModel{self.col['w']}:"
            f" \n{self.col['m']}{dumps(char_dict, indent=4, default=str)}{self.col['w']}"
        )

    def print_live_char_model(self, live_char: LiveCharacterModel = None) -> None:
        """Requires: live_char (LiveCharacterModel); returns nothing.
        Prints the current LiveCharacterModel in memory."""
        logging.info(
            f"{self.chk} {self.col['y']}[print_live_char_model]{self.col['w']}"
        )

        if not live_char:
            live_char = self.live_char

        live_char_dict = live_char.dict()
        print(
            f"{self.chk} {self.py_txt} Current {self.col['m']}LiveCharacterModel{self.col['w']}:"
            f" \n{self.col['m']}{dumps(live_char_dict, indent=4, default=str)}{self.col['w']}"
        )

    def mod_name_search(
        self,
        search_text: str,
        mod_cat: str = "",
        mod_type: str = "",
        search_type: str = "name",
        cli_print: bool = False,
    ) -> dict:
        """Method for searching for mod names that begin with a number of characters.
        search_type options: name, cat, type, name_cat, name_type, all"""
        logging.warning(f"{self.chk} {self.col['y']}[mod_name_search]{self.col['w']}")
        search_text = search_text.lower()
        return_dict: dict = {}

        print(f"MOD NAME SEARCH")

        # Match type of search
        match search_type:
            case "cat":
                fetch_sql = (
                    f"SELECT mod_id, name, category, type FROM gamedata "
                    f"WHERE category='{mod_cat}' ORDER BY name"
                )
            case "type":
                fetch_sql = (
                    f"SELECT mod_id, name, category, type FROM gamedata "
                    f"WHERE type='{mod_type}' ORDER BY name"
                )
            case "sliver":
                fetch_sql = (
                    f"SELECT mod_id, name, category, type FROM gamedata "
                    f"WHERE category='{mod_cat}' AND type='{mod_type}' AND mod_id='{search_text}' ORDER BY name"
                )
            case "name_cat":
                fetch_sql = (
                    f"SELECT mod_id, name, category, type FROM gamedata "
                    f"WHERE LOWER(name) LIKE '{search_text}%' AND category='{mod_cat}' ORDER BY category, name"
                )
            case "name_type":
                fetch_sql = (
                    f"SELECT mod_id, name, category, type FROM gamedata "
                    f"WHERE LOWER(name) LIKE '{search_text}%' AND type='{mod_type}' ORDER BY category, name"
                )
            case "cat_type":
                fetch_sql = (
                    f"SELECT mod_id, name, category, type FROM gamedata "
                    f"WHERE LOWER(name) LIKE '{search_text}%' AND category='{mod_cat}' AND type='{mod_type}' "
                    f"ORDER BY category, name"
                )
            case "all":
                fetch_sql = (
                    f"SELECT mod_id, name, category, type FROM gamedata "
                    f"WHERE LOWER(name) LIKE '{search_text}%' AND category='{mod_cat}' AND type='{mod_type}' "
                    f"ORDER BY category, name"
                )
            case _:
                # "name"
                fetch_sql = (
                    f"SELECT mod_id, name, category, type FROM gamedata "
                    f"WHERE LOWER(name) LIKE '{search_text}%' ORDER BY category, name"
                )

        # TODO: Comment this out! FOR TESTING ONLY
        print(f"{fetch_sql}")

        logging.warning(
            f"{self.chk} {self.sql_txt} Fetching all mods that begin with:"
            f"'{self.col['g']}{search_text}{self.col['w']}'.\n"
            f"{fetch_sql}"
        )
        if cli_print:
            print(
                f"{self.chk} {self.sql_txt} Fetching all mods that begin with:"
                f"'{self.col['g']}{search_text}{self.col['w']}'.\n"
                f"{fetch_sql}"
            )

        return_data = self.db_fetch(
            self.gamedata_db["db"], self.gamedata_db["db_path"], fetch_sql
        )

        len_rr = len(return_data)
        logging.warning(
            f"{self.info} {self.sql_txt} Record(s) returned: {self.col['g']}{len_rr}{self.col['w']}"
        )
        count: int = 0
        for record in return_data:
            return_dict[count] = record
            count += 1

        return return_dict

    def get_mod_info(
        self, mod_id: str, optional_fields: str = "", lower_case: bool = False
    ) -> dict:
        """Requires mod_id (int), optional_fields (string); returns dict.
        Get full information on a specific mod_id. Defaults to ALL information (SELECT *)"""
        logging.info(f"{self.chk} {self.col['y']}[get_mod_info]{self.col['w']}")

        if optional_fields:
            select_range = optional_fields
        else:
            select_range = "*"

        if lower_case:
            fetch_sql = f"SELECT {select_range} FROM gamedata WHERE LOWER(mod_id)='{mod_id.lower()}'"
        else:
            fetch_sql = f"SELECT {select_range} FROM gamedata WHERE mod_id='{mod_id}'"

        logging.info(
            f"{self.chk} {self.sql_txt} Fetching all details of mod_id:{self.col['g']}{mod_id}{self.col['w']}."
        )

        return_data = self.db_fetch(
            self.gamedata_db["db"], self.gamedata_db["db_path"], fetch_sql
        )

        len_rr = len(return_data)
        logging.info(
            f"{self.info} {self.sql_txt} Record returned: {self.col['g']}{len_rr}{self.col['w']}"
        )

        return return_data

    def check_mod_exists(self, mod_id: str, lower_case: bool = False) -> bool:
        """Requires: mod_id (str), lower_case (bool); returns bool.
        Simple method for checking if a Mod_ID exists in the gamedata DB.
        Setting lower_case to True makes the search case-insensitive."""
        logging.info(f"{self.chk} {self.col['y']}[check_mod_exists]{self.col['w']}")

        if lower_case:
            fetch_sql = f"SELECT * FROM gamedata WHERE LOWER(mod_id)='{mod_id.lower()}'"
        else:
            fetch_sql = f"SELECT * FROM gamedata WHERE mod_id='{mod_id}'"

        mod_check = self.db_fetch(
            db=self.gamedata_db["db"],
            db_path=self.gamedata_db["db_path"],
            fetch_sql=fetch_sql,
            lower_case=True,
        )
        if mod_check:
            logging.info(
                f"{self.chk} Mod ID:{self.col['y']}{mod_id} {self.col['g']}EXISTS{self.col['w']} "
            )
            return True
        else:
            logging.info(
                f"{self.cross} Mod ID:{self.col['y']}{mod_id} {self.col['r']}DOES NOT EXIST{self.col['w']} "
            )
            return False

    def get_mod_name(self, mod_id: str) -> str:
        """Requires: mod_id (str); returns str
        Simple method to return a mod_id's name. That's it."""
        mod_name_search = self.get_mod_info(mod_id=mod_id, optional_fields="name")
        mod_name = mod_name_search[0][0]
        logging.info(f"{self.chk} Mod name:{self.col['g']}{mod_name}{self.col['w']}")

        return mod_name

    def check_multiple_mods_exist(
        self, mods_dict: dict, char: CharacterModel = None
    ) -> dict:
        """Requires mods_dict (dict), char (CharacterModel); returns dict
        Method for checking a dictionary of mods in form mod_location:mod_id or mod_location{mod_id:mod_id} exists.
        Returns a dictionary of all the mods that exist and dumps those that don't with error messages."""
        logging.info(
            f"{self.chk} {self.col['y']}[check_multiple_mods_exist]{self.col['w']}"
        )
        if not char:
            char = self.char

        additional_mods: dict = {}
        for mod_location in mods_dict:
            # Check if mod_id and mod_location exist
            if mod_location in char.nodes:
                if type(mods_dict[mod_location]) is dict:
                    mod_id = mods_dict[mod_location]["mod_id"]
                else:
                    mod_id = mods_dict[mod_location]

                mod_exists = self.check_mod_exists(mod_id=mod_id, lower_case=True)
                if mod_exists:
                    additional_mods[mod_location] = mods_dict[mod_location]
                else:
                    logging.error(
                        f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} The mod_id:{mod_id} "
                        f"submitted at location:{mod_location} DOESN'T EXIST! Skipping...{self.col['w']}"
                    )
            else:
                logging.error(
                    f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} The mod location:{mod_location} "
                    f"(for {mods_dict[mod_location]}DOESN'T EXIST! Skipping...{self.col['w']}"
                )

        return additional_mods

    def get_mod_selection(
        self, mod_category: str, mod_type: str, optional_fields: str
    ) -> dict:
        """Requires mod_category (string), mod_type (string), optional_fields (string); returns dict.
        Produce a dict with relevant mods of (mod_id: name)"""
        logging.info(f"{self.chk} {self.col['y']}[get_mod_selection]{self.col['w']}")

        if optional_fields:
            select_range = optional_fields
        else:
            select_range = "*"

        fetch_sql = f"SELECT {select_range} FROM gamedata WHERE category='{mod_category}' AND type='{mod_type}'"
        logging.info(
            f"{self.chk} {self.sql_txt} Fetching all mod_ids and names where category:"
            f"{self.col['g']}{mod_category}{self.col['w']} and mod_type:{self.col['g']}{mod_type}{self.col['w']}."
        )

        fetched_data = self.db_fetch(
            self.gamedata_db["db"], self.gamedata_db["db_path"], fetch_sql
        )

        if len(fetched_data) > 1:
            return_data = fetched_data
        else:
            return_data = dumps(fetched_data, indent=4, default=str)

        return_type = type(return_data)

        logging.info(
            f"{self.chk} {self.sql_txt} Record type returned from get_mod_selection: {return_type}.\n"
            f"                      {self.col['y']}->{self.col['w']} First record returned is {return_data[0]}"
        )

        return return_data

    def get_mod_selection_full(self, mod_category: str, mod_type: str) -> dict:
        """Requires mod_category (string), mod_type (string); returns dict.
        Produce a dict with all relevant mods and their full information"""
        logging.info(
            f"{self.chk} {self.col['y']}[get_mod_selection_full]{self.col['w']}"
        )

        logging.info(
            f"{self.chk} {self.py_txt} Selecting all mods in category:{self.col['g']}{mod_category}{self.col['w']} and "
            f"type:{self.col['g']}{mod_type}{self.col['w']}."
        )
        return_data = self.get_mod_selection(
            mod_category=mod_category, mod_type=mod_type, optional_fields=""
        )
        len_rr = len(return_data)
        logging.info(
            f"{self.chk} {self.py_txt} Record(s) returned from get_mod_selection_full: "
            f"{self.col['g']}{len_rr}{self.col['w']}"
        )
        return_type = type(return_data)
        subtype = type(return_data[0])
        sub_subtype = type(return_data[0][0])
        logging.info(
            f"{self.chk} {self.py_txt} DATA TYPES RETURNED:\n"
            f"                      {self.col['y']}->{self.col['w']} Top level is "
            f"{self.col['g']}ALL {len_rr}{self.col['w']} records returned and is {return_type}.\n"
            f"                      {self.col['y']}->{self.col['w']} First record returned [0] "
            f"is {subtype}, e.g. {return_data[0]}. \n"
            f"                      {self.col['y']}->{self.col['w']} First sub-record returned [0][0] "
            f"is {sub_subtype}, e.g. {return_data[0][0]}."
        )

        return return_data

    def check_any_all(self, mod_id: str) -> tuple:
        """Requires mod_id (string); returns bool tuple in form of (Prerequisite True/False, Restriction True/False)
        True = ANY, False = ALL.
        This does a simple check of whether a given mod has any or all requirements for prereqs and restrictions"""
        logging.info(f"{self.chk} {self.col['y']}[check_any_all]{self.col['w']}")

        logging.info(
            f"{self.chk} {self.py_txt} Checking any/all requirements prereqs/restrictions of "
            f"mod_id:{self.col['g']}{mod_id}{self.col['w']}."
        )
        main_mod = self.get_mod_info(
            mod_id, optional_fields="prereq_any, restriction_any"
        )
        mod_preq = False
        mod_rest = False
        mod_preq_aa = f"{self.col['r']}ALL (False)"
        mod_rest_aa = f"{self.col['r']}ALL (False)"

        if main_mod[0][0]:
            mod_preq = True
            mod_preq_aa = f"{self.col['y']}ANY (True)"
        if main_mod[0][1]:
            mod_rest = True
            mod_rest_aa = f"{self.col['y']}ANY (True)"

        logging.info(
            f"{self.chk} {self.py_txt} The Prerequisite AND Restriction settings for "
            f"mod_id:{self.col['g']}{mod_id}{self.col['w']} are:\n"
            f"                      {self.col['y']}->{self.col['w']} Prerequisite: "
            f"{mod_preq_aa}{self.col['w']}\n"
            f"                      {self.col['y']}->{self.col['w']} Restriction:  "
            f"{mod_rest_aa}{self.col['w']}"
        )

        is_any = (mod_preq, mod_rest)

        return is_any

    def check_mod_in_list(self, mod_id: str, mod_list: list) -> bool:
        """Requires mod_id (string), mod_list (list); returns bool.
        This method simply checks if mod_id is in the mod_list and returns True if it is"""
        logging.info(f"{self.chk} {self.col['y']}[check_mod_in_list]{self.col['w']}")

        logging.info(
            f"{self.chk} {self.py_txt} Check if mod_id:{self.col['g']}{mod_id}{self.col['w']} "
            f"is in list containing these mods: {mod_list}?"
        )
        if mod_id in mod_list:
            logging.info(
                f"{self.chk} {self.py_txt}{self.col['y']}->{self.col['w']} mod_id:{self.col['g']}{mod_id}"
                f"{self.col['w']} {self.col['g']} IS{self.col['w']} in list."
            )
            return True
        else:
            logging.info(
                f"{self.chk} {self.py_txt}{self.col['y']}->{self.col['w']} mod_id:{self.col['g']}{mod_id}"
                f"{self.col['w']} {self.col['y']}IS NOT{self.col['w']} in list."
            )
            return False

    def multi_check(self, char_mods: list, mod_list: list, check_len: int) -> bool:
        """Requires character_mods (list), is_any (bool), mod_list (list), check_len (int); returns bool.
        Mini method for checking if a mod_id is present in a list of mod_ids"""
        logging.info(f"{self.chk} {self.col['y']}[multi_check]{self.col['w']}")
        # TODO: Work out if we can delete check_len from this method... or at least actually use it!
        count = 0
        for x in mod_list:
            mod_check = self.check_mod_in_list(x, char_mods)
            if mod_check:
                logging.info(
                    f"{self.chk} {self.py_txt} mod_id {self.col['g']}IS{self.col['w']} found in list!"
                )
                count += 1

        # if check_len == count:
        if count > 0:
            logging.info(
                f"{self.chk} {self.py_txt} Multi-check is {self.col['g']}TRUE{self.col['w']}."
            )
            return True
        else:
            logging.info(
                f"{self.chk} {self.py_txt} Multi-check is {self.col['r']}FALSE{self.col['w']}."
            )
            return False

    def get_prereqs_restrictions(self, mod_id: str) -> tuple:
        """Requires mod_id (string); returns tuple of lists with Prerequisites at [0] and Restrictions at [1].
        This makes a list of the prerequisite or restriction mods_ids (if any) for a specified mod_id"""
        logging.info(
            f"{self.chk} {self.col['y']}[get_prereqs_restrictions]{self.col['w']}"
        )

        logging.info(
            f"{self.chk} {self.py_txt} Compiling Prerequisite/Restriction mod list for "
            f"mod_id:{self.col['g']}{mod_id}{self.col['w']}."
        )
        return_data = self.get_mod_info(mod_id, optional_fields="prereqs, restriction")
        pre1 = self.split_string_list_to_true_list(return_data[0][0])
        res2 = self.split_string_list_to_true_list(return_data[0][1])

        pr_tuple = (pre1, res2)
        logging.info(
            f"{self.chk} {self.py_txt} The Prerequisite AND Restriction mod_id requirements for mod_id"
            f":{self.col['g']}{mod_id}{self.col['w']} are: \n"
            f"                      {self.col['y']}->{self.col['w']} Prerequisites: "
            f"{self.col['y']}{pr_tuple[0]}{self.col['w']}\n"
            f"                      {self.col['y']}->{self.col['w']} Restrictions:  "
            f"{self.col['y']}{pr_tuple[1]}{self.col['w']}"
        )
        return pr_tuple

    def check_prerequisite(
        self, mod_id: str, char_mods: list, any_mod: bool, mod_list: list
    ) -> bool:
        """
        Requires: mod_id: str, character_mods: list, any_mod: bool, mod_list: list; returns bool
        LOGIC:
        Prerequisites ->
        ANY -> Null     -> True     -> Case A
            -> Has 0    -> False    -> Case B
            -> Has 1    -> True     -> Case C
            -> Has ALL  -> True     -> Case D
        ALL -> Null     -> True     -> Case E
            -> Has 0    -> False    -> Case F
            -> Has 1    -> False    -> Case G
            -> Has ALL  -> True     -> Case H

        """
        logging.info(f"{self.chk} {self.col['y']}[check_prerequisite]{self.col['w']}")

        # ANY (Case A, B, C, D)
        if any_mod:  # True = ANY, so check if any mod_id from mod_list is present
            logging.info(
                f"{self.chk} {self.py_txt} {mod_id} has {self.col['g']}'ANY'{self.col['w']} type of Prerequisites."
            )
            if mod_list[0] == "null":
                logging.info(
                    f"{self.chk} {self.py_txt} The 'ALL' the Prerequisites for mod_id:{self.col['g']}{mod_id}"
                    f"{self.col['w']} are {self.col['g']}NULL{self.col['w']}, therefore Prerequisites are satisfied. "
                    f"(Case A)"
                )
                return True
            else:
                check_len = len(mod_list)
                is_any_mod_present = self.multi_check(char_mods, mod_list, check_len)
                if is_any_mod_present:
                    logging.info(
                        f"{self.chk} {self.py_txt} At least 1 of the 'ANY' Prerequisites for mod_id:"
                        f"{self.col['g']}{mod_id}{self.col['w']} are "
                        f"{self.col['g']}SATISFIED{self.col['w']}. (Case C, D)"
                    )
                    return True
                else:
                    logging.info(
                        f"{self.chk} {self.py_txt} At least 1 of the 'ANY' Prerequisites for mod_id:"
                        f"{self.col['g']}{mod_id}{self.col['w']} are "
                        f"{self.col['r']}NOT SATISFIED{self.col['w']}. (Case B)"
                    )
                    return False

        # ALL (Cases E, F, G, H)
        else:  # False = ALL, so check if ALL mod_ids are present from mod_list
            logging.info(
                f"{self.chk} {self.py_txt} {mod_id} has {self.col['y']}'ALL'{self.col['w']} type of Prerequisites."
            )
            if mod_list[0] == "null":
                logging.info(
                    f"{self.chk} {self.py_txt} 'ALL' the Prerequisites for "
                    f"mod_id:{self.col['g']}{mod_id}{self.col['w']} are "
                    f"{self.col['g']}NULL{self.col['w']}, therefore Prerequisites are satisfied. (Case E)"
                )
                return True
            else:
                check_len = len(mod_list)  # Count number of mod_ids to chk
                if check_len == 1:
                    # mod_list here is the mod_id Prerequisite we are searching for, it is a list of 1
                    is_any_mod_present = self.check_mod_in_list(mod_list[0], char_mods)
                    if is_any_mod_present:
                        logging.info(
                            f"{self.chk} {self.py_txt} 'ALL' {check_len} of the Prerequisites for mod_id:"
                            f"{self.col['g']}{mod_id}{self.col['w']} are "
                            f"{self.col['g']}SATISFIED{self.col['w']}. (Case G)"
                        )
                        return True
                    else:
                        logging.info(
                            f"{self.chk} {self.py_txt} 'ALL' {check_len} of the Prerequisites for mod_id:"
                            f"{self.col['g']}{mod_id}{self.col['w']} are "
                            f"{self.col['r']}NOT SATISFIED{self.col['w']}. (Case E, F)"
                        )
                        return False
                else:
                    prereq_all = self.multi_check(char_mods, mod_list, check_len)
                    if prereq_all:
                        logging.info(
                            f"{self.chk} {self.py_txt} 'ALL' {check_len} of the Prerequisites for mod_id:"
                            f"{self.col['g']}{mod_id}{self.col['w']} are "
                            f"{self.col['g']}SATISFIED{self.col['w']}. (Case H)"
                        )
                        return True
                    else:
                        logging.info(
                            f"{self.chk} {self.py_txt} 'ALL' {check_len} of the Prerequisites for mod_id:"
                            f"{self.col['g']}{mod_id}{self.col['w']} are "
                            f"{self.col['r']}NOT SATISFIED{self.col['w']}. (Case E, F)"
                        )
                        return False

    def check_restriction(
        self, mod_id: str, char_mods: list, any_mod: bool, mod_list: list
    ) -> bool:
        """
        Requires: mod_id: str, character_mods: list, any_mod: bool, mod_list: list; returns bool
        LOGIC:
        Restrictions ->
        ANY -> Null     -> True     -> Case A
            -> Has 0    -> True     -> Case B
            -> Has 1    -> False    -> Case C
            -> Has ALL  -> False    -> Case D
        ALL -> Null     -> True     -> Case E
            -> Has 0    -> True     -> Case F
            -> Has 1    -> False    -> Case G
            -> Has ALL  -> False    -> Case H

        """
        logging.info(f"{self.chk} {self.col['y']}[check_restriction]{self.col['w']}")

        # ANY (Case A, B, C, D)
        if any_mod:  # True = ANY, so check if any mod_id from mod_list is present
            logging.info(
                f"{self.chk} {self.py_txt} {mod_id} has {self.col['g']}'ANY'{self.col['w']} type of Restrictions."
            )
            if mod_list[0] == "null":
                logging.info(
                    f"{self.chk} {self.py_txt} The 'ANY' Restrictions for "
                    f"mod_id:{self.col['g']}{mod_id}{self.col['w']} are "
                    f"{self.col['g']}NULL{self.col['w']}, therefore Restrictions are satisfied. (Case A)"
                )
                return True
            else:
                check_len = len(mod_list)
                is_any_mod_present = self.multi_check(char_mods, mod_list, check_len)
                if is_any_mod_present:
                    logging.info(
                        f"{self.chk} {self.py_txt} At least 1 of the 'ANY' Restrictions for mod_id:"
                        f"{self.col['g']}{mod_id}{self.col['w']} are present, therefore Restrictions are"
                        f"{self.col['r']}NOT SATISFIED{self.col['w']}. (Case C, D)"
                    )
                    return False
                else:
                    logging.info(
                        f"{self.chk} {self.py_txt} None of the 'ANY' Restrictions for mod_id:"
                        f"{self.col['g']}{mod_id}{self.col['w']} are present, therefore Restrictions are "
                        f"{self.col['g']}SATISFIED{self.col['w']}. (Case B)"
                    )
                    return True

        # ALL (Cases E, F, G, H)
        else:  # False = ALL, so check if ALL mod_ids are present from mod_list
            logging.info(
                f"{self.chk} {self.py_txt} {mod_id} has {self.col['y']}'ALL'{self.col['w']} type of Restrictions."
            )
            if mod_list[0] == "null":
                logging.info(
                    f"{self.chk} {self.py_txt} 'ALL' the Restrictions for "
                    f"mod_id:{self.col['g']}{mod_id}{self.col['w']} are "
                    f"{self.col['g']}NULL{self.col['w']}, therefore Restrictions are satisfied. (Case E)"
                )
                return True
            else:
                check_len = len(mod_list)  # Count number of mod_ids to chk
                if check_len == 1:
                    # mod_list here is the mod_id Prerequisite we are searching for, it is a list of 1
                    is_any_mod_present = self.check_mod_in_list(mod_list[0], char_mods)
                    if is_any_mod_present:
                        logging.info(
                            f"{self.chk} {self.py_txt} At least 1 of the 'ALL' {check_len} Restrictions for "
                            f"mod_id:{self.col['g']}{mod_id}{self.col['w']} are present, therefore "
                            f"Restrictions are {self.col['r']}NOT SATISFIED{self.col['w']}. (Case G)"
                        )
                        return False
                    else:
                        logging.info(
                            f"{self.chk} {self.py_txt} None of the 'ALL' {check_len} Restrictions for mod_id:"
                            f"{self.col['g']}{mod_id}{self.col['w']} are present, therefore Restrictions "
                            f"are {self.col['g']}SATISFIED{self.col['w']}. (Case F)"
                        )
                        return True
                else:
                    prereq_all = self.multi_check(char_mods, mod_list, check_len)
                    if prereq_all:
                        logging.info(
                            f"{self.chk} {self.py_txt} 'ALL' {check_len} of the Restrictions for mod_id:"
                            f"{self.col['g']}{mod_id}{self.col['w']} are present, therefore Restrictions "
                            f"are {self.col['r']}NOT SATISFIED{self.col['w']}. (Case H)"
                        )
                        return False
                    else:
                        logging.info(
                            f"{self.chk} {self.py_txt} None of the 'ALL' {check_len} Restrictions for mod_id:"
                            f"{self.col['g']}{mod_id}{self.col['w']} are present, therefore Restrictions "
                            f"are {self.col['g']}SATISFIED{self.col['w']}. (Case F)"
                        )
                        return True

    def check_preq_restrict_all(self, mod_id: str, char_mods: list) -> tuple:
        """Requires mod_id (string), char_mods (dict); returns tuple.
        Checks that ALL prerequisites or restrictions are met for a mod_id. ANY is already done as that is a
        single test. Returns (True, True) if all passed.
        """
        logging.info(
            f"{self.chk} {self.col['y']}[check_preq_restrict_all]{self.col['w']}"
        )

        # Returns True if ANY, and False if ALL.  [0] = Preq, [1] Restriction.
        any_mod = self.check_any_all(mod_id)

        # Returns list of mod_ids [0] = Preq, [1] Restriction.
        mod_list = self.get_prereqs_restrictions(mod_id)

        # These next two together return an AND gate. If A+B=True proceed, else fail.
        return_preq = self.check_prerequisite(
            mod_id, char_mods, any_mod[0], mod_list[0]
        )
        return_rest = self.check_restriction(mod_id, char_mods, any_mod[1], mod_list[1])
        return_data = (return_preq, return_rest)

        logging.info(
            f"{self.chk} {self.py_txt} {mod_id} has returned "
            f"{self.col['g']}{return_data}{self.col['w']} for Prerequisites AND Restrictions."
        )
        return return_data

    def check_prerequisites_for_node(
        self,
        node_location: str,
        char: CharacterModel,
    ) -> bool:
        """A simple method that checks if any Requirements (req) listed for a NODE are present in a character's
        list of mods and returns True if they are and False if not"""
        logging.info(
            f"{self.chk} {self.col['y']}[check_prerequisites_for_node]{self.col['w']}"
        )

        allowed: bool = True

        # Check if there is a "req" section in the mod's info:
        node_info: dict = getattr(self.nm, node_location)

        # Get list of character's mods:
        char_mods: list = self.get_char_current_mods(char=char, cli_print=False)

        # Check for reqs:
        if "req" in node_info:
            for field in node_info:
                for req in node_info["req"]:
                    if req not in char_mods:
                        logging.info(
                            f"Requirement of {req} not present in character mods for {node_location}"
                        )
                        allowed = False
                    else:
                        logging.info(
                            f"Requirement of {req} IS present in character mods for {node_location}"
                        )
        return allowed

    def check_mods_by_node(
        self,
        node_location: str,
        include_extra: bool = False,
        override: bool = False,
        char: CharacterModel = None,
        cli_print: bool = False,
    ):
        """Returns a list mod_ids.
        So this should check what mods are allowed in a node. In effect a reverse of check_mod_node_mapping
        This should:
        1) Take an input node location as a node_id
        2) Generate up a list of mod_ids that can go in that slot
        3) Filter out mod_ids that the character already has
        4) Filter out mod_ids that the character cannot get (Prerequisites/Restrictions/Multiple/Breed Locked)
        5) Return list of mod_ids"""
        # TODO: Have a think about this one
        logging.info(
            f"{self.chk} {self.col['y']}[check_mod_allowed_location]{self.col['w']}"
        )
        if not char:
            char = self.char

        # DB info for searches
        db = self.gamedata_db["db"]
        db_path = self.gamedata_db["db_path"]
        table = "gamedata"

        # Get character's current mods as a list
        char_mods: list = self.get_char_current_mods(char=char, cli_print=cli_print)
        char_breed: str = getattr(char, "breed", "")

        # Load the full list of a character's locations and current nodes into a dict
        # free_locations: list = self.get_char_free_nodes(char=char, cli_print=cli_print)

        nm = self.nm
        node_info: dict = getattr(nm, node_location)
        node_name = self.get_node_location_name(node_location)
        node_cat = node_info["category"]
        search_type_list_raw: list = []
        search_mod_list_raw: list = []
        search_type_list: list = []
        search_mod_list: list = []
        # Compile search criteria
        for field in node_info:
            if field in nm.node_map_types:
                search_type_list_raw.append(node_info[field])
            elif field in nm.node_mod_types:
                search_mod_list_raw.append(node_info[field])
            elif field in nm.node_map_types_extra:
                if include_extra:
                    search_type_list_raw.append(node_info[field])
            elif field == "name":
                pass
            elif field == "category":
                pass
            elif field == "cxn":
                pass
            elif field == "req":
                pass
            else:
                logging.error(
                    f"{self.cross} {self.err_txt} Unknown field type of {field}"
                )

        # We will have one or more sub-lists that we need to organise into single lists
        count = 0
        for x in search_type_list_raw:
            for x2 in search_type_list_raw[count]:
                search_type_list.append(x2)
            count += 1

        count = 0
        for y in search_mod_list_raw:
            for y2 in search_mod_list_raw[count]:
                search_mod_list.append(y2)
            count += 1

        # Prepare the SQL for searches for mods by category AND type:
        search_str_1: str = ""
        for mod_type in search_type_list:
            if not search_str_1:
                search_str_1 = f"SELECT mod_id FROM gamedata WHERE category='{node_cat}' AND (type='{mod_type}'"
            else:
                search_str_1 = f"{search_str_1} OR type='{mod_type}'"
        if search_str_1:
            search_str_1 = f"{search_str_1}) ORDER BY type"

        # Prepare the SQL for searches for mods by category AND mod_id:
        search_str_2: str = ""
        for mod_id in search_mod_list:
            if not search_str_2:
                search_str_2 = f"SELECT mod_id FROM gamedata WHERE category='{node_cat}' AND (mod_id='{mod_id}'"
            else:
                search_str_2 = f"{search_str_2} OR mod_id='{mod_id}'"
        if search_str_2:
            search_str_2 = f"{search_str_2}) ORDER BY mod_id"

        # Perform the searches
        if search_str_1:
            raw_search_1 = self.db_fetch(db=db, db_path=db_path, fetch_sql=search_str_1)
            search_results_1 = self._filter_for_check_mods_by_node(
                node_name=node_name,
                search_results=raw_search_1,
                char_mods=char_mods,
                char_breed=char_breed,
                override=override,
                cli_print=cli_print,
            )
            return search_results_1

        if search_str_2:
            raw_search_2 = self.db_fetch(db=db, db_path=db_path, fetch_sql=search_str_2)
            search_results_2 = self._filter_for_check_mods_by_node(
                node_name=node_name,
                search_results=raw_search_2,
                char_mods=char_mods,
                char_breed=char_breed,
                override=override,
                cli_print=cli_print,
            )
            return search_results_2

    def _filter_for_check_mods_by_node(
        self,
        node_name: str,
        search_results: dict,
        char_mods: list = list,
        char_breed: str = "",
        override: bool = False,
        cli_print: bool = False,
    ) -> list:
        """Simple method to filter mods available to a node_name searched by check_mods_by_node, and filtered by mods
        the character has (char_mods). Returns a list of all the filtered mod_ids."""
        if override:
            if cli_print:
                print(
                    f"{self.chk} {self.col['g']}Override activated so mods will NOT be filtered for Breed locked "
                    f"status, Prerequisites, Restrictions, Multiple Copies etc for the "
                    f"{self.col['w']}{node_name}{self.col['g']} slot...{self.col['w']}"
                )

        master_mod_list: list = []
        for mod_set in search_results:
            check_mod_id = mod_set[0]
            # Now filter out any that clash due to Restrictions or Prerequisites and Allow Multiples
            if not override:
                breed_locked = self.check_if_breed_mod(
                    mod_id=check_mod_id, mod_location=node_name, breed_name=char_breed
                )
                if not breed_locked:
                    mod_allowed = self.check_mod_allowed(
                        mod_id=check_mod_id, char_mods=char_mods
                    )
                    if mod_allowed:
                        # Possibly add to master_mod_list
                        # Now filter out any the character already has!
                        if check_mod_id not in char_mods:
                            logging.info(
                                f"{self.chk}{self.col['g']}{check_mod_id} is allowed!{self.col['w']}"
                            )
                            master_mod_list.append(mod_set[0])
                        else:
                            # Don't add it to master_mod_list
                            logging.info(
                                f"{self.cross} {self.col['r']}{check_mod_id} is NOT allowed!{self.col['w']}"
                            )
                    else:
                        # Don't add it to master_mod_list
                        logging.info(
                            f"{self.cross} {self.col['r']}{check_mod_id} is NOT allowed!{self.col['w']}"
                        )
                else:
                    # Don't add it to master_mod_list
                    logging.info(
                        f"{self.cross} {self.col['r']}{check_mod_id} is a Breed Locked skill and is NOT "
                        f"allowed!{self.col['w']}"
                    )
            else:
                master_mod_list.append(mod_set[0])

        if master_mod_list:
            if cli_print:
                print(
                    f"{self.info} {self.col['g']}There are {self.col['w']}{len(master_mod_list)}{self.col['g']} "
                    f"available mods for the '{node_name}' slot...{self.col['w']}"
                )

        return master_mod_list

    def get_char_free_nodes(
        self, char: CharacterModel = None, cli_print: bool = False
    ) -> list:
        """Method for generating a list of a character's available nodes for mods"""
        logging.info(f"{self.chk} {self.col['y']}[get_char_free_nodes]{self.col['w']}")
        if not char:
            char = self.char

        # Load the full list of a character's locations and current nodes into a dict
        char_locations: dict = char.nodes

        if cli_print:
            print(
                f"{self.info} {self.col['y']}Generating a list of all free slots for "
                f"{self.col['w']}{self.string_pretty(char.char_name)}{self.col['y']}..."
            )

        # Make a list of all the available (empty locations) for the character:
        unfiltered_free_locations: list = []
        free_locations: list = []
        filled_locations: list = []
        for x in char_locations:
            if char_locations[x]:
                logging.info(
                    f"{self.chk} {self.py_txt} {self.col['b']}Filled Slot: {x}{self.col['w']}"
                )
                filled_locations.append(x)
            else:
                logging.info(
                    f"{self.chk} {self.py_txt} {self.col['y']}Unfiltered Free Slot: {x}{self.col['w']}"
                )
                unfiltered_free_locations.append(x)

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['y']}Character current FILLED LOCATIONS: "
            f"{filled_locations}{self.col['w']}"
        )

        for empty_loc in unfiltered_free_locations:
            node_info: dict = getattr(self.nm, empty_loc, {})
            # Get connection list for cxn_location
            cxn_list = node_info["cxn"]
            if cxn_list[0] != "null":
                if "entry_node" in cxn_list:
                    logging.info(f"ENTRY NODE FOR {empty_loc}\n{node_info}")
                    if "req" in node_info:
                        logging.info(f"Checking if mod_location is allowed")
                        check_allowed = self.check_prerequisites_for_node(
                            node_location=empty_loc, char=char
                        )
                        if check_allowed:
                            free_locations.append(empty_loc)
                            logging.info(
                                f"{self.chk} {self.py_txt} {self.col['g']}Valid req found for "
                                f"{self.col['w']}{empty_loc}"
                            )
                    else:
                        free_locations.append(empty_loc)
                else:
                    check_cxn = self.check_node_cxn(
                        node_location=empty_loc, cxn_list=filled_locations
                    )
                    if check_cxn:
                        if "req" in node_info:
                            logging.info(f"Checking if mod_location is allowed")
                            check_allowed = self.check_prerequisites_for_node(
                                node_location=empty_loc, char=char
                            )
                            if check_allowed:
                                free_locations.append(empty_loc)
                                logging.info(
                                    f"{self.chk} {self.py_txt} {self.col['g']}Valid req found for "
                                    f"{self.col['w']}{empty_loc}"
                                )
                            else:
                                pass
                        else:
                            free_locations.append(empty_loc)
                            logging.info(
                                f"{self.chk} {self.py_txt} {self.col['g']}Valid connection found for "
                                f"{self.col['w']}{empty_loc}"
                            )

        return free_locations

    def check_node_cxn(self, node_location: str, cxn_list: list):
        """Check all connections (CXN) for a node. Is node_location (A) in the CNX set for cxn_location (B)?
        Return True if connected, False if not

        # check if node_location in any cxn locations in skills of cxn_list...
        """
        logging.info(f"{self.chk} {self.col['y']}[check_node_cxn]{self.col['w']}")
        cxn: bool = False
        for existing_skill in cxn_list:
            cxn_node: dict = getattr(self.nm, existing_skill, {})
            # Get connection list for cxn_location
            cxn_list = cxn_node["cxn"]
            for connect in cxn_list:
                if connect == node_location:
                    logging.info(
                        f"{self.chk} {self.py_txt} {self.col['g']}{existing_skill} found in connection list! \n"
                        f"{self.ind1}Returning True...{self.col['w']}"
                    )
                    # print(f"CXN")
                    cxn = True

        return cxn

    def get_node_cat(self, node_location: str):
        logging.info(f"{self.chk} {self.col['y']}[get_node_cat]{self.col['w']}")

        node_cat = self.nm_dict[node_location]["category"]

        logging.info(
            f"{self.chk} {self.py_txt} Node location {node_location} category is '{node_cat}'"
        )
        return node_cat

    def get_node_location_name(self, node_location: str, max_characters: int = 0):
        """Simple method for returning a prettified name of a node location. You can limit the max characters with
        the max_characters value"""
        logging.info(
            f"{self.chk} {self.col['y']}[check_mod_node_mapping]{self.col['w']}"
        )

        node_name = self.string_pretty(self.nm_dict[node_location]["name"])

        if max_characters > 0:
            node_name = textwrap.shorten(
                node_name, width=max_characters, placeholder="..."
            )

        logging.info(
            f"{self.chk} {self.py_txt} Node location {node_location} name is '{node_name}'"
        )

        return node_name

    def check_mod_node_mapping(
        self,
        mod_id: str,
        mod_location: str,
        char: CharacterModel = None,
        check_allowed: bool = False,
    ) -> bool:
        """Requires: mod_id (string), mod_location (string); returns bool (True = allowed).
        This is the dataclass that specifies what type (e.g. pkc, ssw), skill (skl), drug (drg), cyberware (cyb),
        bioware (bio), a range of injuries (iX0)/ wounds (wX0) or "extra" which is a list of types or other that
        are allowed but with special rules...
        ["skl", "type", "extra", "drg", "cyb", "bio", "ip0", "is0", "ir0", "iw0", "id0", "iv0", "wp0", "ws0", "wr0",
        "ww0", "wd0", "wv0"]
        """
        # TODO: NOT FINISHED! Add code to check for correct Injuries, Wounds and Drugs.
        logging.info(
            f"{self.chk} {self.col['y']}[check_mod_node_mapping]{self.col['w']}"
        )

        logging.info(
            f"{self.chk} {self.py_txt} Checking if mod_id:{self.col['g']}{mod_id}{self.col['w']} "
            f"is allowed in mod_location:{self.col['y']}{mod_location}{self.col['w']}."
        )

        # Default values:
        am_list = []
        mod_allowed = False

        # Pull the mod info from the gamedata DB:
        mod_id_details = self.get_mod_info(
            mod_id=mod_id, optional_fields="mod_id, name, type"
        )
        mod_name = mod_id_details[0][1]
        mod_type = mod_id_details[0][2]

        # Instantiate a NodeMap object and convert into a dict:
        am_mode = self.nm_dict[mod_location]

        for loc in am_mode:
            count = 0
            for x in am_mode[loc]:
                if loc in [
                    "skl",
                    "cyb",
                    "bio",
                    "opp",
                    "slot",
                ]:
                    # Skill, Cyberware or Bioware
                    if count == 0:
                        logging.info(
                            f"{self.chk} {self.py_txt} Type = skl, cyb, bio, opp, slot."
                        )
                    if am_mode[loc][count] == mod_id:
                        am_list.append(am_mode[loc][count])
                        mod_allowed = True
                elif loc in ["type", "extra"]:  # Mod type, extra.
                    if count == 0:
                        logging.info(f"{self.chk} {self.py_txt} Type = type, or extra.")
                    am_list.append(am_mode[loc][count])
                elif loc in [
                    "ip0",
                    "is0",
                    "ir0",
                    "iw0",
                    "id0",
                    "iv0",
                    "ic0",
                    "ig0",
                ]:  # Injuries
                    if count == 0:
                        logging.warning(
                            f"{self.chk} {self.py_txt} Type = injury (iX0) {self.col['y']}[NOT IMPLEMENTED]"
                            f"{self.col['w']}."
                        )
                    # TODO
                    mod_allowed = True

                elif loc in ["wp0", "ws0", "wr0", "ww0", "wd0", "wv0"]:  # Wounds
                    if count == 0:
                        logging.warning(
                            f"{self.chk} {self.py_txt} Type = wound (wX0) "
                            f"{self.col['y']}[NOT IMPLEMENTED YET]{self.col['w']}."
                        )
                    # TODO
                    mod_allowed = True
                elif loc in ["drg"]:  # Drugs
                    if count == 0:
                        logging.warning(
                            f"{self.chk} {self.py_txt} Type = drugs (drg) "
                            f"{self.col['y']}[NOT IMPLEMENTED YET]{self.col['w']}."
                        )
                    # TODO
                    mod_allowed = True
                elif loc in ["name"]:  # Name of location
                    # TODO: Do we need this?
                    logging.info(
                        f"{self.chk} {self.py_txt} Skill name is {self.string_pretty(am_mode[loc])} "
                    )
                elif loc in ["category"]:
                    pass
                elif loc in ["cxn"]:
                    pass
                elif loc in ["req"]:
                    pass
                else:  # Unknown -> skip.
                    logging.error(
                        f"{self.cross} {self.err_txt} Type = {self.col['r']}UNKNOWN MOD TYPE{self.col['w']}."
                    )
                    mod_allowed = False
                count += 1

        if mod_type in am_list:
            mod_allowed = True

        if mod_allowed:
            logging.info(
                f"{self.chk} {self.py_txt} Mod_id:{self.col['g']}{mod_id}{self.col['w']} "
                f"({mod_name}) {self.col['g']}IS{self.col['w']} allowed in "
                f"mod_location:{self.col['y']}{mod_location}{self.col['w']} \n"
                f"                      {self.col['y']}->{self.col['w']} "
                f"This mod_type:{self.col['y']}{mod_type}{self.col['w']} "
                f"{self.col['g']}IS{self.col['w']} in list of allowed mods: \n"
                f"                      {self.col['y']}->{self.col['w']} {am_list}.\n"
                f"                      {self.col['y']}->{self.col['w']} Therefore Mod Allowed? "
                f"{self.col['g']}{mod_allowed}{self.col['w']}."
            )
        else:
            logging.warning(
                f"{self.chk} {self.py_txt} Mod_id:{self.col['g']}{mod_id}{self.col['w']} "
                f"({mod_name}) {self.col['r']}IS NOT{self.col['w']} allowed in "
                f"mod_location:{self.col['y']}{mod_location}{self.col['w']} \n"
                f"                      {self.col['y']}->{self.col['w']} "
                f"This mod_type:{self.col['y']}{mod_type}{self.col['w']} "
                f"{self.col['r']}IS NOT{self.col['w']} in list of allowed mods: \n"
                f"                      {self.col['y']}->{self.col['w']} {am_list}.\n"
                f"                      {self.col['y']}->{self.col['w']} Therefore Mod Allowed? "
                f"{self.col['r']}{mod_allowed}{self.col['w']}."
            )
        return mod_allowed

    def check_allowed_multiple(self, mod_id: str) -> bool:
        """Requires mod_id (string); returns bool.
        This method checks if you are allowed multiple copies of a specific mod."""
        logging.info(
            f"{self.chk} {self.col['y']}[check_allowed_multiple]{self.col['w']}"
        )

        logging.info(
            f"{self.chk} {self.sql_txt} Checking if you are allowed multiple copies of mod_id: '{mod_id}'."
        )
        return_data = self.get_mod_info(mod_id, optional_fields="allow_multiple")

        # return_data[0][0] contains the required data
        if return_data[0][0] == 1:
            logging.info(
                f"{self.chk} {self.sql_txt} You {self.col['g']}ARE{self.col['w']} allowed multiples of "
                f"mod_id: '{mod_id}'."
            )
            return True
        else:
            logging.warning(
                f"{self.chk} {self.sql_txt} You {self.col['r']}ARE NOT{self.col['w']} "
                f"allowed multiple copies of mod_id: '{mod_id}'."
            )
            return False

    def check_mod_allowed(self, mod_id: str, char_mods: list) -> bool:
        """Requires mod_id (string), char_mods (dict); returns bool.
        Here we check if a character has any/all the prerequisites and restrictions for a specific mod
        Accept mod to be checked in and current list of character_mods
        Steps:
        1. check prerequisites and restrictions -> check_preq_restrict_all
        2. check if mod can be chosen multiple times if it already exists
        If all are True, proceed
        """
        logging.info(f"{self.chk} {self.col['y']}[check_mod_allowed]{self.col['w']}")

        logging.info(f"{self.chk} {self.py_txt} Checking if {mod_id} is allowed.")
        check_mult = True
        check_pr = self.check_preq_restrict_all(mod_id, char_mods)
        check_preq = check_pr[0]
        check_restrict = check_pr[1]
        if mod_id in char_mods:
            count = 0
            for x in char_mods:
                if x == mod_id:
                    count += 1

            # We ONLY want to run this test if MORE THAN 1 on that mod_id is in char_mods
            if count > 1:
                logging.info(
                    f"{self.chk} {self.py_txt} {mod_id} {self.col['y']}IS ALREADY{self.col['w']} "
                    f"in character_mods, so checking if character is allowed {self.col['y']}MULTIPLE "
                    f"COPIES{self.col['w']} of this mod_id."
                )
                check_mult = self.check_allowed_multiple(mod_id)
        else:
            logging.info(
                f"{self.chk} {self.py_txt} {mod_id} {self.col['g']}IS NOT{self.col['w']} "
                f"in character_mods, so {self.col['g']}SKIPPING{self.col['w']} check multiple for "
                f"this mod."
            )

        if check_preq and check_restrict and check_mult:
            logging.info(
                f"{self.chk} {self.py_txt} {self.col['g']}{mod_id} meets all criteria (Prerequisites, "
                f"Restrictions, Check Multiple), so is ALLOWED{self.col['w']}."
            )
            return True
        else:
            logging.info(
                f"{self.chk} {self.py_txt} {self.col['r']}{mod_id} fails one or more criteria "
                f"(Prerequisites, Restrictions, Check Multiple), so is DENIED{self.col['w']}."
            )
            return False

    def get_touched_skills(self, mod_id: str) -> list:
        """Requires mod_id (string); returns list.
        This method gets a list of all the skills touched by a mod_id. The SQLite db dumps this information out as a
        STRING rather than a LIST, so we must reconvert it to a LIST before returning it."""
        logging.info(f"{self.chk} {self.col['y']}[get_touched_skills]{self.col['w']}")

        clean_list = []
        logging.info(
            f"{self.chk} {self.sql_txt} Fetching list of skills TOUCHED by mod_id '{mod_id}'."
        )
        return_data = list(self.get_mod_info(mod_id, optional_fields="skills_touched"))
        # Convert STRING from DB back to LIST
        list_data = return_data[0][0].strip("][").split(", ")

        # list_data still has an issue in that each entry in enclosed in extra double quotation marks.
        # We need to remove those
        for x in list_data:
            x = x.replace('"', "")
            clean_list.append(x)

        logging.info(
            f"{self.chk} {self.sql_txt} List of skills {self.col['g']}TOUCHED{self.col['w']}"
            f" by mod_id '{mod_id}' is \n"
            f"                      {self.col['y']}->{self.col['w']} {clean_list}"
        )
        return_type = type(clean_list)
        logging.info(
            f"{self.chk} {self.py_txt} Data has been successfully been converted back to {return_type} "
            f"from STRING."
        )

        return clean_list

    def get_modded_skills(self, mod_id: str) -> dict:
        """Requires mod_id (string); returns dict.
        This method gets a list of all the skills modified by a mod_id.
        Available Options:
        mod_id: mod_id (string) of required mod"""
        logging.info(f"{self.chk} {self.col['y']}[get_modded_skills]{self.col['w']}")

        logging.info(
            f"{self.chk} {self.sql_txt} Fetching list of skills and effects "
            f"{self.col['g']}MODIFIED{self.col['w']} by mod_id '{mod_id}'."
        )
        return_data = self.get_mod_info(mod_id, optional_fields="effects")
        skills_modded = loads(return_data[0][0])  # Convert STRING from DB back to DICT
        logging.info(
            f"{self.chk} {self.sql_txt} List of skills and effects "
            f"{self.col['g']}MODIFIED{self.col['w']} by mod_id '{mod_id}' is \n"
            f"                      {self.col['y']}->{self.col['w']} {skills_modded}"
        )

        return_type = type(skills_modded)
        logging.info(
            f"{self.chk} {self.py_txt} Data has been successfully been converted back to {return_type} "
            f"from STRING."
        )

        return skills_modded

    def node_slot_already_free(
        self, mod_location: str, char: CharacterModel = None
    ) -> bool:
        """Requires: mod_location (string), character (CharacterModel); Returns bool.
        A simple method for checking if there is already a mod_id in a specific node slot. Returns True if slot is
        FREE, and False if filled."""
        # TODO: Work out why I'm not using this method...?
        logging.info(
            f"{self.chk} {self.col['y']}[node_slot_already_free]{self.col['w']}"
        )
        if not char:
            char = self.char

        logging.info(
            f"{self.chk} {self.py_txt} Checking the contents of node location:{mod_location} in CharacterModel "
            f"for {self.col['g']}{char.char_name}{self.col['w']} from DB."
        )

        retrieve_node = self.get_character_specific_node(char, mod_location)
        if retrieve_node:
            logging.info(
                f"{self.chk} {self.py_txt} Node_location: {self.col['y']}"
                f"'{mod_location}'{self.col['w']} is "
                f"{self.col['y']}FILLED{self.col['w']} by "
                f"{self.col['y']}{retrieve_node}{self.col['w']}. You will need to replace it."
            )
            return False
        else:
            logging.info(
                f"{self.chk} {self.py_txt} Node_location: {self.col['y']}"
                f"'{mod_location}'{self.col['w']} is "
                f"{self.col['g']}AVAILABLE{self.col['w']} for a new mod."
            )
            return True

    def _check_mod_for_user_defined_text(self, mod_id) -> bool:
        """Utility method that checks if a specified mod has the 'choose_text' field set to True"""
        logging.info(
            f"{self.chk} {self.col['y']}[_check_mod_for_user_defined_text]{self.col['w']}"
        )

        mod_choose_text = self.get_mod_info(
            mod_id=mod_id, optional_fields="choose_text"
        )
        if mod_choose_text[0][0] == 1:
            logging.info(
                f"{self.chk} {self.sql_txt} mod_id:{self.col['g']}{mod_id}{self.col['w']} "
                f"{self.col['g']}HAS{self.col['w']} 'choose_text' field."
            )
            return True
        else:
            logging.info(
                f"{self.chk} {self.sql_txt} mod_id:{self.col['g']}{mod_id}{self.col['w']} "
                f"{self.col['y']}DOES NOT{self.col['w']} have 'choose_text' field."
            )
            return False

    def save_user_defined_text(
        self,
        mod_id: str,
        mod_location: str,
        char: CharacterModel = None,
        choose_text: str = "",
        cli_print: bool = False,
    ) -> str:
        """Requires: mod_id (string), mod_location (string), char (CharacterModel), choose_text (string); returns bool.
        This method saves the player's defined text for mods that require additional information, such as
        t_enemy, for example, t_enemy("Emperor") in the CharacterModel. Because this is user-submitted text we need
        to make sure it is thoroughly purged of troublesome data.
        Step 1 check if mod_id has 'choose_text, else return False'
        Step 2 if it does process user_text and save it in form:
        char.text_replace_mods: {"mod_location": {"mod_id": "replacement_text"}
        Step 3 Save char, return true"""
        logging.info(
            f"{self.chk} {self.col['y']}[save_user_defined_text]{self.col['w']}"
        )
        if not char:
            char = self.char

        logging.info(
            f"{self.chk} {self.py_txt} Checking if mod_id:{self.col['g']}{mod_id}{self.col['w']} "
            f"in mod_location:{self.col['g']}{mod_location}{self.col['w']} in CharacterModel has "
            f"{self.col['g']}'choose text'{self.col['w']} field."
        )

        mod_choose_text = self._check_mod_for_user_defined_text(mod_id=mod_id)
        existing_text = char.text_replace_mods
        mod_name = self.get_mod_name(mod_id=mod_id)

        if mod_choose_text:
            # Process choose_text and make sure it is safe.
            if cli_print:
                user_text = input(
                    f"{self.info} {self.col['y']}The {self.col['w']}{mod_name}{self.col['y']} "
                    f"mod requires custom text. The current text is '{self.col['g']}{choose_text}"
                    f"{self.col['y']}'. Please enter your text here, or type 0 to skip: "
                )
                match user_text:
                    case "0":
                        pass
                    case _:
                        choose_text = user_text

            if choose_text:
                replacement_text = self.string_safe(
                    input_string=choose_text,
                    allow_hash=True,
                    parenthesis=True,
                    allow_hyphen=True,
                    allow_at=True,
                )
            elif not choose_text and mod_location in existing_text:
                logging.info(
                    f"{self.chk} {self.col['g']}{mod_location} found in {existing_text}{self.col['w']}"
                )
                replacement_text = existing_text[mod_location][mod_id]
            else:
                replacement_text = "*Replace This*"

            logging.info(
                f"{self.info} {self.py_txt} mod_id:{self.col['g']}{mod_id}{self.col['w']} "
                f"in mod_location:{self.col['g']}{mod_location}{self.col['w']} "
                f"{self.col['g']}DOES{self.col['w']} have 'choose_text' field. "
                f"Returning {self.col['g']}TRUE{self.col['w']} and entering processed user "
                f"text as: \n"
                f"                      {self.col['y']}->{self.col['w']} "
                f"{self.col['y']}{replacement_text}{self.col['w']}."
            )
            # Add replacement text to CharacterModel
            # {"mod_location": {"mod_id": "replacement_text"}
            char.text_replace_mods[mod_location] = {mod_id: replacement_text}

            if cli_print:
                print(
                    f"{self.info} {self.col['g']}The text for {self.col['w']}{mod_name}{self.col['g']} now says: "
                    f"'{self.col['w']}{self.string_pretty(replacement_text)}{self.col['g']}'"
                )

            # Update CharacterModel
            self.char = char
            return replacement_text
        else:
            logging.info(
                f"{self.info} {self.py_txt} mod_id:{self.col['g']}{mod_id}{self.col['w']} "
                f"in mod_location:{self.col['g']}{mod_location}{self.col['w']} "
                f"{self.col['y']}DOES NOT{self.col['w']} have 'choose_text' field. "
                f"Returning {self.col['y']}FALSE{self.col['w']}."
            )
            return ""

    def remove_user_defined_text(
        self, mod_id: str, mod_location: str, char: CharacterModel = None
    ) -> bool:
        """Requires: mod_id (string), mod_location (string), char (CharacterModel); returns bool.
        This simply removes the user supplied text entry for a mod that exists"""
        logging.info(
            f"{self.chk} {self.col['y']}[remove_user_defined_text]{self.col['w']}"
        )
        if not char:
            char = self.char

        logging.info(
            f"{self.chk} {self.py_txt} Checking if mod_id:{self.col['g']}{mod_id}{self.col['w']} "
            f"in mod_location:{self.col['g']}{mod_location}{self.col['w']} in CharacterModel has "
            f"{self.col['g']}'choose text'{self.col['w']} field."
        )

        mod_choose_text = self.get_mod_info(
            mod_id=mod_id, optional_fields="choose_text"
        )
        if mod_choose_text:
            if char.text_replace_mods[mod_location]:
                logging.info(
                    f"{self.chk} {self.py_txt} mod_id:{self.col['g']}{mod_id}{self.col['w']} "
                    f"in mod_location:{self.col['g']}{mod_location}{self.col['w']} "
                    f"{self.col['g']}DOES{self.col['w']} have 'choose_text' field."
                    f"{self.col['y']}REMOVING{self.col['w']} processed user text."
                )
                # Remove replacement text from CharacterModel
                # {"mod_location": {"mod_id": "replacement_text"}
                char.text_replace_mods[mod_location].pop(mod_id, None)

                # Update CharacterModel
                self.char = char
                return True
            else:
                logging.error(
                    f"{self.cross} {self.py_txt} There is NO saved text for mod_id:"
                    f"{self.col['y']}{mod_id}{self.col['w']} "
                    f"at mod_location:{self.col['y']}{mod_location}{self.col['w']} "
                )
                return False
        else:
            logging.info(
                f"{self.cross} {self.py_txt} mod_id:{self.col['g']}{mod_id}{self.col['w']} "
                f"in mod_location:{self.col['g']}{mod_location}{self.col['w']} "
                f"{self.col['r']}DOES NOT{self.col['w']} have 'choose_text' field."
            )
            return False

    def check_if_breed_mod(
        self, mod_id: str, mod_location: str, breed_name: str
    ) -> bool:
        """Requires: mod_id (str) mod_location (str), breed (str); returns bool"""
        logging.info(f"{self.chk} {self.col['y']}[check_if_breed_mod]{self.col['w']}")

        breed_dict = self._breed_match(breed=breed_name)
        if mod_location in breed_dict:
            if mod_id in breed_dict[mod_location]:
                logging.info(
                    f"{self.chk} {self.col['y']}mod_id:{mod_id} IS Breed Locked{self.col['w']}"
                )
                return True
            else:
                logging.info(
                    f"{self.chk} {self.col['g']}mod_id:{mod_id} is NOT Breed Locked{self.col['w']}"
                )
                return False
        else:
            logging.info(
                f"{self.chk} {self.col['g']}mod_id:{mod_id} is NOT Breed Locked{self.col['w']}"
            )
            return False

    def _breed_match(self, breed: str = "human") -> dict:
        """Requires: breed (str); returns dict.
        This simple method searches the Breeds Dict in BreedTemplates for the breed name and returns the relevant
        Breed dict."""
        logging.info(f"{self.chk} {self.col['y']}[_breed_match]{self.col['w']}")

        template: dict = {}

        for b in self.bt.breeds_list:
            if b == breed:
                template = getattr(self.bt, b)

        return template

    def apply_breed_template_to_char(
        self, breed: str = "human", char: CharacterModel = None
    ) -> CharacterModel:
        """This method applies the user selected Breed to the CharacterModel."""
        logging.warning(
            f"{self.chk} {self.col['y']}[apply_breed_template_to_char]{self.col['w']}"
        )
        if not char:
            char = self.char

        logging.warning(
            f"{self.chk} {self.py_txt} Apply the {self.col['y']}{breed}{self.col['w']} Breed template to "
            f"{self.col['g']}{char.char_name}{self.col['w']} "
        )

        template = self._breed_match(breed=breed)
        logging.warning(
            f"{self.chk} {self.py_txt} {self.col['m']}Breed Template:{template}{self.col['w']}"
        )

        if template["breed_n0"] in char.nodes["breed_n0"]:
            logging.warning(
                f"{self.chk} {self.py_txt} {self.col['y']}Breed ALREADY applied so skipping this step...{self.col['w']}"
            )
            return char
        else:
            for x in template:
                logging.warning(
                    f"{self.chk} {self.py_txt} {self.col['m']}ADDING BREED{self.col['w']} "
                    f"mod_id:{self.col['g']}{template[x]}{self.col['w']} to location:{self.col['y']}{x}{self.col['w']}."
                )
                char = self.apply_mod_to_character(
                    mod_id=template[x],
                    mod_location=x,
                    char=char,
                    ignore_pr=True,
                )
            char.breed = breed
            # Update CharacterModel
            self.char = char
            return char

    def remove_breed_template_from_char(
        self, breed: str = "human", char: CharacterModel = None
    ) -> CharacterModel:
        """This method removes the user selected Breed to the CharacterModel in preparation for adding a NEW Breed."""
        logging.info(
            f"{self.chk} {self.col['y']}[remove_breed_template_from_char]{self.col['w']}"
        )
        if not char:
            char = self.char

        logging.info(
            f"{self.chk} {self.py_txt} Removing {self.col['r']}{breed}{self.col['w']} Breed "
            f"template from {self.col['g']}{char.char_name}{self.col['w']} "
        )

        template = self._breed_match(breed=breed)

        logging.info(
            f"{self.chk} {self.py_txt} Template for {self.col['g']}{breed}{self.col['w']} Breed "
            f"is: \n{self.col['c']}{dumps(template, indent=4, default=str)}{self.col['w']} "
        )

        for x in template:
            logging.info(
                f"{self.chk} {self.py_txt} {self.col['r']}REMOVING{self.col['w']} mod_id:{template[x]} "
                f"from location:{x}."
            )
            char = self.remove_mod_from_character(
                mod_id=template[x], mod_location=x, char=char
            )

        # Update CharacterModel
        self.char = char
        return char

    def process_char(self, char: CharacterModel = None) -> CharacterModel:
        """
        Requires: char (CharacterModel); returns CharacterModel
        This method batch processes all the mods for a SINGLE character"""
        logging.info(f"{self.chk} {self.col['y']}[process_char]{self.col['w']}")
        if not char:
            char = self.char

        multiple_mods = self.process_char_mods_overrides_text(char=char)
        char = self.apply_multiple_mods_to_char(char=char, **multiple_mods)

        self.char = char
        return char

    def process_char_mods_overrides_text(self, char: CharacterModel = None) -> dict:
        """
        Requires: char (CharacterModel); returns dict
        This method processes an entire CharacterModel in one go by passing off a list of mods, overrides, and
        text to apply_multiple_mods_to_char method."""
        logging.info(
            f"{self.chk} {self.col['y']}[process_char_mods_overrides_text]{self.col['w']}"
        )
        if not char:
            char = self.char

        char_mods: dict = getattr(char, "nodes", {})
        text_replace_mods: dict = getattr(char, "text_replace_mods", {})
        stored_overrides: dict = getattr(char, "stored_overrides", {})
        multiple_mods: dict = {}
        char_breed = getattr(char, "breed", "human")
        breed_mods: dict = getattr(self.bt, char_breed, {})

        for mod in char_mods:
            if char_mods[mod]:
                full = False
                logging.info(
                    f"{self.chk} {self.py_txt} Adding {self.col['g']}{mod}={char_mods[mod]}{self.col['w']} to "
                    f"multiple_mod dict for batch processing character."
                )
                if mod in text_replace_mods:
                    text_replace = text_replace_mods[mod][char_mods[mod]]
                    full = True
                else:
                    text_replace = ""
                if char_mods[mod] in stored_overrides:
                    override = True
                    full = True
                else:
                    if mod in breed_mods:
                        override = False
                        full = True
                    else:
                        override = False

                if full:
                    multiple_mods[mod] = {
                        "mod_id": char_mods[mod],
                        "over": override,
                        "text": text_replace,
                    }
                else:
                    multiple_mods[mod] = char_mods[mod]

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['g']}multiple_mods = {dumps(multiple_mods, indent=4, default=str)}"
            f"{self.col['w']}"
        )

        return multiple_mods

    def apply_multiple_mods_to_char(
        self, char: CharacterModel, **mods_dict
    ) -> CharacterModel:
        """Requires: char (CharacterModel), mods_dict (**kwargs/dict); returns None.
        Method processes a dictionary of mod_locations: mod_ids, for example:
        self.apply_multiple_mods_to_char(char, control_edge_n0= "e_brave", cnsbooster_n0= "s_cnsbooster") etc.
        This is especially useful when you need to quickly feed a set of mods into a CharacterModel.
        To set override or replacement text,submit the mod_id as:
        control_edge_n0= {"mod_id":"e_brave", "over":True, "text":"Fish Fingers"}
        NOTE: 'over' and 'text' fields both optional, just use the ones you need :)"""
        logging.info(
            f"{self.chk} {self.col['y']}[apply_multiple_mods_to_char]{self.col['w']}"
        )

        count = 0

        logging.info(
            f"{self.chk} {self.py_txt} Applying {self.col['g']}MULTIPLE{self.col['w']} mods to "
            f"character:{self.col['g']}'{char.char_name}'{self.col['w']}."
        )

        additional_mods = self.check_multiple_mods_exist(mods_dict=mods_dict, char=char)

        if additional_mods:
            for arg in mods_dict:
                mod_id = mods_dict[arg]
                mod_location = arg
                count += 1
                over = False
                replace_text = ""

                if type(mods_dict[arg]) is dict:
                    mod_id = mods_dict[arg]["mod_id"]
                    if (
                        "over" in mods_dict[arg]
                        and type(mods_dict[arg]["over"]) is bool
                    ):
                        over = mods_dict[arg]["over"]
                    if "text" in mods_dict[arg] and type(mods_dict[arg]["text"]) is str:
                        replace_text = self.string_safe(mods_dict[arg]["text"])

                logging.info(
                    f"{self.chk} {self.py_txt} Applying {self.col['g']}MOD #{count}{self.col['w']}: "
                    f"{self.col['g']}{mod_id}{self.col['w']} to location:{self.col['y']}{mod_location}{self.col['w']}."
                )

                if over:
                    logging.info(
                        f"{self.chk} {self.py_txt} Override for {mod_id}: {self.col['y']}{over}{self.col['w']}."
                    )
                if replace_text:
                    logging.info(
                        f"{self.chk} {self.py_txt} Replace Text for {mod_id}: '{self.col['y']}{replace_text}"
                        f"{self.col['w']}'."
                    )

                char = self.apply_mod_to_character(
                    mod_id=mod_id,
                    mod_location=mod_location,
                    char=char,
                    ignore_pr=over,
                    override=over,
                    replace_text=replace_text,
                )

        return char

    def apply_mod_to_character(
        self,
        mod_id: str,
        mod_location: str,
        char: CharacterModel = None,
        live_char: LiveCharacterModel = None,
        ignore_pr: bool = False,
        replace_text: str = "",
        override: bool = False,
        cli_print: bool = False,
    ) -> CharacterModel:
        """Requires: mod_id (string), mod_location (string), character (CharacterModel), live_char (LiveCharacterModel),
        ignore_pr (bool), replace_text (string), override (bool); Returns CharacterModel.
        Add a single mod to a CharacterModel. If ignore_pr == True, then all prerequisite and restriction checks will
        be skilled. If override is set to True then anything is allowed anywhere - useful for GMs
        """
        logging.info(
            f"{self.chk} {self.col['y']}[apply_mod_to_character]{self.col['w']}"
        )
        if not char:
            char = self.char
            if char.stored_overrides[mod_id]:
                override = True
        if not live_char:
            live_char = self.live_char

        logging.info(
            f"{self.chk} {self.py_txt} Applying mod_id:{mod_id}{self.col['w']} "
            f"to mod_location:{self.col['g']}{mod_location}{self.col['w']} in CharacterModel for "
            f"{self.col['g']}{char.char_name}{self.col['w']} from DB."
        )
        if cli_print:
            mod_name = self.get_mod_name(mod_id=mod_id)
            print(
                f"{self.chk} {self.col['y']}Adding {self.col['w']}{mod_name}{self.col['y']} "
                f"to mod_location:{self.col['g']}{mod_location}{self.col['y']}...\n{self.col['w']} "
            )
        # Retrieve a list of all the character's applied mods from the CharacterModel
        mod_list = self.get_char_current_mods(char)

        # Get the official Breed name for various uses
        # breed_name = live_char.gamedata_name
        breed_name = char.breed

        if ignore_pr or override:
            # We skip Prerequisites and Restriction tests for Breed mods and breed_locked_mods or for override calls
            check_allowed = True
            breed_locked_skill = False
        else:
            check_allowed = self.check_mod_allowed(mod_id=mod_id, char_mods=mod_list)
            breed_locked_skill = self.check_if_breed_mod(
                mod_id=mod_id, mod_location=mod_location, breed_name=breed_name
            )

        if override and not breed_locked_skill:
            check_node_map = True
            override_mod_name = self.get_mod_name(mod_id=mod_id)
            # Add a note about the override to the LiveCharacter
            live_char = self.add_note(
                note_type="warning",
                note_value=f"Override was activated for {override_mod_name}, so prerequisites, restrictions, and "
                f"correct placement checks were skipped!",
                save_note=True,
                live_char=live_char,
            )
            # Save this override in the stored_overrides dict in CharacterModel
            stored_overrides = char.stored_overrides
            stored_override = getattr(stored_overrides, mod_id, None)
            if not stored_override:
                stored_overrides.update({mod_id: True})
                char.stored_overrides = stored_overrides
        else:
            # CHECK mod_id allowed in node slot
            check_node_map = self.check_mod_node_mapping(
                mod_id=mod_id, mod_location=mod_location
            )

        # We don't allow breed mods to be overwritten unless the override bool is set to True
        if not breed_locked_skill or override:
            if check_allowed and check_node_map:
                logging.info(
                    f"{self.chk} {self.py_txt} The mod_id:{self.col['g']}{mod_id}{self.col['w']} in CharacterModel "
                    f"for {self.col['g']}{char.char_name}{self.col['w']} is {self.col['g']}ALLOWED{self.col['w']}."
                )

                # Add mod_id to appropriate node
                logging.info(
                    f"{self.chk} {self.py_txt} {self.col['g']}ADDING{self.col['w']} mod_id:{self.col['g']}{mod_id}"
                    f"{self.col['w']} to nodes location:{self.col['g']}{mod_location}{self.col['w']} in "
                    f"CharacterModel for {self.col['g']}{char.char_name}{self.col['w']}."
                )

                # This is where we add the new mod_id to the mod_location in the nodes dict within CharacterModel
                logging.info(
                    f"{self.chk} {self.py_txt} {self.col['y']}char.nodes[mod_location]"
                    f"{self.col['w']} = {self.col['g']}{mod_location}[{mod_id}]{self.col['w']}"
                )
                # setattr(char.nodes, mod_location, mod_id)
                # Add mod_id to the specified node (as in give the character that mod)
                char.nodes[mod_location] = mod_id

                # From here we have to set custom text for placeholder replacement
                has_trm = hasattr(char, "text_replace_mods")
                if has_trm:
                    logging.info(
                        f"{self.chk} {self.py_txt} Mod Location:{mod_location} and live_char.text_replace_mods:"
                        f"{char.text_replace_mods}{self.col['w']}"
                    )

                    if mod_location in char.text_replace_mods:
                        logging.info(
                            f"{self.chk} {self.py_txt} Existing replacement text exists at mod_location:"
                            f"{self.col['y']}{mod_location}{self.col['w']}: "
                            f"{char.text_replace_mods[mod_location][mod_id]}'"
                        )
                        # TODO! XXX This is problematic. If a different mod_id exists at this mod_location this will
                        #  throw an error. So we will need to pop the current value first if present
                        if mod_id in char.text_replace_mods[mod_location]:
                            replace_text = char.text_replace_mods[mod_location][mod_id]
                        else:
                            logging.info(
                                f"{self.chk} {self.py_txt} A different mod_id:{self.col['y']}"
                                f"{char.text_replace_mods[mod_location]}{self.col['w']} "
                                f"already exists in text_replace_mods, so deleting that entry.'"
                            )
                            live_char.text_replace_mods.pop(mod_location, None)
                            # replace_text is then either blank or set by method call, above

                    # Save any user defined text -> Defaults to "To be decided"
                    ud_text = self.save_user_defined_text(
                        mod_id=mod_id,
                        mod_location=mod_location,
                        char=char,
                        choose_text=replace_text,
                        cli_print=cli_print,
                    )

                    # Update any user defined text by replacing the existing dict
                    if ud_text:
                        live_char.text_replace_mods[mod_location] = {mod_id: ud_text}

                    if replace_text:
                        replace_text = self.string_safe(
                            replace_text,
                            input_name="Replacement Text",
                            allow_hyphen=True,
                        )
                        logging.info(
                            f"{self.chk} {self.py_txt} Sending replacement text of {self.col['g']}'{replace_text}'"
                            f"{self.col['w']} to apply_mod_to_live_char...'"
                        )

                    updated_lc = self.apply_mod_to_live_character(
                        mod_id=mod_id,
                        mod_location=mod_location,
                        live_char=live_char,
                        replace_text_in=replace_text,
                    )

                    # Update live_char model
                    self.live_char = updated_lc

                    if cli_print:
                        mod_name = self.get_mod_name(mod_id=mod_id)
                        print(
                            f"{self.chk} {self.col['g']}Mod {self.col['w']}{mod_name}{self.col['g']} SUCCESSFULLY "
                            f"added to mod_location:{self.col['w']}{mod_location}{self.col['g']} for character:"
                            f"{self.col['w']}{char.char_name.title()}{self.col['g']}.\n"
                            f"{self.chk} {self.col['g']}You have {self.col['w']}{char.tp_unspent}{self.col['g']} "
                            f"unspent Talent Points remaining.{self.col['w']}"
                        )
                # Update char model
                self.char = char

                # We also return the modified char
                return char
            else:
                logging.info(
                    f"{self.chk} {self.py_txt} {self.col['r']}NOT ADDING{self.col['w']} "
                    f"mod_id:{self.col['g']}{mod_id}{self.col['w']} "
                    f"to nodes location:{self.col['g']}{mod_location}{self.col['w']} in "
                    f"CharacterModel for {self.col['g']}{char.char_name}{self.col['w']} "
                    f"due to {self.col['y']}failing{self.col['w']} one (or more) of the checks."
                )
                return char
        else:
            logging.info(
                f"{self.chk} {self.py_txt} {self.col['y']}NOT ADDING mod_id:{mod_id} "
                f"to nodes location:{mod_location} in CharacterModel because it is a BREED LOCKED SKILL, "
                f"so skipping...{self.col['w']}"
            )
            return char

    def remove_mod_from_character(
        self,
        mod_id: str,
        mod_location: str,
        char: CharacterModel = None,
        live_char: LiveCharacterModel = None,
        override: bool = False,
        cli_print: bool = False,
    ) -> CharacterModel:
        """Requires: mod_id (string), mod_location (string), character (CharacterModel),
        live_char (LiveCharacterModel); Returns CharacterModel.
        Removes a single mod from a CharacterModel
        """
        logging.info(
            f"{self.chk} {self.col['y']}[remove_mod_from_character]{self.col['w']}"
        )
        if not char:
            char = self.char
        if not live_char:
            live_char = self.live_char

        logging.info(
            f"{self.chk} {self.py_txt} Removing mod_id:{self.col['r']}{mod_id}{self.col['w']} "
            f"from mod_location:{self.col['g']}{mod_location}{self.col['w']} in CharacterModel for "
            f"{self.col['g']}{char.char_name}{self.col['w']}."
        )
        if cli_print:
            print(
                f"{self.chk} {self.col['y']}Removing mod_id:{self.col['r']}{mod_id}{self.col['w']} "
                f"from mod_location:{self.col['g']}{mod_location}{self.col['w']} from from "
                f"{self.col['w']}{char.char_name.title()}{self.col['w']}."
            )

        if char.nodes[mod_location] == mod_id:
            # REMOVE mod_id from appropriate node
            logging.info(
                f"{self.chk} {self.py_txt} {self.col['r']}REMOVING{self.col['w']} "
                f"mod_id:{self.col['g']}{mod_id}{self.col['w']} "
                f"from node location:{self.col['y']}{mod_location}{self.col['w']}."
            )

            # This is where we blank the mod_id from the mod_location in the nodes dict within CharacterModel
            check_breed = self.check_if_breed_mod(
                mod_id=mod_id, mod_location=mod_location, breed_name=char.breed
            )

            if check_breed and not override:
                logging.info(
                    f"{self.chk} {self.py_txt} {self.err_txt} {self.col['r']}Mod_id:{mod_id}"
                    f"from node location:{mod_location} is a Breed Mod, so you're not allowed to"
                    f"remove it!{self.col['w']}."
                )
                if cli_print:
                    print(
                        f"{self.cross} {self.err_txt} {self.col['r']}Mod_id:{mod_id}"
                        f"from node location:{mod_location} is a Breed Mod, so you're not allowed to"
                        f"remove it!{self.col['w']}."
                    )
            else:
                # Load the nodes, clear that mod_location and then save
                nodes: dict = char.nodes
                nodes[mod_location] = ""
                char.nodes = nodes
                # Remove any user defined text
                user_defined_text: dict = char.text_replace_mods
                if mod_location in user_defined_text:
                    removed = self.remove_user_defined_text(
                        mod_id=mod_id, mod_location=mod_location, char=char
                    )

                # Create a new, blank live_character, but don't save it to DB
                live_char = LiveCharacterModel(
                    live_char_id=live_char.live_char_id,
                    char_id=char.char_id,
                    char_name=char.char_name,
                    player_id=char.player_id,
                    player_name=live_char.player_name,
                    deleted=char.deleted,
                )

                # Process all the mods for the character
                char = self.process_char(char=char)

                # Make NEW live_char model in the DB
                live_char = self.new_or_update_live_char(
                    char_id=char.char_id,
                    player_id=char.player_id,
                    write_to_db=True,
                    live_char=live_char,
                )
                if override and not check_breed:
                    override_mod_name = self.get_mod_name(mod_id=mod_id)
                    # Add a note about the override to the LiveCharacter
                    live_char = self.add_note(
                        note_type="warning",
                        note_value=f"Override was activated for {override_mod_name}, so prerequisites, restrictions, "
                        f"and correct placement checks were skipped!",
                        save_note=True,
                        live_char=live_char,
                    )
                    # Save this override in the stored_overrides dict in CharacterModel
                    stored_overrides = char.stored_overrides
                    stored_override = getattr(stored_overrides, mod_id, None)
                    if not stored_override:
                        stored_overrides.update({mod_id: True})
                        char.stored_overrides = stored_overrides

                logging.info(
                    f"{self.chk} {self.py_txt} Mod_id:{self.col['y']}{mod_id}{self.col['w']} has "
                    f"{self.col['g']}SUCCESSFULLY{self.col['w']} been removed from node location:{self.col['y']}"
                    f"{mod_location}{self.col['w']}."
                )
                if cli_print:
                    print(
                        f"{self.chk} {self.col['g']}Mod_id:{self.col['w']}{mod_id}{self.col['g']} has "
                        f"SUCCESSFULLY been removed from node location:{self.col['w']}"
                        f"{mod_location}{self.col['g']}."
                    )

                # Update LiceCharacterModel
                self.live_char = live_char

                # Update CharacterModel model
                self.char = char

            # We also return the modified char
            return char
        else:
            logging.error(
                f"{self.cross} {self.py_txt} The mod_id:{self.col['y']}{mod_id}{self.col['w']} "
                f"{self.col['r']}IS NOT PRESENT{self.col['w']} "
                f"at node location:{self.col['y']}{mod_location}{self.col['w']} for "
                f"CharacterModel for {self.col['y']}{char.char_name}{self.col['w']}."
            )

            return char

    def applied_mods_check(
        self, mod_id: str, live_char: LiveCharacterModel = None, invert: bool = False
    ) -> bool:
        """Requires: mod_id (str), live_char (LiveCharacterModel), invert (bool) = False; returns bool
        This method checks if the indicated md_id has already been applied to the LiveCharacter stats, if it has
        the method returns False, if it has not yet been applied it returns True. If invert is set to True this method
        checks if an applied mod exists for removal purposes (so inverts the output while keeping the feedback for
        success still True)"""
        logging.info(f"{self.chk} {self.col['y']}[applied_mods_check]{self.col['w']}")

        if not live_char:
            live_char = self.live_char

        applied_mods = live_char.applied_mods
        logging.info(
            f"{self.chk} {self.sql_txt} Mods already applied to "
            f"live_character:{self.col['g']}'{live_char.char_name}'{self.col['w']} are: {applied_mods}."
        )
        if type(applied_mods) is None:
            am_list = []
        else:
            am_list = applied_mods

        if mod_id in applied_mods:
            if invert:
                logging.info(
                    f"{self.chk} {self.py_txt} The mod_id:{self.col['y']}{mod_id}{self.col['w']} "
                    f"{self.col['g']}HAS BEEN{self.col['w']} been applied, so proceeding..."
                )
                mod_continue = True
            else:
                logging.info(
                    f"{self.cross} {self.py_txt} The mod_id:{self.col['y']}{mod_id}{self.col['w']} "
                    f"has {self.col['r']}ALREADY{self.col['w']} been applied, so skipping..."
                )
                mod_continue = False
        else:
            if invert:
                logging.info(
                    f"{self.cross} {self.py_txt} The mod_id:{self.col['y']}{mod_id}{self.col['w']} "
                    f"is {self.col['r']}NOT{self.col['w']} in applied_mods list, so skipping..."
                )
                mod_continue = False
            else:
                logging.info(
                    f"{self.chk} {self.py_txt} The mod_id:{self.col['y']}{mod_id}{self.col['w']} "
                    f"is {self.col['g']}NOT{self.col['w']} in applied_mods list, so appending..."
                )
                am_list.append(mod_id)
                live_char.applied_mods = am_list
                mod_continue = True

        return mod_continue

    def _replace_live_text_placeholder(
        self,
        mod_id: str,
        mod_location: str,
        live_char: LiveCharacterModel = None,
        base_text: str = "",
    ) -> str:
        """This method is a simple utility method that replaces %TEXT% in mod_id information with the contents of
        base_text"""
        logging.info(
            f"{self.chk} {self.col['y']}[_replace_live_text_placeholder]{self.col['w']}"
        )
        if not live_char:
            live_char = self.live_char

        user_defined_text = self._check_mod_for_user_defined_text(mod_id=mod_id)
        if user_defined_text:
            logging.info(
                f"{self.chk} {self.py_txt} {self.col['g']}REPLACING{self.col['w']} placeholder "
                f"%TEXT% with live_character:{self.col['g']}'{base_text}'{self.col['w']}."
            )
            # text_replace_mods:{"mod_location": {"mod_id": "replacement_text"}
            # e.g. 'To be decided'
            replacement_text = live_char.text_replace_mods[mod_location][mod_id]
            replacement_text = self.string_pretty(replacement_text)
            # replaces %TEXT% with e.g. 'To be decided'
            return_text = base_text.replace("%TEXT%", replacement_text)
            return return_text
        else:
            logging.info(
                f"{self.chk} {self.py_txt} {self.col['y']}NO placeholder %TEXT% replacement required.{self.col['w']}"
            )
            return_text = base_text
            return return_text

    def write_all_mod_touched_entries(
        self, mod_id: str, touched_skills: list, live_char: LiveCharacterModel = None
    ) -> LiveCharacterModel:
        """This method runs write_touched_entry as many times as requires for each skill applied to a Live Character"""
        logging.info(
            f"{self.chk} {self.col['y']}[write_all_mod_touched_entries]{self.col['w']}"
        )
        if not live_char:
            live_char = self.live_char

        logging.info(f"{self.chk} {self.py_txt} Touched Skills: {touched_skills}")

        for skill in touched_skills:
            self.write_touched_entry(
                mod_id=mod_id, touched_skill=skill, live_char=live_char
            )

        self.live_char = live_char
        return live_char

    def write_touched_entry(
        self, mod_id: str, touched_skill: str, live_char: LiveCharacterModel = None
    ) -> LiveCharacterModel:
        """Requires: mod_id (str), touched_skill (str), live_char (LiveCharacterModel); returns LiveCharacterModel
        This method appends the MOD NAME to the _touched_by entry for each slot in LiveCharacter so the player
        can see a list of all the things that effected that stat"""
        logging.info(f"{self.chk} {self.col['y']}[write_touched_entry]{self.col['w']}")
        if not live_char:
            live_char = self.live_char

        mod_name = self.get_mod_name(mod_id=mod_id)
        ts_name = touched_skill + "_touched_by"
        touched_by = getattr(live_char, ts_name, None)
        if touched_by:
            touched_by = str(touched_by) + f", {mod_name}"
        else:
            touched_by = f"{mod_name}"
        setattr(live_char, ts_name, touched_by)

        self.live_char = live_char
        return live_char

    def apply_mod_to_live_character(
        self,
        mod_id: str,
        mod_location: str,
        live_char: LiveCharacterModel = None,
        replace_text_in: str = "",
        char: CharacterModel = None,
    ) -> LiveCharacterModel:
        """Requires mod_id (str), live_char (LiveCharacterModel); returns LiveCharacterModel
        This method applies (ADDS/APPENDS) ALL the effects of a SINGLE mod to the live_character.
        SpecialStats.protected_stats = stats that this should never touch (e.g. char_id)
        SpecialStats.replace_stats = stats that should be replaced by new value, not added/appended to (e.g. breed)"""
        logging.info(
            f"{self.chk} {self.col['y']}[apply_mod_to_live_character]{self.col['w']}"
        )
        if not char:
            char = self.char
        if not live_char:
            live_char = self.live_char

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['g']}APPLYING{self.col['w']} a SINGLE mod_id:"
            f"{self.col['g']}{mod_id}{self.col['w']} to "
            f"live_character:{self.col['g']}'{live_char.char_name}'{self.col['w']}."
        )
        # Show all the touched skills
        touched_skills = self.get_touched_skills(mod_id=mod_id)

        # Get alist of all the mod_ids that have already been applied, so we don't repeat ourselves
        # TODO: There is a problem here with mod_ids that are allowed to be taken more than once!
        # This returns True if safe to continue, False if not:
        mod_continue = self.applied_mods_check(mod_id=mod_id, live_char=live_char)
        if mod_continue:
            live_char = self.write_all_mod_touched_entries(
                mod_id=mod_id, touched_skills=touched_skills, live_char=live_char
            )

            live_char = self._if_mod_is_ets_add_note(mod_id=mod_id, live_char=live_char)

            # Update the modified skills
            skills = self.get_modded_skills(mod_id=mod_id)
            for x in skills:
                if x in self.ss.protected_stats:  # was live_char.protected_stats
                    logging.info(
                        f"{self.cross} {self.err_txt} The skill:{self.col['y']}{x}{self.col['w']} is marked as "
                        f"{self.col['r']}PROTECTED{self.col['w']} so skipping..."
                    )
                else:
                    if x == "replace_text":
                        # Move all of this to a helper method once working...
                        replace_base = skills[x].split("|", maxsplit=3)
                        r_node = replace_base[0]
                        r_text_id = replace_base[1]
                        r_text = replace_base[2].replace(")", "")
                        char.text_replace_mods[r_node] = {r_text_id: r_text}
                        # Overwrite this whole section with user input:

                        if replace_text_in:
                            safe_text = self.string_safe(
                                replace_text_in, allow_hyphen=True
                            )
                            char.text_replace_mods[mod_location] = {mod_id: safe_text}
                    else:
                        current_val = getattr(live_char, x)
                        logging.info(
                            f"{self.chk} {self.py_txt} {self.col['m']}CURRENT{self.col['w']} "
                            f"value for {self.col['m']}{x}{self.col['w']} = "
                            f"{self.col['m']}{current_val}{self.col['w']}"
                        )
                        if x in self.ss.replace_stats:
                            logging.info(
                                f"{self.chk} {self.py_txt} value is set to {self.col['y']}REPLACE"
                                f"{self.col['w']}, so replacing rather than appending."
                            )
                        else:
                            logging.info(
                                f"{self.chk} {self.py_txt} value is set to {self.col['g']}APPEND"
                                f"{self.col['w']}, so appending rather than replacing."
                            )

                        if type(current_val) == int:
                            if x in self.ss.replace_stats:
                                new_val = int(skills[x])
                            else:
                                logging.info(
                                    f"{self.chk} {self.py_txt} {self.col['m']}Current value = {current_val}, "
                                    f"adding {skills[x]}{self.col['w']}"
                                )
                                # To ensure correct calculations of minimum skills we also write to the
                                # value of the "_actual" version of each skill in special_stats.min_1_skills
                                if x in self.ss.min_1_skills:
                                    actual = x + "_actual"
                                    actual_val = getattr(live_char, actual, 0)
                                    new_val = actual_val + int(skills[x])
                                    setattr(live_char, actual, new_val)
                                # We do the same with Armour value actual (armour_value_actual)
                                elif x in self.ss.armour_values:
                                    actual = x + "_actual"
                                    logging.info(
                                        f"SETTING ACTUAL ARMOUR VALUE FOR {actual}"
                                    )
                                    actual_val = getattr(live_char, actual, 0)
                                    logging.info(f"CURRENT ACTUAL = {actual_val}")
                                    new_val = actual_val + int(skills[x])
                                    logging.info(f"NEW ACTUAL = {new_val}")
                                    setattr(live_char, actual, new_val)
                                else:
                                    new_val = current_val + int(skills[x])

                        elif type(current_val) == str:
                            new_text = self._replace_live_text_placeholder(
                                mod_id=mod_id,
                                mod_location=mod_location,
                                live_char=live_char,
                                base_text=skills[x],
                            )
                            # Was live_char.replace_stats
                            if x in self.ss.replace_stats:
                                new_val = new_text
                            else:
                                mod_name = self.get_mod_name(mod_id=mod_id)
                                if current_val:
                                    if x.endswith("general_note"):
                                        new_val = f"{current_val}. \n**{mod_name}:** {new_text}"
                                    else:
                                        new_val = f"{current_val}, {new_text}"
                                else:
                                    new_val = f"{new_text}"

                        elif type(current_val) == bool:
                            # This was saving true as "true", rather than just true... corrected now
                            if skills[x] == "true":
                                new_val = True
                            else:
                                new_val = False

                        elif type(current_val) == list:
                            new_val = current_val.append(skills[x])

                        else:
                            new_val = skills[x]

                        logging.info(
                            f"{self.chk} {self.py_txt} {self.col['g']}NEW{self.col['w']} "
                            f"value for {self.col['g']}{x}{self.col['w']} = "
                            f"{self.col['g']}{new_val}{self.col['w']}"
                        )

                        setattr(live_char, x, new_val)

        self.live_char = live_char
        return live_char

    def housekeeping(
        self, char: CharacterModel = None, live_char: LiveCharacterModel = None
    ) -> LiveCharacterModel:
        """Requires: char (CharacterModel), live_char (LiveCharacterModel); returns LiveCharacterModel.
        This method performs all the general housekeeping tasks for CharacterModel that don't fit anywhere else,
        such as applying the correct lifestyle"""
        logging.info(f"{self.chk} {self.col['y']}[char_housekeeping]{self.col['w']}")

        if not char:
            char = self.char
        if not live_char:
            live_char = self.live_char

        logging.info(
            f"{self.chk} {self.py_txt} Performing CharacterModel housekeeping..."
        )

        # Apply Sliverware Completion Bonuses
        live_char = self.calc_sliverware_completion_bonus(
            live_char=live_char, char=char
        )

        # Calc Permanent Wyld Injuries & Also Total Wyld Cancer
        live_char = self.calc_wyld_cancer_injuries(live_char=live_char)

        # Apply Lifestyle_mod_id
        lifestyle_mod_id = self.calc_lifestyle(live_char=live_char)
        logging.info(
            f"{self.chk} {self.py_txt} Set lifestyle_mod_id:{self.col['g']}{lifestyle_mod_id}{self.col['w']}."
        )
        self.apply_lifestyle_mod_id(lifestyle_mod_id=lifestyle_mod_id, char=char)

        # Skill Masteries
        live_char = self.set_skill_masteries(char=char, live_char=live_char)

        # Skill Minimums
        live_char = self.set_skill_minimums(live_char=live_char)

        # Recalculate initiative
        live_char = self.calc_live_char_initiative(live_char=live_char)

        # Recalculate Wound Thresholds for Physical, Smarts, Resources, Wyld and Divinity
        live_char = self.calc_live_char_wound_thresholds(live_char=live_char)

        # Check all AVs are 2 or greater and less than max_av allowed:
        live_char = self.set_armour_value_caps(live_char=live_char)

        # Bonus Languages
        live_char = self.calc_bonus_languages(live_char=live_char)

        # Set Secondary Info (Weapons, Gear, Contact, Missions, Commendations, Reprimands etc)
        live_char = self.set_secondary_info(live_char=live_char, char=char)

        # Append any saved notes
        live_char = self.get_saved_notes(live_char=live_char, char=char)

        # Calculate Current TPs and available TPs (this returns a tuple of (char, live_char):
        tp_calc = self.calc_talent_points(char=char, live_char=live_char)
        char = tp_calc[0]
        live_char = tp_calc[1]

        self.live_char = live_char
        self.char = char
        return live_char

    def set_char_int_val(
        self,
        user_key: str,
        user_val: int = -1,
        nice_key: str = "",
        char_or_live: bool = True,
        replace_or_add: bool = True,
        char: CharacterModel = None,
        live_char: LiveCharacterModel = None,
        cli_query: bool = False,
        cli_print: bool = False,
    ) -> tuple:
        """A generic method for setting character's int value for some something such as tp_mission, tp_create etc.
        Allows replacing values or adding old and new values. If you set cli_query to True the method will request
        user input for user_val.
        user_key = key
        user_val = value
        char_or_live = if True, load from CharacterModel, if false load from Live_characterModel
        replace_or_add = if True REPLACE existing value, if false ADD to existing value
        cli_query = if True, request user input
        cli_print = if True, print feedback
        Returns a tuple of (char, live_char)"""
        logging.info(f"{self.chk} {self.col['y']}[set_char_int_val]{self.col['w']}")
        current_val = None

        if not char:
            char = self.char
        if not live_char:
            live_char = self.live_char

        if nice_key:
            key_title = self.string_pretty(nice_key)
        else:
            key_title = self.string_pretty(user_key)

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['y']}Setting value for {self.col['w']}{key_title}"
        )

        if char_or_live:
            if hasattr(char, user_key):
                current_val = getattr(char, user_key, 0)
        else:
            if hasattr(live_char, user_key):
                current_val = getattr(live_char, user_key, 0)

        if current_val >= 0:
            if cli_query or user_val == -1:
                is_digit = False
                while not is_digit:
                    print(
                        f"{self.l_break}"
                        f"{self.ind2}{self.col['w']}SET {key_title.upper()}{self.col['y']}"
                        f"{self.l_break}"
                    )
                    print(
                        f"{self.info} {self.col['y']}The current value of {self.col['w']}{char.char_name.title()}'s "
                        f"{self.col['g']}{key_title}{self.col['y']} is "
                        f"{self.col['w']}{current_val}{self.col['y']}.{self.col['w']}\n"
                    )
                    choice_text = (
                        f"{self.chk} {self.col['y']}Please enter the value you wish to change it to "
                        f"(leave blank and press enter to keep the current value):{self.col['w']} "
                    )

                    user_option = input(f"{choice_text}")
                    if user_option is None:
                        logging.info(
                            f"{self.chk} {self.py_txt} {self.col['y']}User input is blank, therefore use"
                            f"CURRENT VALUE"
                        )
                        user_val = current_val
                        is_digit = True
                    else:
                        if user_option.isdigit():
                            logging.info(
                                f"{self.chk} {self.py_txt} {self.col['y']}User input IS DIGIT. Proceed."
                            )
                            user_val = int(user_option)
                            is_digit = True
                        elif user_option == "":
                            logging.info(
                                f"{self.chk} {self.py_txt} {self.col['y']}User input is blank, therefore use"
                                f"CURRENT VALUE"
                            )
                            user_val = current_val
                            is_digit = True
                        else:
                            logging.info(
                                f"{self.chk} {self.py_txt} {self.col['y']}User input is not a digit. Restarting..."
                            )
                            print(
                                f"\n{self.cross} {self.col['r']}ERROR: You entered: "
                                f"{self.col['w']}'{user_option}'{self.col['r']}\n"
                            )

            if user_val >= 0:
                if current_val != user_val:
                    logging.info(
                        f"{self.info} {self.py_txt} {self.col['w']}{key_title}"
                        f"{self.col['g']} of {self.col['b']}{current_val}{self.col['g']} does not match entered "
                        f"value of {self.col['c']}{user_val}{self.col['g']} for character:"
                        f"{self.col['w']}'{char.char_name}'{self.col['g']}. "
                    )
                    if cli_print:
                        print(
                            f"\n{self.info} {self.col['w']}{key_title}"
                            f"{self.col['g']} of {self.col['w']}{current_val}{self.col['g']} has been changed to "
                            f"{self.col['w']}{user_val}{self.col['g']} for "
                            f"{self.col['w']}{char.char_name.title()}{self.col['g']}.{self.col['w']} "
                        )
                    if replace_or_add:
                        # Replace
                        logging.info(
                            f"{self.chk} {self.py_txt} REPLACING existing value with "
                            f"{self.col['w']}{user_val}{self.col['g']}.{self.col['w']}"
                        )
                        if cli_print:
                            print(
                                f"\n{self.chk} {self.col['g']}Updating {self.col['w']}{key_title}{self.col['g']} "
                                f"value to {self.col['w']}{user_val}{self.col['g']}.{self.col['w']}"
                            )
                        if hasattr(char, user_key):
                            setattr(char, user_key, user_val)
                        if hasattr(live_char, user_key):
                            setattr(live_char, user_key, user_val)
                    else:
                        # Add
                        new_val = current_val + user_val
                        logging.info(
                            f"{self.chk} {self.py_txt} ADDING to existing value for a new total of "
                            f"{self.col['w']}{new_val}{self.col['g']}.{self.col['w']}"
                        )
                        if cli_print:
                            print(
                                f"{self.chk} {self.col['g']}Updating {self.col['w']}{key_title}{self.col['g']} value "
                                f"for a new total of {self.col['w']}{new_val}{self.col['g']}.{self.col['w']}"
                            )
                        if hasattr(char, user_key):
                            setattr(char, user_key, new_val)
                        if hasattr(live_char, user_key):
                            setattr(live_char, user_key, new_val)

                        if cli_print:
                            print(
                                f"{self.info} {self.col['y']}Don't forget to save "
                                f"{self.col['w']}'{char.char_name}'{self.col['g']}!{self.col['w']}"
                            )

                    live_char = self.housekeeping(char=char, live_char=live_char)
                    char = self.char
                else:
                    # current_Val and user_val match, so skip
                    logging.info(
                        f"{self.chk} {self.py_txt} {self.col['g']}Current value of {self.col['w']}{key_title}"
                        f"{self.col['g']} and new value MATCH so leaving current value unchanged for "
                        f"{self.col['g']}'{char.char_name}'{self.col['w']}."
                    )
                    if cli_print:
                        print(
                            f"{self.info} {self.col['g']}Current value of {self.col['w']}{key_title}"
                            f"{self.col['g']} and new value MATCH so leaving current value unchanged for "
                            f"{self.col['g']}'{char.char_name}'{self.col['w']}."
                        )
            else:
                # user_val is less than 0
                logging.info(
                    f"{self.cross} {self.err_txt} {self.col['r']}"
                    f"Provided user_val must be an integer of 0 or greater."
                )
                if cli_print:
                    print(
                        f"\n{self.cross} {self.col['r']}ERROR: You must enter an integer value of 0 or greater for "
                        f"{self.col['w']}'{user_key}'{self.col['r']}\n"
                    )
        else:
            # current_val doesn't exist / is less than zero
            logging.info(
                f"{self.cross} {self.err_txt} {self.col['r']}"
                f"Provided user_val must be an integer of 0 or greater."
            )
            if cli_print:
                print(
                    f"\n{self.cross} {self.col['r']}ERROR: You must enter an integer value of 0 or greater for "
                    f"{self.col['w']}'{user_key}'{self.col['r']}\n"
                )

        return char, live_char

    def calc_talent_points(
        self, char: CharacterModel = None, live_char: LiveCharacterModel = None
    ) -> tuple:
        """A simple method for calculating the character's total talent points and how many remain to be spent.
        Returns a tuple of (char, live_char)"""
        logging.info(f"{self.chk} {self.col['y']}[calc_talent_points]{self.col['w']}")
        if not char:
            char = self.char
        if not live_char:
            live_char = self.live_char

        # Get information on Talent Points to spend form live_char and char:
        tp_total: int = getattr(char, "tp_total", 0)
        tp_create: int = getattr(char, "tp_create", 0)
        tp_missions: int = getattr(char, "tp_missions", 0)
        tp_bonus: int = getattr(char, "tp_bonus", 0)
        tp_unspent: int = getattr(char, "tp_unspent", 0)
        tp_spent: int = getattr(char, "tp_spent", 0)
        # Breed TP corrections
        breed_tp_spent: int = getattr(char, "breed_tp_spent", 0)
        breed_tp_bonus: int = getattr(char, "breed_tp_bonus", 0)
        logging.info(
            f"tp_total: {tp_total}\n"
            f"tp_create: {tp_create}\n"
            f"tp_missions: {tp_missions}\n"
            f"tp_bonus: {tp_bonus}\n"
            f"tp_unspent: {tp_unspent}\n"
            f"tp_spent: {tp_spent}\n"
            f"breed_tp_spent: {breed_tp_spent}\n"
            f"breed_tp_bonus: {breed_tp_bonus}\n"
        )

        # If any of the values of TP elements in live_char and char are different update them
        """
        tp_total: int = 0
        tp_spent: int = 0
        tp_unspent: int = 0
        tp_create: int = 30
        tp_missions: int = 0
        tp_bonus: int = 0
        breed_tp_spent: int = 0
        breed_tp_bonus: int = 0
        """
        # Calculate Total Talent Points
        tp_new_total: int = tp_create + tp_bonus + tp_missions - breed_tp_bonus
        logging.info(f"tp_new_total: {tp_new_total}\n")
        setattr(char, "tp_total", tp_new_total)

        if hasattr(live_char, "tp_total"):
            logging.info(f"Live character has tp_total")
            setattr(live_char, "tp_total", tp_new_total)
            logging.info(f"{live_char.tp_total}")
        else:
            logging.info(f"Live character does not have tp_total!")

        # Calculate Unspent TPs
        tp_new_unspent = tp_unspent - tp_spent + breed_tp_spent
        tp_change = tp_new_total - tp_new_unspent
        tp_unspent_updated = tp_new_unspent + tp_change
        logging.info(f"tp_unspent_updated: {tp_unspent_updated}\n")
        setattr(char, "tp_unspent", tp_unspent_updated)
        setattr(live_char, "tp_unspent", tp_unspent_updated)

        setattr(live_char, "tp_create", tp_create)
        setattr(live_char, "tp_missions", tp_missions)
        setattr(live_char, "tp_bonus", tp_bonus)
        setattr(live_char, "tp_spent", tp_spent)
        setattr(live_char, "breed_tp_spent", breed_tp_spent)
        setattr(live_char, "breed_tp_bonus", breed_tp_bonus)

        self.char = char
        self.live_char = char

        return char, live_char

    def remove_mod_from_live_character(
        self, mod_id: str, live_char: LiveCharacterModel = None
    ) -> LiveCharacterModel:
        """
        THIS METHOD HAS BEEN REMOVED. COMMENTED OUT FOR NOW, BUT WILL BE DELETED!
        Requires mod_id (str), live_char (LiveCharacterModel); returns LiveCharacterModel
        This method removes (DELETES/REMOVES) ALL the effects of a SINGLE mod to the live_character.
        SpecialStats.protected_stats = stats that this should never touch (e.g. char_id)
        SpecialStats.replace_stats = stats that should be replaced by new value, not added/appended to (e.g. breed)"""
        logging.info(
            f"{self.chk} {self.col['y']}[remove_mod_from_live_character]{self.col['w']}"
        )
        """
        special_stats = SpecialStats()

        if not live_char:
            live_char = self.live_char

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['r']}REMOVING{self.col['w']} mod_id:{self.col['y']}{mod_id}"
            f"{self.col['w']} from live_character:{self.col['g']}'{live_char.char_name}'{self.col['w']}."
        )
        # Show all the touched skills
        self.get_touched_skills(mod_id=mod_id)

        # This returns True if safe to continue, False if not:
        mod_continue = self.applied_mods_check(
            mod_id=mod_id, live_char=live_char, invert=True
        )
        if mod_continue:
            # Mod has been applied
            # Update the modified skills
            skills = self.get_modded_skills(mod_id=mod_id)
            for x in skills:
                if x in special_stats.protected_stats:
                    logging.error(
                        f"{self.chk} {self.err_txt} The skill:{self.col['y']}{x}{self.col['w']} is marked as "
                        f"{self.col['r']}PROTECTED{self.col['w']} so skipping..."
                    )
                else:
                    if x in special_stats.replace_stats:
                        logging.info(
                            f"{self.chk} {self.py_txt} value is set to {self.col['y']}REPLACE{self.col['w']}, "
                            f"so replacing rather than replacing in existing string."
                        )
                    else:
                        logging.info(
                            f"{self.chk} {self.py_txt} value is set to {self.col['g']}APPEND{self.col['w']}, "
                            f"so deleting from existing string rather than replacing."
                        )

                    current_val = getattr(live_char, x)
                    logging.info(
                        f"{self.chk} {self.py_txt} {self.col['y']}CURRENT{self.col['w']} value for {self.col['y']}{x}"
                        f"{self.col['w']} = {self.col['y']}{current_val}{self.col['w']}"
                    )
                    if type(current_val) == int:
                        if x in special_stats.replace_stats:
                            new_val = 0
                        else:
                            new_val = current_val - int(skills[x])
                    elif type(current_val) == str:
                        if x in special_stats.replace_stats:
                            new_val = ""
                        else:
                            phrase_replace = f"{skills[x]}. "
                            new_val = current_val.replace(phrase_replace, "")
                        # Clean up rogue commas...
                        new_val = new_val.replace(", ,", ",")
                        new_val = new_val.replace(",,", ",")
                    elif type(current_val) == bool:
                        if current_val:
                            new_val = True
                        else:
                            new_val = False
                    elif type(current_val) == list:
                        new_val = current_val.delete(skills[x])
                    else:
                        new_val = 0

                    logging.info(
                        f"{self.chk} {self.py_txt} {self.col['g']}UPDATED{self.col['w']} value for {self.col['g']}{x}"
                        f"{self.col['w']} = {self.col['g']}{new_val}{self.col['w']}"
                    )
                    live_char.applied_mods.remove(mod_id)
                    setattr(live_char, x, new_val)
                    self.live_char = live_char
                    return live_char
        else:
            logging.info(
                f"{self.chk} {self.err_txt} The mod_id:{self.col['y']}{mod_id}{self.col['w']} "
                f"{self.col['r']}IS NOT{self.col['w']} present in applied_mods, so skipping..."
            )

            return live_char"""
        return live_char

    def apply_lifestyle_mod_id(
        self, lifestyle_mod_id: str, char: CharacterModel = None
    ) -> None:
        """Requires: lifestyle_mod_id (str), char (CharacterModel); returns none.
        This method applies the lifestyle mod_id generated by calc_lifestyle to the CharacterModel."""
        logging.info(
            f"{self.chk} {self.col['y']}[apply_lifestyle_mod_id]{self.col['w']}"
        )

        if not char:
            char = self.char

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['g']}APPLYING{self.col['w']} lifestyle mod_id "
            f"of {self.col['g']}{lifestyle_mod_id}{self.col['w']} "
            f"to character:{self.col['g']}'{char.char_name}'{self.col['w']}."
        )

        # Actually apply the lifestyle mod_id to the Character's nodes:
        self.apply_mod_to_character(
            mod_id=lifestyle_mod_id, mod_location="lifestyle_n0", char=char
        )

    def get_character_nodes(self, character: CharacterModel) -> dict:
        """Requires: CharacterModel; returns dict.
        This method accepts a CharacterModel and creates a dict contained in the nodes dict
        and returns it."""
        logging.info(
            f"{self.chk} {self.col['y']}[retrieve_character_nodes]{self.col['w']}"
        )

        logging.info(
            f"{self.chk} {self.py_txt} Loading the nodes dict new dict for character "
            f"{self.col['g']}{character.char_name}{self.col['w']} from DB."
        )

        char_node = character.nodes
        logging.info(
            f"{self.chk} {self.py_txt} Output of the nodes dict in the CharacterModel for "
            f"{self.col['g']}{character.char_name}{self.col['w']} is:"
            f"\n                      {self.col['g']}{char_node}{self.col['w']}"
        )

        return char_node

    def get_character_specific_node(
        self, char: CharacterModel, node_wanted: str
    ) -> str:
        """Requires: CharacterModel, node_wanted; returns str.
        This method accepts a CharacterModel and string for the specific node wanted and returns a string of that
        node's value.
        Available Options:
        character: CharacterModel
        node_wanted: str = 'breed_n0'"""
        logging.info(
            f"{self.chk} {self.col['y']}[retrieve_specific_character_node]{self.col['w']}"
        )

        logging.info(
            f"{self.chk} {self.py_txt} Loading the details of a specific node for character "
            f"{self.col['g']}{char.char_name}{self.col['w']} from DB and returning as a string "
            f"of the mod_id in the node slot."
        )

        char_specific_node = char.nodes[node_wanted]
        if char_specific_node:
            logging.info(
                f"{self.chk} {self.py_txt} Output of node:{self.col['g']}{node_wanted}"
                f"{self.col['w']} in the CharacterModel for "
                f"{self.col['g']}{char.char_name}{self.col['w']} is: "
                f"{self.col['g']}'{char_specific_node}'{self.col['w']}"
            )
        else:
            logging.info(
                f"{self.chk} {self.py_txt} Output of node:{self.col['g']}{node_wanted}"
                f"{self.col['w']} in the CharacterModel for "
                f"{self.col['g']}{char.char_name}{self.col['w']} is: "
                f"{self.col['y']}NULL{self.col['w']}. There is no mod_id in this node slot."
            )

        return char_specific_node

    def get_char_current_mods(
        self, char: CharacterModel = None, cli_print: bool = False
    ) -> list:
        """Requires: CharacterModel; returns list.
        This method accepts a CharacterModel and creates a new list of the VALUES contained in the nodes dict
        and returns it. Useful for quickly parsing to see if a mod_id is in play already for conflicts or multiple
        copies."""
        logging.info(
            f"{self.chk} {self.col['y']}[retrieve_character_nodes_values]{self.col['w']}"
        )

        if not char:
            char = self.char

        output_list: list = []

        logging.info(
            f"{self.chk} {self.py_txt} Loading the values of the nodes dict into a new list for character "
            f"{self.col['g']}{char.char_name}{self.col['w']} from DB."
        )

        char_node = char.nodes.values()
        char_node_values = list(char_node)

        for x in char_node_values:
            if x:
                output_list.append(x)

        logging.debug(
            f"{self.chk} {self.py_txt} Output list of VALUES of the nodes dict in the CharacterModel for "
            f"{self.col['g']}{char.char_name}{self.col['w']} is:"
            f"\n                      {self.col['g']}{output_list}{self.col['w']}"
        )

        if cli_print:
            print(
                f"{self.info} {self.col['y']}Current list of mods that "
                f"{self.col['w']}{self.string_pretty(input_text=char.char_name)}{self.col['y']} has is: \n"
                f"{self.col['b']}{dumps(output_list, indent=4)}{self.col['w']}"
            )

        return output_list

    @staticmethod
    def _resources_influence_code(res_inf: int) -> int:
        """Requires: res_inf (int); returns str.
        This is a simple quick and dirty method that simplifies ranges of the Resources (Influence) skill down to
        a letter value of A (highest) to D (lowest)"""

        match res_inf:
            case 1 | 2 | 3 | 4:
                return_code = 4
            case 5 | 6 | 7:
                return_code = 3
            case 8 | 9 | 10 | 11:
                return_code = 2
            case _:
                return_code = 1

        return return_code

    def calc_bonus_languages(self, live_char: LiveCharacterModel) -> LiveCharacterModel:
        """Requires: live_char (LiveCharacterModel); returns int
        This method calculates how many bonus languages a character should have"""
        logging.info(f"{self.chk} {self.col['y']}[calc_bonus_languages]{self.col['w']}")

        total_languages = live_char.bonus_languages + 2

        # Each language adds one to language_count
        if live_char.language_count > total_languages:
            # Too many languages
            live_char = self.add_note(
                note_type="warning",
                note_value=f"Character has TOO MANY languages, they should have {total_languages} "
                f"but actually have {live_char.language_count}",
                save_note=True,
                live_char=live_char,
            )
        elif live_char.language_count < total_languages:
            # Too few languages
            live_char = self.add_note(
                note_type="warning",
                note_value=f"Character has TOO FEW languages, they should have {total_languages} "
                f"but actually have {live_char.language_count}",
                save_note=True,
                live_char=live_char,
            )
        else:
            live_char = self.add_note(
                note_type="general",
                note_value=f"Character is fluent in {total_languages} languages",
                save_note=True,
                live_char=live_char,
            )

        live_char.total_languages = total_languages

        return live_char

    def apply_sliver_complete_mod_id(
        self,
        mod_id: str,
        mod_location: str,
        char: CharacterModel = None,
        live_char: LiveCharacterModel = None,
    ) -> CharacterModel:
        """Requires: mod_id (string), mod_location (string), char (CharacterModel), live_char (LiveCharacterModel)
        returns CharacterModel.
        This method applies/removes the sliverware complete mods to the CharacterModel."""
        logging.info(
            f"{self.chk} {self.col['y']}[apply_sliverware_complete_mod_id]{self.col['w']}"
        )

        if not char:
            char = self.char

        if not live_char:
            live_char = self.live_char

        char.nodes[mod_location] = live_char.sliver_complete[mod_location]
        if char.nodes[mod_location]:
            logging.warning(
                f"{self.chk} {self.py_txt} Applying mod_id:{self.col['g']}{mod_id}{self.col['w']}"
                f"at location:{self.col['y']}{mod_location}{self.col['w']}."
            )
            live_char = self.apply_mod_to_live_character(
                mod_id=mod_id,
                mod_location=mod_location,
                live_char=live_char,
            )

        self.char = char
        self.live_char = live_char
        return char

    def calc_sliverware_completion_bonus(
        self, live_char: LiveCharacterModel = None, char: CharacterModel = None
    ) -> LiveCharacterModel:
        """
        Requires: live_char (LiveCharacterModel), char (CharacterModel); returns LiveCharacterModel.
        This method adds an additional mod_id to the character for a completed Sliverware set and also
        removes it if it is no longer completed..."""
        logging.info(
            f"{self.chk} {self.col['y']}[calc_sliverware_completion_bonus]{self.col['w']}"
        )

        bscm = self.bscm

        if not char:
            char = self.char
        if not live_char:
            live_char = self.live_char

        sliverware_complete = bscm.sliverware_complete

        for sl_complete in sliverware_complete:
            comp = getattr(live_char, sl_complete, 0)
            if comp > 6:
                location_name = f"{sl_complete}_n0"
                mod_id_name = sl_complete.replace("s_", "n_")
                mod_id_name2 = mod_id_name.replace("_n0", "")
                live_char.sliver_complete[location_name] = mod_id_name2
                print(f"live_char.sliver_complete['{location_name}']='{mod_id_name2}'")
                logging.warning(
                    f"{self.chk} {self.py_txt} {self.col['g']}sl_complete{self.col['w']}"
                    f"={self.col['g']}>6{self.col['w']} so is {self.col['g']}COMPLETE{self.col['w']}. Adding mod_id:"
                    f"{self.col['g']}{mod_id_name2}{self.col['w']} to location:{self.col['y']}{location_name}"
                    f"{self.col['w']}."
                )

                # Apply the mods to the CharacterModel
                char = self.apply_sliver_complete_mod_id(
                    mod_id=mod_id_name2,
                    mod_location=location_name,
                    char=char,
                    live_char=live_char,
                )
                self.live_char = live_char
                self.char = char

        return live_char

    def calc_lifestyle(self, live_char: LiveCharacterModel = None) -> str:
        """This method calculates what lifestyle a character should have based on their Resources (Influence) and
        Social Class and returns the name of the lifestyle mod_id that the system will need to add to their
        CharacterModel. Lifestyles are a list in NodeMap with 0 being Upper Zen and 6 being Undercity."""
        logging.info(f"{self.chk} {self.col['y']}[calc_lifestyle]{self.col['w']}")

        if not live_char:
            live_char = self.live_char

        bscm = self.bscm
        # Use this list to avoid hard coding the mod_ids...
        lifestyle_list: list = bscm.lifestyles

        logging.info(
            f"{self.chk} {self.py_txt} Calculating {self.col['g']}Lifestyle{self.col['w']} "
            f"for character {self.col['g']}{live_char.char_name}{self.col['w']} from DB."
        )

        resources_influence = live_char.resources + live_char.influence
        if resources_influence < 1:
            resources_influence = 1
        # res_code is a number code with 1 being best and 4 being worst, lifestyle[0] is best, lifestyle[6] is worst
        res_code = self._resources_influence_code(res_inf=resources_influence)
        social_class = live_char.social_class

        # Some injuries can alter lifestyle. A positive change = worse lifestyle!
        lifestyle_change = getattr(live_char, "lifestyle_change", 0)

        if lifestyle_change > 0:
            res_code = res_code + lifestyle_change
            logging.warning(
                f"{self.chk} {self.py_txt} {self.col['y']}Lifestyle was altered by one or more mods{self.col['w']}"
            )

        match social_class:
            case "Underclass":
                match res_code:
                    case 1:
                        lifestyle = lifestyle_list[3]
                    case 2:
                        lifestyle = lifestyle_list[4]
                    case 3:
                        lifestyle = lifestyle_list[5]
                    case _:
                        lifestyle = lifestyle_list[6]
            case "Lower Class":
                match res_code:
                    case 1:
                        lifestyle = lifestyle_list[2]
                    case 2:
                        lifestyle = lifestyle_list[3]
                    case 3:
                        lifestyle = lifestyle_list[4]
                    case _:
                        lifestyle = lifestyle_list[5]
            case "Upper Class" | "Patrician Class":
                match res_code:
                    case 1:
                        lifestyle = lifestyle_list[0]
                    case 2:
                        lifestyle = lifestyle_list[1]
                    case 3:
                        lifestyle = lifestyle_list[2]
                    case _:
                        lifestyle = lifestyle_list[3]
            case "Noble Class":
                match res_code:
                    case 1 | 2:
                        lifestyle = lifestyle_list[0]
                    case 3:
                        lifestyle = lifestyle_list[1]
                    case _:
                        lifestyle = lifestyle_list[2]
            case _:
                # Middle Class
                match res_code:
                    case 1:
                        lifestyle = lifestyle_list[1]
                    case 2:
                        lifestyle = lifestyle_list[2]
                    case 3:
                        lifestyle = lifestyle_list[3]
                    case _:
                        lifestyle = lifestyle_list[4]

        logging.info(
            f"{self.chk} {self.py_txt} Lifestyle is {self.col['g']}{lifestyle}{self.col['w']}."
        )
        return lifestyle

    def calc_live_char_initiative(
        self, live_char: LiveCharacterModel = None
    ) -> LiveCharacterModel:
        """
        Requires: live_char (LiveCharacterModel); returns LiveCharacterModel
        This method quickly calculates a live_character's initiative stat from a lookup table to minimise division
        Initiative is calculated thus:
        (physical + smarts + resources) /  + 1 per point of faith (in gamedata) + 1 per point of sense (in gamedata)
         + initiative_bonus
        """
        logging.info(
            f"{self.chk} {self.col['y']}[calc_live_char_initiative]{self.col['w']}"
        )

        if not live_char:
            live_char = self.live_char

        logging.info(
            f"{self.chk} {self.py_txt} Calculating {self.col['g']}initiative stat{self.col['w']} "
            f"for character {self.col['g']}{live_char.char_name}{self.col['w']} from DB."
        )

        physical = live_char.physical
        smarts = live_char.smarts
        resources = live_char.resources
        psr = physical + smarts + resources
        if psr < 0:
            psr = 0
        initiative_bonus = live_char.initiative_bonus
        match psr:
            case 0 | 1 | 2:
                psr_base = 1
            case 3 | 4 | 5:
                psr_base = 2
            case 6 | 7 | 8:
                psr_base = 3
            case 9 | 10 | 11:
                psr_base = 4
            case 12 | 13 | 14:
                psr_base = 5
            case 15 | 16 | 17:
                psr_base = 6
            case 18 | 19 | 20:
                psr_base = 7
            case 21 | 22 | 23:
                psr_base = 8
            case 24 | 25 | 26:
                psr_base = 9
            case 27 | 28 | 29:
                psr_base = 10
            case 30 | 31 | 32:
                psr_base = 11
            case _:
                psr_base = int(psr / 3)

        # Final Initiative calculation
        # initiative = psr_base + faith + sense + initiative_bonus
        initiative = psr_base + initiative_bonus

        logging.info(
            f"{self.chk} {self.py_txt} {live_char.char_name} {self.col['g']}initiative stat"
            f"{self.col['w']} is {self.col['g']}{initiative}{self.col['w']}."
        )

        # Update the LiveCharacterModel's initiative stat
        live_char.initiative = initiative

        self.live_char = live_char
        return live_char

    @staticmethod
    def _wt_lookup(wt_base: int) -> int:

        match wt_base:
            case -2 | -1 | 0:
                return 1
            case 1 | 2 | 3:
                return 2
            case 4 | 5 | 6:
                return 3
            case 7 | 8 | 9:
                return 4
            case 10 | 11 | 12:
                return 5
            case 13 | 14 | 15:
                return 6
            case 16 | 17 | 18:
                return 7
            case 19 | 20 | 21:
                return 8
            case 22 | 23 | 24:
                return 9
            case 25 | 26 | 27:
                return 10
            case 28 | 29 | 30:
                return 11
            case 31 | 32 | 33:
                return 12
            case _:
                return int(wt_base / 3) + 1

    @staticmethod
    def _mook_wt_lookup(wt_base: int) -> int:
        """Requires: wt_base (int); returns int.
        Simple lookup table for Mook Wound Thresholds"""

        match wt_base:
            case -2 | -1 | 0:
                return 1
            case 1 | 2 | 3 | 4 | 5 | 6 | 7:
                return 2
            case 8 | 9 | 10 | 11 | 12 | 13 | 14:
                return 3
            case 15 | 16 | 17 | 18 | 19 | 20 | 21:
                return 4
            case 22 | 23 | 24 | 25 | 26 | 27 | 28:
                return 5
            case 29 | 30 | 31 | 32 | 33 | 34 | 35:
                return 6
            case 36 | 37 | 38 | 39 | 40 | 41 | 42:
                return 7
            case 43 | 44 | 45 | 46 | 47 | 48 | 49:
                return 8
            case 50 | 51 | 52 | 53 | 54 | 55 | 56:
                return 9
            case 57 | 58 | 59 | 60 | 61 | 62 | 63:
                return 10
            case _:
                return int(wt_base / 7) + 1

    def calc_live_char_wound_thresholds(
        self, live_char: LiveCharacterModel = None
    ) -> LiveCharacterModel:
        """
        Requires: live_char (LiveCharacterModel); returns LiveCharacterModel
        This method quickly calculates 5 of a live_character's 7 Wound Thresholds (Physical, Smarts, Resources, Wyld,
        Divinity).
        WT is calculated thus:
        physical_wt =  physical + endurance + scale + Physical_wt_bonus -1
        smarts, resources, wyld, divinity are the same except no Scale.
        Vehicle WT and Mook Threshold are calculated differently
        """
        logging.info(
            f"{self.chk} {self.col['y']}[calc_live_char_wound_thresholds]{self.col['w']}"
        )

        if not live_char:
            live_char = self.live_char

        logging.info(
            f"{self.chk} {self.py_txt} Calculating {self.col['g']}Wound Thresholds{self.col['w']} "
            f"for character {self.col['g']}{live_char.char_name}{self.col['w']} from DB."
        )

        # Calculate the 5 main Wound Thresholds:
        physical_wt_base = (
            live_char.physical_actual + live_char.endurance + live_char.scale - 1
        )
        physical_wt = self._wt_lookup(physical_wt_base) + live_char.physical_wt_bonus
        smarts_wt_base = live_char.smarts_actual + live_char.control
        smarts_wt = self._wt_lookup(smarts_wt_base) + live_char.smarts_wt_bonus
        resources_wt_base = live_char.resources_actual + live_char.influence
        resources_wt = self._wt_lookup(resources_wt_base) + live_char.resources_wt_bonus
        wyld_wt_base = live_char.wyld_actual + live_char.resistance
        wyld_wt = self._wt_lookup(wyld_wt_base) + live_char.wyld_wt_bonus
        divinity_wt_base = live_char.divinity_actual + live_char.faith
        divinity_wt = self._wt_lookup(divinity_wt_base) + live_char.divinity_wt_bonus
        mook_wt_base = (
            physical_wt_base
            + smarts_wt_base
            + resources_wt_base
            + wyld_wt_base
            + divinity_wt_base
        )
        mook_wt = self._mook_wt_lookup(mook_wt_base) + live_char.wyld_wt_bonus

        # All Wound Thresholds have a minimum value of 1, so if wt is less than 1, set = 1
        if physical_wt < 1:
            physical_wt = 1
        if smarts_wt < 1:
            smarts_wt = 1
        if resources_wt < 1:
            resources_wt = 1
        if wyld_wt < 1:
            wyld_wt = 1
        if divinity_wt < 1:
            divinity_wt = 1
        if mook_wt < 1:
            mook_wt = 1

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['g']}Wound Thresholds{self.col['w']} "
            f"for character {self.col['g']}{live_char.char_name}{self.col['w']} are: "
            f"physical_wt = {physical_wt}, smarts_wt = {smarts_wt}, resources_wt = {resources_wt}, "
            f"wyld_wt = {wyld_wt}, divinity_wt = {divinity_wt}, mook_wt = {mook_wt}"
        )

        # Set live_char Wound Thresholds
        live_char.physical_wt = physical_wt
        live_char.smarts_wt = smarts_wt
        live_char.resources_wt = resources_wt
        live_char.wyld_wt = wyld_wt
        live_char.divinity_wt = divinity_wt
        live_char.mook_wt = mook_wt

        self.live_char = live_char
        return live_char

    @staticmethod
    def _min_max_caps(base_value: int, min_cap: int, max_cap: int = 100) -> int:
        """Requires: base_value (int), min_cap (int), max_cap (int); returns int
        A super simple method that returns a value parsed against a min cap or optionally a max cap.
        If base_value is less than min_cap it returns min_cap, if equal to or above max_cap it returns max_cap,
        else it returns base_value"""
        if base_value < min_cap:
            return min_cap
        elif base_value > max_cap:
            return max_cap
        else:
            return base_value

    def set_skill_minimums(
        self, live_char: LiveCharacterModel = None
    ) -> LiveCharacterModel:
        """Requires live_char (LiveCharacterModel); returns LiveCharacterModel
        This method checks the _actual value of the skills that have a minimum skill value of 1 and sets
        the skill value to 1 without deleting or altering the _actual value which is the true value"""
        logging.info(f"{self.chk} {self.col['y']}[set_skill_minimums]{self.col['w']}")

        if not live_char:
            live_char = self.live_char

        ss = self.ss

        logging.info(
            f"{self.chk} {self.py_txt} Setting {self.col['g']}skill minimums of 1{self.col['w']} "
            f"for {ss.min_1_skills} for character "
            f"{self.col['g']}{live_char.char_name}{self.col['w']}."
        )
        for skill in ss.min_1_skills:
            actual = skill + "_actual"
            actual_skill = getattr(live_char, actual)
            # current_skill = getattr(live_char, skill)
            new_value = self._min_max_caps(actual_skill, 1)
            logging.info(
                f"{self.chk} {self.py_txt} Actual value = {self.col['y']}{actual_skill}"
                f"{self.col['w']}, current active value = {self.col['g']}{new_value}"
                f"{self.col['w']}."
            )
            setattr(live_char, skill, new_value)

        self.live_char = live_char
        return live_char

    def set_armour_value_caps(
        self, live_char: LiveCharacterModel = None
    ) -> LiveCharacterModel:
        """
        Requires: live_char (LiveCharacterModel); returns LiveCharacterModel
        This method sets the minimum (AV2) and maximum value caps (AV6 or higher) of Armour Values
        """
        logging.info(
            f"{self.chk} {self.col['y']}[set_armour_value_caps]{self.col['w']}"
        )

        if not live_char:
            live_char = self.live_char

        logging.info(
            f"{self.chk} {self.py_txt} Setting {self.col['g']}Armour Value{self.col['w']} "
            f"maximums and minimums for character {self.col['g']}{live_char.char_name}{self.col['w']}."
        )

        # We grab the armour_value_actual values to calculate from
        # Parse AVs and ensure they are 2 or greater and less than av_max
        physical_av = self._min_max_caps(
            live_char.physical_av_actual,
            live_char.physical_av_min,
            live_char.physical_av_max,
        )
        smarts_av = self._min_max_caps(
            live_char.smarts_av_actual, live_char.smarts_av_min, live_char.smarts_av_max
        )
        resources_av = self._min_max_caps(
            live_char.resources_av_actual,
            live_char.resources_av_min,
            live_char.resources_av_max,
        )
        wyld_av = self._min_max_caps(
            live_char.wyld_av_actual, live_char.wyld_av_min, live_char.wyld_av_max
        )
        divinity_av = self._min_max_caps(
            live_char.divinity_av_actual,
            live_char.divinity_av_min,
            live_char.divinity_av_max,
        )
        vehicle_av = self._min_max_caps(
            live_char.vehicle_av_actual,
            live_char.vehicle_av_min,
            live_char.vehicle_av_max,
        )

        setattr(live_char, "physical_av", physical_av)
        setattr(live_char, "smarts_av", smarts_av)
        setattr(live_char, "resources_av", resources_av)
        setattr(live_char, "wyld_av", wyld_av)
        setattr(live_char, "divinity_av", divinity_av)
        setattr(live_char, "vehicle_av", vehicle_av)

        self.live_char = live_char
        return live_char

    def set_skill_masteries(
        self, char: CharacterModel = None, live_char: LiveCharacterModel = None
    ) -> LiveCharacterModel:
        """Requires: char (CharacterModel), live_char (LiveCharacterModel); returns LiveCharacterModel
        This method applies the extra points from ALL THE character's skill masteries."""
        logging.info(f"{self.chk} {self.col['y']}[set_skill_masteries]{self.col['w']}")

        if not char:
            char = self.char

        if not live_char:
            live_char = self.live_char

        ss = self.ss

        logging.info(
            f"{self.chk} {self.py_txt} Setting {self.col['g']}Skill Masteries{self.col['w']} "
            f"for character {self.col['g']}{live_char.char_name}{self.col['w']}."
        )

        # Call Calc Skill Mastery for each of the Skill Masteries. These start at 1 not 0!!!
        count = 1
        for x in ss.smx_slots:
            smx_val = char.nodes[x]
            if smx_val:
                # Only do anything if the slot has something in it!
                # Apply_mod
                logging.info(
                    f"{self.chk} {self.py_txt} {self.col['m']}Skill Specialisation MASTERY detected!{self.col['w']} "
                )
                logging.info(
                    f"{self.chk} {self.py_txt} The location:{self.col['y']}{x}{self.col['w']} is set to:"
                    f"{self.col['g']}{smx_val}{self.col['w']}"
                )

                # Set the name of the Skill Specialisation
                smx_name = f"smx_name{count}"
                skill_name = self.get_mod_name(smx_val)
                # We want it in lower case :)
                skill_name = skill_name.lower()
                setattr(live_char, smx_name, skill_name)

                # Get current value of Specialisation Mastery. This will be used as a MULTIPLIER!
                smx_skill_name = f"smx{count}"
                # We need to -1 from the total as it counts the first point from the SMX name otherwise!
                smx_skill_value = getattr(live_char, smx_skill_name, 0) - 1

                # Get a dict of all touched skills
                smx_dict = self.get_modded_skills(mod_id=smx_val)

                # There can be multiple stats effected, so we need to go through each
                for effect in smx_dict:
                    # Now we need to get the relevant skill value:
                    smx_actual_val = getattr(live_char, effect, 0)
                    # print(f"smx_actual_val = getattr(live_char, {effect}, 0)")

                    # Also append to _touched_by
                    touched_name = f"n_spec_mastery{count}_0"
                    live_char = self.write_touched_entry(
                        mod_id=touched_name, touched_skill=effect, live_char=live_char
                    )

                    # And the SMX value(s) + skill value
                    new_val = smx_actual_val + smx_skill_value
                    logging.info(
                        f"{self.chk} {self.py_txt} {self.col['g']}New value for {effect} = {smx_actual_val} + "
                        f"{smx_skill_value} = {new_val}{self.col['w']}"
                    )
                    setattr(live_char, effect, new_val)
            else:
                logging.info(
                    f"{self.chk} {self.py_txt} {self.col['y']}NO Skill Specialisation MASTERY detected.{self.col['w']}"
                )

            count += 1

        self.live_char = live_char
        return live_char

    def calc_wyld_cancer(
        self, live_char: LiveCharacterModel = None, char: CharacterModel = None
    ) -> LiveCharacterModel:
        """Requires: live_char (LiveCharacterModel), char (CharacterModel); returns LiveCharacterModel.
        This method calculates the character's total Wyld Cancer"""
        logging.info(f"{self.chk} {self.col['y']}[calc_wyld_cancer]{self.col['w']}")
        if not char:
            char = self.char
        if not live_char:
            live_char = self.live_char

        # Get and Set Live Character Wyld Cancer extra from Character
        wc = getattr(live_char, "wyld_cancer", 0)
        wc_extra = getattr(char, "wyld_cancer_extra", 0)
        setattr(live_char, "wyld_cancer_extra", wc_extra)
        wc_mult = getattr(live_char, "wyld_cancer_mult", 1)

        # Calculate actual Wyld Cancer
        total_wc = (wc * wc_mult) + wc_extra
        setattr(live_char, "wyld_cancer_total", total_wc)

        logging.info(
            f"{self.chk} {self.py_txt} Character {self.col['g']}{live_char.char_name}{self.col['w']} has a "
            f"Base Wyld Cancer:{self.col['y']}{wc}{self.col['w']}; Extra Wyld Cancer:{self.col['y']}{wc_extra}"
            f"{self.col['w']}, and Wyld Cancer Multiplier:{self.col['y']}{wc_mult}{self.col['w']}."
        )
        logging.info(
            f"{self.chk} {self.py_txt} Character {self.col['g']}{live_char.char_name} has "
            f"{self.col['y']}({wc}*{wc_mult})+{wc_extra}={self.col['g']}{total_wc}"
            f"{self.col['w']} Total Wyld Cancer."
        )

        self.live_char = live_char
        return live_char

    def calc_wyld_cancer_injuries(
        self, live_char: LiveCharacterModel = None, char: CharacterModel = None
    ) -> LiveCharacterModel:
        """
        Requires: live_char (LiveCharacterModel); Returns LiveCharacter_model
        Simple method for calculating the character's total number of Permanent Wyld Injuries
        Includes call to calc_wyld_cancer. Also pulls current Wyld Injuries and number of healed Wyld Injuries from
        CharacterModel
        """
        logging.info(
            f"{self.chk} {self.col['y']}[calc_wyld_cancer_injuries]{self.col['w']}"
        )

        if not live_char:
            live_char = self.live_char
        if not char:
            char = self.char

        # Get Wyld Cancer Permanent Injuries and Healed count from CharacterModel and set in LiveCharacterModel
        healed_wyld_perm_injuries = getattr(char, "healed_wyld_perm_injuries", 0)
        wyld_perm_injuries = getattr(char, "wyld_perm_injuries", [])
        setattr(live_char, "healed_wyld_perm_injuries", healed_wyld_perm_injuries)
        setattr(live_char, "wyld_perm_injuries", wyld_perm_injuries)

        live_char = self.calc_wyld_cancer(live_char=live_char)
        total_wc = getattr(live_char, "wyld_cancer_total", 0)

        pwi_thresh = live_char.wyld_cancer_perm_threshold

        if total_wc < pwi_thresh:
            perm_wi = 0
        elif pwi_thresh <= total_wc < (pwi_thresh * 2):
            perm_wi = 1
        elif (pwi_thresh * 2) <= total_wc < (pwi_thresh * 3):
            perm_wi = 2
        elif (pwi_thresh * 3) <= total_wc < (pwi_thresh * 4):
            perm_wi = 3
        elif (pwi_thresh * 4) <= total_wc < (pwi_thresh * 5):
            perm_wi = 4
        else:
            perm_wi = 5

        live_char.wyld_perm_injuries_count = perm_wi
        should_have_wi = perm_wi - live_char.healed_wyld_perm_injuries
        do_have_wi = len(live_char.wyld_perm_injuries)

        if do_have_wi < should_have_wi:
            logging.warning(
                f"{self.chk} {self.py_txt} Character {self.col['g']}{live_char.char_name}{self.col['w']} "
                f"{self.col['r']}HAS TOO FEW{self.col['w']} Permanent Wyld Injuries. They should have "
                f"{self.col['y']}{should_have_wi}{self.col['w']} but only have {self.col['r']}{do_have_wi}"
                f"{self.col['w']} Wyld Injuries."
            )
            live_char = self.add_note(
                note_type="warning",
                note_value=f"Character has TOO FEW Permanent Wyld Injuries, they should have {should_have_wi} "
                f"but only have {do_have_wi}",
                live_char=live_char,
            )
        elif do_have_wi > should_have_wi:
            logging.warning(
                f"{self.chk} {self.py_txt} Character {self.col['g']}{live_char.char_name}{self.col['w']} "
                f"{self.col['r']}HAS TOO MANY{self.col['w']} Permanent Wyld Injuries. They should have "
                f"{self.col['y']}{should_have_wi}{self.col['w']} but actually have {self.col['r']}{do_have_wi}"
                f"{self.col['w']} Wyld Injuries."
            )
            live_char = self.add_note(
                note_type="warning",
                note_value=f"Character has TOO MANY Permanent Wyld Injuries, they should have {should_have_wi} "
                f"but actually have {do_have_wi}",
                live_char=live_char,
            )
        else:
            logging.info(
                f"{self.chk} {self.py_txt} Character {self.col['g']}{live_char.char_name}{self.col['w']} "
                f"{self.col['g']}HAS CORRECT{self.col['w']} number of Permanent Wyld Injuries. They have "
                f"{self.col['g']}{should_have_wi}{self.col['w']} Wyld Injuries."
            )
        self.live_char = live_char
        return live_char

    def set_secondary_info(
        self, live_char: LiveCharacterModel = None, char: CharacterModel = None
    ) -> LiveCharacterModel:
        """Simple method that take each entry from SpecialStat secondary_info, reads its current value in the
        CharacterModel and set the same value in the LiveCharacterModel"""
        logging.info(f"{self.chk} {self.col['y']}[set_secondary_info]{self.col['w']}")
        if not char:
            char = self.char
        if not live_char:
            live_char = self.live_char

        secondary_info = self.ss.secondary_info
        note_text: str = ""

        # Take each entry from secondary_info, read its current value from the CharacterModel and set the same value
        # in the LiveCharacterModel
        for info in secondary_info:
            if hasattr(char, info):
                logging.info(
                    f"{self.chk} {self.py_txt} Setting secondary info field: {self.col['y']}{info}{self.col['w']}. "
                )
                current_info = getattr(char, info)
                setattr(live_char, info, current_info)

                # Also populate the notes for those fields that are dictionaries
                if type(current_info) == dict:
                    logging.info(
                        f"{self.chk} {self.py_txt} Secondary info field is a dictionary:{self.col['y']}{current_info}"
                        f"{self.col['w']}. Populating dictionary..."
                    )
                    if current_info:
                        for x in current_info:
                            note_text = f"{note_text}\n{current_info[x]}"

                    live_char = self.add_note(
                        note_type=info,
                        note_value=note_text,
                        live_char=live_char,
                    )

        self.live_char = live_char
        return live_char

    def add_note(
        self,
        note_type: str = "general",
        note_value: str = "",
        save_note: bool = False,
        live_char: LiveCharacterModel = None,
        char: CharacterModel = None,
    ):
        """
        Requires: note_type (str), note_value (str), save_note (bool), live_char (LiveCharacterModel),
        char (CharacterModel); returns LiveCharacterModel.
        Here we add/append notes to the liveCharacter Models of the character and optionally store them in
        the char.custom_notes dict of the CharacterModel"""
        logging.info(f"{self.chk} {self.col['y']}[add_note]{self.col['w']}")
        if not char:
            char = self.char
        if not live_char:
            live_char = self.live_char

        if note_type in self.ss.note_types:
            # Add it to the LiveCharacter
            note_name = f"{note_type}_note"
            current_note = getattr(live_char, note_name, "")
            if current_note:
                if note_value not in current_note:
                    updated_note = f"{current_note}, {note_value}"
                else:
                    updated_note = f"{current_note}"
            else:
                updated_note = f"{note_value}"

            setattr(live_char, note_name, updated_note)

            # If save_note is True, also save it to the CharacterModel
            if save_note:
                saved_notes = char.custom_notes
                current_saved_note = getattr(saved_notes, note_name, None)
                if current_saved_note:
                    updated_saved_note = f"{current_saved_note}, {note_value}"
                else:
                    updated_saved_note = f"{note_value}"

                saved_notes.update({note_name: updated_saved_note})
                char.custom_notes = saved_notes
                self.char = char

            self.live_char = live_char
            return live_char
        else:
            logging.error(
                f"{self.cross} {self.err_txt}{self.col['r']} Unknown Note Type! Note type must be one of "
                f"{self.ss.note_types}{self.col['w']}"
            )
            return live_char

    def get_saved_notes(
        self, live_char: LiveCharacterModel = None, char: CharacterModel = None
    ) -> LiveCharacterModel:
        """This method gets any saved notes and appends them to the existing notes"""
        logging.info(f"{self.chk} {self.col['y']}[get_saved_notes]{self.col['w']}")
        if not char:
            char = self.char
        if not live_char:
            live_char = self.live_char

        custom_notes = char.custom_notes

        for note in custom_notes:
            current_note = getattr(live_char, note, "")
            if current_note:
                if custom_notes[note] not in current_note:
                    new_note = f"{current_note}, {custom_notes[note]}"
                    setattr(live_char, note, new_note)
            else:
                if custom_notes[note] not in current_note:
                    new_note = f"{custom_notes[note]}"
                    setattr(live_char, note, new_note)

        self.live_char = live_char
        return live_char

    def _if_mod_is_ets_add_note(
        self,
        mod_id: str,
        live_char: LiveCharacterModel = None,
    ) -> LiveCharacterModel:
        """
        Requires: mod_id (str), live_char (LiveCharacterModel), char (CharacterModel); returns LiveCharacterModel
        This method checks if a mod is an Edge, Trait, Team Edge, Team Trait, Temporary Edge, Temporary Trait or
        Sliverware implant and if it is it adds it to the appropriate notes section"""
        logging.info(
            f"{self.chk} {self.col['y']}[_if_mod_is_ets_add_note]{self.col['w']}"
        )
        if not live_char:
            live_char = self.live_char

        mod_info = self.get_mod_info(
            mod_id=mod_id, optional_fields="name, category, type"
        )

        match mod_info[0][1]:
            case "edge":
                live_char = self.add_note(
                    note_type="edges",
                    note_value=f"{mod_info[0][0]}",
                    live_char=live_char,
                )
            case "trait":
                live_char = self.add_note(
                    note_type="traits",
                    note_value=f"{mod_info[0][0]} [{mod_info[0][2].upper()}]",
                    live_char=live_char,
                )

            case "sliverware":
                live_char = self.add_note(
                    note_type="sliverware",
                    note_value=f"{mod_info[0][0]} [{mod_info[0][2].upper()}]",
                    live_char=live_char,
                )

            case _:
                pass

        self.live_char = live_char
        return live_char

    def pc_exists_by_name(
        self,
        search_name: str,
        is_deleted: bool = False,
        pc: str = "player",
        player_id: int = -1,
        lower_case: bool = False,
    ) -> dict:
        """Requires search_name; returns dict.
        Mini method just for checking if a player or character of a specified name exists in the db.
        Available Options:
        search_name: string. pc name made safe
        is_deleted: bool. Include pcs marked for deletion?
        pc: player, char or live_char
        player_id: int, enter a player_id if you want to also search by this and the other id
        lower_case: bool, make the search case-insensitive by making search field and search item lower case
        """
        logging.info(f"{self.chk} {self.col['y']}[pc_exists_by_name]{self.col['w']}")

        if pc in self.pc_types:
            match pc:
                case "char":
                    table = "characters"
                    pc_name = "char_name"
                case "live_char":
                    table = "live_characters"
                    pc_name = "char_name"
                case _:
                    table = "players"
                    pc_name = "player_name"

            if lower_case:
                search_name = search_name.lower()

            if is_deleted:
                if player_id > -1:
                    if lower_case:
                        check_pc_sql = (
                            f"SELECT * FROM {table} WHERE LOWER({pc_name})='{search_name}' AND "
                            f"player_id={player_id}"
                        )
                    else:
                        check_pc_sql = (
                            f"SELECT * FROM {table} WHERE {pc_name}='{search_name}' AND "
                            f"player_id={player_id}"
                        )

                else:
                    if lower_case:
                        check_pc_sql = f"SELECT * FROM {table} WHERE LOWER({pc_name})='{search_name}'"
                    else:
                        check_pc_sql = (
                            f"SELECT * FROM {table} WHERE {pc_name}='{search_name}'"
                        )

            else:
                if player_id > -1:
                    if lower_case:
                        check_pc_sql = (
                            f"SELECT * FROM {table} WHERE LOWER({pc_name})='{search_name}' AND player_id={player_id} "
                            f"AND deleted=0"
                        )
                    else:
                        check_pc_sql = (
                            f"SELECT * FROM {table} WHERE {pc_name}='{search_name}' AND player_id={player_id} "
                            f"AND deleted=0"
                        )
                else:
                    if lower_case:
                        check_pc_sql = f"SELECT * FROM {table} WHERE LOWER({pc_name})='{search_name}' AND deleted=0"
                    else:
                        check_pc_sql = f"SELECT * FROM {table} WHERE {pc_name}='{search_name}' AND deleted=0"

            pc_exists = self.db_fetch(
                self.chardata_db["db"], self.chardata_db["db_path"], check_pc_sql
            )

            return pc_exists
        else:
            logging.error(
                f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} You can only "
                f"use the pc_exists_by_name method to search for matches in players, characters, or "
                f"live_characters tables .{self.col['w']}"
            )

    def pc_exists_by_id(
        self, search_id: int, is_deleted: bool = False, pc="player", lc=False
    ) -> dict:
        """Requires search_id; returns dict.
        Mini method just for checking if a player or character of a specified ID exists in the db.
        Available Options:
        search_id: int. ID for PC
        is_deleted: bool. Include pcs marked for deletion?
        pc: player, char or live_char
        lc: bool. Set this to true, and it will search for a live_char_id by char_id"""
        logging.info(f"{self.chk} {self.col['y']}[pc_exists_by_id]{self.col['w']}")

        if pc in self.pc_types:
            match pc:
                case "char":
                    table = "characters"
                    pc_id = "char_id"
                case "live_char":
                    table = "live_characters"
                    pc_id = "live_char_id"
                case _:
                    table = "players"
                    pc_id = "player_id"

            if is_deleted:
                if lc:
                    check_pc_sql = f"SELECT * FROM {table} WHERE char_id={search_id}"
                else:
                    check_pc_sql = f"SELECT * FROM {table} WHERE {pc_id}={search_id}"
            else:
                if lc:
                    check_pc_sql = f"SELECT * FROM {table} WHERE char_id={search_id}"
                else:
                    check_pc_sql = (
                        f"SELECT * FROM {table} WHERE {pc_id}={search_id} AND deleted=0"
                    )

            pc_exists = self.db_fetch(
                self.chardata_db["db"], self.chardata_db["db_path"], check_pc_sql
            )
            return pc_exists
        else:
            logging.error(
                f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} You can only "
                f"use the pc_exists_by_id method to search for matches in players, characters, or "
                f"live_characters tables .{self.col['w']}"
            )

    def _pc_exists_feedback(self, pc_name, deleted, pc="player"):
        """Extends pc_exists_by_name for logging/feedback purposes."""
        logging.info(f"{self.chk} {self.col['y']}[_pc_exists_feedback]{self.col['w']}")

        pc_exists_check = self.pc_exists_by_name(
            search_name=pc_name,
            is_deleted=deleted,
            pc=pc,
            lower_case=True,
        )
        if pc_exists_check:
            logging.info(
                f"{self.chk} {self.sql_txt} Player/Character '{pc_name}' "
                f"{self.col['g']}SUCCESSFULLY{self.col['w']} inserted into or updated in DB."
            )
            return True
        else:
            logging.info(
                f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} Player/Character '{pc_name}' "
                f"NOT inserted into or updated in DB.{self.col['w']}"
            )
            return False

    def _convert_model_to_dict(
        self,
        model: BaseModel | PlayerModel | CharacterModel | LiveCharacterModel,
        logging_name: str,
    ):
        """Requires: model (BaseModel), logging_name; returns json.
        Quick method for converting a Pydantic Model to JSON for storing.
        logging_name is used purely for the logging output to identify what is being converted!"""
        logging.info(
            f"{self.chk} {self.col['y']}[_convert_model_to_dict]{self.col['w']}"
        )

        # Turns the CharacterModel, LiveCharacterModel, or PlayerModel into a dict for storage
        model_dict = model.dict()
        # Convert it to valid JSON
        model_json = dumps(model_dict, default=str)
        logging.debug(
            f"{self.chk} {self.py_txt} Model Dict from _convert_model_to_dict is: {self.col['y']}"
            f"{dumps(model_dict, indent=4, default=str)}{self.col['w']}"
        )
        logging.info(
            f"{self.chk} {self.py_txt} Converting player, character or live_character known as "
            f"{self.col['g']}{logging_name}{self.col['w']} Model to a dict for safe JSON storage in DB."
        )

        return model_json

    def list_pc(
        self,
        include_deleted: bool = False,
        pc: str = "player",
        by_player_id: int = -1,
        cli_print: bool = False,
    ) -> tuple:
        """Requires pc; returns tuple.
        Method to list all players, characters or live_characters.
        Available Options:
        pc: player, char, or live_char
        by_player_id: int = list characters or live_characters by players
        NOTE: we set the default value for by_player_id to -1 because 0 is a valid ID!
        """
        logging.info(f"{self.chk} {self.col['y']}[list_pc]{self.col['w']}")

        if pc in self.pc_types:
            match pc:
                case "char":
                    table = "characters"
                case "live_char":
                    table = "live_characters"
                    #  Live characters can't be searched for by player ID, so we discard this by setting to -1:
                    by_player_id = -1
                case _:
                    table = "players"
            pc_id = pc + "_id"
            pc_name = pc + "_name"

            if include_deleted:
                if by_player_id >= 0:
                    list_pc_sql = f"SELECT {pc_id}, {pc_name} FROM {table} WHERE player_id={by_player_id}"
                else:
                    list_pc_sql = f"SELECT {pc_id}, {pc_name} FROM {table}"
            else:
                if by_player_id >= 0:
                    list_pc_sql = f"SELECT {pc_id}, {pc_name} FROM {table} WHERE deleted=0 AND player_id={by_player_id}"
                else:
                    list_pc_sql = (
                        f"SELECT {pc_id}, {pc_name} FROM {table} WHERE deleted=0"
                    )

            pc_tuple = tuple(
                self.db_fetch(
                    self.chardata_db["db"], self.chardata_db["db_path"], list_pc_sql
                )
            )

            if by_player_id >= 0:
                logging_add = (
                    f"by {self.col['g']}player_id:{by_player_id}{self.col['w']} "
                )
            else:
                logging_add = ""

            if pc_tuple:
                logging.info(
                    f"{self.chk} {self.sql_txt} List of all {table} {logging_add}in DB "
                    f"{self.col['g']}SUCCESSFULLY{self.col['w']} retrieved: \n"
                    f"                      {pc_tuple}"
                )
                if cli_print:
                    print(
                        f"{self.chk} {self.col['g']}List of all {table} {logging_add}in DB "
                        f"{self.col['w']}SUCCESSFULLY{self.col['g']} retrieved: \n"
                    )
                print(
                    f"{self.ind0}{self.col['g']}#: {self.col['w']}Name{self.col['w']} \n"
                    f"{self.ind0}___________________\n"
                )
                for tup in pc_tuple:
                    print(
                        f"{self.ind0}{self.col['g']}{tup[0] + 1}: {self.col['w']}{self.string_pretty(tup[1])} "
                        f"{self.col['y']}(Char_ID:{tup[0]})"
                    )
            else:
                logging.info(
                    f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} List of all {table} "
                    f"{logging_add}in DB NOT retrieved or empty.{self.col['w']} Query returned: \n"
                    f"                      {pc_tuple}"
                )
                if cli_print:
                    print(
                        f"{self.cross} {self.err_txt} {self.col['r']} List of all {table} "
                        f"{logging_add}in DB NOT retrieved or empty.{self.col['w']} Query returned: \n"
                    )
                    for tup in pc_tuple:
                        print(f"{tup}")

            return pc_tuple
        else:
            logging.info(
                f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['r']} You can only "
                f"use the list_pc method to list players, characters, or "
                f"live_characters.{self.col['w']}"
            )

    def _update_char_nodes(
        self, char: CharacterModel = None, cli_print: bool = True
    ) -> CharacterModel:
        """A very simple method to update a CharacterModel's list of nodes with any additions added to the
        default model"""
        logging.info(f"{self.chk} {self.col['y']}[_update_char_nodes]{self.col['w']}")

        if not char:
            char = self.char

        default_model = CharacterModel(
            char_id=0,
            char_name="default",
            player_id=0,
            char_type="character",
            deleted=False,
        )
        default_nodes = getattr(default_model, "nodes", {})

        logging.info(
            f"{self.chk} {self.py_txt} {self.col['g']}UPDATING CharacterModel...{self.col['w']}\n"
            f"{self.chk} {self.py_txt} {self.col['y']}Checking if character:{self.col['w']}'{char.char_name}'"
            f"{self.col['y']} has all required node slots including any added recently...{self.col['w']}"
        )

        if cli_print:
            print(
                f"{self.chk} {self.col['y']}Checking if character:{self.col['w']}'{char.char_name}'"
                f"{self.col['y']} has all required node slots including any added recently...{self.col['w']}"
            )

        char_nodes = char.nodes
        char_nodes_keys = set(char_nodes.keys())
        default_node_keys = set(default_nodes.keys())

        added_nodes = default_node_keys - char_nodes_keys

        missing_nodes = len(added_nodes)

        if missing_nodes:
            logging.info(
                f"{self.chk} {self.py_txt} {self.col['y']}Character:{self.col['w']}'{char.char_name}' "
                f"{self.col['y']} is missing {self.col['r']}{missing_nodes}{self.col['y']} node slots..."
                f"{self.col['w']}"
            )
            if cli_print:
                print(
                    f"{self.chk} {self.col['y']}Character:{self.col['w']}'{char.char_name}' "
                    f"{self.col['y']} is missing {self.col['r']}{missing_nodes}{self.col['y']} node slots..."
                    f"{self.col['w']}"
                )

            for key in added_nodes:
                char.nodes[key] = ""
                logging.info(
                    f"{self.chk} {self.col['y']}Adding: {self.col['g']}{key}{self.col['w']}"
                )
                if cli_print:
                    print(
                        f"{self.chk} {self.col['y']}Adding: {self.col['g']}{key}{self.col['w']}"
                    )

            if cli_print:
                print(
                    f"{self.chk} {self.col['y']}The CharacterModel for:{self.col['w']}'{char.char_name}'"
                    f"{self.col['y']} was {self.col['g']}SUCCESSFULLY UPDATED!{self.col['y']} with al new nodes. "
                    f"Don't forget to {self.col['g']}SAVE{self.col['y']} them...{self.col['w']}"
                )

        return char

    def share_character(self):
        """Share a character as a QR code or shortcode"""
        pass

    def character_try_mod(self):
        """Some mods, especially Injuries have a 'try x else y' keyword structure this is where we process that
        keyword."""
        pass

    def character_custom_mod(self):
        """Create a custom mod, usually an Edge or Trait."""
        pass

    def get_skill_value(self, skill) -> int:
        """Here we display the value of a skill"""
        pass

    def set_datetime(self, new=True):
        """Here we set the datetime for newly created characters and also set the modification date for characters"""
        if new:  # Save new datetime for new character
            pass
        else:  # False Set Update datetime for modified character
            pass

    def set_character_strings(self) -> dict:
        """Here we set the character info that isn't a bunch of lists or dicts, name, age, description, gender etc"""
        pass

    def request_input(self):
        """Here we ping the frontend when we need input"""
        pass

    def confirm_input(self) -> bool:
        """Here we ping the front end when we need to confirm input, such as deleting a character"""
        pass

    def confirm_override(self) -> bool:
        """Here we get the user to confirm tey are overriding prerequisites, restrictions and placement limitations"""
        pass

    def get_damage_taken(self, skill) -> int:
        """Here we get info on a character's current Damage Taken"""
        pass

    def set_damage_taken(self, skill) -> int:
        """Here we set the current Damage Taken for a character in play"""
        pass

    def overflow_damage_taken(self, skill) -> int:
        """Here we overflow extra Damage Taken into the next skill"""
        pass

    def get_wounds(self, skill) -> int:
        """Here we get info on a character's current Wound status"""
        pass

    def set_wounds(self, skill) -> int:
        """Here we set the current Wounds for a character in play"""
        pass

    def get_injuries(self, skill):
        """Here we calculate what Injuries a character sustains in play"""
        pass

    def set_injuries(self, skill):
        """Here we set the Injuries a character has received during play"""

    def heal_damage_taken(self, skill) -> int:
        """Here we heal any Damage Taken in a specified skill"""
        pass

    def heal_wounds(self, skill) -> int:
        """Here we heal one or more Wounds in a specified skill"""
        pass

    def heal_injuries(self, skill):
        """Here we heal one or more Injuries in a specified skill"""
        pass

    def get_stun_damage(self) -> int:
        """Here we calculate how may Rounds of Stun a character takes in play"""
        pass

    def set_stun_damage(self) -> int:
        """Here we set the number of Rounds a character is stunned for in play"""
        pass

    def heal_stun_damage(self) -> int:
        """Heals one or more rounds of Stun"""
        pass

    def get_emp_damage(self) -> int:
        """Here we calculate how many Scenes of EMP a character takes during play"""
        pass

    def set_emp_damage(self) -> int:
        """Here we set the number of Scenes a character is EMPed"""
        pass

    def heal_emp_damage(self) -> int:
        """Heals one or more Scenes of EMP damage"""
        pass

    def take_drug_toxin(self):
        pass

    def end_scene(self):
        pass
