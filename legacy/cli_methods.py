# encoding: utf-8
__version__ = "2.1.50"
__author__ = "Gunnar Roxen <gunnar@brokenshield.net>"

from character_dataclasses import (
    BSCMConfig,
    BreedTemplates,
    CharacterModel,
    LiveCharacterModel,
    CLIMenus,
)
from delete_methods import DeleteMethods

# from json import dumps
from time import sleep
import logging

logging.basicConfig(level=logging.WARNING)


class CLIMethods(DeleteMethods):
    """This class contains the methods necessary to use BSCM2 on the command line with python."""

    def __init__(self, **kwargs):
        super(DeleteMethods, self).__init__(**kwargs)
        bscm = BSCMConfig()
        self.bscm = bscm
        menus = CLIMenus()
        self.menus = menus
        bt = BreedTemplates()
        self.bt = bt

        which_app = "main.py"
        self.which_app = which_app

        char_options: dict = {}
        count = 0
        for char_type in bscm.valid_char_types:
            char_options[count] = char_type
            count += 1

        count = 0
        breeds_options: dict = {}
        for breed in bt.breeds_list:
            breeds_options[count] = self.string_pretty(input_text=breed)
            count += 1

        # These are generated here, so don't comment out!
        self.char_options = char_options
        self.breeds_options = breeds_options

        help_header: str = (
            f"{self.info} {self.col['c']}"
            f"HELP ________________________________________________________________\n"
        )
        self.help_header = help_header

        help_notes: list = [
            # 0
            f"{help_header}"
            f"    {self.col['w']}Mods{self.col['c']} "
            f"are Edges, Traits, Skill Points, Sliverware, Opportunity Points,\n"
            f"    Ranks, Disciples, Injuries, Wounds and anything else in the system",
            # 1
            f"{help_header}"
            f"    {self.col['c']}[*] is the {self.col['w']}default option{self.col['c']} for each menu\n"
            f"    _____________________________________________________________________\n"
            f"    For {self.col['r']}EXTERNAL{self.col['c']} use only. Remember: "
            f"{self.col['w']}THOTH{self.col['c']} is watching you!\n"
            f"    Please contact your nearest {self.col['m']}WEAVER-PRIEST{self.col['c']} if you suffer\n"
            f"    from any unexplained or paranormal side effects {self.col['y']}[CODE 0451]{self.col['c']}.\n"
            f"    For further information consult {self.col['g']}SPECIAL ORDER 937{self.col['c']}\n"
            f"    _____________________________________________________________________\n"
            f"    Author: {self.col['w']}{__author__}{self.col['c']}, version: {self.col['g']}{__version__}\n",
            # 2
            f"{help_header}"
            f"    Please enter the following information to create a new {self.col['w']}PLAYER{self.col['c']}.\n"
            f"    Don't worry, you will get to confirm, reject or quit at the end.",
            # 3
            f"{help_header}"
            f"    Please proceed through the following steps to create a new {self.col['w']}CHARACTER{self.col['c']}.\n"
            f"    Don't worry, you will get to confirm, reject or quit at the end.",
            # 4
            f"{help_header}"
            f"    Save files should be in the following format: \n"
            f"    {self.col['w']}(Character Name){self.char_save_file_tail}{self.col['c']}. For example: "
            f"'{self.col['w']}joe{self.char_save_file_tail}{self.col['c']}'.\n"
            f"    You don't need to add the {self.col['w']}'{self.char_save_file_tail}.json'{self.col['c']} "
            f"part of the save game file.\n",
            # 5
            f"\n    {self.col['c']}[*] is the {self.col['w']}default option{self.col['c']} for each menu\n",
            # 6
            f"{help_header}"
            f"    You don't need to add the {self.col['w']}'{self.char_save_file_tail}.json'{self.col['c']} "
            f"part of the save game file.\n",
            # 7
            f"{help_header}"
            f"    {self.col['c']}Thank you for using the {self.col['w']}BROKEN SHIELD "
            f"{self.col['m']}CHARACTER MANAGER V2 {self.col['y']}({self.col['w']}BSCM2{self.col['y']})"
            f"{self.col['c']}!\n\n"
            f"    To return to the BSCM2 app, please type the white text (below) and \n"
            f"    press enter: \n"
            f"    $ {self.col['w']}python {self.which_app}{self.col['w']}\n"
            f"    {self.col['c']}_____________________________________________________________________\n"
            f"    Author: {self.col['g']}{__author__}{self.col['c']}, version: {self.col['g']}{__version__}\n"
            f"    {self.col['c']}_____________________________________________________________________{self.col['w']}"
            f"\n",
        ]
        self.help_notes = help_notes

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def main(self, *args, **kwargs):

        print(
            f"{self.l_break}"
            f"{self.col['w']}WELCOME TO THE {self.col['c']}BROKEN SHIELD {self.col['m']}CHARACTER MANAGER V2 "
            f"{self.col['y']}({self.col['w']}BSCM2{self.col['y']})\n"
            f"                        {self.col['w']}PYTHON COMMAND LINE INTERFACE"
            f"{self.l_break}"
        )

        loaded_char: str = ""
        if hasattr(self.char, "char_id"):
            loaded_char = self._cli_loaded_player_info(char=self.char)
            notes: str = f"{loaded_char}{self.help_notes[5]}"
            char_id = getattr(self.char, "char_id", 0)
        else:
            notes: str = f"{self.help_notes[1]}"
            char_id = -1

        if self.char:
            char = self.char
        else:
            char = None

        if self.live_char:
            live_char = self.live_char
        else:
            live_char = None

        title: str = f"What would you like to do?"
        options = self._present_options_menu(
            options_dict=self.menus.select_options,
            title=title,
            notes=notes,
            default_choice=1,
        )

        match options[1]:
            case 0:
                print(f"{self.help_notes[7]}")
                sleep(self.bscm.sleep)
                quit()
            case 2:
                # List All Players
                self.cli_list_all_pcs(list_type="player")
            case 3:
                # Create a New Player
                self.cli_create_new_player()
            case 4:
                # List All Characters
                self.cli_list_all_pcs(list_type="character")
            case 5:
                # Create a New Character
                self.cli_create_new_char()
            case 6:
                # Load Character
                self.cli_load_char()
            case 7:
                # View currently loaded char's CharacterModel
                if loaded_char:
                    if char:
                        self.cli_search_like(
                            search_type="char", search_id=char_id, char=char
                        )
                    else:
                        self.cli_search_like(search_type="char", search_id=char_id)
                else:
                    print(
                        f"\n{self.cross} {self.col['r']}You need to load a {self.col['w']}character{self.col['r']} "
                        f"first before they can be viewed with this option!{self.col['w']}\n"
                    )
                    sleep(self.bscm.sleep)
                    self.cli_load_char()
            case 8:
                # View currently loaded char's LiveCharacterModel
                if loaded_char:
                    if live_char:
                        self.cli_search_like(
                            search_type="live_char",
                            search_id=char_id,
                            live_char=live_char,
                        )
                    else:
                        self.cli_search_like(search_type="live_char", search_id=char_id)
                else:
                    print(
                        f"\n{self.cross} {self.col['r']}You need to load a {self.col['w']}character{self.col['r']} "
                        f"first before they can be viewed with this option!{self.col['w']}\n"
                    )
                    sleep(self.bscm.sleep)
                    self.cli_load_char()
            case 9:
                # Save Currently Loaded Character
                if loaded_char:
                    self.cli_save_char(char=char, live_char=live_char, header=True)
                else:
                    print(
                        f"\n{self.cross} {self.col['r']}You need to load a {self.col['w']}character{self.col['r']} "
                        f"first before they can be saved to the database!{self.col['w']}\n"
                    )
                    sleep(self.bscm.sleep)
                    self.cli_load_char()
            case 10:
                # Export Character to JSON
                if loaded_char:
                    self.cli_save_char(char=char, live_char=live_char)
                    self.cli_export_char()
                else:
                    print(
                        f"\n{self.cross} {self.col['r']}You need to load a {self.col['w']} first before they can be "
                        f"exported to a save file!{self.col['w']}\n"
                    )
                    sleep(self.bscm.sleep)
                    self.cli_load_char()
            case 11:
                # Import NEW Character from JSON
                self.cli_import_char()
            case 12:
                if loaded_char:
                    if char:
                        self.cli_list_free_nodes(char=char, cli_print=True)
                    else:
                        self.cli_list_free_nodes(cli_print=True)
                else:
                    print(
                        f"\n{self.cross} {self.col['r']}You need to load a {self.col['w']} first before you can see "
                        f"what available node slots for skills, edges, traits etc. they have!{self.col['w']}\n"
                    )
                    sleep(self.bscm.sleep)
                    self.cli_load_char()
            case 13:
                # Spent Talent Points
                if loaded_char:
                    if char:
                        self.cli_mod_options_list(char=char)
                    else:
                        self.cli_mod_options_list()
                else:
                    print(
                        f"\n{self.cross} {self.col['r']}You need to load a {self.col['w']} first before you can spend "
                        f"any Talent Points!{self.col['w']}\n"
                    )
                    sleep(self.bscm.sleep)
                    self.cli_load_char()
            case _:
                # Search for Player, Character, Live Character or Mod
                self.cli_search_frontend()

    def cli_load_char(self, header: bool = True):
        """Simple method for loading a character into memory."""
        if header:
            print(
                f"{self.l_break}"
                f"{self.ind2}{self.col['w']}LOAD CHARACTER{self.col['y']}"
                f"{self.l_break}"
            )

        print(f"{self.chk} {self.col['y']}Please choose a character to load:\n")
        # Load Character:
        self.cli_list_all_pcs(
            list_type="char", header=False, load_character=True, cli_print=False
        )
        char = self.char
        live_char = self.live_char

        print(
            f"{self.chk} {self.col['g']}Character {self.col['w']}{self.string_pretty(char.char_name)}{self.col['g']} "
            f"successfully loaded! ({live_char.char_id}){self.col['w']}"
        )
        self._any_key_to_continue()

    def cli_save_char(
        self,
        char: CharacterModel = None,
        live_char: LiveCharacterModel = None,
        header: bool = False,
    ):
        """Simple method for saving the currently loaded character to DB"""
        if header:
            print(
                f"{self.l_break}"
                f"{self.ind2}{self.col['w']}SAVE CURRENT CHARACTER{self.col['y']}"
                f"{self.l_break}"
            )

        if not char:
            char = self.char

        if not live_char:
            if hasattr(self.live_char, "char_id"):
                live_char = self.live_char

        self.save_complete_character(char=char, live_char=live_char)

        print(
            f"{self.chk} {self.col['g']}Character {self.col['w']}{self.string_pretty(char.char_name)}{self.col['g']} "
            f"successfully saved to the database!{self.col['w']}"
        )
        if header:
            self._any_key_to_continue()

    def cli_search_frontend(self):
        print(
            f"{self.l_break}"
            f"{self.ind2}{self.col['w']}SEARCH{self.col['y']}"
            f"{self.l_break}"
        )

        title: str = "What would you like to search for?"
        notes: str = self.help_notes[0]

        options = self._present_options_menu(
            options_dict=self.menus.search_options,
            title=title,
            notes=notes,
            default_choice=4,
        )

        match options[1]:
            case 0:
                self._return_to_main()
            case 1:
                self.cli_search_like(search_type="player")
            case 2:
                self.cli_search_like(search_type="char")
            case 3:
                self.cli_search_like(search_type="live_char")
            case 4:
                self.cli_search_like(search_type="mod")
            case _:
                self._return_to_main()

    def cli_list_all_pcs(
        self,
        list_type: str = "player",
        header: bool = True,
        load_character: bool = False,
        cli_print: bool = False,
    ):
        """Method to list all players/characters in the DB and optionally load them."""
        if header:
            print(
                f"{self.l_break}"
                f"{self.ind2}{self.col['w']}LISTING ALL {list_type.upper()}S{self.col['y']}"
                f"{self.l_break}"
            )
        if list_type == "character":
            search_tuple = self.list_pc(pc="char", cli_print=cli_print)
            search_type = "char"
        else:
            search_tuple = self.list_pc(pc=list_type, cli_print=cli_print)
            search_type = list_type

        if load_character:
            search_text = f"\n{self.chk} {self.col['y']}Enter {self.col['w']}#{self.col['y']} of character to load"
        else:
            search_text = (
                f"\n{self.chk} {self.col['y']}Enter the {self.col['w']}#{self.col['y']} of the {list_type} "
                f"to view in more detail"
            )

        end_text = f", or {self.col['w']}0{self.col['y']} to return to the main menu.\n"

        print(f"{search_text}{end_text}")

        id_search = input(
            f"{self.chk} {self.col['y']}Please enter your selected option: [{self.col['g']}0{self.col['y']}-"
            f"{self.col['g']}{len(search_tuple)}{self.col['y']}]:{self.col['w']} "
        )

        if id_search.isnumeric():
            id_search = int(id_search)
            if id_search == 0:
                self._return_to_main()

            elif 0 < id_search <= len(search_tuple):

                id_index = int(id_search) - 1
                more_detail = search_tuple[id_index][1]
                if load_character:
                    print(
                        f"{self.chk} {self.col['g']}Loading {self.col['w']}"
                        f"{more_detail}{self.col['g']}..."
                    )
                    sleep(self.bscm.sleep)
                    pc_id = self.pc_exists_by_name(
                        search_name=more_detail.lower(), pc=search_type, lower_case=True
                    )
                    if list_type == "player":
                        load_player = self.load_player(player_id=pc_id[0][0])
                        self.player = load_player
                    else:
                        load_char_tuple = self.load_complete_character(
                            char_id=pc_id[0][0]
                        )
                        if cli_print:
                            self.print_char_model()
                            # This sets self.char and self.live_char
                else:
                    self.cli_search_like(
                        search_type=search_type, search_str=more_detail
                    )
                    repeat_search_text = (
                        f"{self.col['y']}Would you like to return to the list of "
                        f"{self.col['w']}{list_type.title()}s{self.col['y']}?"
                    )
                    options = self._present_options_menu(
                        options_dict=self.menus.yes_quit,
                        title=repeat_search_text,
                        default_choice=0,
                    )
                    match options[1]:
                        case 1:
                            self.cli_list_all_pcs(
                                list_type=list_type,
                                header=header,
                                load_character=load_character,
                            )
                        case _:
                            self._return_to_main()
            else:
                self._list_all_pcs_error(
                    search_tuple=search_tuple,
                    list_type=list_type,
                    header=header,
                    load_character=load_character,
                )
        else:
            self._list_all_pcs_error(
                search_tuple=search_tuple,
                list_type=list_type,
                header=header,
                load_character=load_character,
            )

    def _list_all_pcs_error(
        self,
        search_tuple: tuple,
        list_type: str = "player",
        header: bool = True,
        load_character: bool = False,
    ):
        """Private method to just save some repetitive code"""
        print(
            f"\n{self.cross} {self.col['r']}ERROR: Please enter a number between "
            f"{self.col['w']}0{self.col['r']} and {self.col['w']}{len(search_tuple)}{self.col['r']}!"
            f"{self.col['w']}\n"
        )
        sleep(self.bscm.sleep)
        self.cli_list_all_pcs(
            list_type=list_type,
            header=header,
            load_character=load_character,
        )

    def cli_create_new_player(self, header: bool = True):
        """Method to create a new character via the CLI."""
        player_name: str
        player_real_name: str
        player_email: str

        if header:
            print(
                f"{self.l_break}"
                f"{self.ind2}{self.col['w']}CREATE NEW PLAYER{self.col['y']}"
                f"{self.l_break}"
            )
            print(f"{self.help_notes[2]}")

        print(" ")
        player_name = self._check_name(pc="player", step=1)
        if player_name:
            unsafe_real_name = input(
                f"{self.chk} {self.col['m']}STEP 2......\n"
                f"{self.chk} {self.col['y']}Please enter the player's {self.col['w']}REAL NAME{self.col['y']} "
                f"{self.col['b']}[Optional]{self.col['y']}:{self.col['w']} "
            )
            if unsafe_real_name:
                player_real_name = self.string_safe(
                    input_string=unsafe_real_name,
                    input_name="Player Real Name",
                    to_lower=True,
                    allow_hyphen=True,
                    allow_at=True,
                )
                print(
                    f"\n     - Player Name {self.col['b']}[Optional]{self.col['y']} = "
                    f"{self.col['g']}{player_real_name}{self.col['y']}\n"
                )

            else:
                player_real_name = ""
            unsafe_email = input(
                f"{self.chk} {self.col['m']}STEP 3......\n"
                f"{self.chk} {self.col['y']}Please enter the player's {self.col['w']}EMAIL ADDRESS{self.col['y']} "
                f"{self.col['b']}[Optional]{self.col['y']}: {self.col['w']} "
            )
            if unsafe_email:
                if "@" in unsafe_email:
                    if "." in unsafe_email:
                        player_email = self.string_safe(
                            input_string=unsafe_email,
                            input_name="Player Email",
                            to_lower=True,
                            allow_hyphen=True,
                            allow_at=True,
                        )
                    else:
                        print(
                            f"\n{self.cross} {self.col['r']}ERROR: All email addresses MUST include the "
                            f"{self.col['w']}'.'{self.col['r']} symbol!"
                            f"{self.col['w']}\n"
                        )
                        unsafe_email = ""
                        player_email = ""
                else:
                    print(
                        f"\n{self.cross} {self.col['r']}ERROR: All email addresses MUST include the "
                        f"{self.col['w']}'@'{self.col['r']} symbol!"
                        f"{self.col['w']}\n"
                    )
                    unsafe_email = ""
                    player_email = ""
            else:
                player_email = ""

            print(
                f"{self.info} {self.col['y']}You entered the following information:\n"
                f"{self.ind0}{self.col['y']}- {self.col['w']}Player Username{self.col['y']}      = "
                f"{self.col['g']}{player_name}{self.col['w']}\n"
                f"{self.ind0}{self.col['y']}- {self.col['w']}Player Real Name{self.col['y']}     = "
                f"{self.col['g']}{player_real_name}{self.col['w']}\n"
                f"{self.ind0}{self.col['y']}- {self.col['w']}Player Email Address{self.col['y']} = "
                f"{self.col['g']}{player_email}{self.col['w']}\n\n"
            )
            player_confirm = (
                f"{self.col['m']}STEP 4......\n"
                f"{self.chk} {self.col['y']}Is this player information listed "
                f"{self.col['w']}above{self.col['y']} correct?"
            )
            options = self._present_options_menu(
                options_dict=self.menus.yes_no_quit,
                title=player_confirm,
                default_choice=1,
            )

            match options[1]:
                case 0:
                    self._return_to_main()
                case 2:
                    print(
                        f"\n{self.cross} {self.col['r']}Information was incorrect. Retrying... {self.col['w']}"
                    )
                    self.cli_create_new_player(header=False)
                case _:
                    print(
                        f"\n{self.chk} {self.col['y']}Information was {self.col['g']}correct{self.col['y']}. "
                    )
                    print(
                        f"{self.chk} {self.col['g']}Creating a new player called '{player_name}'!{self.col['w']}\n"
                    )
                    new_player = self.new_or_update_player(
                        player_name=player_name,
                        player_real_name=player_real_name,
                        player_email=player_email,
                    )
                    self.print_player_model(player=new_player)
                    self._return_to_main()
        else:
            self.cli_create_new_player(header=False)

    def cli_create_new_char(self, header: bool = True, proceed: bool = False):
        """This method adds a CLI way to create a new character and save it to the DB."""
        bt = BreedTemplates()
        char_name: str
        char_archetype: str
        char_type: str
        player_id: int

        if header:
            print(
                f"{self.l_break}"
                f"{self.ind2}{self.col['w']}CREATE A NEW CHARACTER{self.col['y']}"
                f"{self.l_break}"
            )
            print(f"{self.help_notes[3]}")

        # SET PLAYER ID
        player_choice = (
            f"\n{self.chk} {self.col['m']}STEP 1......\n"
            f"{self.chk} {self.col['y']}What is the {self.col['w']}PLAYER ID#{self.col['y']} of the player "
            f"whom will play this character {self.col['r']}[REQUIRED]{self.col['y']}?{self.col['w']} "
        )

        unsafe_player_id = input(f"{player_choice}")
        unsafe_player_id = int(unsafe_player_id)

        # print(f"\n")

        if unsafe_player_id > -1:
            is_player = self.pc_exists_by_id(search_id=unsafe_player_id, pc="player")
            player_name = self.string_pretty(is_player[0][2])
            is_player_text = (
                f"{self.col['g']}Player ID:{self.col['w']}{unsafe_player_id}'s{self.col['g']} name is:\n"
                f"{self.col['w']}'{player_name}'\n"
                f"{self.col['g']}Is that the correct player?"
            )
            options = self._present_options_menu(
                options_dict=self.menus.yes_no,
                title=is_player_text,
                default_choice=1,
            )

            match options[1]:
                case 0:
                    print(
                        f"\n{self.cross} {self.col['r']}Incorrect player. Please check this list of "
                        f"players:{self.col['w']}"
                    )
                    self.cli_list_all_pcs(
                        list_type="player",
                        header=False,
                    )
                    self.cli_create_new_char(header=False)
                case _:
                    player_id = unsafe_player_id
                    print(
                        f"\n     {self.col['y']}- {self.col['w']}Player ID{self.col['y']} "
                        f"{self.col['r']}[REQUIRED]{self.col['y']} = {self.col['g']}{player_id}\n"
                    )

                    # SET CHAR NAME:
                    char_name = self._check_name(pc="char", step=2)
                    if char_name:

                        # SET CHAR TITLE:
                        char_archetype = self._check_str_field(
                            field="Character Archetype",
                            pc="char",
                            step=3,
                            parenthesis=True,
                            allow_hyphen=True,
                            skip_confirm=True,
                        )

                        # SET CHAR TYPE:
                        type_of_char = (
                            f"{self.col['m']}STEP 4......\n"
                            f"{self.chk} {self.col['y']}What {self.col['w']}TYPE{self.col['y']} of character are "
                            f"you making {self.col['r']}[REQUIRED]{self.col['y']}?"
                        )
                        options_a = self._present_options_menu(
                            options_dict=self.char_options,
                            title=type_of_char,
                            default_choice=0,
                        )
                        if options_a[1] <= options_a[0]:
                            char_type = self.char_options[options_a[1]]
                            print(
                                f"\n     {self.col['y']}- {self.col['w']}Character Type "
                                f"{self.col['r']}[REQUIRED]{self.col['y']} = "
                                f"{self.col['g']}{char_type.title()}\n"
                            )

                            proceed = True
                        else:
                            print(
                                f"{self.cross} {self.col['r']}ERROR! Unrecognised Character Type! Setting "
                                f"character type to {self.col['w']}'{self.char_options[options_a[1]].title()}"
                            )
                            char_type = self.char_options[0]
                            proceed = True

                        if proceed:
                            # Time to save the information to the CharacterModel and the DB:
                            char = self.new_or_update_char(
                                char_name=char_name,
                                player_id=player_id,
                                char_archetype=char_archetype,
                                char_type=char_type,
                                write_to_db=True,
                                cli_print=True,
                            )

                            char = self.cli_choose_breed(
                                char=char,
                                step=5,
                            )

                            current_culture_mod_id = char.nodes["culture_n0"]
                            culture_name = self.get_mod_name(
                                mod_id=current_culture_mod_id
                            )

                            # Summary...
                            print(
                                f"{self.chk} {self.col['m']}STEP 5......"
                                f"\n{self.info} {self.col['g']}Here are the details for your character "
                                f"{self.col['w']}{char.char_name}{self.col['g']} so far:\n"
                                f"{self.ind0}{self.col['y']}- {self.col['w']}Player ID{self.col['y']}           = "
                                f"{self.col['g']}{player_id}{self.col['w']}\n"
                                f"{self.ind0}{self.col['y']}- {self.col['w']}Player Name{self.col['y']}         = "
                                f"{self.col['g']}{player_name}{self.col['w']}\n"
                                f"{self.ind0}{self.col['y']}- {self.col['w']}Character ID{self.col['y']}        = "
                                f"{self.col['g']}{char.char_id}{self.col['w']}\n"
                                f"{self.ind0}{self.col['y']}- {self.col['w']}Character Name{self.col['y']}      = "
                                f"{self.col['g']}{char_name.title()}{self.col['w']}\n"
                                f"{self.ind0}{self.col['y']}- {self.col['w']}Character Archetype{self.col['y']} = "
                                f"{self.col['g']}{char_archetype.title()}{self.col['w']}\n"
                                f"{self.ind0}{self.col['y']}- {self.col['w']}Character Type{self.col['y']}      = "
                                f"{self.col['g']}{char_type.title()}{self.col['w']}\n"
                                f"{self.ind0}{self.col['y']}- {self.col['w']}Character Breed{self.col['y']}     = "
                                f"{self.col['g']}{char.breed.title()}{self.col['w']}\n"
                                f"{self.ind0}{self.col['y']}- {self.col['w']}Character Culture{self.col['y']}   = "
                                f"{self.col['g']}{culture_name.title()}{self.col['w']}\n"
                                f"\n{self.chk}{self.col['y']}You can now add additional Skills, Opportunity Points, "
                                f"Edges, Traits, Sliverware and character information from the main menu!"
                                f"{self.col['w']}"
                            )
                            self.housekeeping(char=char)

                            self.print_char_model(char=char)

                            self.save_complete_character(
                                char=char, live_char=self.live_char
                            )
                            self._return_to_main()
                        else:
                            self.cli_create_new_char(header=False)
                    else:
                        self.cli_create_new_char(header=False)
        else:
            self.cli_create_new_char(header=False)

    def cli_choose_breed(
        self,
        char: CharacterModel,
        step: int = 0,
    ) -> CharacterModel:
        bt = BreedTemplates()
        breeds_list: list = []
        breed_mod_name: str = ""
        char_name: str = char.char_name
        proceed: bool

        for breed in bt.breeds_list:
            breeds_list.append(breed)

        if step > 0:
            step_text = f"{self.col['m']}STEP {step}......\n"
        else:
            step_text = ""

        breed_choice = (
            f"{step_text}{self.chk} {self.col['y']}What {self.col['w']}BREED{self.col['y']} "
            f"is your character {self.col['w']}{char_name.title()}"
            f"{self.col['r']} [REQUIRED]{self.col['y']}?{self.col['w']} "
        )
        options_c = self._present_options_menu(
            options_dict=self.breeds_options,
            title=breed_choice,
            default_choice=0,
            char=char,
        )

        match options_c[1]:
            case 0:
                # Human
                breed_mod_name = breeds_list[0]
            case 1:
                # Hulk
                breed_mod_name = breeds_list[1]
            case 2:
                # Gethan
                breed_mod_name = breeds_list[2]
            case 3:
                # Kapaethjan Pure
                breed_mod_name = breeds_list[3]
            case 4:
                # Balláetic Pure
                breed_mod_name = breeds_list[4]
            case 5:
                # Motley Pure
                breed_mod_name = breeds_list[5]
            case 6:
                # Fallen Pure
                breed_mod_name = breeds_list[6]
            case 7:
                # Atropoan
                breed_mod_name = breeds_list[7]
            case 8:
                # Feral
                breed_mod_name = breeds_list[8]
            case 9:
                # Creature
                breed_mod_name = breeds_list[9]
            case 10:
                # Rezhadi
                breed_mod_name = breeds_list[10]

        breed_name = self.string_pretty(input_text=breed_mod_name)

        char = self.apply_breed_template_to_char(breed=breed_mod_name, char=char)

        print(
            f"\n     {self.col['y']}- {self.col['w']}Breed "
            f"{self.col['y']}{self.col['r']}[REQUIRED]{self.col['y']}{self.col['y']} = "
            f"{self.col['g']}{breed_name.title()}\n"
        )

        return char

    def cli_mod_options_list(
        self,
        char: CharacterModel = None,
        step: int = 0,
        header: bool = True,
    ) -> None:
        """This method is a general menu for modifying a character and will get looped back into repeatedly."""
        end_loop: bool = False

        if not char:
            print(
                f"\n{self.chk} {self.col['y']}Before you can alter a character, please choose a character to load."
            )
            # Load PC First:
            self.cli_list_all_pcs(list_type="char", header=False, load_character=True)
            char = self.char

        live_char = self.live_char

        count = 0

        # Now we make a User Input while loop so the player can make multiple changes
        while not end_loop:
            count += 1
            add_mod_text = self._cli_header(
                step=step,
                optional=True,
                header=header,
                choose="alter",
                char_name=char.char_name,
                header_name="Mod or Detail",
            )

            options = self._present_options_menu(
                options_dict=self.menus.mod_options,
                title=add_mod_text,
                default_choice=0,
                char=char,
            )

            stub1 = f"\n{self.info} {self.col['g']}You chose to "
            stub2 = f" your character {self.col['w']}{char.char_name.title()}{self.col['g']}. \n"

            # XXX

            match options[1]:
                case 0:
                    end_loop = True
                    self._return_to_main()
                case 2:
                    action = f"Add an Opportunity Point from"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.cli_display_mod_sets(
                        char=char,
                        mod_cat="opportunity",
                        search_type="cat",
                        step=step,
                    )
                case 3:
                    action = f"Add a Cybernetic Sliverware Implant from"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.cli_display_mod_sets(
                        char=char,
                        mod_cat="cyb",
                        search_type="cat",
                        step=step,
                    )
                case 4:
                    action = f"Add a Biogenetic Sliverware Implant from"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.cli_display_mod_sets(
                        char=char,
                        mod_cat="bio",
                        search_type="cat",
                        step=step,
                    )
                case 5:
                    action = f"Add an Edge from"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.cli_display_mod_sets(
                        char=char,
                        mod_cat="edge",
                        search_type="cat",
                        step=step,
                    )
                case 6:
                    action = f"Add a Trait from"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.cli_display_mod_sets(
                        char=char,
                        mod_cat="trait",
                        search_type="cat",
                        step=step,
                    )
                case 7:
                    action = f"Add a Specialisation Mastery from"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.cli_display_mod_sets(
                        char=char,
                        mod_cat="trait",
                        search_type="cat",
                        step=step,
                    )
                case 8:
                    action = f"Set the Starting Talent Points of"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.set_char_details(
                        char=char,
                        live_char=live_char,
                        char_detail="talent_points",
                        step=step,
                    )
                case 9:
                    action = f"Set the Earned Talent Points of"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.set_char_details(
                        char=char,
                        live_char=live_char,
                        char_detail="talent_points_earned",
                        step=step,
                    )
                case 10:
                    action = f"Set an Echo Power, or Wyld Cancer and Wyld Permanent Injuries for"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.set_char_details(
                        char=char,
                        live_char=live_char,
                        char_detail="echo_wyld_cancer",
                        step=step,
                    )
                case 11:
                    action = f"Set the Breed and Culture of"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.cli_choose_breed(char=char, step=step)
                case 12:
                    action = f"Set the Patron Disciple(s) and Avatar of"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.set_char_details(
                        char=char,
                        live_char=live_char,
                        char_detail="disciple",
                        step=step,
                    )
                case 13:
                    action = (
                        f"Set the Organisation, Rank, Commendations and Reprimands of"
                    )
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.set_char_details(
                        char=char,
                        live_char=live_char,
                        char_detail="org_rank",
                        step=step,
                    )
                case 14:
                    action = f"Set the Age, Gender and Description of"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.set_char_details(
                        char=char,
                        live_char=live_char,
                        char_detail="age_gender_desc",
                        step=step,
                    )
                case 15:
                    action = f"Set the fluent Languages for"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.set_char_details(
                        char=char,
                        live_char=live_char,
                        char_detail="languages",
                        step=step,
                    )
                case 16:
                    action = f"Set the Weapons and Equipment of"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.set_char_details(
                        char=char,
                        live_char=live_char,
                        char_detail="weapons_equip",
                        step=step,
                    )
                case 17:
                    action = f"Set the Contacts, Allies and Enemies of"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.set_char_details(
                        char=char,
                        live_char=live_char,
                        char_detail="contacts",
                        step=step,
                    )
                case 18:
                    action = f"Modify the various Notes for"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.set_char_details(
                        char=char, live_char=live_char, char_detail="notes", step=step
                    )
                case 19:
                    action = f"Load Free Nodes for"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.cli_list_free_nodes(char=char, cli_print=True)
                case _:
                    action = f"Add a Skill Point from"
                    print(f"{stub1}{action}{stub2}", flush=True)
                    self.cli_display_mod_sets(
                        char=char,
                        mod_cat="skill",
                        search_type="cat",
                        step=step,
                    )

    def set_char_details(
        self,
        char: CharacterModel,
        live_char: LiveCharacterModel,
        char_detail: str = "",
        header: bool = True,
        step: int = 0,
    ):
        """This method sets the non-skill/edges/traits/sliverware."""
        match char_detail:
            case "talent_points":
                self.set_char_int_val(
                    user_key="tp_create",
                    nice_key="Starting TPs",
                    char_or_live=True,
                    replace_or_add=True,
                    char=char,
                    live_char=live_char,
                    cli_query=True,
                    cli_print=True,
                )
                self._any_key_to_continue()

                # sleep(self.bscm.sleep)
                # self.cli_mod_options_list(char=char, step=step, header=header)

            case "talent_points_earned":
                self.set_char_int_val(
                    user_key="tp_missions",
                    nice_key="Mission Earned TPs",
                    char_or_live=True,
                    replace_or_add=True,
                    char=char,
                    live_char=live_char,
                    cli_query=True,
                    cli_print=True,
                )
                # sleep(self.bscm.sleep)
                self._any_key_to_continue()
                # self.cli_mod_options_list(char=char, step=step, header=header)
            case "echo_wyld_cancer":
                pass
            case "disciple":
                pass
            case "org_rank":
                pass
            case "age_gender_desc":
                pass
            case "languages":
                pass
            case "weapons_equip":
                pass
            case "contacts":
                pass
            case "notes":
                pass

    def cli_display_mod_sets(
        self,
        char: CharacterModel,
        header: bool = True,
        search_text: str = "",
        mod_cat: str = "",
        mod_type: str = "",
        search_type: str = "",
        step: int = 0,
    ):
        """This method adds a mod to a character, in effect spending a Talent Point, though some are free and Traits
        actually give the player some more TPs.
        Process:
        1. Select Proceed
        2. Search for MOD ID
        3. Check requirements (light check of prerequisites/restrictions etc)
        4. If not allowed, option to set override
        5. Search for Mod Location (list allowed locations only)
        6. Select location
        7. Enter Mod ID
        8. Add another Mod or quit this part?
        """
        # TODO: perform self.housekeeping(char=char)
        mod_sliver: str = ""
        mod_type: str = "uni"
        search_type: str = "cat"
        end_loop: bool = False

        match mod_cat:
            case "edge":
                options_menu = self.menus.edge_cat_options
                art = "an"
                header_name = "Edge"
            case "trait":
                options_menu = self.menus.trait_cat_options
                art = "a"
                header_name = "Trait"
            case "skill":
                options_menu = self.menus.skill_cat_options
                art = "a"
                header_name = "Skill"
            case "opportunity":
                options_menu = self.menus.opportunity_cat_options
                art = "an"
                header_name = "Opportunity"
            case "bio":
                options_menu = self.menus.bio_cat_options
                art = "a"
                header_name = "Bioware Implant"
            case "cyb":
                options_menu = self.menus.cyb_cat_options
                art = "a"
                header_name = "Cyberware Implant"
            case "smx":
                options_menu = self.menus.smx_cat_options
                art = "a"
                header_name = "Specialisation Mastery"
            case _:
                options_menu = self.menus.edge_cat_options
                art = "an"
                header_name = "Edge"

        if header:
            print(
                f"{self.l_break}"
                f"{self.ind2}{self.col['w']}ADD {art.upper()} {header_name.upper()}{self.col['y']}"
                f"{self.l_break}"
            )

        title = (
            f"Please choose one of the options below for the type of "
            f"{self.col['w']}{header_name.upper()}{self.col['y']} you would like to add: {self.col['w']}"
        )

        options = self._present_options_menu(
            options_dict=options_menu, title=title, default_choice=0, char=char
        )

        # XXX
        # TODO: Make sure we filter out the options that are unavailable to the character!

        if options[1] == 0:
            self.cli_mod_options_list(char=char, step=step, header=header)
        else:
            match mod_cat:
                case "edge":
                    search_type = "cat_type"
                    match options[1]:
                        case 2:
                            mod_type = "uni"
                        case 3:
                            mod_type = "pkc"
                        case 4:
                            mod_type = "ssw"
                        case 5:
                            mod_type = "rmv"
                        case 6:
                            mod_type = "wex"
                        case 7:
                            mod_type = "dgx"
                        case 8:
                            mod_type = "mce"
                        case 9:
                            mod_type = "gas"
                        case _:
                            # Option 1
                            mod_type = ""
                case "trait":
                    search_type = "cat_type"
                    match options[1]:
                        case 2:
                            mod_type = "pas"
                        case 3:
                            mod_type = "beh"
                        case 4:
                            mod_type = "nar"
                        case 5:
                            mod_type = "gas"
                        case _:
                            # Option 1
                            mod_type = ""
                case "opportunity":
                    search_type = "cat_type"
                    mod_type = "opp"
                    match options[1]:
                        case 2:
                            search_text = "smarts"
                        case 3:
                            search_text = "resources"
                        case 4:
                            search_text = "wyld"
                        case 5:
                            search_text = "divinity"
                        case _:
                            # Option 1
                            search_text = "physical"
                case "cyb":
                    # XXX
                    mod_sliver = "sliverware"
                    search_type = "sliver"
                    mod_type = "cyb"
                    match options[1]:
                        case 2:
                            sliver_list = self.bscm.sliver_headlink
                        case 3:
                            sliver_list = self.bscm.sliver_optics
                        case 4:
                            sliver_list = self.bscm.sliver_neuralrewiring
                        case _:
                            # Option 1
                            sliver_list = self.bscm.sliver_bodyweb
                    for i in sliver_list:
                        if search_text:
                            search_text = f"{search_text}' OR mod_id='{i}"
                        else:
                            search_text = f"{i}"
                case "bio":
                    mod_sliver = "sliverware"
                    search_type = "sliver"
                    mod_type = "bio"
                    match options[1]:
                        case 2:
                            sliver_list = self.bscm.sliver_biocore
                        case 3:
                            sliver_list = self.bscm.sliver_nanocore
                        case _:
                            # Option 1
                            sliver_list = self.bscm.sliver_biosculpting
                    for i in sliver_list:
                        if search_text:
                            search_text = f"{search_text}' OR mod_id='{i}"
                        else:
                            search_text = f"{i}"
                case "skill":
                    pass
                case "smx":
                    pass

        if mod_sliver:
            mod_cat_search = mod_sliver
        else:
            mod_cat_search = mod_cat

        self.cli_search_like_mod(
            char=char,
            header=False,
            search_text=search_text,
            mod_cat=mod_cat_search,
            mod_type=mod_type,
            search_type=search_type,
        )

        return mod_type

    def cli_list_free_slots(self, char: CharacterModel, cli_print: bool = False):
        # Load the full list of a character's locations and current nodes into a dict
        free_locations: list = self.get_char_free_nodes(char=char, cli_print=cli_print)

        location_options: dict = {}

        title: str = "What location you like to add or remove a mod from?"
        notes: str = self.help_notes[0]

        count = 1
        for location in free_locations:
            location_options[count] = location
            count += 1

        options = self._present_options_menu(
            options_dict=location_options, title=title, notes=notes, default_choice=0
        )

        # XXX

    def cli_import_char(self):
        """Method to import a new character from a JSON file"""
        bscm = self.bscm
        print(
            f"{self.l_break}"
            f"{self.ind2}{self.col['w']}IMPORT CHARACTER{self.col['y']}"
            f"{self.l_break}"
        )
        proceed: bool = False
        filename: str = ""

        print(f"{self.help_notes[4]}")

        while not proceed:
            # Request filename
            input_file_name = input(
                f"\n"
                f"{self.chk} {self.col['m']}STEP 1......\n"
                f"{self.chk} {self.col['y']}What is the {self.col['w']}NAME{self.col['y']} of the save file you wish "
                f"to import?{self.col['w']} "
            )

            filename_input = f"{input_file_name.lower()}{self.char_save_file_tail}"
            if ".json" in filename_input:
                filename_input = filename_input.replace(".json", "")
            if self.char_save_file_tail in filename_input:
                filename_input = filename_input.replace(self.char_save_file_tail, "")
            filename = self.string_safe(
                input_string=filename_input,
                to_lower=True,
                parenthesis=True,
                allow_hyphen=True,
            )
            filename = f"{filename}{self.char_save_file_tail}"

            # Confirm file name:
            load_proceed_text = f"{self.col['y']}Is the file name {self.col['w']}'{filename}'{self.col['y']}?"
            load_proceed = self._present_options_menu(
                options_dict=self.menus.yes_no_quit,
                title=load_proceed_text,
                default_choice=1,
            )

            match load_proceed:
                case 0:
                    proceed = False
                    self._return_to_main()
                case 2:
                    print(
                        f"\n{self.cross}{self.col['r']}Please enter the {self.col['w']}filename{self.col['r']} "
                        f"of the character save game file...{self.col['w']}"
                    )
                    proceed = False
                    sleep(self.bscm.sleep)
                case _:
                    print(
                        f"\n{self.chk} {self.col['g']}Loading {self.col['w']}'{filename}.json'{self.col['g']}..."
                        f"{self.col['w']}"
                    )
                    sleep(self.bscm.sleep)
                    proceed = True

        if proceed:
            char_dict = self.open_json(
                readfile=filename, directory="import", cli_print=True
            )
            # VALIDATION
            # We validate and check several key details:
            char_name = self.string_safe(
                input_string=char_dict["char_name"], allow_hyphen=True
            )
            char_dict["char_name"] = char_name
            raw_player_id = char_dict["player_id"]
            if type(raw_player_id) is int:
                player_id = char_dict["player_id"]
            elif raw_player_id.isnumeric():
                player_id = int(char_dict["player_id"])
            else:
                player_id = -1

            raw_char_id = char_dict["char_id"]
            if type(raw_char_id) is int:
                char_id = char_dict["char_id"]
            elif raw_char_id.isnumeric():
                char_id = int(char_dict["char_id"])
            else:
                char_id = -1

            if player_id >= 0 and char_id >= 0:
                # CHECK IF PLAYER EXISTS OR NOT:
                player_exists = self.pc_exists_by_id(
                    search_id=player_id, is_deleted=True, pc="player"
                )

                if player_exists:
                    # CHECK IF CHARACTER EXISTS OR NOT:
                    safe_player_id: int = player_id
                    char_dict["player_id"] = safe_player_id
                    char_exists = self.pc_exists_by_id(
                        search_id=char_id, is_deleted=True, pc="char"
                    )

                    if char_exists:
                        # UPDATE EXISTING CHARACTER
                        safe_char_id: int = char_id
                        char_dict["char_id"] = safe_char_id
                    else:
                        # CREATE NEW ELSE UPDATE
                        next_char_id = self.fetch_next_id(id_type="char")
                        char_dict["char_id"] = next_char_id

                    char_archetype = self.string_safe(
                        input_string=char_dict["char_archetype"],
                        allow_hyphen=True,
                        parenthesis=True,
                    )
                    char_dict["char_archetype"] = char_archetype
                    if char_dict["char_type"] in bscm.valid_char_types:
                        char_type = char_dict["char_type"]
                    else:
                        char_type = "character"
                        char_dict["char_type"] = "character"

                    # We need to check all the mod_ids are valid and exist and throw an error if they don't
                    nodes_dict = char_dict["nodes"]

                    failed_mods = self._check_mod_fail(
                        nodes_dict=nodes_dict, cli_print=True
                    )

                    if not failed_mods:
                        print(
                            f"\n{self.chk} {self.col['g']}Save game file for {self.col['w']}{char_name.title()}"
                            f"{self.col['g']} has successfully VALIDATED. Proceeding with import...{self.col['w']} "
                        )
                        import_char = CharacterModel(**char_dict)
                        char = self.new_or_update_char(
                            char_name=char_name,
                            player_id=safe_player_id,
                            char_archetype=char_archetype,
                            char_type=char_type,
                            deleted=False,
                            char=import_char,
                            write_to_db=True,
                            cli_print=True,
                            import_char=True,
                        )
                        self.char = char
                        sleep(self.bscm.sleep)
                        self._return_to_main()

                    else:
                        print(
                            f"\n{self.cross} {self.col['r']}ERROR: One or more mods in the import file are "
                            f"INVALID. The failed Mod_IDs were: {self.col['y']}"
                            f"\n{failed_mods}. "
                            f"\n{self.col['r']}Please check the save file, amend listed mod_ids and try again..."
                            f"{self.col['w']} "
                        )
                        self._return_to_main()

                else:
                    print(
                        f"\n{self.cross} {self.col['r']}ERROR: Your save file contains an INVALID "
                        f"{self.col['w']}player_ID{self.col['r']}.\n"
                        f"\nPlease check the player_ID from the list below, amend the save file and try again..."
                        f"{self.col['w']} "
                    )
                    self.cli_list_all_pcs(
                        list_type="player", header=False, cli_print=True
                    )
            else:
                print(
                    f"\n{self.cross} {self.col['r']}ERROR: Your save file contains an INVALID "
                    f"{self.col['w']}player_ID{self.col['r']} and/or "
                    f"{self.col['w']}char_id{self.col['r']}. They must be numeric entries or blank!\n"
                    f"\nPlease check the player_ID is a valid player_id, mend the save file and try again..."
                    f"{self.col['w']} "
                )
                self.cli_list_all_pcs(list_type="player", header=False, cli_print=True)

    def cli_export_char(self, char: CharacterModel = None):
        print(
            f"{self.l_break}"
            f"{self.ind2}{self.col['w']}EXPORT CHARACTER{self.col['y']}"
            f"{self.l_break}"
        )

        print(f"{self.help_notes[4]}")

        user_choice: int = 0
        step: int = 1

        if hasattr(self.char, "player_id"):
            char = self.char

        if char:
            export_current_char = (
                f"{self.col['m']}STEP {step}......\n"
                f"{self.chk} {self.col['y']}Do you want to export the currently loaded character: "
                f"{self.col['w']}'{self.string_pretty(char.char_name)}'{self.col['y']} "
            )
            options = self._present_options_menu(
                options_dict=self.menus.yes_no,
                title=export_current_char,
                default_choice=1,
            )

            print(f"\n")

            match options[1]:
                case 0:
                    # No
                    user_choice = 1
                    step += 1
                case _:
                    # Yes
                    user_choice = 2
                    step += 1

        match user_choice:
            case 1:
                unsafe_char_id = int(
                    input(
                        f"{self.chk} {self.col['m']}STEP {step}......\n"
                        f"{self.chk} {self.col['y']}Please enter the {self.col['w']}Character ID#{self.col['y']} for "
                        f"character you wish to export:{self.col['w']} "
                    )
                )
                if unsafe_char_id or unsafe_char_id == 0:
                    print(
                        f"\n{self.chk} {self.col['y']}Searching for character with "
                        f"{self.col['w']}Char ID{self.col['y']} of "
                        f"{self.col['g']}{unsafe_char_id}{self.col['w']}..."
                    )
                    char_dict = self.pc_exists_by_id(
                        search_id=unsafe_char_id, pc="char"
                    )
                    if char_dict:
                        self._run_import_export(
                            input_char_id=unsafe_char_id,
                            char_dict=char_dict,
                            is_import=False,
                        )
                    else:
                        print(
                            f"\n{self.cross} {self.col['r']}ERROR: No character with that "
                            f"{self.col['w']}Char ID{self.col['r']}"
                            f" found! Please check the character's Char ID and try again...{self.col['w']}\n"
                        )
                        self.cli_list_all_pcs(list_type="character")
                        self.cli_export_char()
                else:
                    print(
                        f"\n{self.cross} {self.col['r']}ERROR: Please enter a valid "
                        f"{self.col['w']}Char ID{self.col['r']}. "
                        f"Please check the character's Char ID and try again...{self.col['w']}\n"
                    )
                    sleep(self.bscm.sleep)
                    self.cli_list_all_pcs(list_type="character")
                    self.cli_export_char()
            case _:
                char_dict = self.pc_exists_by_id(search_id=char.char_id, pc="char")
                self._run_import_export(
                    input_char_id=char.char_id,
                    char_dict=char_dict,
                    is_import=False,
                    skip_question=True,
                )

    def cli_search_like_mod(
        self,
        char: CharacterModel = None,
        step: int = 0,
        header: bool = True,
        search_text: str = "",
        mod_cat: str = "",
        mod_type: str = "",
        search_type: str = "name",
    ):
        """Method for CLI searching for a mod then getting more detail on an individual mod"""
        # We must blank/clear more_detail!
        more_detail: str = ""
        search_phrase: str = ""

        if step:
            step_text = f"\n{self.chk} {self.col['m']}STEP {step}......\n"
        else:
            step_text = f"\n{self.chk} {self.col['m']}SEARCH......\n"

        if header:
            # Print the help notes
            help_notes: str = self.help_notes[0]
            print(f"\n{help_notes}")

            input_like = input(
                f"{step_text}"
                f"{self.chk} {self.col['y']}Please enter the first few characters of the {self.col['w']}"
                f"Mod Name{self.col['y']} you wish to search for "
                f"({self.col['w']}Case Insensitive{self.col['y']}):{self.col['w']} "
            )
            safe_input = self.string_safe(input_string=input_like, to_lower=True)
        else:
            safe_input = search_text
            # safe_input = self.string_safe(input_string=search_text)

        db_search = self.mod_name_search(
            search_text=safe_input,
            mod_cat=mod_cat,
            mod_type=mod_type,
            search_type=search_type,
        )

        if char:
            mod_list = self.get_char_current_mods(char)
            allowed_mods: dict = {}
            m_count = 0
            for mod in db_search:
                check_allowed = self.check_mod_allowed(
                    mod_id=db_search[mod][0], char_mods=mod_list
                )
                if check_allowed:
                    # If not allowed remove from dict
                    allowed_mods[mod] = db_search[mod]
                m_count += 1

            db_search = allowed_mods

        results_len = len(db_search)
        print(
            f"\n"
            f"{self.ind0}{self.col['g']} #: {self.col['w']}Mod Name{self.col['w']} \n"
            f"{self.ind0}_____________________________"
        )

        if results_len:
            count: int = 1
            for search_return in db_search:
                if count > 9:
                    pad = ""
                else:
                    pad = " "
                print(
                    f"{self.ind0}{pad}{self.col['g']}{count}{self.col['w']}: "
                    f"{db_search[search_return][1]} {self.col['y']}"
                    f"[{db_search[search_return][2].title()}]{self.col['w']}"
                )
                count += 1

            if safe_input:
                search_phrase = safe_input
            else:
                if mod_cat:
                    search_phrase = f"Category={mod_cat.title()}"
                if mod_type:
                    search_phrase = f"{search_phrase}' and Type='{mod_type.title()}"

            print(
                f"\n{self.info} {self.col['y']}Your search "
                f"returned {self.col['g']}{results_len}{self.col['y']} result(s). \n"
                f"{self.info} {self.col['r']}IMPORTANT!{self.col['y']} Only results that are filtered to meet "
                f"{self.col['w']}ALL{self.col['y']} prerequisites and restrictions criteria are shown! "
                f"{self.col['w']}"
            )

            id_search_text = (
                f"{self.chk} {self.col['y']}Enter the {self.col['w']}#{self.col['y']} of the Mod you would "
                f"like to view in more detail "
                f"[{self.col['g']}1{self.col['y']}-{self.col['g']}{count - 1}{self.col['y']}, or "
                f"{self.col['g']}0{self.col['y']} to quit]:{self.col['w']} "
            )

            id_search = input(id_search_text)

            if id_search.isnumeric():
                id_search = int(id_search)
                if id_search == 0:
                    self._return_to_main()
                else:
                    id_index = id_search - 1
                    more_detail = db_search[id_index][1]
                    mod_id = db_search[id_index][0]
                    # print(f"db_search_results = {db_search[id_index]}")
                    mod_info = self.cli_search_like(
                        search_type="mod", search_str=more_detail, mod_id=mod_id
                    )

                    # TODO: Add in option to add to character here
                    """
                      check_allowed = self.check_mod_allowed(mod_id=mod_id, char_mods=mod_list)
                      breed_locked_skill = self.check_if_breed_mod(
                          mod_id=mod_id, mod_location=mod_location, breed_name=breed_name
                      )
                      check_node_map = self.check_mod_node_mapping(
                          mod_id=mod_id, mod_location=mod_location
                      )
                      # If not allowed, add in option to set Override!
                      """
                    if char:
                        options = self._present_options_menu(
                            options_dict=self.menus.yes_no_quit,
                            title=f"Would you like to add {self.col['g']}{mod_info[0][1]}{self.col['y']} to "
                            f"{self.col['w']}{char.char_name}{self.col['y']}",
                            default_choice=0,
                            char=char,
                        )

                        match options[1]:
                            case 0:
                                self._return_to_main()
                            case 1:
                                print(
                                    f"Adding {mod_info[0][1]} to {self.col['w']}{char.char_name}{self.col['y']}"
                                )
                                # TODO LOCATION CHECK & LIST
                                # XXX
                            case _:
                                self._return_to_main()
                    else:
                        options = self._present_options_menu(
                            options_dict=self.menus.yes_no_quit,
                            title=f"Would you like to perform another Mod search",
                        )

                        match options[1]:
                            case 0:
                                self._return_to_main()
                            case 1:
                                self.cli_search_like_mod(step=step, header=False)
                            case _:
                                self._return_to_main()
            else:
                print(
                    f"\n{self.cross} {self.col['r']}ERROR: Please enter a number between "
                    f"{self.col['w']}0{self.col['r']} and {self.col['w']}{count -1}{self.col['r']}...{self.col['w']}\n"
                )
                sleep(self.bscm.sleep)
                self.cli_search_like_mod(
                    char=char,
                    step=step,
                    header=header,
                    search_text=search_text,
                    mod_cat=mod_cat,
                    mod_type=mod_type,
                    search_type=search_type,
                ),

    def cli_list_free_nodes(
        self, char: CharacterModel = None, header: bool = True, cli_print: bool = True
    ):
        """Method for listing all the free/available mod locations for a loaded character"""

        if header:
            print(
                f"{self.l_break}"
                f"{self.ind2}{self.col['w']}LISTING FREE/AVAILABLE MOD SLOTS{self.col['y']}"
                f"{self.l_break}"
            )

        if not char:
            char = self.char

        count: int = 1
        free_nodes = self.get_char_free_nodes(char=char, cli_print=cli_print)
        len_free_nodes = len(free_nodes)
        choice_dict: dict = {}

        print(
            f"\n"
            f"{self.ind1} {self.col['g']}#: {self.col['w']}Slot Name{self.col['w']} \n"
            f"{self.ind1} ___________________\n"
        )
        print(f"{self._add_option_zero(option_len=len_free_nodes)}")

        if len_free_nodes:

            for node in free_nodes:
                if count < 10:
                    space = f"  "
                elif 10 <= count <= 99:
                    space = f" "
                else:
                    space = f""

                node_name = self.get_node_location_name(node_location=node)
                print(
                    f"{self.ind0}{self.col['g']}{space}{count}{self.col['w']}: {self.string_pretty(node_name)}"
                )
                count += 1

            print(
                f"\n{self.info} {self.col['g']}{self.col['w']}{self.string_pretty(char.char_name)}{self.col['g']} has "
                f"{self.col['w']}{len_free_nodes}{self.col['g']} available/free mod slots. You may need to scroll "
                f"up to see the full list! \n"
                f"{self.info} {self.col['r']}IMPORTANT!{self.col['y']} Only {self.col['w']}EMPTY/UNFILLED"
                f"{self.col['y']} slots are shown! That includes any from {self.col['w']}BREEDS{self.col['y']}!"
                f"{self.col['w']}"
            )

            search_text = (
                f"\n{self.chk} {self.col['y']}Enter the {self.col['w']}#{self.col['y']} of the available/free mod slot "
                f"you would like to add a mod to "
            )

            end_text = (
                f"[{self.col['g']}1{self.col['y']}-{self.col['g']}{count - 1}{self.col['y']}, or "
                f"{self.col['g']}0{self.col['y']} to quit]:{self.col['w']} "
            )

            id_search = input(f"{search_text}{end_text}")
            decision_loop: bool = True
            filter_list: list = []

            print(f"We are here!")

            while decision_loop:
                if id_search is None or id_search == "":
                    print(
                        f"{self.cross} {self.col['r']}ERROR: Please enter a number between "
                        f"[{self.col['g']}1{self.col['r']}-{self.col['g']}{count - 1}{self.col['r']}, or "
                        f"{self.col['g']}0{self.col['r']} to quit.{self.col['w']} "
                    )
                    sleep(self.bscm.sleep)
                    self.cli_list_free_nodes()
                else:
                    if id_search.isdigit():
                        id_search = int(id_search)
                        if id_search == 0:
                            decision_loop = False
                            self._return_to_main()
                        else:
                            # Adjust for array starting at 0
                            true_id = id_search - 1
                            node_choice = free_nodes[true_id]
                            node_choice_name = self.get_node_location_name(
                                node_location=node_choice
                            )
                            node_cat = self.get_node_cat(node_location=node_choice)

                            print(
                                f"\n{self.chk} {self.col['g']}You chose option "
                                f"{self.col['w']}{id_search}{self.col['g']}: "
                                f"{self.col['w']}{node_choice_name}{self.col['y']} (Mod Category is "
                                f"{self.col['c']}'{node_cat.title()}'{self.col['y']}){self.col['g']}..."
                                f"{self.col['w']}\n"
                            )
                            sleep(self.bscm.sleep)
                            node_dict = self.nm_dict[node_choice]
                            mod_type: str = ""
                            if "type" in node_dict:
                                type_list = node_dict["type"]
                                # print(f"TYPE LIST = {type_list}")
                                for t in type_list:
                                    if mod_type:
                                        mod_type = f"{mod_type}' OR type='{t}"
                                    else:
                                        mod_type = t

                            mod_id = ""
                            if "cyb" in node_dict:
                                implant_list = node_dict["cyb"]
                                print(f"IMPLANT LIST = {implant_list}")
                                for c in implant_list:
                                    if mod_id:
                                        mod_id = f"{mod_id}' OR mod_id='{c}"
                                    else:
                                        mod_id = f"{c}"
                                mod_type = "cyb"
                                print(f"{mod_id}")

                            if "bio" in node_dict:
                                implant_list = node_dict["bio"]
                                print(f"IMPLANT LIST = {implant_list}")
                                for b in implant_list:
                                    if mod_id:
                                        mod_id = f"{mod_id}' OR mod_id='{b}"
                                    else:
                                        mod_id = f"{b}"
                                mod_type = "bio"

                            mod_skl: str = ""

                            if "skl" in node_dict:
                                skl_list = node_dict["skl"]
                                # print(f"SKILL LIST = {skl_list}")
                                for s in skl_list:
                                    if "_limit_" in s:
                                        pass
                                    else:
                                        if mod_skl:
                                            mod_skl = f"{mod_skl}' OR mod_id='{s}"
                                        else:
                                            mod_skl = s

                            #if "opportunity" in node_dict:
                            # XXX

                            # Load list of appropriate mods for that location
                            # Now we have node_location and node_cat. We need to feed ths to a version of the search
                            # that allows us to get a sub-selection of valid mods that can be added to this location
                            # with apply_mod_to_char
                            if mod_type:
                                if mod_skl:
                                    choice_dict = self.cli_search_like(
                                        search_type="cat_type",
                                        mod_cat=node_cat,
                                        mod_type=mod_type,
                                        mod_skl=mod_skl,
                                        mod_location=node_choice,
                                    )
                                elif mod_id:
                                    choice_dict = self.cli_search_like(
                                        search_type="mod",
                                        mod_cat=node_cat,
                                        mod_type=mod_type,
                                        mod_id=mod_id,
                                        mod_location=node_choice,
                                    )
                                else:
                                    choice_dict = self.cli_search_like(
                                        search_type="cat_type",
                                        mod_cat=node_cat,
                                        mod_type=mod_type,
                                        mod_location=node_choice,
                                    )
                            elif mod_skl:
                                if mod_type:
                                    choice_dict = self.cli_search_like(
                                        search_type="cat_type",
                                        mod_cat=node_cat,
                                        mod_type=mod_type,
                                        mod_skl=mod_skl,
                                        mod_location=node_choice,
                                    )
                                else:
                                    choice_dict = self.cli_search_like(
                                        search_type="cat_type",
                                        mod_cat=node_cat,
                                        mod_skl=mod_skl,
                                        mod_location=node_choice,
                                    )
                            else:
                                choice_dict = self.cli_search_like(
                                    search_type="cat_type",
                                    mod_cat=node_cat,
                                    mod_location=node_choice,
                                )

                            # TODO: XXX
                            char = self.apply_mod_to_character(
                                mod_id=choice_dict[0],
                                mod_location=node_choice,
                                char=char,
                                cli_print=True,
                            )
                            self.char = char
                            self.save_complete_character(
                                char=self.char, live_char=self.live_char
                            )
                            print(
                                f"{self.info} {self.col['w']}{char.char_name.title()}{self.col['y']} has "
                                f"{self.col['w']}{char.tp_unspent}{self.col['y']} unspent Talent Points remaining."
                                f"{self.col['w']}"
                            )
                            self.load_complete_character(char_id=self.char.char_id)
                            sleep(self.bscm.sleep)
                            title = (
                                f"Do you want to add another mod to a free location or view "
                                f"{self.col['w']}{char.char_name.title()}'s{self.col['y']} Build or Play information? "
                            )
                            options = self._present_options_menu(
                                options_dict=self.menus.yes_no_build_play, title=title
                            )

                            match options[1]:
                                case 0:
                                    decision_loop = False
                                    self._return_to_main()
                                case 2:
                                    decision_loop = False
                                    self.cli_search_like(
                                        search_type="char",
                                        search_id=char.char_id,
                                        char=char,
                                    )
                                case 3:
                                    decision_loop = False
                                    self.cli_search_like(
                                        search_type="live_char",
                                        search_id=char.char_id,
                                        live_char=self.live_char,
                                    )
                                case _:
                                    self.cli_list_free_nodes(char=char, cli_print=True)
                    else:
                        print(
                            f"{self.cross} {self.col['r']}ERROR: Please enter a number between "
                            f"[{self.col['g']}1{self.col['r']}-{self.col['g']}{count - 1}{self.col['r']}, or "
                            f"{self.col['g']}0{self.col['r']} to quit.{self.col['w']} "
                        )
                        sleep(self.bscm.sleep)
                        self.cli_list_free_nodes()

    def cli_search_like(
        self,
        search_type: str = "mod",
        search_id: int = 0,
        search_str: str = "",
        mod_id: str = "",
        mod_cat: str = "",
        mod_type: str = "",
        mod_skl: str = "",
        mod_location: str = "",
        char: CharacterModel = None,
        live_char: LiveCharacterModel = None,
    ):
        """A generic search method for searching for PlayerModel, CharacterModel, LiveCharacterModel, or Mod
        information"""
        bscm = self.bscm
        placed_text: str
        # db_search: dict = {}
        safe_input: str = ""
        char_check: bool = False
        no_char: bool = False

        logging.info(
            f"search_type: {search_type}\n"
            f"search_id: {search_id}\n"
            f"search_str: {search_str}\n"
            f"mod_id: {mod_id}\n"
            f"mod_cat: {mod_cat}\n"
            f"mod_type: {mod_type}\n"
            f"mod_skl: {mod_skl}\n"
            f"mod_location: {mod_location}\n"
        )

        match search_type:
            case "player":
                search_name = "player"
                search_table = "players"
                search_field = "player_name"
                id_field = "player_id"
                db = self.chardata_db["db"]
                db_path = self.chardata_db["db_path"]
                search_title = 1
                display_fields = 4
                field_names = bscm.players_fields
            case "char":
                search_name = "character"
                search_table = "characters"
                search_field = "char_name"
                id_field = "char_id"
                db = self.chardata_db["db"]
                db_path = self.chardata_db["db_path"]
                search_title = 1
                display_fields = 5
                field_names = bscm.characters_fields
            case "live_char":
                search_name = "character"
                search_table = "live_characters"
                search_field = "char_name"
                id_field = "char_id"
                db = self.chardata_db["db"]
                db_path = self.chardata_db["db_path"]
                search_title = 3
                display_fields = 4
                field_names = bscm.live_characters_fields
            case "cat_type":
                search_name = "mod by location"
                search_table = "gamedata"
                search_field = "name"
                id_field = "category"
                db = self.gamedata_db["db"]
                db_path = self.gamedata_db["db_path"]
                search_title = 1
                display_fields = 8
                field_names = bscm.gamedata_subset_fields
                no_char = True
            case _:
                search_name = "mod"
                search_table = "gamedata"
                search_field = "name"
                id_field = "mod_id"
                db = self.gamedata_db["db"]
                db_path = self.gamedata_db["db_path"]
                search_title = 1
                display_fields = 8
                field_names = bscm.gamedata_subset_fields
                no_char = True

        expand_out: list = [
            "nodes",
            "text_replace_mods",
            "custom_notes",
            "stored_overrides",
            "sliver_complete",
            "effects",
        ]

        extract_from_list: list = [
            "prerequisites",
            "restrictions",
        ]

        if not no_char:
            if not char:
                if hasattr(self.char, "char_id"):
                    char = self.char
                    char_check = True
            if not live_char:
                if hasattr(self.live_char, "char_id"):
                    live_char = self.live_char
                    char_check = True

        if not char_check:
            logging.info(f"NO CHAR ACTIVE")
            if mod_cat:
                if mod_type:
                    if mod_skl:
                        logging.info(f"search criteria: mod_cat, mod_type, mod_skl")
                        safe_input = mod_skl
                        sql_search_like = (
                            f"SELECT mod_id, name, description, category, type, prereqs, restriction, effects, ref "
                            f"FROM gamedata WHERE category='{mod_cat}' AND type='{mod_type}' "
                            f"AND mod_id='{mod_skl}'"
                        )
                    elif mod_id:
                        logging.info(f"search criteria: mod_cat, mod_type, mod_id")
                        safe_input = mod_id
                        sql_search_like = (
                            f"SELECT mod_id, name, description, category, type, prereqs, restriction, effects, ref "
                            f"FROM gamedata WHERE category='{mod_cat}' AND type='{mod_type}' "
                            f"AND mod_id='{mod_id}'"
                        )
                    else:
                        logging.info(f"search criteria: mod_cat, mod_type")
                        safe_input = mod_cat
                        sql_search_like = (
                            f"SELECT mod_id, name, description, category, type, prereqs, restriction, effects, ref "
                            f"FROM gamedata WHERE category='{mod_cat}' AND type='{mod_type}'"
                        )
                else:
                    if mod_skl:
                        logging.info(f"search criteria: mod_cat, mod_skl")
                        safe_input = mod_skl
                        sql_search_like = (
                            f"SELECT mod_id, name, description, category, type, prereqs, restriction, "
                            f"effects, ref FROM gamedata WHERE category='{mod_cat}' AND mod_id='{mod_skl}'"
                        )
                    elif mod_id:
                        logging.info(f"search criteria: mod_cat, mod_id")
                        safe_input = mod_id
                        sql_search_like = (
                            f"SELECT mod_id, name, description, category, type, prereqs, restriction, effects, ref "
                            f"FROM gamedata WHERE category='{mod_cat}' AND type='{mod_type}' "
                            f"AND mod_id='{mod_id}'"
                        )
                    else:
                        logging.info(f"search criteria: mod_cat")
                        safe_input = mod_cat
                        sql_search_like = (
                            f"SELECT mod_id, name, description, category, type, prereqs, restriction, effects, ref "
                            f"FROM gamedata WHERE category='{mod_cat}'"
                        )
            elif mod_type:
                if mod_cat:
                    if mod_skl:
                        logging.info(f"search criteria: mod_cat, mod_type, mod_skl")
                        safe_input = mod_skl
                        sql_search_like = (
                            f"SELECT mod_id, name, description, category, type, prereqs, restriction, effects, ref "
                            f"FROM gamedata WHERE category='{mod_cat}' AND type='{mod_type}' AND mod_id='{mod_skl}'"
                        )
                    elif mod_id:
                        logging.info(f"search criteria: mod_cat, mod_type, mod_id")
                        safe_input = mod_id
                        sql_search_like = (
                            f"SELECT mod_id, name, description, category, type, prereqs, restriction, effects, ref "
                            f"FROM gamedata WHERE category='{mod_cat}' AND type='{mod_type}' "
                            f"AND mod_id='{mod_id}'"
                        )
                    else:
                        logging.info(f"search criteria: mod_cat, mod_type")
                        safe_input = mod_cat
                        sql_search_like = (
                            f"SELECT mod_id, name, description, category, type, prereqs, restriction, effects, ref "
                            f"FROM gamedata WHERE category='{mod_cat}' AND type='{mod_type}'"
                        )
                else:
                    if mod_skl:
                        logging.info(f"search criteria: mod_type, mod_skl")
                        safe_input = mod_skl
                        sql_search_like = (
                            f"SELECT mod_id, name, description, category, type, prereqs, restriction, effects, ref "
                            f"FROM gamedata WHERE type='{mod_type}' AND mod_id='{mod_skl}'"
                        )
                    elif mod_id:
                        logging.info(f"search criteria: mod_type, mod_id")
                        safe_input = mod_id
                        sql_search_like = (
                            f"SELECT mod_id, name, description, category, type, prereqs, restriction, effects, ref "
                            f"FROM gamedata WHERE category='{mod_cat}' AND type='{mod_type}' "
                            f"AND mod_id='{mod_id}'"
                        )
                    else:
                        logging.info(f"search criteria: mod_type")
                        safe_input = mod_type
                        sql_search_like = (
                            f"SELECT mod_id, name, description, category, type, prereqs, restriction, effects, ref "
                            f"FROM gamedata WHERE type='{mod_type}'"
                        )
            elif search_id:  # and not mod_cat and not mod_type and not search str
                logging.info(f"search criteria: search_id")
                safe_input = str(search_id)
                sql_search_like = (
                    f"SELECT * FROM {search_table} WHERE {id_field}={search_id}"
                )
            elif search_str:  # and not mod_cat and not mod_type and not search id
                logging.info(f"search criteria: search_str")
                safe_input = search_str
                if mod_id:
                    sql_search_like = (
                        f"SELECT mod_id, name, description, category, type, prereqs, restriction, effects, ref "
                        f"FROM gamedata WHERE mod_id='{mod_id}' "
                    )
                else:
                    sql_search_like = f"SELECT * FROM {search_table} WHERE LOWER({search_field}) LIKE '{safe_input}%' "
            else:
                logging.info(f"search criteria: other")
                input_like = input(
                    f"\n{self.chk} {self.col['m']}SEARCH......\n"
                    f"{self.chk} {self.col['y']}Please enter the first few characters of the {self.col['w']}"
                    f"{search_name.title()} Name{self.col['y']} you wish to search for "
                    f"({self.col['w']}Case Insensitive{self.col['y']}):{self.col['w']} "
                )
                safe_input = self.string_safe(input_string=input_like, to_lower=True)
                if search_type == "mod":
                    sql_search_like = (
                        f"SELECT mod_id, name, description, category, type, prereqs, restriction, effects, ref "
                        f"FROM gamedata WHERE LOWER({search_field}) LIKE '{safe_input}%' "
                        f"ORDER BY {search_field}"
                    )
                else:
                    sql_search_like = (
                        f"SELECT * FROM {search_table} WHERE LOWER({search_field}) LIKE '{safe_input}%' "
                        f"ORDER BY {search_field}"
                    )

            logging.info(f"SQL: {sql_search_like}")
            db_search = self.db_fetch(db=db, db_path=db_path, fetch_sql=sql_search_like)
        else:
            if search_type == "char":
                if char.deleted:
                    del_code = 1
                else:
                    del_code = 0
                char_dict = self._convert_model_to_dict(
                    model=char, logging_name=char.char_name
                )
                data_file = (
                    char.char_id,
                    char.char_name,
                    char.char_archetype,
                    char.player_id,
                    char.char_type,
                    char_dict,
                    del_code,
                )
                db_search = [data_file]
                safe_input = f"{char.char_name.title()}"
            elif search_type == "live_char":
                if live_char.deleted:
                    del_code = 1
                else:
                    del_code = 0
                live_char_dict = self._convert_model_to_dict(
                    model=live_char, logging_name=live_char.char_name
                )
                data_file = (
                    live_char.char_id,
                    live_char.live_char_id,
                    live_char.player_id,
                    live_char.char_name,
                    live_char_dict,
                    del_code,
                )
                db_search = [data_file]
                safe_input = f"{live_char.char_name.title()}"

        logging.info(f"DB SEARCH = {db_search}")

        id_return_dict: dict = {}
        results_len = len(db_search)

        if results_len:
            count: int = 1
            for search_return in db_search:
                id_return_dict[search_return[0]] = search_return[1]

                field_count = 0

                print(
                    f"\n     {self.col['g']}________________________________________________________SEARCH RESULT"
                    f"\n     {self.col['g']}{count}{self.col['w']}: "
                    f"{self.col['c']}{search_return[search_title].upper()}{self.col['w']}"
                    f"\n     {self.col['g']}_____________________________________________________________________"
                    f"{self.col['w']}"
                )

                for info_field in search_return:
                    if field_count <= display_fields:
                        if type(info_field) is str:
                            if "JSON" in field_names[field_count]:
                                print(
                                    f"{self.ind0}{self.col['g']}"
                                    f"{self.string_pretty(field_names[field_count]).upper()}"
                                    f"{self.col['w']}:{self._strindent(field_names[field_count])}"
                                )
                                info_dict = self.convert_db_str_to_dict(info_field)
                                for sub_field in info_dict:
                                    if sub_field in expand_out:
                                        print(
                                            f"{self.ind1}- {self.col['c']}{self.string_pretty(sub_field).title()}"
                                            f"{self.col['w']}: "
                                        )
                                        sub_field_dict = info_dict[sub_field]
                                        for node in sub_field_dict:
                                            if sub_field_dict[node]:
                                                if sub_field.lower() == "nodes":
                                                    print(
                                                        f"{self.ind4}- {self.col['m']}"
                                                        f"{self.get_node_location_name(node)}{self.col['w']}:"
                                                        f" "
                                                        f"{self.string_pretty(self.get_mod_name(sub_field_dict[node]))}"
                                                    )
                                                else:
                                                    print(
                                                        f"{self.ind4}- {self.col['m']}"
                                                        f"{self.string_pretty(node).title()}{self.col['w']}:"
                                                        f" "
                                                        f"{self.string_pretty(sub_field_dict[node])}"
                                                    )

                                    elif "applied_mods" in sub_field:
                                        print(
                                            f"{self.ind1}- {self.col['c']}{self.string_pretty(sub_field).title()}"
                                            f"{self.col['w']}: "
                                        )
                                        sub_field_list = info_dict[sub_field]
                                        for node2 in sub_field_list:
                                            print(
                                                f"{self.ind4}- {self.col['m']}"
                                                f"{self.string_pretty(node2)}{self.col['w']}"
                                            )

                                    else:
                                        if info_dict[sub_field]:
                                            # We filter out several fields that players don't need to see
                                            if sub_field.lower().endswith("actual"):
                                                pass
                                            elif sub_field.lower().endswith("max"):
                                                pass
                                            elif sub_field.lower().endswith("min"):
                                                pass
                                            elif sub_field.lower().endswith("comp"):
                                                pass
                                            elif sub_field.lower().endswith(
                                                "twin_touched_by"
                                            ):
                                                pass
                                            elif sub_field.lower().endswith(
                                                "parent_touched_by"
                                            ):
                                                pass
                                            elif sub_field.lower().endswith(
                                                "children_touched_by"
                                            ):
                                                pass
                                            else:
                                                placed_text = self.string_wrap(
                                                    input_string=info_dict[sub_field],
                                                    lvl=3,
                                                )
                                                print(
                                                    f"{self.ind1}- {self.col['c']}"
                                                    f"{self.string_pretty(sub_field).title()}"
                                                    f"{self.col['w']}: "
                                                    f"{self._strindent(sub_field)}"
                                                    f"{self.string_pretty(placed_text, title_case=False)}"
                                                )

                            else:
                                # Most fields are this...
                                if info_field:
                                    if field_names[field_count].lower() in expand_out:
                                        print(
                                            f"{self.ind0}{self.col['g']}"
                                            f"{self.string_pretty(field_names[field_count]).upper()}"
                                            f"{self.col['w']}:{self._strindent(field_names[field_count])}"
                                        )
                                        cleaned_info = info_field.replace("'", '"')
                                        effect_dict = self.convert_db_str_to_dict(
                                            cleaned_info
                                        )
                                        for effect in effect_dict:
                                            if effect.lower().endswith("actual"):
                                                pass
                                            elif effect.lower().endswith("max"):
                                                pass
                                            else:
                                                placed_text = self.string_wrap(
                                                    input_string=effect_dict[effect],
                                                    lvl=2,
                                                )
                                                print(
                                                    f"{self.ind3}- {self.col['c']}{self.string_pretty(effect).title()}"
                                                    f"{self.col['w']}: "
                                                    f"{self.string_pretty(placed_text, title_case=False)}"
                                                )
                                    elif (
                                        field_names[field_count].lower()
                                        in extract_from_list
                                    ):
                                        print(
                                            f"{self.ind0}{self.col['g']}"
                                            f"{self.string_pretty(field_names[field_count]).upper()}"
                                            f"{self.col['w']}:{self._strindent(field_names[field_count])}"
                                        )
                                        logging.info(f"INFO FIELD = {info_field}")
                                        effect_list = info_field.split(",")
                                        logging.info(f"EFFECT LIST = {effect_list}")
                                        for list_element in effect_list:
                                            logging.info(
                                                f"LIST ELEMENT = {list_element}"
                                            )
                                            if "[" in list_element:
                                                if "," in list_element:
                                                    list_element_item = self._str_strip(
                                                        list_element
                                                    )
                                                    list_element_list = (
                                                        list_element_item.split(",")
                                                    )
                                                    sub_effect_list = list_element_list
                                                    for sub_element in sub_effect_list:
                                                        sub_element_item = (
                                                            self._str_strip(sub_element)
                                                        )
                                                        cleaned_mod_name = self.string_pretty(
                                                            self.get_mod_name(
                                                                mod_id=sub_element_item
                                                            )
                                                        )
                                                        print(
                                                            f"{self.ind3}- {self.col['w']}"
                                                            f"{cleaned_mod_name}"
                                                        )
                                                else:
                                                    logging.info(f"Second+ Item")
                                                    list_element_item = self._str_strip(
                                                        list_element
                                                    )
                                                    print(
                                                        f"{self.ind3}- {self.col['w']}"
                                                        f"{self.get_mod_name(mod_id=list_element_item)}"
                                                    )
                                            else:
                                                logging.info(f"{list_element}")
                                                list_element_item2 = self._str_strip(
                                                    list_element
                                                )
                                                logging.info(f"{list_element_item2}")
                                                if "null" in list_element_item2.lower():
                                                    print(
                                                        f"{self.ind3}- {self.col['w']}None"
                                                    )

                                                else:
                                                    logging.info(
                                                        f"MOD ID SEARCHING FOR IS {list_element_item2}"
                                                    )
                                                    print(
                                                        f"{self.ind3}- {self.col['w']}"
                                                        f"{self.get_mod_name(mod_id=list_element_item2)}"
                                                    )

                                    else:
                                        placed_text = self.string_wrap(
                                            input_string=info_field
                                        )
                                        print(
                                            f"{self.ind0}{self.col['g']}"
                                            f"{self.string_pretty(field_names[field_count]).upper()}"
                                            f"{self.col['w']}:"
                                            f"{self._strindent(input_str=field_names[field_count])}"
                                            f"{placed_text}"
                                        )
                        else:
                            if info_field:
                                placed_text = self.string_wrap(input_string=info_field)
                                print(
                                    f"{self.ind0}{self.col['g']}"
                                    f"{self.string_pretty(field_names[field_count]).upper()}"
                                    f"{self.col['w']}:"
                                    f"{self._strindent(input_str=field_names[field_count])}"
                                    f"{self.string_pretty(placed_text)}"
                                )
                    field_count += 1
                count += 1

                logging.info(f"FIELD COUNT: {field_count}, COUNT: {count}")

            print(
                f"\n{self.info} {self.col['y']}Your search for {self.col['w']}'{safe_input}'{self.col['y']} "
                f"returned {self.col['g']}{results_len}{self.col['y']} result(s). \n"
            )
        else:
            print(
                f"\n{self.cross} {self.col['y']}Your search for {self.col['w']}'{safe_input}'{self.col['y']} returned"
                f" {self.col['r']}0{self.col['y']} results. Perhaps try a different search?\n"
            )

        if not search_str:
            if mod_cat:
                # Enter # of mod you would wish to add to mod_location
                id_search = input(
                    f"\n{self.chk} {self.col['y']}Enter {self.col['w']}#{self.col['y']} of mod you would "
                    f"like to add to {self.col['g']}{mod_location}{self.col['y']}, or "
                    f"{self.col['w']}0{self.col['y']} to return to the main menu "
                    f"[{self.col['g']}0{self.col['y']}-"
                    f"{self.col['g']}{len(id_return_dict)}{self.col['y']}]:{self.col['w']} "
                )

                if id_search is None or id_search == "":
                    logging.info(
                        f"User input is incorrect, therefore reloading cli_search_like()..."
                    )
                    print(
                        f"{self.cross} {self.col['r']}ERROR: I didn't understand that option, reloading options,"
                        f"please try again... {self.col['w']}"
                    )
                    sleep(self.bscm.sleep)
                    self.cli_search_like(
                        search_type=search_type,
                        search_id=search_id,
                        search_str=search_str,
                        mod_cat=mod_cat,
                        mod_type=mod_type,
                        mod_skl=mod_skl,
                        mod_location=mod_location,
                    )
                else:
                    if id_search.isnumeric():
                        id_search = int(id_search)
                        if id_search == 0:
                            self._return_to_main()

                        elif 0 < id_search <= len(id_return_dict):
                            mod_choice: int = id_search - 1
                            mod_dict: dict = db_search[mod_choice]
                            print(
                                f"{self.info} {self.col['g']}You chose option "
                                f"{self.col['w']}{id_search}{self.col['g']}: "
                                f"{self.col['w']}{mod_dict[1].title()}{self.col['g']} to add to mod location: "
                                f"{self.col['w']}{mod_location}{self.col['g']}...\n"
                                f"{self.col['w']}"
                            )
                            return mod_dict
                    else:
                        logging.info(
                            f"User input is incorrect, therefore reloading cli_search_like()..."
                        )
                        print(
                            f"{self.cross} {self.col['r']}ERROR: I didn't understand that option, reloading options,"
                            f"please try again... {self.col['w']}"
                        )
                        sleep(self.bscm.sleep)
                        self.cli_search_like(
                            search_type=search_type,
                            search_id=search_id,
                            search_str=search_str,
                            mod_cat=mod_cat,
                            mod_type=mod_type,
                            mod_skl=mod_skl,
                            mod_location=mod_location,
                        )
            else:
                options = self._present_options_menu(
                    options_dict=self.menus.subsearch_options,
                    title="Would you like to perform another search?",
                    default_choice=2,
                )

                match options[1]:
                    case 0:
                        self._return_to_main(id_return_dict)
                    case 1:
                        self.cli_search_frontend()
                    case 2:
                        self.cli_search_like(search_type=search_type)
                    case _:
                        self._return_to_main(id_return_dict)
        else:
            return db_search

    def _run_import_export(
        self,
        input_char_id: int,
        char_dict: dict,
        is_import: bool = True,
        new_char: bool = False,
        skip_question: bool = False,
    ):
        """Method for processing import and exports."""
        if is_import:
            action_text = "import"
        else:
            action_text = "export"
        # XXX
        # TODO: Figure out why this is always creating a new copy, rather than updating
        character_name = char_dict[0][1]
        options: list = []

        if skip_question:
            options = [1, 1]

        else:
            confirm = (
                f"{self.col['m']}{action_text.upper()}......\n"
                f"{self.chk} {self.col['y']}Is the character you wish to {action_text} called {self.col['g']}"
                f"'{character_name.title()}'{self.col['y']}?"
            )

            print(f"\n")
            options = self._present_options_menu(
                options_dict=self.menus.yes_no_quit, title=confirm, default_choice=1
            )

        match options[1]:
            case 0:
                self._return_to_main()
            case 2:
                print(f"{self.cross} {self.col['y']}Starting again...{self.col['w']}")
                if is_import:
                    self.cli_import_char()
                else:
                    self.cli_export_char()
            case _:
                print(
                    f"\n{self.chk} {self.col['g']}{action_text.title()}ing character '{character_name}'!"
                    f"{self.col['w']}\n"
                )
                if new_char:
                    input_new_player = input(
                        f"\n{self.chk} {self.col['y']}Is there an existing {self.col['w']}PLAYER{self.col['y']} for "
                        f"this character to belong to [{self.col['g']}Y{self.col['y']}/{self.col['g']}n{self.col['y']}"
                        f" or {self.col['g']}q{self.col['y']} to return to main menu]?{self.col['w']} "
                    )
                    input_new_player.lower()
                    match input_new_player:
                        case "n":
                            print(
                                f"{self.cross} {self.col['y']}Please create a {self.col['w']}new Player{self.col['y']} "
                                f"first then return here...{self.col['w']}"
                            )
                            self.cli_create_new_player()
                        case "q":
                            self._return_to_main()
                        case _:
                            self.cli_list_all_pcs()
                            input_player_id = int(
                                input(
                                    f"\n{self.chk} {self.col['y']}Please enter the "
                                    f"{self.col['w']}Player ID#{self.col['y']} "
                                    f"you wish this character to belong to: {self.col['w']} "
                                )
                            )
                            self.list_pc(
                                pc="player",
                                by_player_id=input_player_id,
                                cli_print=True,
                            )

                else:
                    char_id = input_char_id
                    lower_name = character_name.lower()
                    if is_import:
                        self.import_character(
                            char_id=char_id,
                            char_name=lower_name,
                            cli_print=True,
                            import_dir="import",
                        )
                        sleep(self.bscm.sleep)
                    else:
                        self.export_character(
                            char_id=char_id, cli_print=True, export_dir="export"
                        )
                        sleep(self.bscm.sleep)

                self._any_key_to_continue()

    def _check_str_field(
        self,
        field: str,
        pc: str = "player",
        required: bool = False,
        step: int = 0,
        to_lower: bool = False,
        allow_hash: bool = False,
        parenthesis: bool = False,
        allow_hyphen: bool = False,
        allow_at: bool = False,
        skip_confirm: bool = False,
    ) -> str:

        match pc:
            case "char":
                name_type = "character"
            case _:
                name_type = "player"

        if step > 0:
            step_text = f"{self.chk} {self.col['m']}STEP {step}......\n"
        else:
            step_text = ""

        if required:
            required_text = f"{self.col['r']}[REQUIRED]{self.col['y']}"
        else:
            required_text = f"{self.col['b']}[Optional]{self.col['y']}"

        input_field = input(
            f"{step_text}"
            f"{self.chk} {self.col['y']}Please enter the {name_type}'s {self.col['w']}{field.upper()}{self.col['y']} "
            f"{required_text}:{self.col['w']} "
        )

        if required and input_field:
            # Required and info filled: Proceed
            proceed = 1
        elif not required and input_field:
            # Not Required but info filled: Proceed
            proceed = 1
        elif required and not input_field:
            # Not Required and info not filled: Error
            proceed = 3
        else:
            # Not required and info filled: Proceed
            proceed = 2

        match proceed:
            case 1:
                safe_field = self.string_safe(
                    input_string=input_field,
                    to_lower=to_lower,
                    allow_hash=allow_hash,
                    parenthesis=parenthesis,
                    allow_hyphen=allow_hyphen,
                    allow_at=allow_at,
                )

                print(
                    f"\n{self.info} {self.col['g']}You entered the following information:\n"
                    f"\n     {self.col['y']}- {self.col['w']}{field}{self.col['y']} {required_text} = "
                    f"{self.col['g']}{safe_field}{self.col['y']}\n"
                )

                if not skip_confirm:
                    title = f"{self.chk} {self.col['y']}Is this information correct?"
                    options = self._present_options_menu(
                        options_dict=self.menus.yes_no_quit,
                        title=title,
                    )

                    match options[1]:
                        case 0:
                            self._return_to_main()
                        case 2:
                            print(
                                f"{self.cross} {self.col['y']}Information provided for {field.title()} was "
                                f"{self.col['r']}incorrect{self.col['y']}. Retrying...{self.col['w']}\n "
                            )
                            self._check_str_field(
                                field=field,
                                pc=pc,
                                required=required,
                                step=step,
                                to_lower=to_lower,
                                allow_hash=allow_hash,
                                parenthesis=parenthesis,
                                allow_hyphen=allow_hyphen,
                                allow_at=allow_at,
                            )
                        case _:
                            print(
                                f"{self.chk} {self.col['y']}{field.title()} information "
                                f"{self.col['w']}'{safe_field}'{self.col['y']} was correct.{self.col['w']}\n",
                                flush=True,
                            )
                            return safe_field
                else:
                    return safe_field
            case 2:
                print(
                    f"\n{self.chk} {self.col['y']}{field.title()} was {self.col['g']}optional{self.col['y']} and "
                    f"you have chosen to skip it.{self.col['w']}\n"
                )
                return ""
            case 3:
                print(
                    f"{self.cross} {self.col['r']}ERROR: The field {field} is required and cannot be empty! "
                    f"\n{self.cross} {self.col['r']}Starting again...{self.col['w']}\n"
                )
                self._check_str_field(
                    field=field,
                    pc=pc,
                    required=required,
                    step=step,
                    to_lower=to_lower,
                    allow_hash=allow_hash,
                    parenthesis=parenthesis,
                    allow_hyphen=allow_hyphen,
                    allow_at=allow_at,
                )

    def _check_name(self, pc: str = "player", step: int = 0) -> str:
        """Simple method for checking if a name already exists"""
        match pc:
            case "char":
                name_type = "character"
                search_field = "char_name"
            case _:
                name_type = "player"
                search_field = "player_name"

        if step > 0:
            step_text = f"{self.chk} {self.col['m']}STEP {step}......\n"
        else:
            step_text = ""

        input_name = input(
            f"{step_text}"
            f"{self.chk} {self.col['y']}Please enter the {name_type}'s chosen {self.col['w']}NAME{self.col['y']} "
            f"{self.col['r']}[REQUIRED]{self.col['y']}:{self.col['w']} "
        )
        if input_name:
            check_name = self.string_safe(
                input_string=input_name,
                input_name="Name",
                allow_hyphen=True,
                allow_at=True,
            )

            name_exists = self.pc_exists_by_name(
                search_name=search_field, pc=pc, lower_case=True
            )
            if name_exists:
                print(
                    f"\n{self.cross} {self.col['r']}ERROR: That {name_type.title()} name already EXISTS! "
                    f"Please choose a different name for your new {name_type.title()}..."
                    f"{self.col['w']}\n"
                )
                return ""
            else:
                print(
                    f"\n{self.chk} {self.col['g']}{name_type.title()} name {self.col['w']}'{check_name}'{self.col['g']}"
                    f" is AVAILABLE!\n"
                    f"\n     {self.col['y']}- {self.col['w']}{name_type.title()} Name "
                    f"{self.col['r']}[REQUIRED]{self.col['y']} = "
                    f"{self.col['g']}{check_name}\n"
                )

                return input_name
        else:
            print(
                f"{self.cross} {self.col['r']}ERROR: {name_type.upper()} name is REQUIRED! "
                f"Starting again...{self.col['w']}\n"
            )
            return ""

    def _cli_header(
        self,
        step: int = 0,
        header: bool = True,
        optional: bool = True,
        choose: str = "choose",
        char_name: str = "",
        header_name: str = "",
    ) -> str:
        """Simple method to create a standard header for functions. Note this includes check boxes etc., so
        don't add those!"""
        if header:
            print(
                f"{self.l_break}"
                f"{self.ind2}{self.col['w']}{header_name.upper()}{self.col['y']}"
                f"{self.l_break}"
            )

        if step > 0:
            step_text = f"{self.col['m']}STEP {step}......\n"
        else:
            step_text = ""

        if optional:
            # optional_text = f"{self.col['b']}[Optional]{self.col['y']}"
            optional_text = f""
        else:
            optional_text = f"{self.col['r']}[REQUIRED]{self.col['y']}"

        match choose:
            case "add":
                choose_text = f"ADD"
                for_text = f"to"
            case "delete":
                choose_text = f"DELETE/REMOVE"
                for_text = f"to/from"
            case "search":
                choose_text = f"SEARCH"
                for_text = f"for"
            case "alter":
                choose_text = f"ADD/REMOVE"
                for_text = f"to/from"
            case _:
                choose_text = f"CHOOSE"
                for_text = "for"

        header_input = (
            f"{step_text}{self.col['y']}Please choose one of the following options for your character "
            f"{self.col['w']}{self.string_pretty(char_name).title()}{self.col['y']} "
            f"{optional_text}:{self.col['w']}"
        )

        return header_input

    def _add_option_zero(self, option_len: int) -> str:
        """Simple method to add an option zero (return to menu) to menus not made by _present_options_menu()"""
        # Add a Menu 0 option
        if option_len < 10:
            space0 = f"   "
        elif 10 <= option_len <= 99:
            space0 = f"  "
        else:
            space0 = f" "

        option_zero_text = f"{self.ind0}{self.col['g']}{space0}0{self.col['w']}: {self.menus.menu_strings[0]}"

        return option_zero_text

    def _present_options_menu(
        self,
        options_dict: dict,
        title: str = "Please choose an option",
        notes: str = "",
        default_choice: int = 1,
        char: CharacterModel = None,
    ) -> list:
        """This method generates up a menu for the chosen section from the input options_dict. It returns the chosen
        option as well as the count of the total options in a tuple (count, chosen_option).
        'title' sets the title.
        And 'notes' allows you to add some user notes without clogging up the options in the form of a string.
        default_choice sets a default option of an int."""

        if char:
            loaded_char = self._cli_loaded_player_info(char=char)
            notes = f"{notes}{loaded_char}"

        print(f"{self.chk} {self.col['y']}{title}{self.col['w']}\n")

        default_str = str(default_choice)
        allowed_options: list = []
        user_option: str = ""
        chosen_option: int = default_choice
        count: int = 0
        returned_option: list = [0, default_choice]

        # Generate the options menu
        for option in options_dict:
            if option < 10:
                space = " "
            else:
                space = ""
            if option == default_choice:
                default_option = f" {self.col['c']}[*]{self.col['w']}"
            else:
                default_option = f""

            print(
                f"{self.ind0}{self.col['g']}{space}{option}{self.col['w']}: {options_dict[option]}{default_option}"
            )
            allowed_options.append(option)
            count += 1

        return_count = count - 1

        if notes:
            print(f"\n{self.col['y']}{notes}{self.col['w']}\n")
        else:
            print(f"\n")

        choice_text = (
            f"{self.chk} {self.col['y']}{self.menus.menu_strings[2]}: "
            f"[{self.col['g']}0{self.col['y']}-{self.col['g']}{count - 1}{self.col['y']}]:{self.col['w']} "
        )

        is_digit = False
        while not is_digit:
            user_option = input(f"{choice_text}")
            if user_option is None or user_option == "":
                logging.info(f"User input is blank, therefore use DEFAULT CHOICE")
                user_option = default_str
            if user_option.isdigit():
                logging.info(
                    f"User input IS DIGIT. Proceed. Is it in this list of Allowed Options: "
                    f"{allowed_options}?"
                )
                if int(user_option) in allowed_options:
                    logging.info("User input is in list of Allowed Options. Proceed.")
                    chosen_option = int(user_option)
                    is_digit = True
                    print(
                        f"\n{self.chk} {self.col['g']}You chose option {self.col['w']}{chosen_option}{self.col['g']}: "
                        f"'{options_dict[chosen_option]}'{self.col['w']}",
                        flush=True,
                    )

                    returned_option = [int(return_count), int(chosen_option)]
                    return returned_option
                else:
                    logging.info(
                        f"User input is not in list of allowed options. Restarting..."
                    )
                    print(
                        f"\n{self.cross} {self.col['r']}ERROR: You entered: "
                        f"{self.col['g']}'{user_option}'{self.col['r']}\n"
                        f"Please enter a number between 0 and {return_count} for the option you want!{self.col['w']}\n"
                    )
            else:
                logging.info(f"User input is not a digit. Restarting...")
                print(
                    f"\n{self.cross} {self.col['r']}ERROR: You entered: "
                    f"{self.col['w']}'{user_option}'{self.col['r']}\n"
                    f"Please enter a number between 0 and {return_count} for the option you want!{self.col['w']}\n"
                )

    def _cli_loaded_player_info(
        self, char: CharacterModel = None, live_char: LiveCharacterModel = None
    ) -> str:
        """Simple method for creating a help footer displaying currently loaded CharacterModel information"""
        notes: str = ""

        # We only want to load character info if there is a character loaded otherwise we risk an error!
        if not char:
            if self.char:
                char = self.char
        if not live_char:
            if self.live_char:
                live_char = self.live_char

        if char:
            player_info = self.pc_exists_by_id(search_id=char.player_id)
            player_name = player_info[0][1]

            if live_char:
                live_char_id = live_char.char_id
            else:
                live_char_id = 0

            notes = (
                f"{self.help_header}"
                f"    Currently loaded character: \n"
                f"    {self.col['c']}- Name:          "
                f"{self.col['w']}{self.string_pretty(char.char_name)} {self.col['y']}(Char_ID: "
                f"{self.col['g']}{char.char_id}{self.col['y']} / "
                f"Live_Char_ID: {self.col['b']}{live_char_id}{self.col['y']})\n"
                f"    {self.col['c']}- Player:        "
                f"{self.col['w']}{self.string_pretty(player_name)} {self.col['y']}(Player_ID: "
                f"{self.col['g']}{char.player_id}{self.col['y']})\n"
                f"    {self.col['c']}- Unspent TPs:   "
                f"{self.col['w']}{char.tp_unspent} {self.col['y']}(Total TPs: "
                f"{self.col['g']}{char.tp_total}{self.col['y']}){self.col['w']}\n"
            )

        return notes

    def _return_to_main(self, *args, **kwargs) -> None:
        """Simple method for providing a return to main menu function."""
        print(
            f"\n{self.chk} {self.col['g']}{self.menus.menu_strings[1]}...{self.col['w']}",
            flush=True,
        )
        sleep(self.bscm.sleep)

        self.main(self, *args, **kwargs)

    def _any_key_to_continue(self, *args, **kwargs) -> None:
        """Super simple method to pres any key to continue..."""
        input_text = f"\n{self.chk} {self.col['y']}Press any enter to continue... {self.col['w']}"
        press_to_continue = input(input_text)
        if press_to_continue is None or press_to_continue == "":
            sleep(self.bscm.sleep)
            self._return_to_main(*args, **kwargs)
        else:
            sleep(self.bscm.sleep)
            self._return_to_main(*args, **kwargs)


if __name__ == "__main__":
    cli = CLIMethods()
    cli.main()
