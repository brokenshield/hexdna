# encoding: utf-8
__version__ = "2.1.50"
__author__ = "Gunnar Roxen <gunnar@brokenshield.net>"

from json import dumps

import logging

# from character_methods import CharacterMethods
from delete_methods import DeleteMethods
from character_dataclasses import (
    NodeMap,
    BaseModel,
    PlayerModel,
    CharacterModel,
    LiveCharacterModel,
    SpecialStats,
    BreedTemplates,
)

logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(filename='app.log', filemode='w', format='%(message)s')


class TestCharacterMethods(DeleteMethods):
    """This is the test class that extends character_methods.py"""

    def __init__(self, **kwargs):
        super(TestCharacterMethods, self).__init__(**kwargs)
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing: WELCOME TO THE TEST SUITE FOR BCCM v2."
            f"{self.col['w']}"
            f"{self.l_break}"
        )

    def test_db_fetch(self, mod_cat="edge", mod_type="pkc", good=True):
        """
        This method tests the connection to the gamedata db and results of the db_fetch method and ensures that it
        only accepts SELECT SQL queries. It gets the db connection details from self.gamedata.db
        """
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing: Running unit test for db_fetch method."
            f"{self.col['w']}"
        )

        if good:
            # for testing good input
            fetch_sql = f"SELECT * FROM {self.gamedata_db['table']} WHERE category='{mod_cat}' AND type='{mod_type}'"
        else:
            # For testing bad input
            fetch_sql = f"DROP TABLE IF EXISTS {self.gamedata_db['table']}"

        return_data = self.db_fetch(
            self.gamedata_db["db"], self.gamedata_db["db_path"], fetch_sql
        )

        if len(return_data) > 0:
            return True
        else:
            logging.info(
                f"{self.cross} {self.test_text} Dump of fetched record {self.fail_txt}."
            )
            return False

    def test_get_mod_info(self, edge_mod_id="e_gigantic") -> bool:
        """This method tests that the get_mod_info method is returning a single result correctly"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing: Running unit test for get_mod_info "
            f"method.{self.col['w']}"
        )

        return_data = self.get_mod_info(edge_mod_id)
        fetched_record = return_data[0]
        pretty_record = dumps(fetched_record, indent=4, default=str)

        if len(return_data) == 1:
            logging.info(
                f"{self.chk} {self.test_text} Dump of fetched record: \n"
                f"{pretty_record}"
            )
            logging.info(
                f"{self.chk} {self.test_text} Fetched record mod_id is '{fetched_record[0]}'."
            )
            return True
        else:
            logging.info(
                f"{self.cross} {self.test_text} Dump of fetched record: \n"
                f"{pretty_record} \n"
                f"{self.fail_txt}."
            )
            return False

    def test_len(self, return_data):
        """Just a little test method to check that the length of returned data is greater than 0"""
        if len(return_data) > 0:
            logging.info(
                f"{self.l_break}"
                f"{self.chk} {self.test_text} {self.col['y']}Testing: First record fetched "
                f"return_data[0][0]:return_data[0][1] is: "
                f"'{return_data[0][0]}:{return_data[0][1]}'.{self.col['w']}"
            )
            return True
        else:
            logging.info(
                f"{self.cross} {self.test_text} Dump of fetched mod_selection: '{return_data}' {self.fail_txt}."
            )
            return False

    def test_get_mod_selection(self, mod_cat="edge", mod_type="ssw") -> dict:
        """This method tests that the get_mod_selection method is returning a dict of mod_id:name correctly"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing: Running unit test for get_mod_selection "
            f"method.{self.col['w']}"
        )
        logging.info(
            f"{self.chk} {self.test_text} Testing get_mod_selection method for category: '{mod_cat}' and "
            f"type '{mod_type}'."
        )

        return_data = self.get_mod_selection(
            mod_cat, mod_type, optional_fields="mod_id, name"
        )

        return return_data

    def test_get_mod_selection_full(self, mod_cat="edge", mod_type="dgx") -> dict:
        """This method tests that the get_mod_selection_full method is returning a dict of all mod details correctly"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing: Running unit test for get_mod_selection "
            f"method.{self.col['w']}"
        )
        logging.info(
            f"{self.chk} {self.test_text} Testing get_mod_selection_full method for category: '{mod_cat}' and type "
            f"'{mod_type}'."
        )

        return_data = self.get_mod_selection_full(mod_cat, mod_type)

        return return_data

    def test_check_any_all(self, mod_id="e_blood_of_overlord") -> tuple:
        """This method checks the check_any_all method"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing: Running unit test for "
            f"check_any_all method.{self.col['w']}"
        )
        logging.info(
            f"{self.chk} {self.test_text} Testing check_any_all method for mod_id: '{mod_id}'."
        )
        # Check prerequisites and restrictions ANY/ALL
        return_data = self.check_any_all(mod_id)

        if return_data[0]:
            logging.info(
                f"{self.chk} {self.test_text} mod_id: {mod_id} has "
                f"{self.col['g']}'ANY'{self.col['w']} Prerequisites."
            )
        else:
            logging.info(
                f"{self.chk} {self.test_text} mod_id: {mod_id} has "
                f"{self.col['y']}'ALL'{self.col['w']} Prerequisites."
            )

        if return_data[1]:
            logging.info(
                f"{self.chk} {self.test_text} mod_id: {mod_id} has "
                f"{self.col['g']}'ANY'{self.col['w']}  Requirements."
            )
        else:
            logging.info(
                f"{self.chk} {self.test_text} mod_id: {mod_id} has "
                f"{self.col['y']}'ALL'{self.col['w']} Requirements."
            )

        return return_data

    def test_get_prereqs_restrictions(self, mod_id="e_echo_focus") -> tuple:
        """This method checks the get_prereqs_restrictions method"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing: Running unit test for "
            f"get_prereqs_restrictions method.{self.col['w']}"
        )

        logging.info(
            f"{self.chk} {self.test_text} Testing get_prereqs_restrictions method for mod_id: '{mod_id}'."
        )

        # Check prerequisites and restrictions ANY/ALL
        return_data = self.get_prereqs_restrictions(mod_id)

        logging.info(
            f"{self.chk} {self.test_text} Prerequisites for '{mod_id}' are: '{return_data[0]}'."
        )
        logging.info(
            f"{self.chk} {self.test_text} Restrictions for '{mod_id}' are: '{return_data[1]}'."
        )

        return return_data

    def test_check_mod_in_list(
        self, mod_id="e_echo_focus", mod_id_check="e_aerokinesis"
    ) -> tuple:
        """This method tests if mod_id_check is in the prereq/requirements list for mod_id"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing: Running unit test for check_mod_in_list."
            f"{self.col['w']}"
        )
        # mod_id = "e_echo_focus" -> This is the mod_id we are reading the data for
        # mod_id_check = "e_aerokinesis"  # This is the mod_id we are checking for in p an r
        mod_list = self.get_prereqs_restrictions(mod_id)

        # Checking is in Prerequisites list [0][0]
        check_in1 = self.check_mod_in_list(mod_id_check, mod_list[0])
        # Checking is in Requirements list [0][1]
        check_in2 = self.check_mod_in_list(mod_id_check, mod_list[1])

        if check_in1:
            logging.info(
                f"{self.chk} {self.test_text} mod_id '{mod_id_check}' is "
                f"{self.col['g']}IN{self.col['w']} Prerequisites[0] list for: '{mod_id}'"
            )
            check_preq = True
        else:
            logging.info(
                f"{self.chk} {self.test_text} mod_id '{mod_id_check}' is "
                f"{self.col['y']}NOT IN{self.col['w']} Prerequisites[0] list for: "
                f"'{mod_id}'."
            )
            check_preq = False
        if check_in2:
            logging.info(
                f"{self.chk} {self.test_text} mod_id '{mod_id_check}' is "
                f"{self.col['g']}IN{self.col['w']} Requirements[1] list for: '{mod_id}'"
            )
            check_restrict = True
        else:
            logging.info(
                f"{self.chk} {self.test_text} mod_id '{mod_id_check}' is "
                f"{self.col['y']}NOT IN{self.col['w']} Requirements[1] list for: "
                f"'{mod_id}'."
            )
            check_restrict = False

        return check_preq, check_restrict

    def test_check_preq_restrict_all(
        self,
        mod_id="e_enhanced_sprinter",
        character_mods=["e_sprinter", "e_attractive", "e_gigantic"],
    ) -> tuple:
        """Test that the system is checking prerequisites and restrictions when ALL are required"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing if 'ALL' Prerequisite/Restriction "
            f"requirements are satisfied.{self.col['w']}"
        )
        return_data = self.check_preq_restrict_all(mod_id, character_mods)

        if return_data:
            logging.info(
                f"{self.chk} {self.test_text} 'ALL' Prerequisite and Restriction requirements for '{mod_id}' are "
                f"{self.col['g']}SATISFIED{self.col['w']}."
            )
        else:
            logging.info(
                f"{self.chk} {self.test_text} 'ALL' Prerequisite and Restriction requirements for '{mod_id}' are "
                f"{self.col['r']}NOT SATISFIED{self.col['w']}."
            )

        return return_data

    def test_check_allowed_multiple(self, mod_id="e_expertise") -> bool:
        """Testing if the method check_allowed_multiple works correctly"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing if you allowed multiple copies of mod_id: "
            f"'{mod_id}'.{self.col['w']}"
        )

        return_data = self.check_allowed_multiple(mod_id)

        return return_data

    def test_check_mod_allowed(
        self,
        mod_id="e_enhanced_sprinter",
        character_mods=["e_sprinter", "e_enhanced_sprinter", "t_unregistered_echo"],
    ) -> bool:
        """Test for check_mod_allowed method"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing if mod_id {mod_id} meets all "
            f"Prerequisites, Requirements and Allow_Multiple.{self.col['w']}"
        )

        return_data = self.check_mod_allowed(mod_id, character_mods)

        return return_data

    def test_get_touched_skills(self, mod_id="e_deathworld_native") -> list:
        """This test checks that the method get_touched_skills works correctly."""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing skills "
            f"{self.col['g']}TOUCHED{self.col['y']} by mod_id '{mod_id}'.{self.col['w']}"
        )
        return_data = self.get_touched_skills(mod_id)

        return return_data

    def test_get_modded_skills(self, mod_id="e_deathworld_native") -> dict:
        """This test checks that the method get_modded_skills works correctly."""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing skills and effects "
            f"{self.col['g']}MODIFIED{self.col['y']} by mod_id '{mod_id}'.{self.col['w']}"
        )
        return_data = self.get_modded_skills(mod_id)

        logging.info(f"{dumps(return_data, indent=4, default=str)}")

        return return_data

    def test_fetch_next_id(self, id_type="char") -> int:
        """This test checks that we retrieve the last player_id from the DB correctly."""

        if id_type in self.pc_types:
            logging.info(
                f"{self.l_break}"
                f"{self.chk} {self.test_text} {self.col['y']}Testing retrieving record."
                f"\n                      Retrieving last "
                f"{self.col['g']}{id_type}{self.col['y']} "
                f"from db table. Returns 0 if table is empty.{self.col['w']}"
            )
        else:
            logging.info(f"{self.cross} {self.sql_txt} {self.err_txt}")
            return False

        return_data = self.fetch_next_id(id_type=id_type)
        logging.info(
            f"{self.chk} {self.test_text} Test results: Next available "
            f"{self.col['g']}{id_type}{self.col['w']} is: "
            f"{self.col['g']}{return_data}{self.col['w']}"
        )

        return return_data

    def test_query_exists_in_db(
        self, query_id=1, query_table="players", id_label="default"
    ) -> bool:
        """This tests if a specified ID exists in a specified table"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing query_exists_in_db.{self.col['y']} "
            f"\n                      Does ID "
            f"{self.col['g']}{query_id}{self.col['y']} "
            f"exist in db table '{self.col['g']}{query_table}{self.col['y']}'? "
            f"\n                      Returns False if ID is available (does not exist) and True if taken "
            f"(already exists).{self.col['w']}"
        )

        return_data = self.query_exists_in_db(query_id, query_table, id_label)

        return return_data

    def test_insert_update_db(self, write_id=1, write_type="player") -> bool:
        """This tests whether you will insert or update a Database table
        write type: str = player, char or live_char"""
        if write_id in self.pc_types:
            logging.info(
                f"{self.l_break}"
                f"{self.chk} {self.test_text} {self.col['y']}Testing if we must INSERT a new record "
                f"or UPDATE an existing record.{self.col['w']}"
            )
            return_data = self.insert_update_db(write_id, write_type)

            return return_data

    def test_new_player(
        self,
        player_name="T@est;",
        player_real_name="Test @ Player",
        player_email="test@broken:;shield.net",
        deleted=False,
    ) -> PlayerModel:
        """This tests creating a new player"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing creating a NEW player or UPDATING an "
            f"existing player.{self.col['w']}"
        )

        return_data = self.new_or_update_player(
            player_name, player_real_name, player_email, deleted
        )

        return return_data

    def test_list_players(
        self, include_deleted=False, pc="player", by_player_id=-1
    ) -> tuple:
        """This tests creating lists all players"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing listing all players.{self.col['w']}"
        )
        list_players = self.list_pc(
            include_deleted=include_deleted, pc=pc, by_player_id=by_player_id
        )

        return list_players

    def test_mark_pc_for_deletion(self, delete_id=0, delete_type="player") -> bool:
        """This tests creating lists all players"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Marking a {delete_type} for "
            f"deletion.{self.col['w']}"
        )

        delete_pc = self.mark_pc_for_deletion(delete_id, delete_type)
        return delete_pc

    def test_mark_pc_for_undeletion(self, delete_id=0, delete_type="player") -> bool:
        """This tests creating lists all players"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Marking a {delete_type} for "
            f"UNDELETION.{self.col['w']}"
        )

        delete_pc = self.remove_mark_pc_for_deletion(delete_id, delete_type)

        return delete_pc

    def test_check_delete_undelete(self, delete_id=0, undelete=False):
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing delete/undelete check from "
            f"DB.{self.col['w']}"
        )
        test_cdu = self.check_delete_undelete(
            id_type="player_id", table="players", delete_id=delete_id, undelete=undelete
        )

        return test_cdu

    def test_purge_deleted_pc(self, purge_type="player") -> bool:
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing purging deleted {purge_type}s from "
            f"DB.{self.col['w']}"
        )
        purge = self.purge_deleted_pc(purge_type=purge_type)

        return purge

    @staticmethod
    def test_purge_all(self):
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing mass purge from DB.{self.col['w']}"
        )
        self.purge_all_deleted_pc()

    def test_retrieve_player(self, player_id=0, feedback=True):
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing retrieving player with "
            f"player_id:{player_id} from DB.{self.col['w']}"
        )
        player = self.load_player(player_id=player_id, feedback=feedback)

        return player

    def test_retrieve_character(self, char_id=0, feedback=True):
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing retrieving character with char_id:{char_id}"
            f" from DB.{self.col['w']}"
        )
        char = self.load_char(char_id=char_id, feedback=feedback)

        return char

    def test_retrieve_live_character(self, char_id=0, feedback=True):
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing retrieving live character information "
            f"for character with char_id:{char_id} from DB.{self.col['w']}"
        )
        live_char = self.load_live_character(char_id=char_id, feedback=feedback)

        return live_char

    def test_new_update_char(
        self,
        char_name,
        player_id,
        char_archetype="",
        char_type="char",
        deleted=False,
        char=None,
    ) -> CharacterModel:
        """This tests creating a new player
        char_name: str,
        player_id: int,
        char_archetype: str = "",
        char_type: str = "character",
        deleted: bool = False,
        """
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing creating a NEW character or UPDATING an "
            f"existing character.{self.col['w']}"
        )

        return_data = self.new_or_update_char(
            char_name, player_id, char_title, char_type, deleted, char
        )

        return return_data

    def test_new_update_live_char(self, char_id, deleted=False) -> LiveCharacterModel:
        """This tests creating a new live_character"""
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing creating a NEW live_character or "
            f"UPDATING an existing live_character for char_id:{char_id}.{self.col['w']}"
        )
        return_data = self.new_or_update_live_char(char_id, deleted)

        return return_data

    def test_apply_mod_to_character(
        self, mod_id: str, mod_location: str, char: CharacterModel
    ) -> CharacterModel:
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing applying mod_id:{mod_id} in {mod_location} "
            f"to {char.char_name}.{self.col['w']}"
        )
        self.apply_mod_to_character(mod_id=mod_id, mod_location=mod_location, char=char)

        return char

    def test_remove_mod_from_character(
        self, mod_id: str, mod_location: str, char: CharacterModel
    ) -> CharacterModel:
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing removing mod_id:{mod_id} in {mod_location} "
            f"to {char.char_name}.{self.col['w']}"
        )
        self.remove_mod_from_character(
            mod_id=mod_id, mod_location=mod_location, char=char
        )

        return char

    def test_node_slot_already_free(
        self, mod_location: str, char: CharacterModel
    ) -> bool:
        logging.info(
            f"{self.l_break}"
            f"{self.chk} {self.test_text} {self.col['y']}Testing if node_slot:{mod_location} "
            f"for {char.char_name} is already FILLED or FREE (available).{self.col['w']}"
        )

        slot_check = self.node_slot_already_free(mod_location=mod_location)

        return slot_check


