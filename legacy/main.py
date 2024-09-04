# encoding: utf-8
__version__ = "2.1.50"
__author__ = "Gunnar Roxen <gunnar@brokenshield.net>"

import logging
from character_methods import CharacterMethods
from cli_methods import CLIMethods
import character_dataclasses
from json import dumps
from time import sleep

logging.basicConfig(level=logging.WARNING)


def main():

    cli = CLIMethods()
    # cli.get_node_location_name(node_location="hacking_skill_n2")
    # char = cli.load_char(char_id=2)
    # cli.check_mods_by_node(node_location="faith_edge_n0", char=char, cli_print=True)
    cli.main()

    # print('LOADING WEAVE OS', end='', flush=True)
    # for x in range(256):
    #    for frame in r'-\|/-\|/':
    #        # Back up one character then print our next frame in the animation
    #        print('\b', frame, sep='', end='', flush=True)
    #        sleep(0.2)

    # Back up one character, print a space to erase the spinner, then a newline
    # so that the prompt after the program exits isn't on the same line as our
    # message
    # print('\b ')
    """
    
    cm = CharacterMethods()

    if create:
        # CREATE A NEW PLAYER:
        # new_player = cm.create_new_player(
        #    player_name="Hannah",
        #    player_real_name="Hannah Rowlands",
        #    player_email="gunnar@brokenshield.net",
        # )

        # CREATE A NEW CHARACTER:
        character = cm.create_new_char(
            char_name="Test",
            player_id=0,
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
        )
        cm.save_complete_character()
    else:
        character = cm.load_char(char_id=0)

    # LOAD LIVE CHARACTER
    live_char = cm.load_live_character(char_id=0)

    # DO THIS IN EITHER SITUATION
    cm.print_char_model(char=character)
    cm.print_live_char_model(live_char=live_char)

    print(
        f"{cm.chk} {cm.sql_txt} {cm.col['c']}!!!!! DB READ COUNT  = "
        f"{cm.db_read_count} !!!!!{cm.col['w']}\n"
        f"{cm.chk} {cm.sql_txt} {cm.col['m']}!!!!! DB WRITE COUNT = "
        f"{cm.db_write_count} !!!!!{cm.col['w']}"
    )

    cm.export_character(char_id=0)

    # cm.import_character(char_id=1, char_name=character.char_name)
    """


if __name__ == "__main__":
    # main(create=True)
    main()
