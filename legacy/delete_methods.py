# encoding: utf-8
__version__ = "2.1.50"
__author__ = "Gunnar Roxen <gunnar@brokenshield.net>"

from character_methods import CharacterMethods
import logging

logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(filename='app.log', filemode='w', format='%(message)s')


class DeleteMethods(CharacterMethods):
    """The DeleteMethods class extends CharacterMethods and is focussed purely on deleting and purging players,
    characters and live_characters
    THIS SHOULD BE LOCKED TO ADMINS ONLY FOR PURGE and ADMINS + PLAYER FOR THEIR OWN FILES"""

    def __init__(self, **kwargs):
        super(DeleteMethods, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def check_delete_undelete(
        self, id_type: str, table: str, delete_id: int, undelete: bool = False
    ):
        """Quick method to replace repeated code fragment"""
        logging.info(f"{self.l_break} check_delete_undelete]{self.col['white']}")

        if not undelete:
            delete_value = 1
            delete_name = "deletion"
        else:
            delete_value = 0
            delete_name = "undeletion"

        logging.info(
            f"{self.chk} {self.sql_txt} {self.col['yellow']}Confirming if {id_type}:{delete_id} has been "
            f"marked for {delete_name} in DB...{self.col['white']}"
        )

        # CHECK IF MARKED FOR DELETION OR NOT
        delete_check_sql = f"SELECT {id_type} FROM {table} WHERE {id_type}={delete_id} AND deleted={delete_value}"

        delete_check = self.db_fetch(
            self.chardata_db["db"],
            self.chardata_db["db_path"],
            delete_check_sql,
        )

        if delete_check:
            # SQL Query was successful. Return True.
            logging.info(
                f"{self.chk} {self.sql_txt} {id_type}:{delete_id} "
                f"{self.col['green']}SUCCESSFULLY{self.col['white']} marked for {delete_name} in DB."
            )
            return True
        else:
            # SQL Query was not successful. Return False.
            logging.error(
                f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['red']} {id_type}:{delete_id} "
                f"NOT marked for {delete_name} DB.{self.col['white']}"
            )
            return False

    def mark_pc_for_deletion(self, delete_id: int, pc: str = "player") -> bool:
        """Requires delete_id (string), pc (string); returns dict.
        Method to tag a player or character for deletion - it actually HIDES character but doesn't DELETE character. Use
        purge_all_deleted_pc method for that.
        Available Options:
        delete_id: relevant id, either char_id or player_id
        pc: character, player or live_character
        """
        logging.info(
            f"{self.l_break}    {self.col['red']}[mark_pc_for_deletion]{self.col['white']}"
        )

        if pc in self.pc_types:
            match pc:
                case "char":
                    table = "characters"
                case "live_char":
                    table = "live_characters"
                case _:
                    table = "players"
            pc_id = pc + "_id"

            logging.info(
                f"{self.chk} {self.sql_txt} Marking {pc} with ID '{delete_id}' for deletion."
            )

            check_in_db = self.query_exists_in_db(delete_id, table, pc)

            if check_in_db:
                if table and pc_id:
                    # IS ID MARKED FOR DELETION IN DB?
                    check_if_deleted_sql = f"SELECT {pc_id} FROM {table} WHERE {pc_id}={delete_id} and deleted=1"
                    is_deleted = self.db_fetch(
                        self.chardata_db["db"],
                        self.chardata_db["db_path"],
                        check_if_deleted_sql,
                    )

                    if is_deleted:
                        # YES -> RETURN TRUE
                        logging.info(
                            f"{self.chk} {self.sql_txt} {self.col['yellow']}{pc_id}:{delete_id} "
                            f"ALREADY marked for deletion in DB.{self.col['white']}"
                        )

                        # Check mark the live_char entry for deletion
                        if pc == "char":
                            logging.info(
                                f"{self.chk} {self.sql_txt} Also marking "
                                f"{pc_id}:{delete_id} for deletion in live_characters table in DB."
                            )
                            lc = self.pc_exists_by_id(
                                delete_id, pc="live_char", lc=True
                            )
                            lc_id = lc[0][0]
                            logging.info(
                                f"{self.chk} {self.sql_txt} live_char_id:{lc_id}"
                            )
                            lc_delete_sql = f"UPDATE live_characters SET deleted=1 WHERE live_char_id={lc_id}"
                            self.db_fetch(
                                self.chardata_db["db"],
                                self.chardata_db["db_path"],
                                lc_delete_sql,
                                allow_edit=True,
                            )

                        return True
                    else:
                        # NO -> SO CHECK IF ID ACTUALLY EXISTS
                        check_id_exists = self.query_exists_in_db(delete_id, table, pc)
                        if check_id_exists:
                            # ID EXISTS -> MARK FOR DELETION

                            delete_sql = f"UPDATE {table} SET deleted=1 WHERE {pc_id}={delete_id}"

                            self.db_fetch(
                                self.chardata_db["db"],
                                self.chardata_db["db_path"],
                                delete_sql,
                                allow_edit=True,
                            )

                            # Also mark the live_char entry for deletion
                            if pc == "char":
                                logging.info(
                                    f"{self.chk} {self.sql_txt} Also marking "
                                    f"{pc_id}:{delete_id} for deletion in live_characters table in DB."
                                )
                                lc = self.pc_exists_by_id(
                                    delete_id, pc="live_char", lc=True
                                )
                                lc_id = lc[0][0]
                                logging.info(
                                    f"{self.chk} {self.sql_txt} live_char_id:{lc_id}"
                                )
                                lc_delete_sql = f"UPDATE live_characters SET deleted=1 WHERE live_char_id={lc_id}"
                                self.db_fetch(
                                    self.chardata_db["db"],
                                    self.chardata_db["db_path"],
                                    lc_delete_sql,
                                    allow_edit=True,
                                )

                            # CHECK ACTION COMPLETED CORRECTLY
                            quick_check = self.check_delete_undelete(
                                pc_id, table, delete_id
                            )
                            return quick_check
                else:
                    logging.info(
                        f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['red']} "
                        f"NO table selected.{self.col['white']}"
                    )
                    return False
            else:
                logging.info(
                    f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['red']} "
                    f"{pc} with ID:{delete_id} does NOT exist in DB.{self.col['white']}"
                )
                return False
        else:
            logging.warning(
                f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['red']} You can only "
                f"use the mark_pc_for_deletion method to mark players, characters, or "
                f"live_characters.{self.col['white']}"
            )
            return False

    def remove_mark_pc_for_deletion(self, delete_id: int, pc: str = "player") -> bool:
        """Requires delete_id (string), pc (string); returns dict.
        Method to clear the deletion mark from a player or character - it actually HIDES character but doesn't
        DELETE character. Use purge_all_deleted_pc method for that.
        Available Options:
        delete_id: relevant id, either char_id or player_id
        pc: character, player or live_character
        """
        logging.info(
            f"{self.l_break}    {self.col['red']}[remove_mark_pc_for_deletion]{self.col['white']}"
        )

        if pc in self.pc_types:
            match pc:
                case "char":
                    table = "characters"
                case "live_char":
                    table = "live_characters"
                case _:
                    table = "players"
            pc_id = pc + "_id"

            logging.info(
                f"{self.chk} {self.sql_txt} {self.col['green']}REMOVING{self.col['white']} deletion "
                f"mark from {pc} with ID '{delete_id}'"
            )

            check_in_db = self.query_exists_in_db(delete_id, table, pc)

            if check_in_db:
                if table and pc_id:
                    # IS ID ALREADY MARKED FOR DELETION IN DB?
                    check_if_deleted_sql = f"SELECT {pc_id} FROM {table} WHERE {pc_id}={delete_id} and deleted=1"
                    is_deleted = self.db_fetch(
                        self.chardata_db["db"],
                        self.chardata_db["db_path"],
                        check_if_deleted_sql,
                    )

                    if is_deleted:
                        # YES -> RETURN TRUE
                        logging.info(
                            f"{self.chk} {self.sql_txt} {pc_id}:{delete_id} "
                            f"{self.col['red']}REMOVING{self.col['white']} mark for deletion in DB."
                        )

                        undelete_sql = (
                            f"UPDATE {table} SET deleted=0 WHERE {pc_id}={delete_id}"
                        )

                        self.db_fetch(
                            self.chardata_db["db"],
                            self.chardata_db["db_path"],
                            undelete_sql,
                            allow_edit=True,
                        )

                        # Also clear the live_char deletion mark
                        if pc == "char":
                            logging.info(
                                f"{self.chk} {self.sql_txt} Also removing deletion marks from "
                                f"{pc_id}:{delete_id} in live_characters table in DB."
                            )
                            lc = self.pc_exists_by_id(
                                delete_id, pc="live_char", lc=True
                            )
                            lc_id = lc[0][0]
                            logging.info(
                                f"{self.chk} {self.sql_txt} live_char_id:{lc_id}"
                            )
                            lc_delete_sql = f"UPDATE live_characters SET deleted=0 WHERE live_char_id={lc_id}"
                            self.db_fetch(
                                self.chardata_db["db"],
                                self.chardata_db["db_path"],
                                lc_delete_sql,
                                allow_edit=True,
                            )

                        # CHECK ACTION COMPLETED CORRECTLY
                        quick_check = self.check_delete_undelete(
                            pc_id, table, delete_id, undelete=True
                        )
                        return quick_check
                    else:
                        # NO -> SO CHECK IF ID ACTUALLY EXISTS
                        check_id_exists = self.query_exists_in_db(delete_id, table, pc)
                        if check_id_exists:
                            logging.info(
                                f"{self.chk} {self.sql_txt} {self.col['yellow']}{pc_id}:{delete_id} "
                                f"was NOT marked for deletion in DB.{self.col['white']}"
                            )
                            # Also clear the live_char deletion mark
                            if pc == "char":
                                logging.info(
                                    f"{self.chk} {self.sql_txt} Also removing deletion marks from "
                                    f"{pc_id}:{delete_id} in live_characters table in DB."
                                )
                                lc = self.pc_exists_by_id(
                                    delete_id, pc="live_char", lc=True
                                )
                                lc_id = lc[0][0]
                                logging.info(
                                    f"{self.chk} {self.sql_txt} live_char_id:{lc_id}"
                                )
                                lc_delete_sql = f"UPDATE live_characters SET deleted=0 WHERE live_char_id={lc_id}"
                                self.db_fetch(
                                    self.chardata_db["db"],
                                    self.chardata_db["db_path"],
                                    lc_delete_sql,
                                    allow_edit=True,
                                )
                            return True
                else:
                    logging.info(
                        f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['red']} "
                        f"NO table selected.{self.col['white']}"
                    )
                    return False
            else:
                logging.info(
                    f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['red']} "
                    f"{pc} with ID:{delete_id} does NOT exist in DB.{self.col['white']}"
                )
                return False
        else:
            logging.warning(
                f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['red']} You can only "
                f"use the mark_pc_for_deletion method to mark players, characters, or "
                f"live_characters.{self.col['white']}"
            )
            return False

    def purge_deleted_pc(self, pc: str = "player") -> bool:
        """Requires pc (string); returns bool.
        Purges (deletes) all the players or characters with the DELETED tag set to 1.
        Available Option:
        pc = player, character, or live_character
        """
        logging.info(
            f"{self.l_break}    {self.col['red']}[purge_deleted_pc]{self.col['white']}"
        )

        if pc in self.pc_types:
            match pc:
                case "char":
                    table = "characters"
                case "live_char":
                    table = "live_characters"
                case _:
                    table = "players"

            logging.warning(
                f"{self.cross} {self.sql_txt} {self.col['red']}"
                f"PURGING ALL {pc.upper()}S marked for deletion in DB.{self.col['white']}."
                f"This will PERMANENTLY delete them."
            )

            if pc:
                # CHECK IF ANY RECORDS ARE MARKED FOR DELETION
                check_if_deleted_sql = f"SELECT * FROM {table} WHERE deleted=1"

                need_delete = self.db_fetch(
                    self.chardata_db["db"],
                    self.chardata_db["db_path"],
                    check_if_deleted_sql,
                )

                if not need_delete:
                    # NO RECORDS ARE MARKED FOR DELETION -> RETURN FALSE
                    logging.info(
                        f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['red']} "
                        f"NO {table} marked for deletion in DB.{self.col['white']}"
                    )
                    return False
                else:
                    # RECORDS ARE MARKED FOR DELETION -> DELETE THEM
                    purge_sql = f"DELETE FROM {table} WHERE deleted=1"

                    self.db_fetch(
                        self.chardata_db["db"],
                        self.chardata_db["db_path"],
                        purge_sql,
                        allow_edit=True,
                    )

                    # CHECK ACTION COMPLETED CORRECTLY
                    purge_check_sql = f"SELECT * FROM {table} WHERE deleted=1"
                    purge_check_check = self.db_fetch(
                        self.chardata_db["db"],
                        self.chardata_db["db_path"],
                        purge_check_sql,
                    )

                    if not purge_check_check:
                        # NO RECORDS MARKED FOR DELETION REMAIN -> RETURN TRUE
                        logging.info(
                            f"{self.chk} {self.sql_txt} All deleted {table} "
                            f"{self.col['green']}SUCCESSFULLY{self.col['white']} purged from DB."
                        )
                        return True
                    else:
                        # RECORDS MARKED FOR DELETION STILL PRESENT -> RETURN FALSE
                        logging.info(
                            f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['red']} All deleted "
                            f"{table} NOT not purged from DB.{self.col['white']}"
                        )
                        return False
            else:
                logging.info(
                    f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['red']} "
                    f"NO table specified.{self.col['white']}"
                )
                return False
        else:
            logging.warning(
                f"{self.cross} {self.sql_txt} {self.err_txt} {self.col['red']} You can only "
                f"use the purge_all_deleted_pc method to purge players, characters, or "
                f"live_characters.{self.col['white']}"
            )

    def purge_all_deleted_pc(self):
        """Purges all deleted players, characters and live_characters"""
        logging.info(
            f"{self.l_break}    {self.col['red']}[purge_all_deleted_pc]{self.col['white']}"
        )

        logging.info(
            f"{self.chk} {self.sql_txt} {self.col['red']}"
            f"PURGING ALL PLAYERS, CHARACTERS and LIVE_CHARACTERS marked for deletion in DB.{self.col['white']}"
        )
        for x in self.pc_types:
            self.purge_deleted_pc(pc=x)