cm = TestCharacterMethods()
# test1 = cm.test_db_fetch()  # set good=False to try an incorrect SQL query
# test2 = cm.test_get_mod_info()
# test3 = cm.test_get_mod_selection()
# test4 = cm.test_get_mod_selection_full()
# test5 = cm.test_check_any_all(mod_id="e_brave")
# test6 = cm.test_get_prereqs_restrictions(mod_id="e_brave")
# test7 = cm.test_check_mod_in_list(mod_id="e_brave")
# test8 = cm.test_check_allowed_multiple(mod_id="e_brave")
# test9 = cm.test_check_preq_restrict_all(mod_id="s_cnsbooster")
# test10 = cm.test_check_mod_allowed(mod_id="e_brave")
# test11 = cm.test_get_touched_skills(mod_id="e_brave")
# test12 = cm.test_get_modded_skills("e_brave")
# test13 = cm.test_fetch_next_id(id_type="player")
# test14 = cm.test_query_exists_in_db(query_table="characters", id_label="character")
# test15 = cm.test_insert_update_db()
"""
new_player = cm.test_new_player(
    player_name="Hannah",
    player_real_name="Hannah Rowlands",
    player_email="gunnar@brokenshield.net",
)"""
# test17 = cm.test_list_players(pc="player")
# test19 = cm.test_list_players(pc="char", by_player_id=1)
# test20 = cm.test_mark_pc_for_deletion(delete_id=0, delete_type="player")
# test21 = cm.test_mark_pc_for_deletion(delete_id=1, delete_type="char")
# test22 = cm.test_mark_pc_for_undeletion(delete_id=1, delete_type="char")
# test23 = cm.test_check_delete_undelete(delete_id=0, undelete=True)
# test24 = cm.test_purge_all_deleted_pc(purge_type="char")
# test25 = cm.test_retrieve_player(player_id=1)

"""
new_player = cm.create_new_player(
    player_name="Hannah",
    player_real_name="Hannah Rowlands",
    player_email="gunnar@brokenshield.net",
)
"""
"""
# TEST CHARACTER CHARYBDIS
character = cm.create_new_char(
    char_name="Test",
    player_id=7,
    char_archetype="test",
    char_type="character",
    breed="atropoan",
    physical_skill_n1="n_physical_1",
    physical_skill_n2="n_physical_2",
    physical_skill_n3="n_physical_3",
    physical_skill_n4="n_physical_4",
    physical_skill_n5="n_physical_5",
    physical_op_n0="n_physical_op_0",
    smarts_skill_n1="n_smarts_1",
    smarts_skill_n2="n_smarts_2",
    knowledge_skill_n0="n_knowledge_0",
    knowledge_edge_n0="e_sea_sense",
    resources_skill_n3="n_resources_3",
    resources_op_n0="n_resources_op_0",
    divinity_skill_n1="n_divinity_1",
    divinity_skill_n2="n_divinity_2",
    killer_skill_n1="n_killer_1",
    killer_skill_n2="n_killer_2",
    killer_skill_n3="n_killer_3",
    killer_skill_n4="n_killer_4",
    killer_skill_n5="n_killer_5",
    cloak_skill_n1="n_cloak_1",
    cloak_skill_n2="n_cloak_2",
    cloak_skill_n3="n_cloak_3",
    cloak_skill_n4="n_cloak_4",
    cloak_skill_n5="n_cloak_5",
    sandman_skill_n1="n_sandman_1",
    sandman_skill_n2="n_sandman_2",
    sandman_skill_n3="n_sandman_3",
    sandman_skill_n4="n_sandman_4",
    weaver_skill_n1="n_weaver_1",
    weaver_skill_n2="n_weaver_2",
    mouth_skill_n1="n_mouth_1",
    mouth_skill_n2="n_mouth_2",
    mouth_skill_n3="n_mouth_3",
    mouth_skill_n4="n_mouth_4",
    mouth_skill_n5="n_mouth_5",
    mouth_skill_n6="n_mouth_6",
    leadership_skill_n0="n_leadership_0",
    leadership_edge_n0="e_elicit_information",
    vapour_skill_n1="n_vapour_1",
    vapour_skill_n2="n_vapour_2",
    vapour_skill_n3="n_vapour_3",
    vapour_skill_n4="n_vapour_4",
    sandman_trait_n0={"mod_id": "t_sibling_liability", "text": "my brother"},
    weaver_trait_n0={
        "mod_id": "t_honour_code",
        "over": True,
        "text": "do the right thing",
    },
    earned_trait_n0="t_freelancer",
    smarts_skill_n3="n_smarts_3",
    smarts_skill_n4="n_smarts_4",
    smarts_skill_n5="n_smarts_5",
    knowledge_skill_n1="n_knowledge_1",
    knowledge_skill_n2="n_knowledge_2",
    spec_mastery1_name_n0="x_knowledge",
    spec_mastery1_skill_n0="n_spec_mastery1_0",
    spec_mastery1_skill_n1="n_spec_mastery1_1",
    endurance_skill_n0="n_endurance_0",
    endurance_edge_n0="e_thick_skinned",
    bodyweb_n0="s_bodyweb",
    chemjet_n0="s_chemjet",
    cnsbooster_n0="s_cnsbooster",
    dermalplate_n0="s_dermalplate",
    monoclaws_n0="s_monoclaws",
    steelmuscles_n0="s_steelmuscles",
    bodystash_n0="s_bodystash",
)"""

# breed = cm.apply_breed_template_to_char(breed="atropoan", char=character)

"""
cm.apply_multiple_mods_to_char(
    character,
    physical_skill_n1="n_physical_1",
    physical_skill_n2="n_physical_2",
    physical_skill_n3="n_physical_3",
    physical_skill_n4="n_physical_4",
    physical_skill_n5="n_physical_5",
    physical_op_n0="n_physical_op_0",
    smarts_skill_n1="n_smarts_1",
    smarts_skill_n2="n_smarts_2",
    knowledge_skill_n0="n_knowledge_0",
    knowledge_edge_n0="e_sea_sense",
    resources_skill_n3="n_resources_3",
    resources_op_n0="n_resources_op_0",
    divinity_skill_n1="n_divinity_1",
    divinity_skill_n2="n_divinity_2",
    killer_skill_n1="n_killer_1",
    killer_skill_n2="n_killer_2",
    killer_skill_n3="n_killer_3",
    killer_skill_n4="n_killer_4",
    killer_skill_n5="n_killer_5",
    cloak_skill_n1="n_cloak_1",
    cloak_skill_n2="n_cloak_2",
    cloak_skill_n3="n_cloak_3",
    cloak_skill_n4="n_cloak_4",
    cloak_skill_n5="n_cloak_5",
    sandman_skill_n1="n_sandman_1",
    sandman_skill_n2="n_sandman_2",
    sandman_skill_n3="n_sandman_3",
    sandman_skill_n4="n_sandman_4",
    weaver_skill_n1="n_weaver_1",
    weaver_skill_n2="n_weaver_2",
    mouth_skill_n1="n_mouth_1",
    mouth_skill_n2="n_mouth_2",
    mouth_skill_n3="n_mouth_3",
    mouth_skill_n4="n_mouth_4",
    mouth_skill_n5="n_mouth_5",
    mouth_skill_n6="n_mouth_6",
    leadership_skill_n0="n_leadership_0",
    leadership_edge_n0="e_elicit_information",
    vapour_skill_n1="n_vapour_1",
    vapour_skill_n2="n_vapour_2",
    vapour_skill_n3="n_vapour_3",
    vapour_skill_n4="n_vapour_4",
    sandman_trait_n0={"mod_id": "t_sibling_liability", "text": "my brother"},
    weaver_trait_n0={
        "mod_id": "t_honour_code",
        "over": True,
        "text": "do the right thing",
    },
    earned_trait_n0="t_freelancer",
    # )
    # cm.apply_multiple_mods_to_char(
    #    character,
    # smarts_skill_n1="n_smarts_1",
    # smarts_skill_n2="n_smarts_2",
    smarts_skill_n3="n_smarts_3",
    smarts_skill_n4="n_smarts_4",
    smarts_skill_n5="n_smarts_5",
    # knowledge_skill_n0="n_knowledge_0",
    knowledge_skill_n1="n_knowledge_1",
    knowledge_skill_n2="n_knowledge_2",
    spec_mastery1_name_n0="x_knowledge",
    spec_mastery1_skill_n0="n_spec_mastery1_0",
    spec_mastery1_skill_n1="n_spec_mastery1_1",
    endurance_skill_n0="n_endurance_0",
    endurance_edge_n0="e_thick_skinned",
    bodyweb_n0="s_bodyweb",
    chemjet_n0="s_chemjet",
    cnsbooster_n0="s_cnsbooster",
    dermalplate_n0="s_dermalplate",
    monoclaws_n0="s_monoclaws",
    steelmuscles_n0="s_steelmuscles",
    bodystash_n0="s_bodystash",
)
"""
character = cm.load_char(char_id=1)
live_char = cm.load_live_character(char_id=1)
cm.print_live_char_model()


# cm.remove_mod_from_character(
#    mod_id="s_bodystash", mod_location="bodystash_n0", char=character
# )


# cm.save_character()
# print(f"{dumps(cm.char.dict(), indent=4)}")
# print(f"{dumps(cm.live_char.dict(), indent=4)}")
print(
    f"{cm.chk} {cm.sql_txt} {cm.col['c']}!!!!! DB READ COUNT  = "
    f"{cm.db_read_count} !!!!!{cm.col['w']}\n"
    f"{cm.chk} {cm.sql_txt} {cm.col['m']}!!!!! DB WRITE COUNT = "
    f"{cm.db_write_count} !!!!!{cm.col['w']}"
)

# cm.process_char()

# cm.save_character()
# cm.print_char_model(char=character)
# cm.print_live_char_model()
