# encoding: utf-8
__version__ = "2.1.50"
__author__ = "Gunnar Roxen <gunnar@brokenshield.net>"

from datetime import datetime
from pydantic import BaseModel, Extra
from typing import Optional
import sqlite3
import logging

logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(filename='app.log', filemode='w', format='%(message)s')


class BreedTemplates(BaseModel):
    """This is the dataclass of all the Breed templates.
    nodes and mod_ids are stored here.
    raw stat bonuses, general_notes, breed_tp_bonus and breed_name should be stored in gamedata thus:
    human dict here = b_breed_human entry in gamedata
    also add an entry to the Breeds dict.
    """

    class Config:
        extra = Extra.forbid

    breeds_list: dict = {
        "human": "b_breed_human",
        "hulk": "b_breed_hulk",
        "gethan": "b_breed_gethan",
        "pure_kapaethjan": "b_breed_pure_kapaethjan",
        "pure_ballaetic": "b_breed_pure_ballaetic",
        "pure_motley": "b_breed_pure_motley",
        "pure_fallen": "b_breed_pure_fallen",
        "atropoan": "b_breed_atropoan",
        "feral": "b_breed_feral",
        # "creature": "b_breed_creature",
        # "rezhadi": "b_breed_rezhadi",
    }

    """
    Organise Breed template like this:
    - Breed -> This links to the mod_id in gamedata that has all the additional information
    - Culture
    - Social
    - Language
    - Pledge Disciple
    - Skills
    - Edges
    - Traits
    - Skill Limits
    """

    test: dict = {
        "breed_n0": "b_breed_human",
        "physical_skill_n0": "n_physical_0",
    }

    human: dict = {
        "breed_n0": "b_breed_human",
        "culture_n0": "b_culture_truean",
        "social_n0": "l_social_middle",
        "language_n0": "b_language_standard",
        "physical_skill_n0": "n_physical_0",
        "killer_skill_n0": "n_killer_0",
        "cloak_skill_n0": "n_cloak_0",
        "smarts_skill_n0": "n_smarts_0",
        "sandman_skill_n0": "n_sandman_0",
        "weaver_skill_n0": "n_weaver_0",
        "resources_skill_n0": "n_resources_0",
        "mouth_skill_n0": "n_mouth_0",
        "vapour_skill_n0": "n_vapour_0",
        "wyld_skill_n0": "n_wyld_0",
        "divinity_skill_n0": "n_divinity_0",
    }

    hulk: dict = {
        "breed_n0": "b_breed_hulk",
        "culture_n0": "b_culture_truean",
        "social_n0": "l_social_middle",
        "language_n0": "b_language_standard",
        "physical_skill_n0": "n_physical_0",
        "killer_skill_n0": "n_killer_0",
        "cloak_skill_n0": "n_cloak_0",
        "smarts_skill_n0": "n_smarts_0",
        "sandman_skill_n0": "n_sandman_0",
        "weaver_skill_n0": "n_weaver_0",
        "resources_skill_n0": "n_resources_0",
        "mouth_skill_n0": "n_mouth_0",
        "vapour_skill_n0": "n_vapour_0",
        "wyld_skill_n0": "n_wyld_0",
        "divinity_skill_n0": "n_divinity_0",
        "athletics_edge_n0": "e_gigantic",
        "endurance_edge_n0": "e_thick_skinned",
        "control_edge_n0": "e_endure_pain",
        "killer_trait_n0": "t_slow",
        "weaver_trait_n0": "t_obedient",
        "mouth_trait_n0": "t_ugly",
        "control_skill_n2": "n_control_limit_2",
        "knowledge_skill_n2": "n_knowledge_limit_2",
        "psychology_skill_n2": "n_psychology_limit_2",
        "streetwise_skill_n2": "n_streetwise_limit_2",
        "influence_skill_n2": "n_influence_limit_2",
    }

    gethan: dict = {
        "breed_n0": "b_breed_gethan",
        "culture_n0": "b_culture_gethan",
        "language_n0": "b_language_standard",
        "language_n1": "b_language_gethan",
        "physical_skill_n0": "n_physical_0",
        "killer_skill_n0": "n_killer_0",
        "killer_trait_n0": "t_clone",
        "cloak_skill_n0": "n_cloak_0",
        "smarts_skill_n0": "n_smarts_0",
        "sandman_skill_n0": "n_sandman_0",
        "weaver_skill_n0": "n_weaver_0",
        "resources_skill_n0": "n_resources_0",
        "mouth_skill_n0": "n_mouth_0",
        "vapour_skill_n0": "n_vapour_0",
        "wyld_skill_n0": "n_wyld_0",
        "divinity_skill_n0": "n_divinity_0",
        "influence_edge_n0": "e_genesculpting",
        "network_edge_n0": "e_longevity",
        "persuade_edge_n0": "e_attractive",
        "sandman_trait_n0": "t_neat_freak",
        "weaver_trait_n0": "t_perfectionist",
        "mouth_trait_n0": "t_self_righteous",
        "vapour_trait_n0": "t_ambitious",
        "resistance_skill_n1": "n_resistance_limit_1",
        "resistance_skill_n2": "n_resistance_limit_2",
    }

    pure_kapaethjan: dict = {
        "breed_n0": "b_breed_pure_kapaethjan",
        "culture_n0": "b_culture_kapaethjan",
        "language_n0": "b_language_standard",
        "language_n1": "b_language_kapaethjan",
        "pledged_disciple_n0": "d_tattooed_man",
        "physical_skill_n0": "n_physical_0",
        "killer_skill_n0": "n_killer_0",
        "cloak_skill_n0": "n_cloak_0",
        "smarts_skill_n0": "n_smarts_0",
        "sandman_skill_n0": "n_sandman_0",
        "weaver_skill_n0": "n_weaver_0",
        "resources_skill_n0": "n_resources_0",
        "mouth_skill_n0": "n_mouth_0",
        "vapour_skill_n0": "n_vapour_0",
        "wyld_skill_n0": "n_wyld_0",
        "divinity_skill_n0": "n_divinity_0",
        "control_edge_n0": "e_endure_torture",
        "knowledge_edge_n0": "e_brave",
        "streetwise_edge_n0": "e_sensitive_vision",
        "faith_edge_n0": "e_purification",
        "killer_trait_n0": "t_anger",
        "intimidate_edge_n0": "e_scary",
        "weaver_trait_n0": "t_honour_code",
        "mouth_trait_n0": "t_religious",
        "vapour_trait_n0": "t_haemophilia",
        "control_skill_n2": "n_control_limit_2",
        "medic_skill_n2": "n_medic_limit_2",
        "persuade_skill_n2": "n_persuade_limit_2",
    }

    pure_ballaetic: dict = {
        "breed_n0": "b_breed_pure_ballaetic",
        "culture_n0": "b_culture_ballaetic",
        "language_n0": "b_language_standard",
        "language_n1": "b_language_ballaen",
        "pledged_disciple_n0": "d_isoke",
        "physical_skill_n0": "n_physical_0",
        "killer_skill_n0": "n_killer_0",
        "cloak_skill_n0": "n_cloak_0",
        "smarts_skill_n0": "n_smarts_0",
        "sandman_skill_n0": "n_sandman_0",
        "weaver_skill_n0": "n_weaver_0",
        "resources_skill_n0": "n_resources_0",
        "mouth_skill_n0": "n_mouth_0",
        "vapour_skill_n0": "n_vapour_0",
        "wyld_skill_n0": "n_wyld_0",
        "divinity_skill_n0": "n_divinity_0",
        "control_edge_n0": "e_endure_torture",
        "knowledge_edge_n0": "e_brave",
        "streetwise_edge_n0": "e_sensitive_vision",
        "faith_edge_n0": "e_purification",
        "killer_trait_n0": "t_anger",
        "intimidate_edge_n0": "e_scary",
        "weaver_trait_n0": "t_honour_code",
        "mouth_trait_n0": "t_religious",
        "vapour_trait_n0": "t_haemophilia",
        "control_skill_n2": "n_control_limit_2",
        "medic_skill_n2": "n_medic_limit_2",
        "persuade_skill_n2": "n_persuade_limit_2",
    }

    pure_motley: dict = {
        "breed_n0": "b_breed_pure_motley",
        "culture_n0": "b_culture_motley",
        "language_n0": "b_language_standard",
        "language_n1": "b_language_kapaethjan",
        "pledged_disciple_n0": "d_baal",
        "physical_skill_n0": "n_physical_0",
        "killer_skill_n0": "n_killer_0",
        "cloak_skill_n0": "n_cloak_0",
        "smarts_skill_n0": "n_smarts_0",
        "sandman_skill_n0": "n_sandman_0",
        "weaver_skill_n0": "n_weaver_0",
        "resources_skill_n0": "n_resources_0",
        "mouth_skill_n0": "n_mouth_0",
        "vapour_skill_n0": "n_vapour_0",
        "wyld_skill_n0": "n_wyld_0",
        "divinity_skill_n0": "n_divinity_0",
        "control_edge_n0": "e_endure_torture",
        "knowledge_edge_n0": "e_brave",
        "streetwise_edge_n0": "e_sensitive_vision",
        "faith_edge_n0": "e_purification",
        "killer_trait_n0": "t_anger",
        "intimidate_edge_n0": "e_scary",
        "weaver_trait_n0": "t_honour_code",
        "mouth_trait_n0": "t_religious",
        "vapour_trait_n0": "t_haemophilia",
        "control_skill_n2": "n_control_limit_2",
        "medic_skill_n2": "n_medic_limit_2",
        "persuade_skill_n2": "n_persuade_limit_2",
    }

    atropoan: dict = {
        "breed_n0": "b_breed_atropoan",
        "culture_n0": "b_culture_atropoan",
        "language_n0": "b_language_atropoan",
        "pledged_disciple_n0": "d_nihil",
        "physical_skill_n0": "n_physical_0",
        "killer_skill_n0": "n_killer_0",
        "cloak_skill_n0": "n_cloak_0",
        "smarts_skill_n0": "n_smarts_0",
        "sandman_skill_n0": "n_sandman_0",
        "weaver_skill_n0": "n_weaver_0",
        "resources_skill_n0": "n_resources_0",
        "mouth_skill_n0": "n_mouth_0",
        "vapour_skill_n0": "n_vapour_0",
        "wyld_skill_n0": "n_wyld_0",
        "divinity_skill_n0": "n_divinity_0",
        "athletics_edge_n0": "e_aqua_adapted",
        "persuade_edge_n0": "e_bioluminescent_speech",
        "perception_edge_n0": "e_natural_echolocation",
        "streetwise_edge_n0": "e_sensitive_vision",
        "network_edge_n0": "e_waterworld_native",
        "killer_trait_n0": "t_webbed_toes",
        "cloak_trait_n0": "t_taboo",
        "mouth_trait_n0": "t_cultural_inflexibility",
        "vapour_trait_n0": "t_sid",
        "hacking_skill_n1": "n_hacking_limit_1",
        "hacking_skill_n2": "n_hacking_limit_2",
        "hardtech_skill_n1": "n_hardtech_limit_1",
        "hardtech_skill_n2": "n_hardtech_limit_2",
    }

    # Probably want multiple Feral sub-breeds
    feral: dict = {
        "breed_n0": "b_breed_feral",
        "culture_n0": "b_culture_feral",
        "language_n0": "b_language_standard",
        "language_n1": "b_language_guttertalk",
        "pledged_disciple_n0": "d_isoke",
        "physical_skill_n0": "n_physical_0",
        "killer_skill_n0": "n_killer_0",
        "cloak_skill_n0": "n_cloak_0",
        "smarts_skill_n0": "n_smarts_0",
        "sandman_skill_n0": "n_sandman_0",
        "weaver_skill_n0": "n_weaver_0",
        "resources_skill_n0": "n_resources_0",
        "mouth_skill_n0": "n_mouth_0",
        "vapour_skill_n0": "n_vapour_0",
        "wyld_skill_n0": "n_wyld_0",
        "divinity_skill_n0": "n_divinity_0",
        "endurance_edge_n0": "e_endure_hunger",
        "sandman_trait_n0": "t_high_strung",
        "mouth_trait_n0": "t_mania",
        "vapour_trait_n0": "t_infamy",
        "control_skill_n2": "n_control_limit_2",
        "influence_skill_n2": "n_influence_limit_2",
        "spacecraft_skill_n2": "n_spacecraft_limit_2",
        "aircraft_skill_n2": "n_aircraft_limit_2",
    }

    creature: dict = {
        "breed_n0": "b_breed_creature",
        "physical_skill_n0": "n_physical_0",
        "killer_skill_n0": "n_killer_0",
        "cloak_skill_n0": "n_cloak_0",
        "smarts_skill_n0": "n_smarts_0",
        "sandman_skill_n0": "n_sandman_0",
        "weaver_skill_n0": "n_weaver_0",
        "resources_skill_n0": "n_resources_0",
        "mouth_skill_n0": "n_mouth_0",
        "vapour_skill_n0": "n_vapour_0",
        "wyld_skill_n0": "n_wyld_0",
        "divinity_skill_n0": "n_divinity_0",
    }

    rezhadi: dict = {
        "breed_n0": "b_breed_rezhadi",
        "culture_n0": "b_culture_rezhadi",
        "language_n0": "b_language_rezhadi",
        "physical_skill_n0": "n_physical_0",
        "killer_skill_n0": "n_killer_0",
        "cloak_skill_n0": "n_cloak_0",
        "smarts_skill_n0": "n_smarts_0",
        "sandman_skill_n0": "n_sandman_0",
        "weaver_skill_n0": "n_weaver_0",
        "resources_skill_n0": "n_resources_0",
        "mouth_skill_n0": "n_mouth_0",
        "vapour_skill_n0": "n_vapour_0",
        "wyld_skill_n0": "n_wyld_0",
        "divinity_skill_n0": "n_divinity_0",
    }


class BSCMConfig(BaseModel):
    """This class is to store config values for the Character Manager."""

    # Gamedata Database settings
    gamedata_db: dict = {
        "name": "gamedata",
        "db": "broken_shield_gamedata.sqlite",
        "table": "gamedata",
        "db_path": "./gamedata/",
    }

    gamedata_fields: list = [
        "Mod ID",
        "Name",
        "Description",
        "Mod Category",
        "Mod Type",
        "Custom Text",
        "Allow Multiple Copies",
        "Prerequisites",
        "Prerequisites Any/All",
        "Restrictions",
        "Restrictions Any/All",
        "Skills Touched",
        "Effects",
        "Reference",
    ]

    gamedata_subset_fields: list = [
        "Mod ID",
        "Name",
        "Description",
        "Mod Category",
        "Mod Type",
        "Prerequisites",
        "Restrictions",
        "Effects",
        "Reference",
    ]

    # Value for sleep between menu transitions
    sleep: float = 0.3

    # Character Database settings
    chardata_db: dict = {
        "name": "chardata",
        "db": "broken_shield_characters.sqlite",
        "table": "characters",
        "db_path": "./characters/",
    }

    players_fields: list = [
        "Player ID",
        "Player Name",
        "Player Real Name",
        "Player Email",
        "Player JSON",
        "Deleted",
    ]
    characters_fields: list = [
        "Character ID",
        "Character Name",
        "Character Title",
        "Player ID",
        "Character Type",
        "Character JSON",
        "Deleted",
    ]
    live_characters_fields: list = [
        "Live Character ID",
        "Character ID",
        "Player ID",
        "Character Name",
        "Live Character JSON",
        "Deleted",
    ]

    save_dir: str = "export"
    load_dir: str = "import"
    char_save_file_tail: str = "-bscm2_char_save"
    live_char_save_file_tail: str = "-bscm2_live_char_save"

    # Number of characters to wrap displayed text at:
    wrap: int = 60

    node_map_types: list = [
        "skl",
        "type",
        "extra",
        "drg",
        "cyb",
        "bio",
        "ip0",
        "is0",
        "ir0",
        "iw0",
        "id0",
        "iv0",
        "ic0",
        "ig0",
        "wp0",
        "ws0",
        "wr0",
        "ww0",
        "wd0",
        "wv0",
        "soc",
        "lif",
        "spc",
        "ech",
        "cor",
        "wph",
        "wsm",
        "wre",
        "wwy",
        "wdi",
        "wve",
        "sc0",
        "sc1",
        "sc2",
        "sc3",
        "ode",
        "odt",
    ]

    valid_edge_types: list = [
        "pkc",
        "rmv",
        "ssw",
        "wex",
        "dgx",
        "veh",
        "mce",
        "uni",
        "ode",
        "all",
    ]

    node_map_categories: list = [
        "breed",
        "citizen",
        "culture",
        "language",
        "disciple",
        "edge",
        "injury",
        "lifestyle",
        "social",
        "skill",
        "opportunity",
        "slot",
        "organisation",
        "rank",
        "sliverware",
        "trait",
        "name",
        "soulweaving",
        "wound",
    ]

    # Types that don't change Talent Point values at all
    tp_no_change: list = [
        "brd",
        "dis",
        "lif",
        "soc",
        "cul",
        "lan",
        "cit",
        "org",
        "rnk",
        "id0",
        "ip0",
        "is0",
        "iw0",
        "ir0",
        "iv0",
        "ic0",
        "ig0",
        "ech",
        "spc",
        "lim",
        "cor",
        "wph",
        "wsm",
        "wre",
        "wwy",
        "wdi",
        "wve",
        "sc0",
        "sc1",
        "sc2",
        "sc3",
        "ode",
        "odt",
        "env",
    ]

    # Types that GIVE 2 bonus Talent Points
    tp_bonus: list = ["beh", "nar", "pas", "gas"]

    # Types that cost 1 Talent Point
    tp_cost: list = [
        "bio",
        "cyb",
        "dgx",
        "gas",
        "mce",
        "skl",
        "opp",
        "pkc",
        "rmv",
        "ssw",
        "uni",
        "wex",
        "run",
    ]

    sliverware_complete: list = [
        "s_bodyweb_comp",
        "s_headlink_comp",
        "s_optics_comp",
        "s_neural_rewiring_comp",
        "s_biosculpting_comp",
        "s_nanocore_comp",
        "s_biocore_comp",
    ]

    # From best to worst...
    lifestyles: list = [
        "l_lifestyle_upperzen",
        "l_lifestyle_lowerzen",
        "l_lifestyle_uptown",
        "l_lifestyle_downtown",
        "l_lifestyle_groundzero",
        "l_lifestyle_streets",
        "l_lifestyle_undercity",
    ]

    echo_powers: list = [
        "aerokinesis",
        "electrokinesis",
        "ethereal form",
        "msp",
        "pyrokinesis",
        "telepathy",
        "teleportation",
    ]

    valid_char_types: list = [
        "character",
        "mook",
        # "master",
        "creature",
        # "drone",
        # "groundcraft",
        # "aircraft",
        # "spacecraft",
        # "hybrid-character-creature",
        # "hybrid-character-drone",
        # "hybrid-character-groundcraft",
        # "hybrid-character-aircraft",
        # "hybrid-character-spacecraft",
    ]

    pc_tables: list = [
        "players",
        "characters",
        "live_characters",
    ]

    pc_types: list = [
        "player",
        "char",
        "live_char",
    ]

    # These are Effect fields that get converted into lists during a run of run_gamedata_export.py
    convert_to_list: list = [
        "children",
        "siblings",
    ]

    # TODO: Find a way to add the following sliver_ lists to gamedata. This feels ugly...

    sliver_bodyweb: list = [
        "s_bodyweb",
        "s_chemjet",
        "s_cnsbooster",
        "s_dermalplate",
        "s_monoclaws",
        "s_steelmuscles",
        "s_bodystash",
    ]

    sliver_headlink: list = [
        "s_headlink",
        "s_combatlink",
        "s_dronelink",
        "s_nervelink",
        "s_neuralcomm",
        "s_socialanalyser",
        "s_vcs",
    ]

    sliver_optics: list = [
        "s_optics",
        "s_brainbooster",
        "s_eagleeye",
        "s_forensicscanner",
        "s_taclink",
        "s_thermalimaging",
        "s_threatanalyser",
    ]

    sliver_neuralrewiring: list = [
        "s_neuralrewiring",
        "s_audiowire",
        "s_decrypter",
        "s_godlink",
        "s_weaveview",
        "s_weavelink",
        "s_ultrasonics",
    ]

    sliver_biosculpting: list = [
        "s_biosculpting",
        "s_decentralisedheart",
        "s_dns",
        "s_magnaview",
        "s_pharm",
        "s_musclefibers",
        "s_oxycycler",
    ]

    sliver_biocore: list = [
        "s_biocore",
        "s_aquashift",
        "s_beautifier",
        "s_cloneorgan",
        "s_pheromones",
        "s_stressshift",
        "s_voicecontrol",
    ]

    sliver_nanocore: list = [
        "s_nanocore",
        "s_chameleonfield",
        "s_ecmcloak",
        "s_escapegas",
        "s_nanoarmour",
        "s_nbsu",
        "s_nanoregen",
    ]


class CLIMenus(BaseModel):
    """Class of menus used in CLI_methods.py"""

    select_options: dict = {
        0: "Quit BSCM2",
        1: "Player, character or system search",
        2: "List ALL players",
        3: "Create a new player",
        4: "List ALL characters",
        5: "Create a new character",
        6: "Load a character",
        7: "View loaded character's Build information (Nodes/Mods)",
        8: "View loaded character's Play information (Stats)",
        9: "Save loaded character to DB",
        10: "Export character to JSON save files",
        11: "Import a character from a save file and load them [In Testing]",
        12: "Spend Talent Point: Pick free slot then add mods",
        13: "Spend Talent Point: Pick mods and add to character [In Testing]",
    }

    search_options: dict = {
        0: "Return to main menu",
        1: "Search for Player information",
        2: "Search for Character Build information (Character)",
        3: "Search for Character Play information (Live Character)",
        4: "Search for Mod information",
    }

    subsearch_options: dict = {
        0: "Return to main menu",
        1: "Perform a different type of search",
        2: "Perform another of the same type of search",
    }

    yes_no_quit: dict = {
        0: "Return to main menu",
        1: "Yes",
        2: "No",
    }

    yes_no: dict = {
        0: "No",
        1: "Yes",
    }

    yes_quit: dict = {
        0: "Return to main menu",
        1: "Yes",
    }

    yes_no_build_play: dict = {
        0: "No",
        1: "Yes",
        2: "View character's Build information",
        3: "View character's Play information",
    }

    menu_strings: list = [
        "Return to main menu",
        "Returning to main menu",
        "Please enter your selected option",
    ]

    mod_options: dict = {
        0: "Finish and return to main menu",
        1: "Add a Skill Point",
        2: "Add an Opportunity Point",
        3: "Add a Cybernetic Sliverware Implant",
        4: "Add a Biogenetic Sliverware Implant",
        5: "Add an Edge",
        6: "Add a Trait",
        7: "Add a Specialisation Mastery",
        8: "View/Set character's Starting Talent Points",
        9: "View/Set character's Earned Talent Points",
        10: "View/Set character's Echo Power, Wyld Cancer/Wyld Permanent Injuries",
        11: "View/Set character's Breed and Culture",
        12: "View/Set character's Patron Disciple(s) and Avatar",
        13: "View/Set character's Organisation, Rank, Commendations/Reprimands",
        14: "View/Set character's Age, Gender and Description",
        15: "View/Set character's Languages",
        16: "View/Set character's Weapons and Equipment",
        17: "View/Set character's Contacts, Allies and Enemies",
        18: "View/Modify character's Notes",
        19: "Load list of Available/Free Mod Nodes",
    }

    opportunity_cat_options: dict = {
        0: "Finish and return to previous menu",
        1: "Physical Opportunity Points",
        2: "Smarts Opportunity Points",
        3: "Resources Opportunity Points",
        4: "Wyld Opportunity Points",
        6: "Divinity Opportunity Points",
        7: "Combat, Temporary or Mook Opportunity Points",
    }

    skill_cat_options: dict = {
        0: "Finish and return to previous menu",
        1: "Physical, Athletics, Endurance Skills",
        2: "Killer, Energy, Guns, Melee Skills",
        3: "Cloak, Con, Disguise, Sneak Skills",
        4: "Smarts, Control, Knowledge Skills",
        5: "Sandman, Perception, Psychology, Streetwise Skills",
        6: "Weaver, Hacking, Hardtech, Medic Skills",
        7: "Resources, Influence, Networks Skills",
        8: "Mouth, Intimidate, Leadership, Persuade Skills",
        9: "Vapour, Aircraft, Groundcraft, Spacecraft Skills",
        10: "Wyld, Resistance, Sense Skills",
        11: "First Echo Power, Attack, Manipulation, Nature Skills",
        12: "Second Echo Power, Attack, Manipulation, Nature Skills",
        13: "Divinity, Faith, Invocation Skills",
    }

    smx_cat_options: dict = {
        0: "Finish and return to previous menu",
        1: "Athletics or Endurance",
        2: "Energy, Guns or Melee",
        3: "Con, Disguise, or Sneak",
        4: "Control or Knowledge",
        5: "Perception, Psychology, or Streetwise",
        6: "Hacking, Hardtech, or Medic",
        7: "Influence or Networks",
        8: "Intimidate, Leadership, or Persuade",
        9: "Aircraft, Groundcraft, or Spacecraft",
        10: "Resistance or Sense",
        11: "First Echo Power: Attack, Manipulation or Nature",
        12: "Second Echo Power: Attack, Manipulation or Nature",
        13: "Faith or Invocation",
    }

    edge_cat_options: dict = {
        0: "Finish and return to previous menu",
        1: "All Edges",
        2: "Universal Edges only",
        3: "Physical, Killer, and Cloak Edges",
        4: "Smarts, Sandman, and Weaver Edges",
        5: "Resources, Mouth, and Vapour Edges",
        6: "Wyld, and Echo Edges",
        7: "Divinity Edges and Gifts",
        8: "Creature Edges",
        9: "Vehicle Edges",
    }

    trait_cat_options: dict = {
        0: "Finish and return to previous menu",
        1: "All Traits",
        2: "Passive Traits",
        3: "Behaviour Traits",
        4: "Narrative Traits",
        5: "Vehicle Traits",
    }

    cyb_cat_options: dict = {
        0: "Finish and return to previous menu",
        1: "BodyWeb cybernetic sliverware implants",
        2: "HeadLink cybernetic sliverware implants",
        3: "Optics cybernetic sliverware implants",
        4: "Neural Rewiring cybernetic sliverware implants",
    }

    bio_cat_options: dict = {
        0: "Finish and return to previous menu",
        1: "Biosculpting bioware sliverware implants",
        2: "Biocore bioware sliverware implants",
        3: "Nanocore bioware sliverware implants",
    }


class SpecialStats(BaseModel):
    """This is a Class of Special Stats and config lists"""

    class Config:
        extra = Extra.forbid

    # These are the stats that shouldn't be altered by a mod_id
    protected_stats: list = [
        "live_char_id",
        "char_id",
        "deleted",
        "char_name",
        "player_name",
        "player_id",
        "char_type",
        "char_age",
        "char_gender",
        "char_description",
        "char_picture",
        "created",
        "modified",
        "physical_av_min",
        "physical_av_max",
        "smarts_av_min",
        "smarts_av_max",
        "resources_av_min",
        "resources_av_max",
        "wyld_av_min",
        "wyld_av_max",
        "divinity_av_min",
        "divinity_av_max",
        "vehicle_av_min",
        "vehicle_av_max",
        "twin",
        "parent",
        "children",
    ]

    # These stats are strings that should be replaced rather than appended to
    replace_stats: list = [
        "breed_name",
        "culture",
        "char_age",
        "char_gender",
        "citizen",
        "social_class",
        "lifestyle",
        "organisation",
        "rank",
        "echo1_name",
        "echo2_name",
        "char_picture",
        "char_gender",
        "char_age",
        "char_type",
        "char_archetype",
        "char_name",
        "total_languages",
        "smx1_name",
        "smx2_name",
        "smx3_name",
        "wyld_cancer_total",
        "wyld_cancer_mult",
        "wyld_cancer_perm_threshold",
        "wyld_perm_injuries_count",
        "healed_wyld_perm_injuries",
        "wyld_perm_injuries",
        "gamedata_name",
        "pledged_disciple",
        "twin",
        "parent",
        "children",
    ]

    # Some are Dicts, some are Ints so do type check on them!
    secondary_info: list = [
        "weapons",
        "gear",
        "char_missions",
        "char_contacts",
        "commendations",
        "reprimands",
        "reputation",
    ]

    min_1_skills: list = [
        "physical",
        "killer",
        "cloak",
        "smarts",
        "sandman",
        "weaver",
        "resources",
        "mouth",
        "vapour",
        "wyld",
        "divinity",
        "scale",
        "speed",
    ]

    armour_values: list = [
        "physical_av",
        "smarts_av",
        "resources_av",
        "wyld_av",
        "divinity_av",
        "vehicle_av",
    ]

    smx_slots: list = [
        "spec_mastery1_name_n0",
        "spec_mastery2_name_n0",
        "spec_mastery3_name_n0",
    ]

    smx_skills: list = [
        "athletics",
        "endurance",
        "guns",
        "melee",
        "energy",
        "con",
        "disguise",
        "sneak",
        "control",
        "knowledge",
        "perception",
        "streetwise",
        "psychology",
        "hacking",
        "hardtech",
        "medic",
        "influence",
        "network",
        "persuade",
        "leadership",
        "intimidate",
        "aircraft",
        "groundcraft",
        "spacecraft",
        "resistance",
        "sense",
        "attack1",
        "nature1",
        "manipulation1",
        "attack2",
        "nature2",
        "manipulation2",
        "faith",
        "invocation",
    ]

    note_types: list = [
        "edges",
        "traits",
        "team_edges",
        "team_traits",
        "temporary_edges",
        "temporary_traits",
        "sliverware",
        "physical",
        "killer",
        "cloak",
        "smarts",
        "sandman",
        "weaver",
        "resources",
        "mouth",
        "vapour",
        "wyld",
        "echo",
        "divinity",
        "initiative",
        "gifts_curses",
        "general",
        "vehicle",
        "mook",
        "injury",
        "perm_wyld_injury",
        "warning",
        "character",
        "gm",
        "player",
        "pledged_disciple",
        "missions",
        "contacts_allies_enemies",
        "weapons",
        "gear",
        "char_missions",
        "char_contacts",
        "soulweaving",
        "corruption",
        "heresies",
        "geas",
        "blessings",
        "perm_corruption_injury",
    ]


class NodeMap(BaseModel):
    """This is the default mapping of what kinds of mod_ids can go in each node"""

    class Config:
        extra = Extra.forbid

    # A useful list of all the possible categories available to the node map. All entries within each category are
    # in the form of a list e.g. {"type": ["brd"]}
    node_map_types: list = [
        "type",
    ]

    node_map_types_extra: list = [
        "extra",
    ]

    node_mod_types: list = [
        "skl",
        "drg",
        "cyb",
        "bio",
        "ip0",
        "is0",
        "ir0",
        "iw0",
        "id0",
        "iv0",
        "ic0",
        "ig0",
        "wp0",
        "ws0",
        "wr0",
        "ww0",
        "wd0",
        "wv0",
        "soc",
        "lif",
        "spc",
        "ech",
        "cor",
        "sc0",
        "sc1",
        "sc2",
        "sc3",
        "odt",
        "ode",
    ]

    node_map_edge_types: list = [
        "pkc",
        "rmv",
        "ssw",
        "wex",
        "dgx",
        "veh",
        "mce",
        "uni",
        "ode",
        "all",
    ]

    node_map_categories: list = [
        "breed",
        "citizen",
        "culture",
        "language",
        "disciple",
        "edge",
        "injury",
        "lifestyle",
        "social",
        "skill",
        "opportunity",
        "slot",
        "organisation",
        "rank",
        "sliverware",
        "trait",
        "name",
        "soulweaving",
    ]

    # NODE MAP:
    # Lists allowed Mod Types, or Mod_IDs that can go in that particular node slot
    # name = slot nice name
    # category = mod category allowed
    # cxn = connections to other nodes
    breed_n0: dict = {
        "name": "breed_slot",
        "category": "breed",
        "type": ["brd"],
        "cxn": ["entry_node"],
    }
    culture_n0: dict = {
        "name": "culture_slot",
        "category": "culture",
        "type": ["cul"],
        "cxn": ["entry_node"],
    }
    social_n0: dict = {
        "name": "social_class_slot",
        "category": "social",
        "type": ["soc"],
        "cxn": ["null"],
    }
    lifestyle_n0: dict = {
        "name": "lifestyle_slot",
        "category": "lifestyle",
        "type": ["lif"],
        "cxn": ["null"],
    }
    language_n0: dict = {
        "name": "first_language_slot",
        "category": "language",
        "type": ["lan"],
        "cxn": ["entry_node"],
    }
    language_n1: dict = {
        "name": "second_language_slot",
        "category": "language",
        "type": ["lan"],
        "cxn": ["language_n0"],
    }
    language_n2: dict = {
        "name": "third_language_slot",
        "category": "language",
        "type": ["lan"],
        "cxn": ["language_n1"],
    }
    language_n3: dict = {
        "name": "fourth_language_slot",
        "category": "language",
        "type": ["lan"],
        "cxn": ["language_n2"],
    }
    language_n4: dict = {
        "name": "fifth_language_slot",
        "category": "language",
        "type": ["lan"],
        "cxn": ["language_n3"],
    }
    language_n5: dict = {
        "name": "sixth_language_slot",
        "category": "language",
        "type": ["lan"],
        "cxn": ["language_n4"],
    }
    language_n6: dict = {
        "name": "seventh_language_slot",
        "category": "language",
        "type": ["lan"],
        "cxn": ["language_n5"],
    }
    language_n7: dict = {
        "name": "eighth_language_slot",
        "category": "language",
        "type": ["lan"],
        "cxn": ["language_n6"],
    }
    language_n8: dict = {
        "name": "ninth_language_slot",
        "category": "language",
        "type": ["lan"],
        "cxn": ["language_n7"],
    }
    language_n9: dict = {
        "name": "tenth_language_slot",
        "category": "language",
        "type": ["lan"],
        "cxn": ["language_n8"],
    }
    pledged_disciple_n0: dict = {
        "name": "pledged_disciple_slot",
        "category": "disciple",
        "type": ["dis"],
        "cxn": ["entry_node"],
    }
    pledged_disciple_n1: dict = {
        "name": "syncretic_disciple_slot",
        "category": "disciple",
        "type": ["dis"],
        "cxn": ["pledged_disciple_n0"],
    }
    pledged_disciple_n2: dict = {
        "name": "second_syncretic_disciple_slot",
        "category": "disciple",
        "type": ["dis"],
        "cxn": ["pledged_disciple_n1"],
    }
    avatar_n0: dict = {
        "name": "avatar_of_slot",
        "category": "disciple",
        "type": ["dis"],
        "cxn": ["pledged_disciple_n0"],
    }
    avatar_n1: dict = {
        "name": "syncretic_avatar_of_slot",
        "category": "disciple",
        "type": ["dis"],
        "cxn": ["pledged_disciple_n1"],
    }
    avatar_n2: dict = {
        "name": "second_syncretic_avatar_of_slot",
        "category": "disciple",
        "type": ["dis"],
        "cxn": ["pledged_disciple_n2"],
    }
    citizen_n0: dict = {
        "name": "primary_citizenship_slot",
        "category": "citizen",
        "type": ["cit"],
        "cxn": ["entry_node"],
    }
    citizen_n1: dict = {
        "name": "second_citizenship_slot",
        "category": "citizen",
        "type": ["cit"],
        "cxn": ["citizen_n0"],
    }
    citizen_n2: dict = {
        "name": "third_citizenship_slot",
        "category": "citizen",
        "type": ["cit"],
        "cxn": ["citizen_n1"],
    }
    organisation_n0: dict = {
        "name": "organisation_slot",
        "category": "organisation",
        "type": ["org"],
        "cxn": ["entry_node"],
    }
    organisation_n1: dict = {
        "name": "second_organisation_slot",
        "category": "organisation",
        "type": ["org"],
        "cxn": ["organisation_n0"],
    }
    organisation_n2: dict = {
        "name": "third_organisation_slot",
        "category": "organisation",
        "type": ["org"],
        "cxn": ["organisation_n1"],
    }
    organisation_n3: dict = {
        "name": "fourth_organisation_slot",
        "category": "organisation",
        "type": ["org"],
        "cxn": ["organisation_n2"],
    }
    rank_n0: dict = {
        "name": "rank_slot",
        "category": "rank",
        "type": ["rnk"],
        "cxn": ["organisation_n0"],
    }
    rank_n1: dict = {
        "name": "rank_in_second_organisation_slot",
        "category": "rank",
        "type": ["rnk"],
        "cxn": ["organisation_n1"],
    }
    rank_n2: dict = {
        "name": "rank_in_third_organisation_slot",
        "category": "rank",
        "type": ["rnk"],
        "cxn": ["organisation_n2"],
    }
    rank_n3: dict = {
        "name": "rank_in_fourth_organisation_slot",
        "category": "rank",
        "type": ["rnk"],
        "cxn": ["organisation_n3"],
    }

    # PHYSICAL (ATHLETICS/ENDURANCE) SKILL
    physical_skill_n0: dict = {
        "name": "physical_1_skill_slot",
        "category": "skill",
        "skl": ["n_physical_0"],
        "cxn": [
            "entry_node",
            "physical_skill_n1",
            "physical_skill_n2",
            "physical_skill_n3",
            "physical_skill_n4",
            "physical_skill_n5",
            "physical_skill_n6",
        ],
    }
    physical_skill_n1: dict = {
        "name": "physical_2_skill_slot",
        "category": "skill",
        "skl": ["n_physical_1"],
        "cxn": [
            "physical_skill_n0",
            "physical_skill_n6",
            "physical_skill_n2",
            "athletics_skill_n0",
        ],
    }
    physical_skill_n2: dict = {
        "name": "physical_3_skill_slot",
        "category": "skill",
        "skl": ["n_physical_2"],
        "cxn": [
            "physical_n0",
            "physical_skill_n1",
            "physical_skill_n3",
            "endurance_skill_n0",
        ],
    }
    physical_skill_n3: dict = {
        "name": "physical_4_skill_slot",
        "category": "skill",
        "skl": ["n_physical_3"],
        "cxn": [
            "physical_n0",
            "physical_skill_n2",
            "physical_skill_n4",
            "physical_op_n0",
        ],
    }
    physical_skill_n4: dict = {
        "name": "physical_5_skill_slot",
        "category": "skill",
        "skl": ["n_physical_4"],
        "cxn": ["physical_n0", "physical_skill_n3", "physical_skill_n5"],
    }
    physical_skill_n5: dict = {
        "name": "physical_6_skill_slot",
        "category": "skill",
        "skl": ["n_physical_5"],
        "cxn": ["physical_n0", "physical_skill_n4", "physical_skill_n6"],
    }
    physical_skill_n6: dict = {
        "name": "physical_7_skill_slot",
        "category": "skill",
        "skl": ["n_physical_6"],
        "cxn": ["physical_n0", "physical_skill_n5"],
    }
    physical_op_n0: dict = {
        "name": "physical_opportunity_1_slot",
        "category": "opportunity",
        "opp": ["n_physical_op_0"],
        "cxn": ["physical_skill_n3", "physical_op_n1"],
    }
    physical_op_n1: dict = {
        "name": "physical_opportunity_2_slot",
        "category": "opportunity",
        "opp": ["n_physical_op_1"],
        "cxn": ["n_physical_op_0", "n_physical_op_2"],
    }
    physical_op_n2: dict = {
        "name": "physical_opportunity_3_slot",
        "category": "opportunity",
        "opp": ["n_physical_op_2"],
        "cxn": ["n_physical_op_1", "n_physical_op_3"],
    }
    physical_op_n3: dict = {
        "name": "physical_opportunity_4_slot",
        "category": "opportunity",
        "opp": ["n_physical_op_3"],
        "cxn": ["n_physical_op_2"],
    }
    athletics_skill_n0: dict = {
        "name": "athletics_1_skill_slot",
        "category": "skill",
        "skl": ["n_athletics_0", "n_athletics_limit_0"],
        "cxn": ["physical_skill_n1", "athletics_skill_n1", "athletics_edge_n0"],
    }
    athletics_skill_n1: dict = {
        "name": "athletics_2_skill_slot",
        "category": "skill",
        "skl": ["n_athletics_1", "n_athletics_limit_1"],
        "cxn": ["athletics_skill_n0", "athletics_skill_n2"],
    }
    athletics_skill_n2: dict = {
        "name": "athletics_3_skill_slot",
        "category": "skill",
        "skl": ["n_athletics_2", "n_athletics_limit_2"],
        "cxn": ["athletics_skill_n1", "smx"],
    }
    athletics_edge_n0: dict = {
        "name": "athletics_edge_slot",
        "category": "edge",
        "type": ["pkc", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["athletics_skill_n0"],
    }
    endurance_skill_n0: dict = {
        "name": "endurance_1_skill_slot",
        "category": "skill",
        "skl": ["n_endurance_0", "n_endurance_limit_0"],
        "cxn": ["physical_skill_n2", "endurance_skill_n1", "endurance_edge_n0"],
    }
    endurance_skill_n1: dict = {
        "name": "endurance_2_skill_slot",
        "category": "skill",
        "skl": ["n_endurance_1", "n_endurance_limit_1"],
        "cxn": ["endurance_skill_n0", "endurance_skill_n2"],
    }
    endurance_skill_n2: dict = {
        "name": "endurance_3_skill_slot",
        "category": "skill",
        "skl": ["n_endurance_2", "n_endurance_limit_2"],
        "cxn": ["endurance_skill_n1", "smx"],
    }
    endurance_edge_n0: dict = {
        "name": "endurance_edge_slot",
        "category": "edge",
        "type": ["pkc", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["endurance_skill_n0"],
    }

    # KILLER (GUNS/MELEE/ENERGY SKILL)
    killer_skill_n0: dict = {
        "name": "killer_1_skill_slot",
        "category": "skill",
        "skl": ["n_killer_0"],
        "cxn": [
            "entry_node",
            "killer_skill_n1",
            "killer_skill_n2",
            "killer_skill_n3",
            "killer_skill_n4",
            "killer_skill_n5",
            "killer_skill_n6",
        ],
    }
    killer_skill_n1: dict = {
        "name": "killer_2_skill_slot",
        "category": "skill",
        "skl": ["n_killer_1"],
        "cxn": [
            "killer_skill_n0",
            "killer_skill_n6",
            "killer_skill_n2",
            "energy_skill_n0",
        ],
    }
    killer_skill_n2: dict = {
        "name": "killer_3_skill_slot",
        "category": "skill",
        "skl": ["n_killer_2"],
        "cxn": [
            "killer_skill_n0",
            "killer_skill_n1",
            "killer_skill_n3",
            "guns_skill_n0",
        ],
    }
    killer_skill_n3: dict = {
        "name": "killer_4_skill_slot",
        "category": "skill",
        "skl": ["n_killer_3"],
        "cxn": [
            "killer_skill_n0",
            "killer_skill_n2",
            "killer_skill_n4",
            "melee_skill_n0",
        ],
    }
    killer_skill_n4: dict = {
        "name": "killer_5_skill_slot",
        "category": "skill",
        "skl": ["n_killer_4"],
        "cxn": ["killer_skill_n0", "killer_skill_n3", "killer_skill_n5"],
    }
    killer_skill_n5: dict = {
        "name": "killer_6_skill_slot",
        "category": "skill",
        "skl": ["n_killer_5"],
        "cxn": ["killer_skill_n0", "killer_skill_n4", "killer_skill_n6"],
    }
    killer_skill_n6: dict = {
        "name": "killer_7_skill_slot",
        "category": "skill",
        "skl": ["n_killer_6"],
        "cxn": [
            "killer_skill_n0",
            "killer_skill_n1",
            "killer_skill_n5",
            "killer_trait_n0",
        ],
    }
    killer_trait_n0: dict = {
        "name": "killer_trait_slot",
        "category": "trait",
        "type": ["beh", "nar", "pas"],
        "extra": ["veh"],
        "cxn": ["killer_skill_n6"],
    }
    energy_skill_n0: dict = {
        "name": "energy_1_skill_slot",
        "category": "skill",
        "skl": ["n_energy_0", "n_energy_limit_0"],
        "cxn": ["killer_skill_n1", "energy_skill_n0", "energy_edge_n0"],
    }
    energy_skill_n1: dict = {
        "name": "energy_2_skill_slot",
        "category": "skill",
        "skl": ["n_energy_1", "n_energy_limit_1"],
        "cxn": ["energy_skill_n0", "energy_skill_n2"],
    }
    energy_skill_n2: dict = {
        "name": "energy_3_skill_slot",
        "category": "skill",
        "skl": ["n_energy_2", "n_energy_limit_2"],
        "cxn": ["energy_skill_n2", "smx"],
    }
    energy_edge_n0: dict = {
        "name": "energy_edge_slot",
        "category": "edge",
        "type": ["pkc", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["energy_skill_n0"],
    }
    guns_skill_n0: dict = {
        "name": "guns_1_skill_slot",
        "category": "skill",
        "skl": ["n_guns_0", "n_guns_limit_0"],
        "cxn": ["killer_skill_n2", "guns_skill_n1", "guns_edge_n0"],
    }
    guns_skill_n1: dict = {
        "name": "guns_2_skill_slot",
        "category": "skill",
        "skl": ["n_guns_1", "n_guns_limit_1"],
        "cxn": ["guns_skill_n0", "guns_skill_n2"],
    }
    guns_skill_n2: dict = {
        "name": "guns_3_skill_slot",
        "category": "skill",
        "skl": ["n_guns_2", "n_guns_limit_2"],
        "cxn": ["guns_skill_n1", "smx"],
    }
    guns_edge_n0: dict = {
        "name": "guns_edge_slot",
        "category": "edge",
        "type": ["pkc", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["guns_skill_n0"],
    }
    melee_skill_n0: dict = {
        "name": "melee_1_skill_slot",
        "category": "skill",
        "skl": ["n_melee_0", "n_melee_limit_0"],
        "cxn": ["killer_skill_n3", "melee_skill_n1", "melee_edge_n0"],
    }
    melee_skill_n1: dict = {
        "name": "melee_2_skill_slot",
        "category": "skill",
        "skl": ["n_melee_1", "n_melee_limit_1"],
        "cxn": ["melee_skill_n0", "melee_skill_n1"],
    }
    melee_skill_n2: dict = {
        "name": "melee_3_skill_slot",
        "category": "skill",
        "skl": ["n_melee_2", "n_melee_limit_2"],
        "cxn": ["melee_skill_n2", "smx"],
    }
    melee_edge_n0: dict = {
        "name": "melee_edge_slot",
        "category": "edge",
        "type": ["pkc", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["melee_skill_n0"],
    }

    # CLOAK (CON/SNEAK/DISGUISE) SKILL
    cloak_skill_n0: dict = {
        "name": "cloak_1_skill_slot",
        "category": "skill",
        "skl": ["n_cloak_0"],
        "cxn": [
            "entry_node",
            "cloak_skill_n1",
            "cloak_skill_n2",
            "cloak_skill_n3",
            "cloak_skill_n4",
            "cloak_skill_n5",
            "cloak_skill_n6",
        ],
    }
    cloak_skill_n1: dict = {
        "name": "cloak_2_skill_slot",
        "category": "skill",
        "skl": ["n_cloak_1"],
        "cxn": [
            "cloak_skill_n0",
            "cloak_skill_n6",
            "cloak_skill_n2",
            "disguise_skill_n0",
        ],
    }
    cloak_skill_n2: dict = {
        "name": "cloak_3_skill_slot",
        "category": "skill",
        "skl": ["n_cloak_2"],
        "cxn": [
            "cloak_skill_n0",
            "cloak_skill_n1",
            "cloak_skill_n3",
            "con_skill_n0",
        ],
    }
    cloak_skill_n3: dict = {
        "name": "cloak_4_skill_slot",
        "category": "skill",
        "skl": ["n_cloak_3"],
        "cxn": [
            "cloak_skill_n0",
            "cloak_skill_n2",
            "cloak_skill_n4",
            "sneak_skill_n0",
        ],
    }
    cloak_skill_n4: dict = {
        "name": "cloak_5_skill_slot",
        "category": "skill",
        "skl": ["n_cloak_4"],
        "cxn": [
            "cloak_skill_n0",
            "cloak_skill_n3",
            "cloak_skill_n5",
        ],
    }
    cloak_skill_n5: dict = {
        "name": "cloak_6_skill_slot",
        "category": "skill",
        "skl": ["n_cloak_5"],
        "cxn": [
            "cloak_skill_n0",
            "cloak_skill_n4",
            "cloak_skill_n6",
        ],
    }
    cloak_skill_n6: dict = {
        "name": "cloak_7_skill_slot",
        "category": "skill",
        "skl": ["n_cloak_6"],
        "cxn": ["cloak_skill_n0", "cloak_skill_n5", "cloak_skill_n1", "cloak_trait_n0"],
    }
    cloak_trait_n0: dict = {
        "name": "cloak_trait_slot",
        "category": "trait",
        "type": ["beh", "nar", "pas"],
        "extra": ["veh"],
        "cxn": ["cloak_skill_n6"],
    }
    disguise_skill_n0: dict = {
        "name": "disguise_1_skill_slot",
        "category": "skill",
        "skl": ["n_disguise_0", "n_disguise_limit_0"],
        "cxn": ["cloak_skill_n1", "disguise_skill_n1", "disguise_edge_n0"],
    }
    disguise_skill_n1: dict = {
        "name": "disguise_2_skill_slot",
        "category": "skill",
        "skl": ["n_disguise_1", "n_disguise_limit_1"],
        "cxn": [
            "disguise_skill_n0",
            "disguise_skill_n2",
        ],
    }
    disguise_skill_n2: dict = {
        "name": "disguise_3_skill_slot",
        "category": "skill",
        "skl": ["n_disguise_2", "n_disguise_limit_2"],
        "cxn": ["disguise_skill_n1"],
    }
    disguise_edge_n0: dict = {
        "name": "disguise_edge_slot",
        "category": "edge",
        "type": ["pkc", "uni"],
        "extra": ["veh", "mce", "all"],
        "cxn": ["disguise_skill_n0", "smx"],
    }
    con_skill_n0: dict = {
        "name": "con_1_skill_slot",
        "category": "skill",
        "skl": ["n_con_0", "n_con_limit_0"],
        "cxn": ["cloak_skill_n2", "con_skill_n1", "con_edge_n0"],
    }
    con_skill_n1: dict = {
        "name": "con_2_skill_slot",
        "category": "skill",
        "skl": ["n_con_1", "n_con_limit_1"],
        "cxn": ["con_skill_n0", "con_skill_n2"],
    }
    con_skill_n2: dict = {
        "name": "con_3_skill_slot",
        "category": "skill",
        "skl": ["n_con_2", "n_con_limit_2"],
        "cxn": ["con_skill_n1"],
    }
    con_edge_n0: dict = {
        "name": "con_edge_slot",
        "category": "edge",
        "type": ["pkc", "uni"],
        "extra": ["veh", "mce", "all"],
        "cxn": ["con_skill_n0", "smx"],
    }
    sneak_skill_n0: dict = {
        "name": "sneak_1_skill_slot",
        "category": "skill",
        "skl": ["n_sneak_0", "n_sneak_limit_0"],
        "cxn": ["cloak_skill_n3", "sneak_skill_n1", "sneak_edge_n0"],
    }
    sneak_skill_n1: dict = {
        "name": "sneak_2_skill_slot",
        "category": "skill",
        "skl": ["n_sneak_1", "n_sneak_limit_1"],
        "cxn": ["sneak_skill_n0", "sneak_skill_n2"],
    }
    sneak_skill_n2: dict = {
        "name": "sneak_3_skill_slot",
        "category": "skill",
        "skl": ["n_sneak_2", "n_sneak_limit_2"],
        "cxn": ["sneak_skill_n1", "smx"],
    }
    sneak_edge_n0: dict = {
        "name": "sneak_edge_slot",
        "category": "edge",
        "type": ["pkc", "uni"],
        "extra": ["veh", "mce", "all"],
        "cxn": ["sneak_skill_n0"],
    }

    # SMARTS (KNOWLEDGE/CONTROL) SKILL
    smarts_skill_n0: dict = {
        "name": "smarts_1_skill_slot",
        "category": "skill",
        "skl": ["n_smarts_0"],
        "cxn": [
            "entry_node",
            "smarts_skill_n1",
            "smarts_skill_n2",
            "smarts_skill_n3",
            "smarts_skill_n4",
            "smarts_skill_n5",
            "smarts_skill_n6",
        ],
    }
    smarts_skill_n1: dict = {
        "name": "smarts_2_skill_slot",
        "category": "skill",
        "skl": ["n_smarts_1"],
        "cxn": [
            "smarts_skill_n0",
            "smarts_skill_n6",
            "smarts_skill_n2",
            "knowledge_skill_n0",
        ],
    }
    smarts_skill_n2: dict = {
        "name": "smarts_3_skill_slot",
        "category": "skill",
        "skl": ["n_smarts_2"],
        "cxn": [
            "smarts_skill_n0",
            "smarts_skill_n1",
            "smarts_skill_n3",
            "control_skill_n0",
        ],
    }
    smarts_skill_n3: dict = {
        "name": "smarts_4_skill_slot",
        "category": "skill",
        "skl": ["n_smarts_3"],
        "cxn": [
            "smarts_skill_n0",
            "smarts_skill_n2",
            "smarts_skill_n4",
            "smarts_op_n0",
        ],
    }
    smarts_skill_n4: dict = {
        "name": "smarts_5_skill_slot",
        "category": "skill",
        "skl": ["n_smarts_4"],
        "cxn": [
            "smarts_skill_n0",
            "smarts_skill_n3",
            "smarts_skill_n5",
        ],
    }
    smarts_skill_n5: dict = {
        "name": "smarts_6_skill_slot",
        "category": "skill",
        "skl": ["n_smarts_5"],
        "cxn": [
            "smarts_skill_n0",
            "smarts_skill_n4",
            "smarts_skill_n6",
        ],
    }
    smarts_skill_n6: dict = {
        "name": "smarts_7_skill_slot",
        "category": "skill",
        "skl": ["n_smarts_6"],
        "cxn": [
            "smarts_skill_n0",
            "smarts_skill_n5",
            "smarts_skill_n1",
        ],
    }
    smarts_op_n0: dict = {
        "name": "smarts_opportunity_1_slot",
        "category": "opportunity",
        "opp": ["n_smarts_op_0"],
        "cxn": ["smarts_skill_n3", "smarts_op_n1"],
    }
    smarts_op_n1: dict = {
        "name": "smarts_opportunity_2_slot",
        "category": "opportunity",
        "opp": ["n_smarts_op_1"],
        "cxn": ["smarts_op_n0", "smarts_op_n2"],
    }
    smarts_op_n2: dict = {
        "name": "smarts_opportunity_3_slot",
        "category": "opportunity",
        "opp": ["n_smarts_op_2"],
        "cxn": ["smarts_op_n1", "smarts_op_n3"],
    }
    smarts_op_n3: dict = {
        "name": "smarts_opportunity_4_slot",
        "category": "opportunity",
        "opp": ["n_smarts_op_3"],
        "cxn": ["smarts_op_n2"],
    }
    knowledge_skill_n0: dict = {
        "name": "knowledge_1_skill_slot",
        "category": "skill",
        "skl": ["n_knowledge_0", "n_knowledge_limit_0"],
        "cxn": ["smarts_skill_n1", "knowledge_skill_n1", "knowledge_edge_n0"],
    }
    knowledge_skill_n1: dict = {
        "name": "knowledge_2_skill_slot",
        "category": "skill",
        "skl": ["n_knowledge_1", "n_knowledge_limit_1"],
        "cxn": ["knowledge_skill_n0", "knowledge_skill_n2"],
    }
    knowledge_skill_n2: dict = {
        "name": "knowledge_3_skill_slot",
        "category": "skill",
        "skl": ["n_knowledge_2", "n_knowledge_limit_2"],
        "cxn": ["knowledge_skill_n1", "smx"],
    }
    knowledge_edge_n0: dict = {
        "name": "knowledge_edge_slot",
        "category": "edge",
        "type": ["ssw", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["knowledge_skill_n0"],
    }
    control_skill_n0: dict = {
        "name": "control_1_skill_slot",
        "category": "skill",
        "skl": ["n_control_0", "n_control_limit_1"],
        "cxn": ["smarts_skill_n2", "control_skill_n1", "control_edge_n0"],
    }
    control_skill_n1: dict = {
        "name": "control_2_skill_slot",
        "category": "skill",
        "skl": ["n_control_1", "n_control_limit_1"],
        "cxn": ["control_skill_n0", "control_skill_n2"],
    }
    control_skill_n2: dict = {
        "name": "control_3_skill_slot",
        "category": "skill",
        "skl": ["n_control_2", "n_control_limit_2"],
        "cxn": ["control_skill_n1", "smx"],
    }
    control_edge_n0: dict = {
        "name": "control_edge_slot",
        "category": "edge",
        "type": ["ssw", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["control_skill_n0"],
    }

    # SANDMAN (PERCEPTION/STREETWISE/PSYCHOLOGY) SKILL
    sandman_skill_n0: dict = {
        "name": "sandman_1_skill_slot",
        "category": "skill",
        "skl": ["n_sandman_0"],
        "cxn": [
            "entry_node",
            "sandman_skill_n1",
            "sandman_skill_n2",
            "sandman_skill_n3",
            "sandman_skill_n4",
            "sandman_skill_n5",
            "sandman_skill_n6",
        ],
    }
    sandman_skill_n1: dict = {
        "name": "sandman_2_skill_slot",
        "category": "skill",
        "skl": ["n_sandman_1"],
        "cxn": [
            "sandman_skill_n0",
            "sandman_skill_n6",
            "sandman_skill_n2",
            "psychology_skill_n0",
        ],
    }
    sandman_skill_n2: dict = {
        "name": "sandman_3_skill_slot",
        "category": "skill",
        "skl": ["n_sandman_2"],
        "cxn": [
            "sandman_skill_n0",
            "sandman_skill_n1",
            "sandman_skill_n3",
            "streetwise_skill_n0",
        ],
    }
    sandman_skill_n3: dict = {
        "name": "sandman_4_skill_slot",
        "category": "skill",
        "skl": ["n_sandman_3"],
        "cxn": [
            "sandman_skill_n0",
            "sandman_skill_n2",
            "sandman_skill_n4",
            "perception_skill_n0",
        ],
    }
    sandman_skill_n4: dict = {
        "name": "sandman_5_skill_slot",
        "category": "skill",
        "skl": ["n_sandman_4"],
        "cxn": [
            "sandman_skill_n0",
            "sandman_skill_n3",
            "sandman_skill_n5",
        ],
    }
    sandman_skill_n5: dict = {
        "name": "sandman_6_skill_slot",
        "category": "skill",
        "skl": ["n_sandman_5"],
        "cxn": [
            "sandman_skill_n0",
            "sandman_skill_n4",
            "sandman_skill_n6",
        ],
    }
    sandman_skill_n6: dict = {
        "name": "sandman_7_skill_slot",
        "category": "skill",
        "skl": ["n_sandman_6"],
        "cxn": [
            "sandman_skill_n0",
            "sandman_skill_n5",
            "sandman_skill_n1",
            "sandman_trait_n0",
        ],
    }
    sandman_trait_n0: dict = {
        "name": "sandman_trait_slot",
        "category": "trait",
        "type": ["beh", "nar", "pas"],
        "extra": ["veh"],
        "cxn": ["sandman_skill_n6"],
    }
    psychology_skill_n0: dict = {
        "name": "psychology_1_skill_slot",
        "category": "skill",
        "skl": ["n_psychology_0", "n_psychology_limit_0"],
        "cxn": ["sandman_skill_n1", "psychology_skill_n1", "psychology_edge_n0"],
    }
    psychology_skill_n1: dict = {
        "name": "psychology_2_skill_slot",
        "category": "skill",
        "skl": ["n_psychology_1", "n_psychology_limit_1"],
        "cxn": ["psychology_skill_n0", "psychology_skill_n2"],
    }
    psychology_skill_n2: dict = {
        "name": "psychology_3_skill_slot",
        "category": "skill",
        "skl": ["n_psychology_2", "n_psychology_limit_2"],
        "cxn": ["psychology_skill_n1", "smx"],
    }
    psychology_edge_n0: dict = {
        "name": "psychology_edge_slot",
        "category": "edge",
        "type": ["ssw", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["psychology_skill_n0"],
    }
    streetwise_skill_n0: dict = {
        "name": "streetwise_1_skill_slot",
        "category": "skill",
        "skl": ["n_streetwise_0", "n_streetwise_limit_0"],
        "cxn": ["sandman_skill_n2", "streetwise_skill_n1", "streetwise_edge_n0"],
    }
    streetwise_skill_n1: dict = {
        "name": "streetwise_2_skill_slot",
        "category": "skill",
        "skl": ["n_streetwise_1", "n_streetwise_limit_1"],
        "cxn": ["streetwise_skill_n0", "streetwise_skill_n2"],
    }
    streetwise_skill_n2: dict = {
        "name": "streetwise_3_skill_slot",
        "category": "skill",
        "skl": ["n_streetwise_2", "n_streetwise_limit_2"],
        "cxn": ["streetwise_skill_n1", "smx"],
    }
    streetwise_edge_n0: dict = {
        "name": "streetwise_edge_slot",
        "category": "edge",
        "type": ["ssw", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["streetwise_skill_n0"],
    }
    perception_skill_n0: dict = {
        "name": "perception_1_skill_slot",
        "category": "skill",
        "skl": ["n_perception_0", "n_perception_limit_0"],
        "cxn": ["sandman_skill_n3", "perception_skill_n1", "perception_edge_n0"],
    }
    perception_skill_n1: dict = {
        "name": "perception_2_skill_slot",
        "category": "skill",
        "skl": ["n_perception_1", "n_perception_limit_1"],
        "cxn": ["perception_skill_n0", "perception_skill_n2"],
    }
    perception_skill_n2: dict = {
        "name": "perception_3_skill_slot",
        "category": "skill",
        "skl": ["n_perception_2", "n_perception_limit_2"],
        "cxn": ["perception_skill_n1", "smx"],
    }
    perception_edge_n0: dict = {
        "name": "perception_edge_slot",
        "category": "edge",
        "type": ["ssw", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["perception_skill_n0"],
    }

    # WEAVER (MEDIC/HARDTECH/HACKING) SKILL
    weaver_skill_n0: dict = {
        "name": "weaver_1_skill_slot",
        "category": "skill",
        "skl": ["n_weaver_0"],
        "cxn": [
            "entry_node",
            "weaver_skill_n1",
            "weaver_skill_n2",
            "weaver_skill_n3",
            "weaver_skill_n4",
            "weaver_skill_n5",
            "weaver_skill_n6",
        ],
    }
    weaver_skill_n1: dict = {
        "name": "weaver_2_skill_slot",
        "category": "skill",
        "skl": ["n_weaver_1"],
        "cxn": [
            "weaver_skill_n0",
            "weaver_skill_n6",
            "weaver_skill_n2",
            "medic_skill_n0",
        ],
    }
    weaver_skill_n2: dict = {
        "name": "weaver_3_skill_slot",
        "category": "skill",
        "skl": ["n_weaver_2"],
        "cxn": [
            "weaver_skill_n0",
            "weaver_skill_n1",
            "weaver_skill_n3",
            "hardtech_skill_n0",
        ],
    }
    weaver_skill_n3: dict = {
        "name": "weaver_4_skill_slot",
        "category": "skill",
        "skl": ["n_weaver_3"],
        "cxn": [
            "weaver_skill_n0",
            "weaver_skill_n2",
            "weaver_skill_n4",
            "hacking_skill_n0",
        ],
    }
    weaver_skill_n4: dict = {
        "name": "weaver_5_skill_slot",
        "category": "skill",
        "skl": ["n_weaver_4"],
        "cxn": [
            "weaver_skill_n0",
            "weaver_skill_n3",
            "weaver_skill_n5",
        ],
    }
    weaver_skill_n5: dict = {
        "name": "weaver_6_skill_slot",
        "category": "skill",
        "skl": ["n_weaver_5"],
        "cxn": [
            "weaver_skill_n0",
            "weaver_skill_n4",
            "weaver_skill_n6",
        ],
    }
    weaver_skill_n6: dict = {
        "name": "weaver_7_skill_slot",
        "category": "skill",
        "skl": ["n_weaver_6"],
        "cxn": [
            "weaver_skill_n0",
            "weaver_skill_n5",
            "weaver_skill_n1",
            "weaver_trait_n0",
        ],
    }
    weaver_trait_n0: dict = {
        "name": "weaver_trait_slot",
        "category": "trait",
        "type": ["beh", "nar", "pas"],
        "extra": ["veh"],
        "cxn": ["weaver_skill_n6"],
    }
    medic_skill_n0: dict = {
        "name": "medic_1_skill_slot",
        "category": "skill",
        "skl": ["n_medic_0", "n_medic_limit_0"],
        "cxn": ["weaver_skill_n1", "medic_skill_n1", "medic_edge_n0"],
    }
    medic_skill_n1: dict = {
        "name": "medic_2_skill_slot",
        "category": "skill",
        "skl": ["n_medic_1", "n_medic_limit_1"],
        "cxn": ["medic_skill_n0", "medic_skill_n2"],
    }
    medic_skill_n2: dict = {
        "name": "medic_3_skill_slot",
        "category": "skill",
        "skl": ["n_medic_2", "n_medic_limit_2"],
        "cxn": ["medic_skill_n1", "smx"],
    }
    medic_edge_n0: dict = {
        "name": "medic_edge_slot",
        "category": "edge",
        "type": ["ssw", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["medic_skill_n0"],
    }
    hardtech_skill_n0: dict = {
        "name": "hardtech_1_skill_slot",
        "category": "skill",
        "skl": ["n_hardtech_0", "n_hardtech_limit_0"],
        "cxn": ["weaver_skill_n2", "hardtech_skill_n1", "hardtech_edge_n0"],
    }
    hardtech_skill_n1: dict = {
        "name": "hardtech_2_skill_slot",
        "category": "skill",
        "skl": ["n_hardtech_1", "n_hardtech_limit_1"],
        "cxn": ["hardtech_skill_n0", "hardtech_skill_n2"],
    }
    hardtech_skill_n2: dict = {
        "name": "hardtech_3_skill_slot",
        "category": "skill",
        "skl": ["n_hardtech_2", "n_hardtech_limit_2"],
        "cxn": ["hardtech_skill_n1", "smx"],
    }
    hardtech_edge_n0: dict = {
        "name": "hardtech_edge_slot",
        "category": "edge",
        "type": ["ssw", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["hardtech_skill_n0"],
    }
    hacking_skill_n0: dict = {
        "name": "hacking_1_skill_slot",
        "category": "skill",
        "skl": ["n_hacking_0", "n_hacking_limit_0"],
        "cxn": ["weaver_skill_n3", "hacking_skill_n1", "hacking_edge_n0"],
    }
    hacking_skill_n1: dict = {
        "name": "hacking_2_skill_slot",
        "category": "skill",
        "skl": ["n_hacking_1", "n_hacking_limit_1"],
        "cxn": ["hacking_skill_n0", "hacking_skill_n2"],
    }
    hacking_skill_n2: dict = {
        "name": "hacking_3_skill_slot",
        "category": "skill",
        "skl": ["n_hacking_2", "n_hacking_limit_2"],
        "cxn": ["hacking_skill_n1", "smx"],
    }
    hacking_edge_n0: dict = {
        "name": "hacking_edge_slot",
        "category": "edge",
        "type": ["ssw", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["hacking_skill_n0"],
    }

    # RESOURCES (NETWORK/INFLUENCE) SKILL
    resources_skill_n0: dict = {
        "name": "resources_1_skill_slot",
        "category": "skill",
        "skl": ["n_resources_0"],
        "cxn": [
            "entry_node",
            "resources_skill_n1",
            "resources_skill_n2",
            "resources_skill_n3",
            "resources_skill_n4",
            "resources_skill_n5",
            "resources_skill_n6",
        ],
    }
    resources_skill_n1: dict = {
        "name": "resources_2_skill_slot",
        "category": "skill",
        "skl": ["n_resources_1"],
        "cxn": [
            "resources_skill_n0",
            "resources_skill_n6",
            "resources_skill_n2",
            "network_skill_n0",
        ],
    }
    resources_skill_n2: dict = {
        "name": "resources_3_skill_slot",
        "category": "skill",
        "skl": ["n_resources_2"],
        "cxn": [
            "resources_skill_n0",
            "resources_skill_n1",
            "resources_skill_n3",
            "influence_skill_n0",
        ],
    }
    resources_skill_n3: dict = {
        "name": "resources_4_skill_slot",
        "category": "skill",
        "skl": ["n_resources_3"],
        "cxn": [
            "resources_skill_n0",
            "resources_skill_n2",
            "resources_skill_n4",
            "resources_op_n0",
        ],
    }
    resources_skill_n4: dict = {
        "name": "resources_5_skill_slot",
        "category": "skill",
        "skl": ["n_resources_4"],
        "cxn": [
            "resources_skill_n0",
            "resources_skill_n3",
            "resources_skill_n5",
        ],
    }
    resources_skill_n5: dict = {
        "name": "resources_6_skill_slot",
        "category": "skill",
        "skl": ["n_resources_5"],
        "cxn": [
            "resources_skill_n0",
            "resources_skill_n4",
            "resources_skill_n6",
        ],
    }
    resources_skill_n6: dict = {
        "name": "resources_7_skill_slot",
        "category": "skill",
        "skl": ["n_resources_6"],
        "cxn": [
            "resources_skill_n0",
            "resources_skill_n5",
            "resources_skill_n1",
        ],
    }
    resources_op_n0: dict = {
        "name": "resources_opportunity_1_slot",
        "category": "opportunity",
        "opp": ["n_resources_op_0"],
        "cxn": ["resources_skill_n3", "resources_op_n1"],
    }
    resources_op_n1: dict = {
        "name": "resources_opportunity_2_slot",
        "category": "opportunity",
        "opp": ["n_resources_op_1"],
        "cxn": ["resources_op_n0", "resources_op_n2"],
    }
    resources_op_n2: dict = {
        "name": "resources_opportunity_3_slot",
        "category": "opportunity",
        "opp": ["n_resources_op_2"],
        "cxn": ["resources_op_n1", "resources_op_n3"],
    }
    resources_op_n3: dict = {
        "name": "resources_opportunity_4_slot",
        "category": "opportunity",
        "opp": ["n_resources_op_3"],
        "cxn": ["resources_op_n2"],
    }
    network_skill_n0: dict = {
        "name": "network_1_skill_slot",
        "category": "skill",
        "skl": ["n_network_0", "n_network_limit_0"],
        "cxn": ["resources_skill_n1", "network_skill_n1", "network_edge_n0"],
    }
    network_skill_n1: dict = {
        "name": "network_2_skill_slot",
        "category": "skill",
        "skl": ["n_network_1", "n_network_limit_1"],
        "cxn": ["network_skill_n0", "network_skill_n2"],
    }
    network_skill_n2: dict = {
        "name": "network_3_skill_slot",
        "category": "skill",
        "skl": ["n_network_2", "n_network_limit_2"],
        "cxn": ["network_skill_n1", "smx"],
    }
    network_edge_n0: dict = {
        "name": "network_edge_slot",
        "category": "edge",
        "type": ["rmv", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["network_skill_n0"],
    }
    influence_skill_n0: dict = {
        "name": "influence_1_skill_slot",
        "category": "skill",
        "skl": ["n_influence_0", "n_influence_limit_0"],
        "cxn": ["resources_skill_n2", "influence_skill_n1", "influence_edge_n0"],
    }
    influence_skill_n1: dict = {
        "name": "influence_2_skill_slot",
        "category": "skill",
        "skl": ["n_influence_1", "n_influence_limit_1"],
        "cxn": ["influence_skill_n0", "influence_skill_n2"],
    }
    influence_skill_n2: dict = {
        "name": "influence_3_skill_slot",
        "category": "skill",
        "skl": ["n_influence_2", "n_influence_limit_2"],
        "cxn": ["influence_skill_n1", "smx"],
    }
    influence_edge_n0: dict = {
        "name": "influence_edge_slot",
        "category": "edge",
        "type": ["rmv", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["influence_skill_n0"],
    }

    # MOUTH (PERSUADE/LEADERSHIP/INTIMIDATE) SKILL
    mouth_skill_n0: dict = {
        "name": "mouth_1_skill_slot",
        "category": "skill",
        "skl": ["n_mouth_0"],
        "cxn": [
            "entry_node",
            "mouth_skill_n1",
            "mouth_skill_n2",
            "mouth_skill_n3",
            "mouth_skill_n4",
            "mouth_skill_n5",
            "mouth_skill_n6",
        ],
    }
    mouth_skill_n1: dict = {
        "name": "mouth_2_skill_slot",
        "category": "skill",
        "skl": ["n_mouth_1"],
        "cxn": [
            "mouth_skill_n0",
            "mouth_skill_n6",
            "mouth_skill_n2",
            "leadership_skill_n0",
        ],
    }
    mouth_skill_n2: dict = {
        "name": "mouth_3_skill_slot",
        "category": "skill",
        "skl": ["n_mouth_2"],
        "cxn": [
            "mouth_skill_n0",
            "mouth_skill_n1",
            "mouth_skill_n3",
            "persuade_skill_n0",
        ],
    }
    mouth_skill_n3: dict = {
        "name": "mouth_4_skill_slot",
        "category": "skill",
        "skl": ["n_mouth_3"],
        "cxn": [
            "mouth_skill_n0",
            "mouth_skill_n2",
            "mouth_skill_n4",
            "intimidate_skill_n0",
        ],
    }
    mouth_skill_n4: dict = {
        "name": "mouth_5_skill_slot",
        "category": "skill",
        "skl": ["n_mouth_4"],
        "cxn": [
            "mouth_skill_n0",
            "mouth_skill_n3",
            "mouth_skill_n5",
        ],
    }
    mouth_skill_n5: dict = {
        "name": "mouth_6_skill_slot",
        "category": "skill",
        "skl": ["n_mouth_5"],
        "cxn": [
            "mouth_skill_n0",
            "mouth_skill_n4",
            "mouth_skill_n6",
        ],
    }
    mouth_skill_n6: dict = {
        "name": "mouth_7_skill_slot",
        "category": "skill",
        "skl": ["n_mouth_6"],
        "cxn": ["mouth_skill_n0", "mouth_skill_n5", "mouth_skill_n1", "mouth_trait_n0"],
    }
    mouth_trait_n0: dict = {
        "name": "mouth_trait_slot",
        "category": "trait",
        "type": ["beh", "nar", "pas"],
        "extra": ["veh"],
        "cxn": ["mouth_skill_n6"],
    }
    leadership_skill_n0: dict = {
        "name": "leadership_1_skill_slot",
        "category": "skill",
        "skl": ["n_leadership_0", "n_leadership_limit_0"],
        "cxn": ["mouth_skill_n1", "leadership_skill_n1", "leadership_edge_n0"],
    }
    leadership_skill_n1: dict = {
        "name": "leadership_2_skill_slot",
        "category": "skill",
        "skl": ["n_leadership_1", "n_leadership_limit_1"],
        "cxn": ["leadership_skill_n0", "leadership_skill_n2"],
    }
    leadership_skill_n2: dict = {
        "name": "leadership_3_skill_slot",
        "category": "skill",
        "skl": ["n_leadership_2", "n_leadership_limit_2"],
        "cxn": ["leadership_skill_n1", "smx"],
    }
    leadership_edge_n0: dict = {
        "name": "leadership_edge_slot",
        "category": "edge",
        "type": ["rmv", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["leadership_skill_n0"],
    }
    persuade_skill_n0: dict = {
        "name": "persuade_1_skill_slot",
        "category": "skill",
        "skl": ["n_persuade_0", "n_persuade_limit_0"],
        "cxn": ["mouth_skill_n2", "persuade_skill_n1", "persuade_edge_n0"],
    }
    persuade_skill_n1: dict = {
        "name": "persuade_2_skill_slot",
        "category": "skill",
        "skl": ["n_persuade_1", "n_persuade_limit_1"],
        "cxn": ["persuade_skill_n0", "persuade_skill_n2"],
    }
    persuade_skill_n2: dict = {
        "name": "persuade_3_skill_slot",
        "category": "skill",
        "skl": ["n_persuade_2", "n_persuade_limit_2"],
        "cxn": ["persuade_skill_n1", "smx"],
    }
    persuade_edge_n0: dict = {
        "name": "persuade_edge_slot",
        "category": "edge",
        "type": ["rmv", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["persuade_skill_n0"],
    }
    intimidate_skill_n0: dict = {
        "name": "intimidate_1_skill_slot",
        "category": "skill",
        "skl": ["n_intimidate_0", "n_intimidate_limit_0"],
        "cxn": ["mouth_skill_n3", "intimidate_skill_n0", "intimidate_edge_n0"],
    }
    intimidate_skill_n1: dict = {
        "name": "intimidate_2_skill_slot",
        "category": "skill",
        "skl": ["n_intimidate_1", "n_intimidate_limit_1"],
        "cxn": ["intimidate_skill_n0", "intimidate_skill_n2"],
    }
    intimidate_skill_n2: dict = {
        "name": "intimidate_3_skill_slot",
        "category": "skill",
        "skl": ["n_intimidate_2", "n_intimidate_limit_2"],
        "cxn": ["intimidate_skill_n1", "smx"],
    }
    intimidate_edge_n0: dict = {
        "name": "intimidate_edge_slot",
        "category": "edge",
        "type": ["rmv", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["intimidate_skill_n0"],
    }

    # VAPOUR SKILL
    vapour_skill_n0: dict = {
        "name": "vapour_1_skill_slot",
        "category": "skill",
        "skl": ["n_vapour_0"],
        "cxn": [
            "entry_node",
            "vapour_skill_n1",
            "vapour_skill_n2",
            "vapour_skill_n3",
            "vapour_skill_n4",
            "vapour_skill_n5",
            "vapour_skill_n6",
        ],
    }
    vapour_skill_n1: dict = {
        "name": "vapour_2_skill_slot",
        "category": "skill",
        "skl": ["n_vapour_1"],
        "cxn": [
            "vapour_skill_n0",
            "vapour_skill_n6",
            "vapour_skill_n2",
            "groundcraft_skill_n0",
        ],
    }
    vapour_skill_n2: dict = {
        "name": "vapour_3_skill_slot",
        "category": "skill",
        "skl": ["n_vapour_2"],
        "cxn": [
            "vapour_skill_n0",
            "vapour_skill_n1",
            "vapour_skill_n3",
            "spacecraft_skill_n0",
        ],
    }
    vapour_skill_n3: dict = {
        "name": "vapour_4_skill_slot",
        "category": "skill",
        "skl": ["n_vapour_3"],
        "cxn": [
            "vapour_skill_n0",
            "vapour_skill_n2",
            "vapour_skill_n4",
            "aircraft_skill_n0",
        ],
    }
    vapour_skill_n4: dict = {
        "name": "vapour_5_skill_slot",
        "category": "skill",
        "skl": ["n_vapour_4"],
        "cxn": [
            "vapour_skill_n0",
            "vapour_skill_n3",
            "vapour_skill_n5",
        ],
    }
    vapour_skill_n5: dict = {
        "name": "vapour_6_skill_slot",
        "category": "skill",
        "skl": ["n_vapour_5"],
        "cxn": [
            "vapour_skill_n0",
            "vapour_skill_n4",
            "vapour_skill_n6",
        ],
    }
    vapour_skill_n6: dict = {
        "name": "vapour_7_skill_slot",
        "category": "skill",
        "skl": ["n_vapour_6"],
        "cxn": [
            "vapour_skill_n0",
            "vapour_skill_n5",
            "vapour_skill_n1",
            "vapour_trait_n0",
        ],
    }
    vapour_trait_n0: dict = {
        "name": "vapour_trait_slot",
        "category": "trait",
        "type": ["beh", "nar", "pas"],
        "extra": ["veh"],
        "cxn": ["vapour_skill_n6"],
    }
    groundcraft_skill_n0: dict = {
        "name": "groundcraft_1_skill_slot",
        "category": "skill",
        "skl": ["n_groundcraft_0", "n_groundcraft_limit_0"],
        "cxn": ["vapour_skill_n1", "groundcraft_skill_n1", "groundcraft_edge_n0"],
    }
    groundcraft_skill_n1: dict = {
        "name": "groundcraft_2_skill_slot",
        "category": "skill",
        "skl": ["n_groundcraft_1", "n_groundcraft_limit_1"],
        "cxn": ["groundcraft_skill_n0", "groundcraft_skill_n2"],
    }
    groundcraft_skill_n2: dict = {
        "name": "groundcraft_3_skill_slot",
        "category": "skill",
        "skl": ["n_groundcraft_2", "n_groundcraft_limit_2"],
        "cxn": ["groundcraft_skill_n1", "smx"],
    }
    groundcraft_edge_n0: dict = {
        "name": "groundcraft_edge_slot",
        "category": "edge",
        "type": ["rmv", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["groundcraft_skill_n0"],
    }
    spacecraft_skill_n0: dict = {
        "name": "spacecraft_1_skill_slot",
        "category": "skill",
        "skl": ["n_spacecraft_0", "n_spacecraft_limit_0"],
        "cxn": ["vapour_skill_n2", "spacecraft_skill_n1", "spacecraft_edge_n0"],
    }
    spacecraft_skill_n1: dict = {
        "name": "spacecraft_2_skill_slot",
        "category": "skill",
        "skl": ["n_spacecraft_1", "n_spacecraft_limit_1"],
        "cxn": ["spacecraft_skill_n0", "spacecraft_skill_n2"],
    }
    spacecraft_skill_n2: dict = {
        "name": "spacecraft_3_skill_slot",
        "category": "skill",
        "skl": ["n_spacecraft_2", "n_spacecraft_limit_2"],
        "cxn": ["spacecraft_skill_n1", "smx"],
    }
    spacecraft_edge_n0: dict = {
        "name": "spacecraft_edge_slot",
        "category": "edge",
        "type": ["rmv", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["spacecraft_skill_n0"],
    }
    aircraft_skill_n0: dict = {
        "name": "aircraft_1_skill_slot",
        "category": "skill",
        "skl": ["n_aircraft_0", "n_aircraft_limit_0"],
        "cxn": ["vapour_skill_n3", "aircraft_skill_n1", "aircraft_edge_n0"],
    }
    aircraft_skill_n1: dict = {
        "name": "aircraft_2_skill_slot",
        "category": "skill",
        "skl": ["n_aircraft_1", "n_aircraft_limit_1"],
        "cxn": ["aircraft_skill_n0", "aircraft_skill_n2"],
    }
    aircraft_skill_n2: dict = {
        "name": "aircraft_3_skill_slot",
        "category": "skill",
        "skl": ["n_aircraft_2", "n_aircraft_limit_2"],
        "cxn": ["aircraft_skill_n1", "smx"],
    }
    aircraft_edge_n0: dict = {
        "name": "aircraft_edge_slot",
        "category": "edge",
        "type": ["rmv", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["aircraft_skill_n0"],
    }

    # WYLD
    wyld_skill_n0: dict = {
        "name": "wyld_1_skill_slot",
        "category": "skill",
        "skl": ["n_wyld_0"],
        "cxn": [
            "entry_node",
            "wyld_skill_n1",
            "wyld_skill_n2",
            "wyld_skill_n3",
            "wyld_skill_n4",
            "wyld_skill_n5",
            "wyld_skill_n6",
        ],
    }
    wyld_skill_n1: dict = {
        "name": "wyld_2_skill_slot",
        "category": "skill",
        "skl": ["n_wyld_1"],
        "cxn": [
            "wyld_skill_n0",
            "wyld_skill_n6",
            "wyld_skill_n1",
            "sense_skill_n0",
        ],
    }
    wyld_skill_n2: dict = {
        "name": "wyld_3_skill_slot",
        "category": "skill",
        "skl": ["n_wyld_2"],
        "cxn": [
            "wyld_skill_n0",
            "wyld_skill_n1",
            "wyld_skill_n3",
            "resistance_skill_n0",
        ],
    }
    wyld_skill_n3: dict = {
        "name": "wyld_4_skill_slot",
        "category": "skill",
        "skl": ["n_wyld_3"],
        "cxn": [
            "wyld_skill_n0",
            "wyld_skill_n2",
            "wyld_skill_n4",
            "wyld_op_n0",
        ],
    }
    wyld_skill_n4: dict = {
        "name": "wyld_5_skill_slot",
        "category": "skill",
        "skl": ["n_wyld_4"],
        "cxn": [
            "wyld_skill_n0",
            "wyld_skill_n3",
            "wyld_skill_n5",
        ],
    }
    wyld_skill_n5: dict = {
        "name": "wyld_6_skill_slot",
        "category": "skill",
        "skl": ["n_wyld_5"],
        "cxn": [
            "wyld_skill_n0",
            "wyld_skill_n4",
            "wyld_skill_n6",
        ],
    }
    wyld_skill_n6: dict = {
        "name": "wyld_7_skill_slot",
        "category": "skill",
        "skl": ["n_wyld_6"],
        "cxn": [
            "wyld_skill_n0",
            "wyld_skill_n5",
            "wyld_skill_n1",
        ],
    }
    wyld_op_n0: dict = {
        "name": "wyld_opportunity_1_slot",
        "category": "opportunity",
        "opp": ["n_wyld_op_0"],
        "cxn": ["wyld_skill_n3", "wyld_op_n1"],
    }
    wyld_op_n1: dict = {
        "name": "wyld_opportunity_2_slot",
        "category": "opportunity",
        "opp": ["n_wyld_op_1"],
        "cxn": ["wyld_op_n0", "wyld_op_n2"],
    }
    wyld_op_n2: dict = {
        "name": "wyld_opportunity_3_slot",
        "category": "opportunity",
        "opp": ["n_wyld_op_2"],
        "cxn": ["wyld_op_n1", "wyld_op_n3"],
    }
    wyld_op_n3: dict = {
        "name": "wyld_opportunity_4_slot",
        "category": "opportunity",
        "opp": ["n_wyld_op_3"],
        "cxn": ["wyld_op_n2"],
    }
    sense_skill_n0: dict = {
        "name": "sense_1_skill_slot",
        "category": "skill",
        "skl": ["n_sense_0", "n_sense_limit_0"],
        "cxn": ["wyld_skill_n1", "sense_skill_n1", "sense_edge_n0"],
    }
    sense_skill_n1: dict = {
        "name": "sense_2_skill_slot",
        "category": "skill",
        "skl": ["n_sense_1", "n_sense_limit_1"],
        "cxn": ["sense_skill_n0", "sense_skill_n2"],
    }
    sense_skill_n2: dict = {
        "name": "sense_3_skill_slot",
        "category": "skill",
        "skl": ["n_sense_2", "n_sense_limit_2"],
        "cxn": ["sense_skill_n1", "smx"],
    }
    sense_edge_n0: dict = {
        "name": "sense_edge_slot",
        "category": "edge",
        "type": ["wex", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["sense_skill_n0"],
    }
    resistance_skill_n0: dict = {
        "name": "resistance_1_skill_slot",
        "category": "skill",
        "skl": ["n_resistance_0", "n_resistance_limit_0"],
        "cxn": ["wyld_skill_n2", "resistance_skill_n1", "resistance_edge_n0"],
    }
    resistance_skill_n1: dict = {
        "name": "resistance_2_skill_slot",
        "category": "skill",
        "skl": ["n_resistance_1", "n_resistance_limit_1"],
        "cxn": ["resistance_skill_n0", "resistance_skill_n2"],
    }
    resistance_skill_n2: dict = {
        "name": "resistance_3_skill_slot",
        "category": "skill",
        "skl": ["n_resistance_2", "n_resistance_limit_2"],
        "cxn": ["resistance_skill_n1", "smx"],
    }
    resistance_edge_n0: dict = {
        "name": "resistance_edge_slot",
        "category": "edge",
        "type": ["wex", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["resistance_skill_n0"],
    }

    # ECHO1
    echo1_name_n0: dict = {
        "name": "first_echo_power_slot",
        "category": "name",
        "type": ["ech"],
        "cxn": ["entry_node"],
        "req": [
            "e_echo_power_aerokinesis",
            "e_echo_power_pyrokinesis",
            "e_echo_power_electrokinesis",
            "e_echo_power_telepathy",
            "e_echo_power_msp",
            "e_echo_power_ethereal_form",
            "e_echo_power_teleportation",
        ],
    }
    echo1_skill_n0: dict = {
        "name": "first_echo_1_skill_slot",
        "category": "skill",
        "skl": ["n_echo1_0"],
        "cxn": [
            "echo1_name_n0",
            "echo1_skill_n1",
            "echo1_skill_n2",
            "echo1_skill_n3",
            "echo1_skill_n4",
            "echo1_skill_n5",
            "echo1_skill_n6",
        ],
    }
    echo1_skill_n1: dict = {
        "name": "first_echo_2_skill_slot",
        "category": "skill",
        "skl": ["n_echo1_1"],
        "cxn": [
            "echo1_skill_n0",
            "echo1_skill_n6",
            "echo1_skill_n2",
            "attack1_skill_n0",
        ],
    }
    echo1_skill_n2: dict = {
        "name": "first_echo_3_skill_slot",
        "category": "skill",
        "skl": ["n_echo1_2"],
        "cxn": [
            "echo1_skill_n0",
            "echo1_skill_n1",
            "echo1_skill_n3",
            "nature1_skill_n0",
        ],
    }
    echo1_skill_n3: dict = {
        "name": "first_echo_4_skill_slot",
        "category": "skill",
        "skl": ["n_echo1_3"],
        "cxn": [
            "echo1_skill_n0",
            "echo1_skill_n2",
            "echo1_skill_n4",
            "manipulation1_skill_n0",
        ],
    }
    echo1_skill_n4: dict = {
        "name": "first_echo_5_skill_slot",
        "category": "skill",
        "skl": ["n_echo1_4"],
        "cxn": [
            "echo1_skill_n0",
            "echo1_skill_n3",
            "echo1_skill_n5",
        ],
    }
    echo1_skill_n5: dict = {
        "name": "first_echo_6_skill_slot",
        "category": "skill",
        "skl": ["n_echo1_5"],
        "cxn": [
            "echo1_skill_n0",
            "echo1_skill_n4",
            "echo1_skill_n6",
        ],
    }
    echo1_skill_n6: dict = {
        "name": "first_echo_7_skill_slot",
        "category": "skill",
        "skl": ["n_echo1_6"],
        "cxn": [
            "echo1_skill_n0",
            "echo1_skill_n5",
            "echo1_skill_n1",
            "echo1_trait_n0",
        ],
    }
    echo1_trait_n0: dict = {
        "name": "first_echo_trait_slot",
        "category": "trait",
        "type": ["beh", "nar", "pas"],
        "extra": ["veh"],
        "cxn": ["echo1_skill_n6"],
    }
    attack1_skill_n0: dict = {
        "name": "first_echo_attack_1_skill_slot",
        "category": "skill",
        "skl": ["n_attack1_0", "n_attack1_limit_0"],
        "cxn": ["echo1_skill_n1", "attack1_skill_n1", "attack1_edge_n0"],
    }
    attack1_skill_n1: dict = {
        "name": "first_echo_attack_2_skill_slot",
        "category": "skill",
        "skl": ["n_attack1_1", "n_attack1_limit_1"],
        "cxn": ["attack1_skill_n0", "attack1_skill_n2"],
    }
    attack1_skill_n2: dict = {
        "name": "first_echo_attack_3_skill_slot",
        "category": "skill",
        "skl": ["n_attack1_2", "n_attack1_limit_2"],
        "cxn": ["attack1_skill_n1", "smx"],
    }
    attack1_edge_n0: dict = {
        "name": "first_echo_attack_edge_slot",
        "category": "edge",
        "type": ["wex", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["attack1_skill_n0"],
    }
    nature1_skill_n0: dict = {
        "name": "first_echo_nature_1_skill_slot",
        "category": "skill",
        "skl": ["n_nature1_0", "n_nature1_limit_0"],
        "cxn": ["echo1_skill_n2", "nature1_skill_n1", "nature1_edge_n0"],
    }
    nature1_skill_n1: dict = {
        "name": "first_echo_nature_2_skill_slot",
        "category": "skill",
        "skl": ["n_nature1_1", "n_nature1_limit_1"],
        "cxn": ["nature1_skill_n0", "nature1_skill_n2"],
    }
    nature1_skill_n2: dict = {
        "name": "first_echo_nature_3_skill_slot",
        "category": "skill",
        "skl": ["n_nature1_2", "n_nature1_limit_2"],
        "cxn": ["nature1_skill_n1", "smx"],
    }
    nature1_edge_n0: dict = {
        "name": "first_echo_nature_edge_slot",
        "category": "edge",
        "type": ["wex", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["nature1_skill_n0"],
    }
    manipulation1_skill_n0: dict = {
        "name": "first_echo_manipulation_1_skill_slot",
        "category": "skill",
        "skl": ["n_manipulation1_0", "n_manipulation1_limit_0"],
        "cxn": ["echo1_skill_n3", "manipulation1_skill_n1", "manipulation1_edge_n0"],
    }
    manipulation1_skill_n1: dict = {
        "name": "first_echo_manipulation_1_skill_slot",
        "category": "skill",
        "skl": ["n_manipulation1_1", "n_manipulation1_limit_1"],
        "cxn": ["manipulation1_skill_n0", "manipulation1_skill_n2"],
    }
    manipulation1_skill_n2: dict = {
        "name": "first_echo_manipulation_3_skill_slot",
        "category": "skill",
        "skl": ["n_manipulation1_2", "n_manipulation1_limit_2"],
        "cxn": ["manipulation1_skill_n1", "smx"],
    }
    manipulation1_edge_n0: dict = {
        "name": "first_echo_manipulation_edge_slot",
        "category": "edge",
        "type": ["wex", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["manipulation1_skill_n0"],
    }

    # ECHO2
    echo2_name_n0: dict = {
        "name": "second_echo_power_slot",
        "category": "name",
        "type": ["ech"],
        "cxn": ["entry_node"],
        "req": [
            "e_echo_power_aerokinesis",
            "e_echo_power_pyrokinesis",
            "e_echo_power_electrokinesis",
            "e_echo_power_telepathy",
            "e_echo_power_msp",
            "e_echo_power_ethereal_form",
            "e_echo_power_teleportation",
        ],
    }
    echo2_skill_n0: dict = {
        "name": "second_echo_1_skill_slot",
        "category": "skill",
        "skl": ["n_echo2_0"],
        "cxn": [
            "echo2_name_n0",
            "echo2_skill_n1",
            "echo2_skill_n2",
            "echo2_skill_n3",
            "echo2_skill_n4",
            "echo2_skill_n5",
            "echo2_skill_n6",
        ],
    }
    echo2_skill_n1: dict = {
        "name": "second_echo_2_skill_slot",
        "category": "skill",
        "skl": ["n_echo2_1"],
        "cxn": [
            "echo2_skill_n0",
            "echo2_skill_n6",
            "echo2_skill_n2",
            "attack2_skill_n0",
        ],
    }
    echo2_skill_n2: dict = {
        "name": "second_echo_3_skill_slot",
        "category": "skill",
        "skl": ["n_echo2_2"],
        "cxn": [
            "echo2_skill_n0",
            "echo2_skill_n1",
            "echo2_skill_n3",
            "nature2_skill_n0",
        ],
    }
    echo2_skill_n3: dict = {
        "name": "second_echo_4_skill_slot",
        "category": "skill",
        "skl": ["n_echo2_3"],
        "cxn": [
            "echo2_skill_n0",
            "echo2_skill_n2",
            "echo2_skill_n4",
            "manipulation2_skill_n0",
        ],
    }
    echo2_skill_n4: dict = {
        "name": "second_echo_5_skill_slot",
        "category": "skill",
        "skl": ["n_echo2_4"],
        "cxn": [
            "echo2_skill_n0",
            "echo2_skill_n3",
            "echo2_skill_n5",
        ],
    }
    echo2_skill_n5: dict = {
        "name": "second_echo_6_skill_slot",
        "category": "skill",
        "skl": ["n_echo2_5"],
        "cxn": [
            "echo2_skill_n0",
            "echo2_skill_n4",
            "echo2_skill_n6",
        ],
    }
    echo2_skill_n6: dict = {
        "name": "second_echo_7_skill_slot",
        "category": "skill",
        "skl": ["n_echo2_6"],
        "cxn": [
            "echo2_skill_n0",
            "echo2_skill_n5",
            "echo2_skill_n1",
            "echo2_trait_n0",
        ],
    }
    echo2_trait_n0: dict = {
        "name": "second_echo_trait_slot",
        "category": "trait",
        "type": ["beh", "nar", "pas"],
        "extra": ["veh"],
        "cxn": ["echo2_skill_n6"],
    }
    attack2_skill_n0: dict = {
        "name": "second_echo_attack_1_skill_slot",
        "category": "skill",
        "skl": ["n_attack2_0", "n_attack2_limit_0"],
        "cxn": ["echo2_skill_n1", "attack2_skill_n1", "attack2_edge_n0"],
    }
    attack2_skill_n1: dict = {
        "name": "second_echo_attack_2_skill_slot",
        "category": "skill",
        "skl": ["n_attack2_1", "n_attack2_limit_1"],
        "cxn": ["attack2_skill_n0", "attack2_skill_n2"],
    }
    attack2_skill_n2: dict = {
        "name": "second_echo_attack_3_skill_slot",
        "category": "skill",
        "skl": ["n_attack2_2", "n_attack2_limit_2"],
        "cxn": ["attack2_skill_n1", "smx"],
    }
    attack2_edge_n0: dict = {
        "name": "second_echo_attack_edge_slot",
        "category": "edge",
        "type": ["wex", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["attack2_skill_n0"],
    }
    nature2_skill_n0: dict = {
        "name": "second_echo_nature_1_skill_slot",
        "category": "skill",
        "skl": ["n_nature2_0", "n_nature2_limit_0"],
        "cxn": ["echo2_skill_n2", "nature2_skill_n1", "nature2_edge_n0"],
    }
    nature2_skill_n1: dict = {
        "name": "second_echo_nature_2_skill_slot",
        "category": "skill",
        "skl": ["n_nature2_1", "n_nature2_limit_1"],
        "cxn": ["nature2_skill_n0", "nature2_skill_n2"],
    }
    nature2_skill_n2: dict = {
        "name": "second_echo_nature_3_skill_slot",
        "category": "skill",
        "skl": ["n_nature2_2", "n_nature2_limit_2"],
        "cxn": ["nature2_skill_n1", "smx"],
    }
    nature2_edge_n0: dict = {
        "name": "second_echo_nature_edge_slot",
        "category": "edge",
        "type": ["wex", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["nature2_skill_n0"],
    }
    manipulation2_skill_n0: dict = {
        "name": "second_echo_manipulation_1_skill_slot",
        "category": "skill",
        "skl": ["n_manipulation2_0", "n_manipulation2_limit_0"],
        "cxn": ["echo2_skill_n3", "manipulation2_skill_n1", "manipulation2_edge_n0"],
    }
    manipulation2_skill_n1: dict = {
        "name": "second_echo_manipulation_1_skill_slot",
        "category": "skill",
        "skl": ["n_manipulation2_1", "n_manipulation2_limit_1"],
        "cxn": ["manipulation2_skill_n0", "manipulation2_skill_n2"],
    }
    manipulation2_skill_n2: dict = {
        "name": "second_echo_manipulation_3_skill_slot",
        "category": "skill",
        "skl": ["n_manipulation2_2", "n_manipulation2_limit_2"],
        "cxn": ["manipulation2_skill_n1", "smx"],
    }
    manipulation2_edge_n0: dict = {
        "name": "second_echo_manipulation_edge_slot",
        "category": "edge",
        "type": ["wex", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["manipulation2_skill_n0"],
    }

    # DIVINITY SKILL
    divinity_skill_n0: dict = {
        "name": "divinity_1_skill_slot",
        "category": "skill",
        "skl": ["n_divinity_0"],
        "cxn": [
            "entry_node",
            "divinity_skill_n1",
            "divinity_skill_n2",
            "divinity_skill_n3",
            "divinity_skill_n4",
            "divinity_skill_n5",
            "divinity_skill_n6",
        ],
    }
    divinity_skill_n1: dict = {
        "name": "divinity_2_skill_slot",
        "category": "skill",
        "skl": ["n_divinity_1"],
        "cxn": [
            "divinity_skill_n0",
            "divinity_skill_n6",
            "divinity_skill_n2",
            "invocation_skill_n0",
        ],
    }
    divinity_skill_n2: dict = {
        "name": "divinity_3_skill_slot",
        "category": "skill",
        "skl": ["n_divinity_2"],
        "cxn": [
            "divinity_skill_n0",
            "divinity_skill_n1",
            "divinity_skill_n3",
            "faith_skill_n0",
        ],
    }
    divinity_skill_n3: dict = {
        "name": "divinity_4_skill_slot",
        "category": "skill",
        "skl": ["n_divinity_3"],
        "cxn": [
            "divinity_skill_n0",
            "divinity_skill_n2",
            "divinity_skill_n4",
            "divinity_op_n0",
        ],
    }
    divinity_skill_n4: dict = {
        "name": "divinity_5_skill_slot",
        "category": "skill",
        "skl": ["n_divinity_4"],
        "cxn": [
            "divinity_skill_n0",
            "divinity_skill_n3",
            "divinity_skill_n5",
        ],
    }
    divinity_skill_n5: dict = {
        "name": "divinity_6_skill_slot",
        "category": "skill",
        "skl": ["n_divinity_5"],
        "cxn": [
            "divinity_skill_n0",
            "divinity_skill_n4",
            "divinity_skill_n6",
        ],
    }
    divinity_skill_n6: dict = {
        "name": "divinity_7_skill_slot",
        "category": "skill",
        "skl": ["n_divinity_6"],
        "cxn": [
            "divinity_skill_n0",
            "divinity_skill_n5",
            "divinity_skill_n1",
        ],
    }
    divinity_op_n0: dict = {
        "name": "divinity_opportunity_1_slot",
        "category": "opportunity",
        "opp": ["n_divinity_op_0"],
        "cxn": ["divinity_skill_n3", "divinity_op_n1"],
    }
    divinity_op_n1: dict = {
        "name": "divinity_opportunity_2_slot",
        "category": "opportunity",
        "opp": ["n_divinity_op_1"],
        "cxn": ["divinity_op_n0", "divinity_op_n2"],
    }
    divinity_op_n2: dict = {
        "name": "divinity_opportunity_3_slot",
        "category": "opportunity",
        "opp": ["n_divinity_op_2"],
        "cxn": ["divinity_op_n1", "divinity_op_n3"],
    }
    divinity_op_n3: dict = {
        "name": "divinity_opportunity_4_slot",
        "category": "opportunity",
        "opp": ["n_divinity_op_3"],
        "cxn": ["divinity_op_n3"],
    }
    invocation_skill_n0: dict = {
        "name": "invocation_1_skill_slot",
        "category": "skill",
        "skl": ["n_invocation_0", "n_invocation_limit_0"],
        "cxn": ["divinity_skill_n1", "invocation_skill_n1", "invocation_edge_n0"],
    }
    invocation_skill_n1: dict = {
        "name": "invocation_2_skill_slot",
        "category": "skill",
        "skl": ["n_invocation_1", "n_invocation_limit_1"],
        "cxn": ["invocation_skill_n0", "invocation_skill_n2"],
    }
    invocation_skill_n2: dict = {
        "name": "invocation_3_skill_slot",
        "category": "skill",
        "skl": ["n_invocation_2", "n_invocation_limit_2"],
        "cxn": ["invocation_skill_n1", "smx"],
    }
    invocation_edge_n0: dict = {
        "name": "invocation_edge_slot",
        "category": "edge",
        "type": ["dgx", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["invocation_skill_n0"],
    }
    faith_skill_n0: dict = {
        "name": "faith_1_skill_slot",
        "category": "skill",
        "skl": ["n_faith_0", "n_faith_limit_0"],
        "cxn": ["divinity_skill_n2", "faith_skill_n1", "faith_edge_n0"],
    }
    faith_skill_n1: dict = {
        "name": "faith_2_skill_slot",
        "category": "skill",
        "skl": ["n_faith_1", "n_faith_limit_1"],
        "cxn": ["faith_skill_n0", "faith_skill_n2"],
    }
    faith_skill_n2: dict = {
        "name": "faith_3_skill_slot",
        "category": "skill",
        "skl": ["n_faith_2", "n_faith_limit_2"],
        "cxn": ["faith_skill_n1", "smx"],
    }
    faith_edge_n0: dict = {
        "name": "faith_edge_slot",
        "category": "edge",
        "type": ["dgx", "uni"],
        "extra": ["gas", "mce", "all"],
        "cxn": ["faith_skill_n0"],
    }

    # SMX 1
    spec_mastery1_name_n0: dict = {
        "name": "first_spec_mastery_name_slot",
        "category": "name",
        "type": ["spc"],
        "cxn": ["smx"],
    }
    spec_mastery1_skill_n0: dict = {
        "name": "first_spec_mastery_1_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery1_0"],
        "cxn": [
            "spec_mastery1_name_n0",
            "spec_mastery1_skill_n1",
            "spec_mastery1_edge_n0",
        ],
    }
    spec_mastery1_skill_n1: dict = {
        "name": "first_spec_mastery_2_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery1_1"],
        "cxn": [
            "spec_mastery1_skill_n0",
            "spec_mastery1_skill_n2",
        ],
    }
    spec_mastery1_skill_n2: dict = {
        "name": "first_spec_mastery_3_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery1_2"],
        "cxn": [
            "spec_mastery1_skill_n1",
            "spec_mastery1_skill_n3",
            "spec_mastery1_edge_n1",
        ],
    }
    spec_mastery1_skill_n3: dict = {
        "name": "first_spec_mastery_4_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery1_3"],
        "cxn": [
            "spec_mastery1_skill_n2",
            "spec_mastery1_skill_n4",
        ],
    }
    spec_mastery1_skill_n4: dict = {
        "name": "first_spec_mastery_5_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery1_4"],
        "cxn": [
            "spec_mastery1_skill_n3",
            "spec_mastery1_skill_n5",
        ],
    }
    spec_mastery1_skill_n5: dict = {
        "name": "first_spec_mastery_6_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery1_5"],
        "cxn": ["spec_mastery1_skill_n4", "spec_mastery1_edge_n2"],
    }
    spec_mastery1_edge_n0: dict = {
        "name": "first_spec_mastery_edge_1_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": ["spec_mastery1_skill_n0"],
    }
    spec_mastery1_edge_n1: dict = {
        "name": "first_spec_mastery_edge_2_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": ["spec_mastery1_skill_n2"],
    }
    spec_mastery1_edge_n2: dict = {
        "name": "first_spec_mastery_edge_3_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": ["spec_mastery1_skill_n5"],
    }

    # SMX 2
    spec_mastery2_name_n0: dict = {
        "name": "second_spec_mastery_name_slot",
        "category": "name",
        "type": ["spc"],
        "cxn": ["smx"],
    }
    spec_mastery2_skill_n0: dict = {
        "name": "second_spec_mastery_1_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery2_0"],
        "cxn": [
            "spec_mastery2_name_n0",
            "spec_mastery2_skill_n1",
            "spec_mastery2_edge_n0",
        ],
    }
    spec_mastery2_skill_n1: dict = {
        "name": "second_spec_mastery_2_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery2_1"],
        "cxn": [
            "spec_mastery2_skill_n0",
            "spec_mastery2_skill_n2",
        ],
    }
    spec_mastery2_skill_n2: dict = {
        "name": "second_spec_mastery_3_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery2_2"],
        "cxn": [
            "spec_mastery2_skill_n1",
            "spec_mastery2_skill_n3",
            "spec_mastery2_edge_n1",
        ],
    }
    spec_mastery2_skill_n3: dict = {
        "name": "second_spec_mastery_4_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery2_3"],
        "cxn": [
            "spec_mastery2_skill_n2",
            "spec_mastery2_skill_n4",
        ],
    }
    spec_mastery2_skill_n4: dict = {
        "name": "second_spec_mastery_5_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery2_4"],
        "cxn": [
            "spec_mastery2_skill_n3",
            "spec_mastery2_skill_n5",
        ],
    }
    spec_mastery2_skill_n5: dict = {
        "name": "second_spec_mastery_6_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery2_5"],
        "cxn": ["spec_mastery2_skill_n4", "spec_mastery2_edge_n2"],
    }
    spec_mastery2_edge_n0: dict = {
        "name": "second_spec_mastery_edge_1_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": ["spec_mastery2_skill_n0"],
    }
    spec_mastery2_edge_n1: dict = {
        "name": "second_spec_mastery_edge_2_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": ["spec_mastery2_skill_n2"],
    }
    spec_mastery2_edge_n2: dict = {
        "name": "second_spec_mastery_edge_3_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": ["spec_mastery2_skill_n5"],
    }

    # SMX 3
    spec_mastery3_name_n0: dict = {
        "name": "third_spec_mastery_name_slot",
        "category": "name",
        "type": ["spc"],
        "cxn": ["smx"],
    }
    spec_mastery3_skill_n0: dict = {
        "name": "third_spec_mastery_1_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery3_0"],
        "cxn": [
            "spec_mastery3_name_n0",
            "spec_mastery3_skill_n1",
            "spec_mastery3_edge_n0",
        ],
    }
    spec_mastery3_skill_n1: dict = {
        "name": "third_spec_mastery_2_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery3_1"],
        "cxn": [
            "spec_mastery3_skill_n0",
            "spec_mastery3_skill_n2",
        ],
    }
    spec_mastery3_skill_n2: dict = {
        "name": "third_spec_mastery_3_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery3_2"],
        "cxn": [
            "spec_mastery3_skill_n1",
            "spec_mastery3_skill_n3",
            "spec_mastery3_edge_n1",
        ],
    }
    spec_mastery3_skill_n3: dict = {
        "name": "third_spec_mastery_4_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery3_3"],
        "cxn": [
            "spec_mastery3_skill_n2",
            "spec_mastery3_skill_n4",
        ],
    }
    spec_mastery3_skill_n4: dict = {
        "name": "third_spec_mastery_5_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery3_4"],
        "cxn": [
            "spec_mastery3_skill_n3",
            "spec_mastery3_skill_n5",
        ],
    }
    spec_mastery3_skill_n5: dict = {
        "name": "third_spec_mastery_6_skill_slot",
        "category": "skill",
        "skl": ["n_spec_mastery3_5"],
        "cxn": ["spec_mastery3_skill_n4", "spec_mastery3_edge_n2"],
    }
    spec_mastery3_edge_n0: dict = {
        "name": "third_spec_mastery_edge_1_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": ["spec_mastery3_skill_n0"],
    }
    spec_mastery3_edge_n1: dict = {
        "name": "third_spec_mastery_edge_2_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": ["spec_mastery3_skill_n2"],
    }
    spec_mastery3_edge_n2: dict = {
        "name": "third_spec_mastery_edge_3_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": ["spec_mastery3_skill_n5"],
    }

    # EARNED EDGES
    earned_edge_n0: dict = {
        "name": "earned_edge_1_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": [
            "entry_node",
            "earned_edge_n1",
        ],
    }
    earned_edge_n1: dict = {
        "name": "earned_edge_2_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": [
            "earned_edge_n0",
            "earned_edge_n2",
        ],
    }
    earned_edge_n2: dict = {
        "name": "earned_edge_3_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": [
            "earned_edge_n1",
            "earned_edge_n3",
        ],
    }
    earned_edge_n3: dict = {
        "name": "earned_edge_4_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": [
            "earned_edge_n2",
            "earned_edge_n4",
        ],
    }
    earned_edge_n4: dict = {
        "name": "earned_edge_5_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": ["earned_edge_n3"],
    }

    # EARNED TRAITS
    earned_trait_n0: dict = {
        "name": "earned_trait_1_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "veh"],
        "cxn": [
            "entry_node",
            "earned_trait_n1",
        ],
    }
    earned_trait_n1: dict = {
        "name": "earned_trait_2_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "veh"],
        "cxn": [
            "earned_trait_n0",
            "earned_trait_n2",
        ],
    }
    earned_trait_n2: dict = {
        "name": "earned_trait_3_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "veh"],
        "cxn": [
            "earned_trait_n1",
            "earned_trait_n3",
        ],
    }
    earned_trait_n3: dict = {
        "name": "earned_trait_4_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "veh"],
        "cxn": [
            "earned_trait_n2",
            "earned_trait_n4",
        ],
    }
    earned_trait_n4: dict = {
        "name": "earned_trait_5_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "veh"],
        "cxn": [
            "earned_trait_n3",
        ],
    }

    # TEAM EDGES
    team_edge_n0: dict = {
        "name": "team_edge_1_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "ode", "all"],
        "cxn": [
            "entry_node",
            "team_edge_n1",
        ],
    }
    team_edge_n1: dict = {
        "name": "team_edge_2_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "ode", "all"],
        "cxn": [
            "team_edge_n0",
            "team_edge_n2",
        ],
    }
    team_edge_n2: dict = {
        "name": "team_edge_3_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "ode", "all"],
        "cxn": [
            "team_edge_n1",
            "team_edge_n3",
        ],
    }
    team_edge_n3: dict = {
        "name": "team_edge_4_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "ode", "all"],
        "cxn": [
            "team_edge_n2",
            "team_edge_n4",
        ],
    }
    team_edge_n4: dict = {
        "name": "team_edge_5_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "ode", "all"],
        "cxn": [
            "team_edge_n3",
        ],
    }

    # TEAM TRAITS
    team_trait_n0: dict = {
        "name": "team_trait_1_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "odt"],
        "cxn": [
            "entry_node",
            "team_trait_n1",
        ],
    }
    team_trait_n1: dict = {
        "name": "team_trait_2_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "odt"],
        "cxn": [
            "team_trait_n0",
            "team_trait_n2",
        ],
    }
    team_trait_n2: dict = {
        "name": "team_trait_3_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "odt"],
        "cxn": [
            "team_trait_n1",
            "team_trait_n3",
        ],
    }
    team_trait_n3: dict = {
        "name": "team_trait_4_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "odt"],
        "cxn": [
            "team_trait_n2",
            "team_trait_n4",
        ],
    }
    team_trait_n4: dict = {
        "name": "team_trait_5_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "odt"],
        "cxn": [
            "team_trait_n3",
        ],
    }

    # TEMPORARY EDGES
    temporary_edge_n0: dict = {
        "name": "temporary_edge_1_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": [
            "entry_node",
            "temporary_edge_n1",
        ],
    }
    temporary_edge_n1: dict = {
        "name": "temporary_edge_2_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": [
            "temporary_edge_n0",
            "temporary_edge_n2",
        ],
    }
    temporary_edge_n2: dict = {
        "name": "temporary_edge_3_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": [
            "temporary_edge_n1",
            "temporary_edge_n3",
        ],
    }
    temporary_edge_n3: dict = {
        "name": "temporary_edge_4_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": [
            "temporary_edge_n2",
            "temporary_edge_n4",
        ],
    }
    temporary_edge_n4: dict = {
        "name": "temporary_edge_5_slot",
        "category": "edge",
        "extra": ["pkc", "ssw", "rmv", "wex", "dgx", "uni", "gas", "mce", "all"],
        "cxn": [
            "temporary_edge_n3",
        ],
    }

    # TEMP TRAITS
    temporary_trait_n0: dict = {
        "name": "temporary_trait_1_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "veh"],
        "cxn": [
            "entry_node",
            "temporary_trait_n1",
        ],
    }
    temporary_trait_n1: dict = {
        "name": "temporary_trait_2_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "veh"],
        "cxn": [
            "temporary_trait_n0",
            "temporary_trait_n2",
        ],
    }
    temporary_trait_n2: dict = {
        "name": "temporary_trait_3_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "veh"],
        "cxn": [
            "temporary_trait_n1",
            "temporary_trait_n3",
        ],
    }
    temporary_trait_n3: dict = {
        "name": "temporary_trait_4_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "veh"],
        "cxn": [
            "temporary_trait_n2",
            "temporary_trait_n4",
        ],
    }
    temporary_trait_n4: dict = {
        "name": "temporary_trait_5_slot",
        "category": "trait",
        "extra": ["beh", "nar", "pas", "veh"],
        "cxn": [
            "temporary_trait_n3",
        ],
    }

    # ENVIRONMENTAL TRAITS
    environmental_trait_n0: dict = {
        "name": "environmental_trait_1_slot",
        "category": "trait",
        "extra": ["env"],
        "cxn": [
            "entry_node",
            "environmental_trait_n1",
        ],
    }
    environmental_trait_n1: dict = {
        "name": "environmental_trait_2_slot",
        "category": "trait",
        "extra": ["env"],
        "cxn": [
            "environmental_trait_n0",
            "environmental_trait_n2",
        ],
    }
    environmental_trait_n2: dict = {
        "name": "environmental_trait_3_slot",
        "category": "trait",
        "extra": ["env"],
        "cxn": [
            "environmental_trait_n1",
            "environmental_trait_n3",
        ],
    }
    environmental_trait_n3: dict = {
        "name": "environmental_trait_4_slot",
        "category": "trait",
        "extra": ["env"],
        "cxn": [
            "environmental_trait_n2",
            "environmental_trait_n4",
        ],
    }
    environmental_trait_n4: dict = {
        "name": "environmental_trait_5_slot",
        "category": "trait",
        "extra": ["env"],
        "cxn": [
            "environmental_trait_n3",
        ],
    }

    # SLIVERWARE COMPLETE
    s_bodyweb_comp_n0: dict = {
        "name": "bodyweb_complete_sliverware_slot",
        "category": "skill",
        "skl": ["n_bodyweb_comp"],
        "cxn": ["null"],
    }
    s_headlink_comp_n0: dict = {
        "name": "headlink_complete_sliverware_slot",
        "category": "skill",
        "skl": ["n_headlink_comp"],
        "cxn": ["null"],
    }
    s_optics_comp_n0: dict = {
        "name": "optics_complete_sliverware_slot",
        "category": "skill",
        "skl": ["n_optics_comp"],
        "cxn": ["null"],
    }
    s_neural_rewiring_comp_n0: dict = {
        "name": "neural_rewiring_complete_sliverware_slot",
        "category": "skill",
        "skl": ["n_neuralrewiring_comp"],
        "cxn": ["null"],
    }
    s_biosculpting_comp_n0: dict = {
        "name": "biosculpting_complete_sliverware_slot",
        "category": "skill",
        "skl": ["n_biosculpting_comp"],
        "cxn": ["null"],
    }
    s_nanocore_comp_n0: dict = {
        "name": "nanocore_complete_sliverware_slot",
        "category": "skill",
        "skl": ["n_nanocore_comp"],
        "cxn": ["null"],
    }
    s_biocore_comp_n0: dict = {
        "name": "biocore_complete_sliverware_slot",
        "category": "skill",
        "skl": ["n_biocore_comp"],
        "cxn": ["null"],
    }

    # SLIVERWARE
    # BODYWEB
    bodyweb_n0: dict = {
        "name": "bodyweb_sliverware_entry_slot",
        "category": "sliverware",
        "cyb": ["s_bodyweb"],
        "cxn": [
            "entry_node",
            "s_bodyweb_comp_n0",
            "chemjet_n0",
            "cnsbooster_n0",
            "dermalplate_n0",
            "monoclaws_n0",
            "steelmuscles_n0",
            "bodystash_n0",
        ],
    }
    chemjet_n0: dict = {
        "name": "chemjet_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_chemjet"],
        "cxn": [
            "bodyweb_n0",
            "cnsbooster_n0",
            "dermalplate_n0",
            "monoclaws_n0",
            "steelmuscles_n0",
            "bodystash_n0",
        ],
    }
    cnsbooster_n0: dict = {
        "name": "cns_booster_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_cnsbooster"],
        "cxn": [
            "bodyweb_n0",
            "chemjet_n0",
            "dermalplate_n0",
            "monoclaws_n0",
            "steelmuscles_n0",
            "bodystash_n0",
        ],
    }
    dermalplate_n0: dict = {
        "name": "demal_plate_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_dermalplate"],
        "cxn": [
            "bodyweb_n0",
            "chemjet_n0",
            "cnsbooster_n0",
            "monoclaws_n0",
            "steelmuscles_n0",
            "bodystash_n0",
        ],
    }
    monoclaws_n0: dict = {
        "name": "monoclaws_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_monoclaws"],
        "cxn": [
            "bodyweb_n0",
            "chemjet_n0",
            "cnsbooster_n0",
            "dermalplate_n0",
            "steelmuscles_n0",
            "bodystash_n0",
        ],
    }
    steelmuscles_n0: dict = {
        "name": "steel_muscles_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_steelmuscles"],
        "cxn": [
            "bodyweb_n0",
            "chemjet_n0",
            "cnsbooster_n0",
            "dermalplate_n0",
            "monoclaws_n0",
            "bodystash_n0",
        ],
    }
    bodystash_n0: dict = {
        "name": "bodystash_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_bodystash"],
        "cxn": [
            "bodyweb_n0",
            "chemjet_n0",
            "cnsbooster_n0",
            "dermalplate_n0",
            "monoclaws_n0",
            "steelmuscles_n0",
        ],
    }

    # HEADLINK
    headlink_n0: dict = {
        "name": "headlink_sliverware_entry_slot",
        "category": "sliverware",
        "cyb": ["s_headlink"],
        "cxn": [
            "entry_node",
            "s_headlink_comp_n0",
            "combatlink_n0",
            "dronelink_n0",
            "nervelink_n0",
            "neuralcomm_n0",
            "socialanalyser_n0",
            "vcs_n0",
        ],
    }
    combatlink_n0: dict = {
        "name": "combatlink_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_combatlink"],
        "cxn": [
            "headlink_n0",
            "dronelink_n0",
            "nervelink_n0",
            "neuralcomm_n0",
            "socialanalyser_n0",
            "vcs_n0",
        ],
    }
    dronelink_n0: dict = {
        "name": "dronelink_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_dronelink"],
        "cxn": [
            "headlink_n0",
            "combatlink_n0",
            "nervelink_n0",
            "neuralcomm_n0",
            "socialanalyser_n0",
            "vcs_n0",
        ],
    }
    nervelink_n0: dict = {
        "name": "nervelink_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_nervelink"],
        "cxn": [
            "headlink_n0",
            "combatlink_n0",
            "dronelink_n0",
            "neuralcomm_n0",
            "socialanalyser_n0",
            "vcs_n0",
        ],
    }
    neuralcomm_n0: dict = {
        "name": "neuralcomm_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_neuralcomm"],
        "cxn": [
            "headlink_n0",
            "combatlink_n0",
            "dronelink_n0",
            "nervelink_n0",
            "socialanalyser_n0",
            "vcs_n0",
        ],
    }
    socialanalyser_n0: dict = {
        "name": "social_analyser_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_socialanalyser"],
        "cxn": [
            "headlink_n0",
            "combatlink_n0",
            "dronelink_n0",
            "nervelink_n0",
            "neuralcomm_n0",
            "vcs_n0",
        ],
    }
    vcs_n0: dict = {
        "name": "vehicle_control_system_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_vcs"],
        "cxn": [
            "headlink_n0",
            "combatlink_n0",
            "dronelink_n0",
            "nervelink_n0",
            "neuralcomm_n0",
            "socialanalyser_n0",
        ],
    }

    # OPTICS
    optics_n0: dict = {
        "name": "optics_sliverware_entry_slot",
        "category": "sliverware",
        "cyb": ["s_optics"],
        "cxn": [
            "entry_node",
            "s_optics_comp_n0",
            "brainbooster_n0",
            "eagleeye_n0",
            "forensicscanner_n0",
            "taclink_n0",
            "thermalimaging_n0",
            "threatanalyser_n0",
        ],
    }
    brainbooster_n0: dict = {
        "name": "brain_booster_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_brainbooster"],
        "cxn": [
            "optics_n0",
            "eagleeye_n0",
            "forensicscanner_n0",
            "taclink_n0",
            "thermalimaging_n0",
            "threatanalyser_n0",
        ],
    }
    eagleeye_n0: dict = {
        "name": "eagle_eye_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_eagleeye"],
        "cxn": [
            "optics_n0",
            "brainbooster_n0",
            "forensicscanner_n0",
            "taclink_n0",
            "thermalimaging_n0",
            "threatanalyser_n0",
        ],
    }
    forensicscanner_n0: dict = {
        "name": "forensic_scanner_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_forensicscanner"],
        "cxn": [
            "optics_n0",
            "brainbooster_n0",
            "eagleeye_n0",
            "taclink_n0",
            "thermalimaging_n0",
            "threatanalyser_n0",
        ],
    }
    taclink_n0: dict = {
        "name": "taclink_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_taclink"],
        "cxn": [
            "optics_n0",
            "brainbooster_n0",
            "eagleeye_n0",
            "forensicscanner_n0",
            "thermalimaging_n0",
            "threatanalyser_n0",
        ],
    }
    thermalimaging_n0: dict = {
        "name": "thermal_imaging_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_thermalimaging"],
        "cxn": [
            "optics_n0",
            "brainbooster_n0",
            "eagleeye_n0",
            "forensicscanner_n0",
            "taclink_n0",
            "threatanalyser_n0",
        ],
    }
    threatanalyser_n0: dict = {
        "name": "threat_analyser_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_threatanalyser"],
        "cxn": [
            "optics_n0",
            "brainbooster_n0",
            "eagleeye_n0",
            "forensicscanner_n0",
            "taclink_n0",
            "thermalimaging_n0",
        ],
    }

    # NEURAL REWIRING
    neuralrewiring_n0: dict = {
        "name": "neural_rewiring_sliverware_entry_slot",
        "category": "sliverware",
        "cyb": ["s_neuralrewiring"],
        "cxn": [
            "entry_node",
            "s_neural_rewiring_comp_n0",
            "audiowire_n0",
            "decrypter_n0",
            "godlink_n0",
            "weaveview_n0",
            "weavelink_n0",
            "ultrasonics_n0",
        ],
    }
    audiowire_n0: dict = {
        "name": "audiowire_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_audiowire"],
        "cxn": [
            "neuralrewiring_n0",
            "decrypter_n0",
            "godlink_n0",
            "weaveview_n0",
            "weavelink_n0",
            "ultrasonics_n0",
        ],
    }
    decrypter_n0: dict = {
        "name": "decrypter_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_decrypter"],
        "cxn": [
            "neuralrewiring_n0",
            "audiowire_n0",
            "godlink_n0",
            "weaveview_n0",
            "weavelink_n0",
            "ultrasonics_n0",
        ],
    }
    godlink_n0: dict = {
        "name": "godlink_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_godlink"],
        "cxn": [
            "neuralrewiring_n0",
            "audiowire_n0",
            "decrypter_n0",
            "weaveview_n0",
            "weavelink_n0",
            "ultrasonics_n0",
        ],
    }
    weaveview_n0: dict = {
        "name": "weave_view_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_weaveview"],
        "cxn": [
            "neuralrewiring_n0",
            "audiowire_n0",
            "decrypter_n0",
            "godlink_n0",
            "weavelink_n0",
            "ultrasonics_n0",
        ],
    }
    weavelink_n0: dict = {
        "name": "weavelink_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_weavelink"],
        "cxn": [
            "neuralrewiring_n0",
            "audiowire_n0",
            "decrypter_n0",
            "godlink_n0",
            "weavelink_n0",
            "ultrasonics_n0",
        ],
    }
    ultrasonics_n0: dict = {
        "name": "ultrasonics_sliverware_slot",
        "category": "sliverware",
        "cyb": ["s_ultrasonics"],
        "cxn": [
            "neuralrewiring_n0",
            "audiowire_n0",
            "decrypter_n0",
            "godlink_n0",
            "weavelink_n0",
            "weavelink_n0",
        ],
    }

    # BIOSCULPTING
    biosculpting_n0: dict = {
        "name": "biosculpting_sliverware_entry_slot",
        "category": "sliverware",
        "bio": ["s_biosculpting"],
        "cxn": [
            "entry_node",
            "s_biosculpting_comp_n0",
            "decentralisedheart_n0",
            "dns_n0",
            "magnaview_n0",
            "pharm_n0",
            "musclefibers_n0",
            "oxycycler_n0",
        ],
        "req": [
            "e_genesculpting",
            "e_social_upper",
            "e_social_patrician",
            "e_social_noble",
        ],
    }
    decentralisedheart_n0: dict = {
        "name": "decentralised_heart_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_decentralisedheart"],
        "cxn": [
            "biosculpting_n0",
            "dns_n0",
            "magnaview_n0",
            "pharm_n0",
            "musclefibers_n0",
            "oxycycler_n0",
        ],
    }
    dns_n0: dict = {
        "name": "decentralised_nervous_system_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_dns"],
        "cxn": [
            "biosculpting_n0",
            "decentralisedheart_n0",
            "magnaview_n0",
            "pharm_n0",
            "musclefibers_n0",
            "oxycycler_n0",
        ],
    }
    magnaview_n0: dict = {
        "name": "magnaview_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_magnaview"],
        "cxn": [
            "biosculpting_n0",
            "decentralisedheart_n0",
            "dns_n0",
            "pharm_n0",
            "musclefibers_n0",
            "oxycycler_n0",
        ],
    }
    pharm_n0: dict = {
        "name": "pharm_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_pharm"],
        "cxn": [
            "biosculpting_n0",
            "decentralisedheart_n0",
            "dns_n0",
            "magnaview_n0",
            "musclefibers_n0",
            "oxycycler_n0",
        ],
    }
    musclefibers_n0: dict = {
        "name": "musclefibers_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_musclefibers"],
        "cxn": [
            "biosculpting_n0",
            "decentralisedheart_n0",
            "dns_n0",
            "magnaview_n0",
            "pharm_n0",
            "oxycycler_n0",
        ],
    }
    oxycycler_n0: dict = {
        "name": "oxycycler_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_oxycycler"],
        "cxn": [
            "biosculpting_n0",
            "decentralisedheart_n0",
            "dns_n0",
            "magnaview_n0",
            "pharm_n0",
            "musclefibers_n0",
        ],
    }

    # NANOCORE
    nanocore_n0: dict = {
        "name": "nanocore_sliverware_entry_slot",
        "category": "sliverware",
        "bio": ["s_nanocore"],
        "cxn": [
            "entry_node",
            "s_nanocore_comp_n0",
            "chameleonfield_n0",
            "ecmcloak_n0",
            "escapegas_n0",
            "nanoarmour_n0",
            "nbsu_n0",
            "nanoregen_n0",
        ],
        "req": [
            "e_genesculpting",
            "e_social_upper",
            "e_social_patrician",
            "e_social_noble",
        ],
    }
    chameleonfield_n0: dict = {
        "name": "chameleon_field_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_chameleonfield"],
        "cxn": [
            "nanocore_n0",
            "ecmcloak_n0",
            "escapegas_n0",
            "nanoarmour_n0",
            "nbsu_n0",
            "nanoregen_n0",
        ],
    }
    ecmcloak_n0: dict = {
        "name": "ecm_cloak_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_ecmcloak"],
        "cxn": [
            "nanocore_n0",
            "chameleonfield_n0",
            "escapegas_n0",
            "nanoarmour_n0",
            "nbsu_n0",
            "nanoregen_n0",
        ],
    }
    escapegas_n0: dict = {
        "name": "escape_gas_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_escapegas"],
        "cxn": [
            "nanocore_n0",
            "chameleonfield_n0",
            "ecmcloak_n0",
            "nanoarmour_n0",
            "nbsu_n0",
            "nanoregen_n0",
        ],
    }
    nanoarmour_n0: dict = {
        "name": "nanoarmour_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_nanoarmour"],
        "cxn": [
            "nanocore_n0",
            "chameleonfield_n0",
            "ecmcloak_n0",
            "escapegas_n0",
            "nbsu_n0",
            "nanoregen_n0",
        ],
    }
    nbsu_n0: dict = {
        "name": "nano_biostatus_unit_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_nbsu"],
        "cxn": [
            "nanocore_n0",
            "chameleonfield_n0",
            "ecmcloak_n0",
            "escapegas_n0",
            "nanoarmour_n0",
            "nanoregen_n0",
        ],
    }
    nanoregen_n0: dict = {
        "name": "nanoregen_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_nanoregen"],
        "cxn": [
            "nanocore_n0",
            "chameleonfield_n0",
            "ecmcloak_n0",
            "escapegas_n0",
            "nanoarmour_n0",
            "nbsu_n0",
        ],
    }

    # BIOCORE
    biocore_n0: dict = {
        "name": "biocore_sliverware_entry_slot",
        "category": "sliverware",
        "bio": ["s_biocore"],
        "cxn": [
            "entry_node",
            "s_biocore_comp_n0",
            "aquashift_n0",
            "beautifier_n0",
            "cloneorgan_n0",
            "pheromones_n0",
            "stressshift_n0",
            "voicecontrol_n0",
        ],
        "req": [
            "e_genesculpting",
            "e_social_upper",
            "e_social_patrician",
            "e_social_noble",
        ],
    }
    aquashift_n0: dict = {
        "name": "aquashift_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_aquashift"],
        "cxn": [
            "biocore_n0",
            "beautifier_n0",
            "cloneorgan_n0",
            "pheromones_n0",
            "stressshift_n0",
            "voicecontrol_n0",
        ],
    }
    beautifier_n0: dict = {
        "name": "beautifier_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_beautifier"],
        "cxn": [
            "biocore_n0",
            "aquashift_n0",
            "cloneorgan_n0",
            "pheromones_n0",
            "stressshift_n0",
            "voicecontrol_n0",
        ],
    }
    cloneorgan_n0: dict = {
        "name": "clone_organ_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_cloneorgan"],
        "cxn": [
            "biocore_n0",
            "aquashift_n0",
            "beautifier_n0",
            "pheromones_n0",
            "stressshift_n0",
            "voicecontrol_n0",
        ],
    }
    pheromones_n0: dict = {
        "name": "pheromones_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_pheromones"],
        "cxn": [
            "biocore_n0",
            "aquashift_n0",
            "beautifier_n0",
            "cloneorgan_n0",
            "stressshift_n0",
            "voicecontrol_n0",
        ],
    }
    stressshift_n0: dict = {
        "name": "stress_shift_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_stressshift"],
        "cxn": [
            "biocore_n0",
            "aquashift_n0",
            "beautifier_n0",
            "cloneorgan_n0",
            "pheromones_n0",
            "voicecontrol_n0",
        ],
    }
    voicecontrol_n0: dict = {
        "name": "voice_control_sliverware_slot",
        "category": "sliverware",
        "bio": ["s_voicecontrol"],
        "cxn": [
            "biocore_n0",
            "aquashift_n0",
            "beautifier_n0",
            "cloneorgan_n0",
            "pheromones_n0",
            "stressshift_n0",
        ],
    }
    # TODO: Cat: Soulweaving and Cat: Rune not used yet!
    soulweaving_n0: dict = {
        "name": "soulweaving_spell_1_slot",
        "category": "soulweaving",
        "type": ["cor"],
        "cxn": ["entry_node"],
        "req": ["e_soulweaving"],
    }
    soulweaving_n1: dict = {
        "name": "soulweaving_spell_2_slot",
        "category": "soulweaving",
        "type": ["cor"],
        "cxn": ["soulweaving_n0"],
    }
    soulweaving_n2: dict = {
        "name": "soulweaving_spell_3_slot",
        "category": "soulweaving",
        "type": ["cor"],
        "cxn": ["soulweaving_n1"],
    }
    soulweaving_n3: dict = {
        "name": "soulweaving_spell_4_slot",
        "category": "soulweaving",
        "type": ["cor"],
        "cxn": ["soulweaving_n2"],
    }
    soulweaving_n4: dict = {
        "name": "soulweaving_spell_5_slot",
        "category": "soulweaving",
        "type": ["cor"],
        "cxn": ["soulweaving_n3"],
    }
    rune_enchantment_n0: dict = {
        "name": "runic_enchantment_1_slot",
        "category": "rune",
        "type": ["run"],
        "cxn": ["entry_node"],
        "req": ["e_rune_enchantment"],
    }
    rune_enchantment_n1: dict = {
        "name": "runic_enchantment_2_slot",
        "category": "rune",
        "type": ["run"],
        "cxn": ["rune_enchantment_n0"],
    }
    rune_enchantment_n2: dict = {
        "name": "runic_enchantment_3_slot",
        "category": "rune",
        "type": ["run"],
        "cxn": ["rune_enchantment_n1"],
    }
    rune_enchantment_n3: dict = {
        "name": "runic_enchantment_4_slot",
        "category": "rune",
        "type": ["run"],
        "cxn": ["rune_enchantment_n2"],
    }
    rune_enchantment_n4: dict = {
        "name": "runic_enchantment_5_slot",
        "category": "rune",
        "type": ["run"],
        "cxn": ["rune_enchantment_n3"],
    }
    # TODO: Cat: drug not used yet
    drug_toxin_n0: dict = {
        "name": "active_drug/toxin_1_slot",
        "category": "drug",
        "type": ["drg"],
        "cxn": ["drug"],
    }
    drug_toxin_n1: dict = {
        "name": "active_drug/toxin_2_slot",
        "category": "drug",
        "type": ["drg"],
        "cxn": ["drug_toxin_n0"],
    }
    drug_toxin_n2: dict = {
        "name": "active_drug/toxin_3_slot",
        "category": "drug",
        "type": ["drg"],
        "cxn": ["drug_toxin_n1"],
    }
    drug_toxin_n3: dict = {
        "name": "active_drug/toxin_4_slot",
        "category": "drug",
        "type": ["drg"],
        "cxn": ["drug_toxin_n2"],
    }
    drug_toxin_n4: dict = {
        "name": "active_drug/toxin_5_slot",
        "category": "drug",
        "type": ["drg"],
        "cxn": ["drug_toxin_n3"],
    }
    drug_toxin_n5: dict = {
        "name": "active_drug/toxin_6_slot",
        "category": "drug",
        "type": ["drg"],
        "cxn": ["drug_toxin_n4"],
    }
    # TODO: Should these be separate for each wound and Injury? Cat: Wound Not used yet!
    # TODO: These don't appear in searches yet as they are NOT in the CharacterModel.nodes dict
    physical_wound_n0: dict = {
        "name": "first_physical_wound",
        "category": "wound",
        "type": ["wph"],
        "cxn": ["wound"],
    }
    physical_wound_n1: dict = {
        "name": "second_physical_wound",
        "category": "wound",
        "type": ["wph"],
        "cxn": ["physical_wound_0"],
    }
    physical_wound_n2: dict = {
        "name": "third_physical_wound",
        "category": "wound",
        "type": ["wph"],
        "cxn": ["physical_wound_1"],
    }
    smarts_wound_n0: dict = {
        "name": "first_smarts_wound",
        "category": "wound",
        "type": ["wsm"],
        "cxn": ["wound"],
    }
    smarts_wound_n1: dict = {
        "name": "second_smarts_wound",
        "category": "wound",
        "type": ["wsm"],
        "cxn": ["smarts_wound_0"],
    }
    smarts_wound_n2: dict = {
        "name": "third_smarts_wound",
        "category": "wound",
        "type": ["wsm"],
        "cxn": ["smarts_wound_1"],
    }
    resources_wound_n0: dict = {
        "name": "first_resources_wounds",
        "category": "wound",
        "type": ["wre"],
        "cxn": ["wound"],
    }
    resources_wound_n1: dict = {
        "name": "second_resources_wounds",
        "category": "wound",
        "type": ["wre"],
        "cxn": ["resources_wound_0"],
    }
    resources_wound_n2: dict = {
        "name": "third_resources_wounds",
        "category": "wound",
        "type": ["wre"],
        "cxn": ["resources_wound_1"],
    }
    wyld_wound_n0: dict = {
        "name": "first_wyld_wound",
        "category": "wound",
        "type": ["wwy"],
        "cxn": ["wound"],
    }
    wyld_wound_n1: dict = {
        "name": "second_wyld_wound",
        "category": "wound",
        "type": ["wwy"],
        "cxn": ["wyld_wound_n0"],
    }
    wyld_wound_n2: dict = {
        "name": "third_wyld_wound",
        "category": "wound",
        "type": ["wwy"],
        "cxn": ["wyld_wound_n1"],
    }
    divinity_wound_n0: dict = {
        "name": "first_divinity_wounds",
        "category": "wound",
        "type": ["wdi"],
        "cxn": ["wound"],
    }
    divinity_wound_n1: dict = {
        "name": "second_divinity_wounds",
        "category": "wound",
        "type": ["wdi"],
        "cxn": ["divinity_wound_n0"],
    }
    divinity_wound_n2: dict = {
        "name": "third_divinity_wounds",
        "category": "wound",
        "type": ["wdi"],
        "cxn": ["divinity_wound_n1"],
    }
    vehicle_wound_n0: dict = {
        "name": "first_vehicle_wound",
        "category": "wound",
        "type": ["wve"],
        "cxn": ["wound"],
    }
    vehicle_wound_n1: dict = {
        "name": "second_vehicle_wound",
        "category": "wound",
        "type": ["wve"],
        "cxn": ["vehicle_wound_n0"],
    }
    vehicle_wound_n2: dict = {
        "name": "third_vehicle_wound",
        "category": "wound",
        "type": ["wve"],
        "cxn": ["vehicle_wound_n1"],
    }
    physical_injury_n0: dict = {
        "name": "physical_injury_1_slot",
        "category": "injury",
        "type": ["ip0"],
        "cxn": ["wound"],
    }
    physical_injury_n1: dict = {
        "name": "physical_injury_2_slot",
        "category": "injury",
        "type": ["ip0"],
        "cxn": ["physical_injury_n0"],
    }
    physical_injury_n2: dict = {
        "name": "physical_injury_3_slot",
        "category": "injury",
        "type": ["ip0"],
        "cxn": ["physical_injury_n1"],
    }
    physical_injury_n3: dict = {
        "name": "physical_injury_4_slot",
        "category": "injury",
        "type": ["ip0"],
        "cxn": ["physical_injury_n2"],
    }
    physical_injury_n4: dict = {
        "name": "physical_injury_5_slot",
        "category": "injury",
        "type": ["ip0"],
        "cxn": ["physical_injury_n3"],
    }
    physical_injury_n5: dict = {
        "name": "physical_injury_6_slot",
        "category": "injury",
        "type": ["ip0"],
        "cxn": ["physical_injury_n4"],
    }
    physical_injury_n6: dict = {
        "name": "physical_injury_7_slot",
        "category": "injury",
        "type": ["ip0"],
        "cxn": ["physical_injury_n5"],
    }
    physical_injury_n7: dict = {
        "name": "physical_injury_8_slot",
        "category": "injury",
        "type": ["ip0"],
        "cxn": ["physical_injury_n6"],
    }
    physical_injury_n8: dict = {
        "name": "physical_injury_9_slot",
        "category": "injury",
        "type": ["ip0"],
        "cxn": ["physical_injury_n7"],
    }
    physical_injury_n9: dict = {
        "name": "physical_injury_10_slot",
        "category": "injury",
        "type": ["ip0"],
        "cxn": ["physical_injury_n8"],
    }
    physical_injury_n10: dict = {
        "name": "physical_injury_11_slot",
        "category": "injury",
        "type": ["ip0"],
        "cxn": ["physical_injury_n9"],
    }
    physical_injury_n11: dict = {
        "name": "physical_injury_12_slot",
        "category": "injury",
        "type": ["ip0"],
        "cxn": ["physical_injury_n10"],
    }
    smarts_injury_n0: dict = {
        "name": "smarts_injury_1_slot",
        "category": "injury",
        "type": ["is0"],
        "cxn": ["wound"],
    }
    smarts_injury_n1: dict = {
        "name": "smarts_injury_2_slot",
        "category": "injury",
        "type": ["is0"],
        "cxn": ["smarts_injury_n0"],
    }
    smarts_injury_n2: dict = {
        "name": "smarts_injury_3_slot",
        "category": "injury",
        "type": ["is0"],
        "cxn": ["smarts_injury_n1"],
    }
    smarts_injury_n3: dict = {
        "name": "smarts_injury_4_slot",
        "category": "injury",
        "type": ["is0"],
        "cxn": ["smarts_injury_n2"],
    }
    smarts_injury_n4: dict = {
        "name": "smarts_injury_5_slot",
        "category": "injury",
        "type": ["is0"],
        "cxn": ["smarts_injury_n3"],
    }
    smarts_injury_n5: dict = {
        "name": "smarts_injury_6_slot",
        "category": "injury",
        "type": ["is0"],
        "cxn": ["smarts_injury_n4"],
    }
    smarts_injury_n6: dict = {
        "name": "smarts_injury_7_slot",
        "category": "injury",
        "type": ["is0"],
        "cxn": ["smarts_injury_n5"],
    }
    smarts_injury_n7: dict = {
        "name": "smarts_injury_8_slot",
        "category": "injury",
        "type": ["is0"],
        "cxn": ["smarts_injury_n6"],
    }
    smarts_injury_n8: dict = {
        "name": "smarts_injury_9_slot",
        "category": "injury",
        "type": ["is0"],
        "cxn": ["smarts_injury_n7"],
    }
    smarts_injury_n9: dict = {
        "name": "smarts_injury_10_slot",
        "category": "injury",
        "type": ["is0"],
        "cxn": ["smarts_injury_n8"],
    }
    smarts_injury_n10: dict = {
        "name": "smarts_injury_11_slot",
        "category": "injury",
        "type": ["is0"],
        "cxn": ["smarts_injury_n9"],
    }
    smarts_injury_n11: dict = {
        "name": "smarts_injury_12_slot",
        "category": "injury",
        "type": ["is0"],
        "cxn": ["smarts_injury_n10"],
    }
    resources_injury_n0: dict = {
        "name": "resources_injury_1_slot",
        "category": "injury",
        "type": ["ir0"],
        "cxn": ["wound"],
    }
    resources_injury_n1: dict = {
        "name": "resources_injury_2_slot",
        "category": "injury",
        "type": ["ir0"],
        "cxn": ["resources_injury_n0"],
    }
    resources_injury_n2: dict = {
        "name": "resources_injury_3_slot",
        "category": "injury",
        "type": ["ir0"],
        "cxn": ["resources_injury_n1"],
    }
    resources_injury_n3: dict = {
        "name": "resources_injury_4_slot",
        "category": "injury",
        "type": ["ir0"],
        "cxn": ["resources_injury_n2"],
    }
    resources_injury_n4: dict = {
        "name": "resources_injury_5_slot",
        "category": "injury",
        "type": ["ir0"],
        "cxn": ["resources_injury_n3"],
    }
    resources_injury_n5: dict = {
        "name": "resources_injury_6_slot",
        "category": "injury",
        "type": ["ir0"],
        "cxn": ["resources_injury_n4"],
    }
    resources_injury_n6: dict = {
        "name": "resources_injury_7_slot",
        "category": "injury",
        "type": ["ir0"],
        "cxn": ["resources_injury_n5"],
    }
    resources_injury_n7: dict = {
        "name": "resources_injury_8_slot",
        "category": "injury",
        "type": ["ir0"],
        "cxn": ["resources_injury_n6"],
    }
    resources_injury_n8: dict = {
        "name": "resources_injury_9_slot",
        "category": "injury",
        "type": ["ir0"],
        "cxn": ["resources_injury_n7"],
    }
    resources_injury_n9: dict = {
        "name": "resources_injury_10_slot",
        "category": "injury",
        "type": ["ir0"],
        "cxn": ["resources_injury_n8"],
    }
    resources_injury_n10: dict = {
        "name": "resources_injury_11_slot",
        "category": "injury",
        "type": ["ir0"],
        "cxn": ["resources_injury_n9"],
    }
    resources_injury_n11: dict = {
        "name": "resources_injury_12_slot",
        "category": "injury",
        "type": ["ir0"],
        "cxn": ["resources_injury_n10"],
    }
    wyld_injury_n0: dict = {
        "name": "wyld_injury_1_slot",
        "category": "injury",
        "type": ["iw0"],
        "cxn": ["wound"],
    }
    wyld_injury_n1: dict = {
        "name": "wyld_injury_2_slot",
        "category": "injury",
        "type": ["iw0"],
        "cxn": ["wyld_injury_n0"],
    }
    wyld_injury_n2: dict = {
        "name": "wyld_injury_3_slot",
        "category": "injury",
        "type": ["iw0"],
        "cxn": ["wyld_injury_n1"],
    }
    wyld_injury_n3: dict = {
        "name": "wyld_injury_4_slot",
        "category": "injury",
        "type": ["iw0"],
        "cxn": ["wyld_injury_n2"],
    }
    wyld_injury_n4: dict = {
        "name": "wyld_injury_5_slot",
        "category": "injury",
        "type": ["iw0"],
        "cxn": ["wyld_injury_n3"],
    }
    wyld_injury_n5: dict = {
        "name": "wyld_injury_6_slot",
        "category": "injury",
        "type": ["iw0"],
        "cxn": ["wyld_injury_n4"],
    }
    wyld_injury_n6: dict = {
        "name": "wyld_injury_7_slot",
        "category": "injury",
        "type": ["iw0"],
        "cxn": ["wyld_injury_n5"],
    }
    wyld_injury_n7: dict = {
        "name": "wyld_injury_8_slot",
        "category": "injury",
        "type": ["iw0"],
        "cxn": ["wyld_injury_n6"],
    }
    wyld_injury_n8: dict = {
        "name": "wyld_injury_9_slot",
        "category": "injury",
        "type": ["iw0"],
        "cxn": ["wyld_injury_n7"],
    }
    wyld_injury_n9: dict = {
        "name": "wyld_injury_10_slot",
        "category": "injury",
        "type": ["iw0"],
        "cxn": ["wyld_injury_n8"],
    }
    wyld_injury_n10: dict = {
        "name": "wyld_injury_11_slot",
        "category": "injury",
        "type": ["iw0"],
        "cxn": ["wyld_injury_n9"],
    }
    wyld_injury_n11: dict = {
        "name": "wyld_injury_12_slot",
        "category": "injury",
        "type": ["iw0"],
        "cxn": ["wyld_injury_n10"],
    }
    divinity_injury_n0: dict = {
        "name": "divinity_injury_1_slot",
        "category": "injury",
        "type": ["id0"],
        "cxn": ["wound"],
    }
    divinity_injury_n1: dict = {
        "name": "divinity_injury_2_slot",
        "category": "injury",
        "type": ["id0"],
        "cxn": ["divinity_injury_n0"],
    }
    divinity_injury_n2: dict = {
        "name": "divinity_injury_3_slot",
        "category": "injury",
        "type": ["id0"],
        "cxn": ["divinity_injury_n1"],
    }
    divinity_injury_n3: dict = {
        "name": "divinity_injury_4_slot",
        "category": "injury",
        "type": ["id0"],
        "cxn": ["divinity_injury_n2"],
    }
    divinity_injury_n4: dict = {
        "name": "divinity_injury_5_slot",
        "category": "injury",
        "type": ["id0"],
        "cxn": ["divinity_injury_n3"],
    }
    divinity_injury_n5: dict = {
        "name": "divinity_injury_6_slot",
        "category": "injury",
        "type": ["id0"],
        "cxn": ["divinity_injury_n4"],
    }
    divinity_injury_n6: dict = {
        "name": "divinity_injury_7_slot",
        "category": "injury",
        "type": ["id0"],
        "cxn": ["divinity_injury_n5"],
    }
    divinity_injury_n7: dict = {
        "name": "divinity_injury_8_slot",
        "category": "injury",
        "type": ["id0"],
        "cxn": ["divinity_injury_n6"],
    }
    divinity_injury_n8: dict = {
        "name": "divinity_injury_9_slot",
        "category": "injury",
        "type": ["id0"],
        "cxn": ["divinity_injury_n7"],
    }
    divinity_injury_n9: dict = {
        "name": "divinity_injury_10_slot",
        "category": "injury",
        "type": ["id0"],
        "cxn": ["divinity_injury_n8"],
    }
    divinity_injury_n10: dict = {
        "name": "divinity_injury_11_slot",
        "category": "injury",
        "type": ["id0"],
        "cxn": ["divinity_injury_n9"],
    }
    divinity_injury_n11: dict = {
        "name": "divinity_injury_12_slot",
        "category": "injury",
        "type": ["id0"],
        "cxn": ["divinity_injury_n10"],
    }
    corruption_injury_n0: dict = {
        "name": "corruption_injury_1_slot",
        "category": "injury",
        "type": ["ic0"],
        "cxn": ["wound"],
    }
    corruption_injury_n1: dict = {
        "name": "corruption_injury_2_slot",
        "category": "injury",
        "type": ["ic0"],
        "cxn": ["corruption_injury_n0"],
    }
    corruption_injury_n2: dict = {
        "name": "corruption_injury_3_slot",
        "category": "injury",
        "type": ["ic0"],
        "cxn": ["corruption_injury_n1"],
    }
    corruption_injury_n3: dict = {
        "name": "corruption_injury_4_slot",
        "category": "injury",
        "type": ["ic0"],
        "cxn": ["corruption_injury_n2"],
    }
    corruption_injury_n4: dict = {
        "name": "corruption_injury_5_slot",
        "category": "injury",
        "type": ["ic0"],
        "cxn": ["corruption_injury_n3"],
    }
    corruption_injury_n5: dict = {
        "name": "corruption_injury_6_slot",
        "category": "injury",
        "type": ["ic0"],
        "cxn": ["corruption_injury_n4"],
    }
    corruption_injury_n6: dict = {
        "name": "corruption_injury_7_slot",
        "category": "injury",
        "type": ["ic0"],
        "cxn": ["corruption_injury_n5"],
    }
    corruption_injury_n7: dict = {
        "name": "corruption_injury_8_slot",
        "category": "injury",
        "type": ["ic0"],
        "cxn": ["corruption_injury_n6"],
    }
    corruption_injury_n8: dict = {
        "name": "corruption_injury_9_slot",
        "category": "injury",
        "type": ["ic0"],
        "cxn": ["corruption_injury_n7"],
    }
    corruption_injury_n9: dict = {
        "name": "corruption_injury_10_slot",
        "category": "injury",
        "type": ["ic0"],
        "cxn": ["corruption_injury_n8"],
    }
    corruption_injury_n10: dict = {
        "name": "corruption_injury_11_slot",
        "category": "injury",
        "type": ["ic0"],
        "cxn": ["corruption_injury_n9"],
    }
    corruption_injury_n11: dict = {
        "name": "corruption_injury_12_slot",
        "category": "injury",
        "type": ["ic0"],
        "cxn": ["corruption_injury_n10"],
    }
    geas_injury_n0: dict = {
        "name": "geas_injury_1_slot",
        "category": "injury",
        "type": ["ig0"],
        "cxn": ["wound"],
    }
    geas_injury_n1: dict = {
        "name": "geas_injury_2_slot",
        "category": "injury",
        "type": ["ig0"],
        "cxn": ["geas_injury_n0"],
    }
    geas_injury_n2: dict = {
        "name": "geas_injury_3_slot",
        "category": "injury",
        "type": ["ig0"],
        "cxn": ["geas_injury_n1"],
    }
    geas_injury_n3: dict = {
        "name": "geas_injury_4_slot",
        "category": "injury",
        "type": ["ig0"],
        "cxn": ["geas_injury_n2"],
    }
    geas_injury_n4: dict = {
        "name": "geas_injury_5_slot",
        "category": "injury",
        "type": ["ig0"],
        "cxn": ["geas_injury_n3"],
    }
    geas_injury_n5: dict = {
        "name": "geas_injury_6_slot",
        "category": "injury",
        "type": ["ig0"],
        "cxn": ["geas_injury_n4"],
    }
    geas_injury_n6: dict = {
        "name": "geas_injury_7_slot",
        "category": "injury",
        "type": ["ig0"],
        "cxn": ["geas_injury_n5"],
    }
    geas_injury_n7: dict = {
        "name": "geas_injury_8_slot",
        "category": "injury",
        "type": ["ig0"],
        "cxn": ["geas_injury_n6"],
    }
    geas_injury_n8: dict = {
        "name": "geas_injury_9_slot",
        "category": "injury",
        "type": ["ig0"],
        "cxn": ["geas_injury_n7"],
    }
    geas_injury_n9: dict = {
        "name": "geas_injury_10_slot",
        "category": "injury",
        "type": ["ig0"],
        "cxn": ["geas_injury_n8"],
    }
    geas_injury_n10: dict = {
        "name": "geas_injury_11_slot",
        "category": "injury",
        "type": ["ig0"],
        "cxn": ["geas_injury_n9"],
    }
    geas_injury_n11: dict = {
        "name": "geas_injury_12_slot",
        "category": "injury",
        "type": ["ig0"],
        "cxn": ["geas_injury_n10"],
    }
    vehicle_injury_n0: dict = {
        "name": "vehicle_injury_1_slot",
        "category": "injury",
        "type": ["iv0"],
        "cxn": ["wound"],
    }
    vehicle_injury_n1: dict = {
        "name": "vehicle_injury_2_slot",
        "category": "injury",
        "type": ["iv0"],
        "cxn": ["vehicle_injury_n0"],
    }
    vehicle_injury_n2: dict = {
        "name": "vehicle_injury_3_slot",
        "category": "injury",
        "type": ["iv0"],
        "cxn": ["vehicle_injury_n1"],
    }
    vehicle_injury_n3: dict = {
        "name": "vehicle_injury_4_slot",
        "category": "injury",
        "type": ["iv0"],
        "cxn": ["vehicle_injury_n2"],
    }
    vehicle_injury_n4: dict = {
        "name": "vehicle_injury_5_slot",
        "category": "injury",
        "type": ["iv0"],
        "cxn": ["vehicle_injury_n3"],
    }
    vehicle_injury_n5: dict = {
        "name": "vehicle_injury_6_slot",
        "category": "injury",
        "type": ["iv0"],
        "cxn": ["vehicle_injury_n4"],
    }
    vehicle_injury_n6: dict = {
        "name": "vehicle_injury_7_slot",
        "category": "injury",
        "type": ["iv0"],
        "cxn": ["vehicle_injury_n5"],
    }
    vehicle_injury_n7: dict = {
        "name": "vehicle_injury_8_slot",
        "category": "injury",
        "type": ["iv0"],
        "cxn": ["vehicle_injury_n6"],
    }
    vehicle_injury_n8: dict = {
        "name": "vehicle_injury_9_slot",
        "category": "injury",
        "type": ["iv0"],
        "cxn": ["vehicle_injury_n7"],
    }
    vehicle_injury_n9: dict = {
        "name": "vehicle_injury_10_slot",
        "category": "injury",
        "type": ["iv0"],
        "cxn": ["vehicle_injury_n8"],
    }
    vehicle_injury_n10: dict = {
        "name": "vehicle_injury_11_slot",
        "category": "injury",
        "type": ["iv0"],
        "cxn": ["vehicle_injury_n9"],
    }
    vehicle_injury_n11: dict = {
        "name": "vehicle_injury_12_slot",
        "category": "injury",
        "type": ["iv0"],
        "cxn": ["vehicle_injury_n10"],
    }


class PlayerModel(BaseModel):
    def __init__(self, **kwargs):
        super(PlayerModel, self).__init__(**kwargs)

    class Config:
        extra = Extra.forbid

    player_id: int
    player_name: str
    player_real_name: str = ""
    player_email: str = ""
    deleted: bool = False

    # TIMESTAMPS
    player_created: datetime = None
    player_modified: datetime = Optional[None]


class CharacterModel(BaseModel):
    """This model maps mod_ids to node_ids as well as containing the essential information for the character too.
    Think of it as the static source file for the character that gets compiled into the LiveCharacterModel.
    NODES DICT:
    This is where the mod_id of everything that is a dropdown or selectable on/off toggle on the build sheet
    and play sheet should live. The actual calculations are performed by the character_methods.py and the final
    values are stored in LiveCharacterModel"""

    def __init__(self, **kwargs):
        super(CharacterModel, self).__init__(**kwargs)

    # CORE CHARACTER INFO
    # ID will be set by the database
    char_id: int
    char_name: str = ""
    char_archetype: str = ""
    player_id: int
    deleted: bool = False
    char_type: str = "char"  # = character, mook, master, creature, vehicle. Validate to these options only
    char_age: int = 18
    char_gender: str = ""
    char_description: str = ""
    char_picture: str = ""
    player_notes: str = ""
    gm_notes: str = ""
    lang_other_name: Optional[str]
    breed: str = ""

    # TALENT POINTS
    tp_total: int = 0  # = tp_create + tp_bonus + tp_missions
    tp_spent: int = 0  # Sum total of TPs spent
    tp_unspent: int = 0  #
    tp_create: int = 30  # Starting TPs
    tp_missions: int = 0  # Experience TPS
    tp_bonus: int = 0  # Bonus TPs given to char
    breed_tp_spent: int = 0
    breed_tp_bonus: int = 0

    # TIMESTAMPS
    char_created: datetime = None
    char_modified: datetime = None

    # EXTRA INFO
    weapons: dict = {}
    gear: dict = {}
    char_missions: dict = {}
    char_contacts: dict = {}

    # ORGANISATION SECONDARY INFO
    commendations: int = 0
    reprimands: int = 0
    reputation: int = 0

    # WYLD CANCER STUFF
    wyld_cancer_extra: int = 0  # Extra Wyld Cancer earned in play
    healed_wyld_perm_injuries: int = (
        0  # How many Permanent Wyld Injuries have been healed by Isoke?
    )
    wyld_perm_injuries: list = []  # List of Wyld Injuries

    # Echo Powers
    echo1: str = ""
    echo2: str = ""

    # Specialisation Masteries
    spec_mastery1: str = ""
    spec_mastery2: str = ""
    spec_mastery3: str = ""

    # Soulweaving
    gifts_curses: str = ""
    heresies: str = ""
    geas: list = []
    blessings: list = []
    bound_rezhadi: list = []
    soulweaving: str = ""
    rune_enchantments: str = ""
    corruption_extra: int = 0
    healed_corruption_perm_injuries: int = 0
    corruption_perm_injuries: list = []

    # %TEXT% REPLACEMENT
    # This is for replacing %TEXT% in mod_ids at specific mod_location with replacement_text
    # In form {"mod_location": {"mod_id": "replacement_text"}
    text_replace_mods: dict = {}

    # Space for custom notes
    custom_notes: dict = {}

    # Stored Overrides
    stored_overrides: dict = {}

    # NODES
    nodes: dict = {
        "breed_n0": "",
        "culture_n0": "",
        "social_n0": "",
        "lifestyle_n0": "",
        "language_n0": "",
        "language_n1": "",
        "language_n2": "",
        "language_n3": "",
        "language_n4": "",
        "language_n5": "",
        "language_n6": "",
        "language_n7": "",
        "language_n8": "",
        "language_n9": "",
        "pledged_disciple_n0": "",
        "pledged_disciple_n1": "",
        "pledged_disciple_n2": "",
        "avatar_n0": "",
        "avatar_n1": "",
        "avatar_n2": "",
        "citizen_n0": "",
        "citizen_n1": "",
        "citizen_n2": "",
        "organisation_n0": "",
        "organisation_n1": "",
        "organisation_n2": "",
        "organisation_n3": "",
        "rank_n0": "",
        "rank_n1": "",
        "rank_n2": "",
        "rank_n3": "",
        "physical_skill_n0": "",
        "physical_skill_n1": "",
        "physical_skill_n2": "",
        "physical_skill_n3": "",
        "physical_skill_n4": "",
        "physical_skill_n5": "",
        "physical_skill_n6": "",
        "physical_op_n0": "",
        "physical_op_n1": "",
        "physical_op_n2": "",
        "physical_op_n3": "",
        "athletics_skill_n0": "",
        "athletics_skill_n1": "",
        "athletics_skill_n2": "",
        "athletics_edge_n0": "",
        "endurance_skill_n0": "",
        "endurance_skill_n1": "",
        "endurance_skill_n2": "",
        "endurance_edge_n0": "",
        "killer_skill_n0": "",
        "killer_skill_n1": "",
        "killer_skill_n2": "",
        "killer_skill_n3": "",
        "killer_skill_n4": "",
        "killer_skill_n5": "",
        "killer_skill_n6": "",
        "killer_trait_n0": "",
        "guns_skill_n0": "",
        "guns_skill_n1": "",
        "guns_skill_n2": "",
        "guns_edge_n0": "",
        "melee_skill_n0": "",
        "melee_skill_n1": "",
        "melee_skill_n2": "",
        "melee_edge_n0": "",
        "energy_skill_n0": "",
        "energy_skill_n1": "",
        "energy_skill_n2": "",
        "energy_edge_n0": "",
        "cloak_skill_n0": "",
        "cloak_skill_n1": "",
        "cloak_skill_n2": "",
        "cloak_skill_n3": "",
        "cloak_skill_n4": "",
        "cloak_skill_n5": "",
        "cloak_skill_n6": "",
        "cloak_trait_n0": "",
        "sneak_skill_n0": "",
        "sneak_skill_n1": "",
        "sneak_skill_n2": "",
        "sneak_edge_n0": "",
        "con_skill_n0": "",
        "con_skill_n1": "",
        "con_skill_n2": "",
        "con_edge_n0": "",
        "disguise_skill_n0": "",
        "disguise_skill_n1": "",
        "disguise_skill_n2": "",
        "disguise_edge_n0": "",
        "smarts_skill_n0": "",
        "smarts_skill_n1": "",
        "smarts_skill_n2": "",
        "smarts_skill_n3": "",
        "smarts_skill_n4": "",
        "smarts_skill_n5": "",
        "smarts_skill_n6": "",
        "smarts_op_n0": "",
        "smarts_op_n1": "",
        "smarts_op_n2": "",
        "smarts_op_n3": "",
        "control_skill_n0": "",
        "control_skill_n1": "",
        "control_skill_n2": "",
        "control_edge_n0": "",
        "knowledge_skill_n0": "",
        "knowledge_skill_n1": "",
        "knowledge_skill_n2": "",
        "knowledge_edge_n0": "",
        "sandman_skill_n0": "",
        "sandman_skill_n1": "",
        "sandman_skill_n2": "",
        "sandman_skill_n3": "",
        "sandman_skill_n4": "",
        "sandman_skill_n5": "",
        "sandman_skill_n6": "",
        "sandman_trait_n0": "",
        "perception_skill_n0": "",
        "perception_skill_n1": "",
        "perception_skill_n2": "",
        "perception_edge_n0": "",
        "streetwise_skill_n0": "",
        "streetwise_skill_n1": "",
        "streetwise_skill_n2": "",
        "streetwise_edge_n0": "",
        "psychology_skill_n0": "",
        "psychology_skill_n1": "",
        "psychology_skill_n2": "",
        "psychology_edge_n0": "",
        "weaver_skill_n0": "",
        "weaver_skill_n1": "",
        "weaver_skill_n2": "",
        "weaver_skill_n3": "",
        "weaver_skill_n4": "",
        "weaver_skill_n5": "",
        "weaver_skill_n6": "",
        "weaver_trait_n0": "",
        "hardtech_skill_n0": "",
        "hardtech_skill_n1": "",
        "hardtech_skill_n2": "",
        "hardtech_edge_n0": "",
        "hacking_skill_n0": "",
        "hacking_skill_n1": "",
        "hacking_skill_n2": "",
        "hacking_edge_n0": "",
        "medic_skill_n0": "",
        "medic_skill_n1": "",
        "medic_skill_n2": "",
        "medic_edge_n0": "",
        "resources_skill_n0": "",
        "resources_skill_n1": "",
        "resources_skill_n2": "",
        "resources_skill_n3": "",
        "resources_skill_n4": "",
        "resources_skill_n5": "",
        "resources_skill_n6": "",
        "resources_op_n0": "",
        "resources_op_n1": "",
        "resources_op_n2": "",
        "resources_op_n3": "",
        "influence_skill_n0": "",
        "influence_skill_n1": "",
        "influence_skill_n2": "",
        "influence_edge_n0": "",
        "network_skill_n0": "",
        "network_skill_n1": "",
        "network_skill_n2": "",
        "network_edge_n0": "",
        "mouth_skill_n0": "",
        "mouth_skill_n1": "",
        "mouth_skill_n2": "",
        "mouth_skill_n3": "",
        "mouth_skill_n4": "",
        "mouth_skill_n5": "",
        "mouth_skill_n6": "",
        "mouth_trait_n0": "",
        "persuade_skill_n0": "",
        "persuade_skill_n1": "",
        "persuade_skill_n2": "",
        "persuade_edge_n0": "",
        "intimidate_skill_n0": "",
        "intimidate_skill_n1": "",
        "intimidate_skill_n2": "",
        "intimidate_edge_n0": "",
        "leadership_skill_n0": "",
        "leadership_skill_n1": "",
        "leadership_skill_n2": "",
        "leadership_edge_n0": "",
        "vapour_skill_n0": "",
        "vapour_skill_n1": "",
        "vapour_skill_n2": "",
        "vapour_skill_n3": "",
        "vapour_skill_n4": "",
        "vapour_skill_n5": "",
        "vapour_skill_n6": "",
        "vapour_trait_n0": "",
        "groundcraft_skill_n0": "",
        "groundcraft_skill_n1": "",
        "groundcraft_skill_n2": "",
        "groundcraft_edge_n0": "",
        "aircraft_skill_n0": "",
        "aircraft_skill_n1": "",
        "aircraft_skill_n2": "",
        "aircraft_edge_n0": "",
        "spacecraft_skill_n0": "",
        "spacecraft_skill_n1": "",
        "spacecraft_skill_n2": "",
        "spacecraft_edge_n0": "",
        "wyld_skill_n0": "",
        "wyld_skill_n1": "",
        "wyld_skill_n2": "",
        "wyld_skill_n3": "",
        "wyld_skill_n4": "",
        "wyld_skill_n5": "",
        "wyld_skill_n6": "",
        "wyld_op_n0": "",
        "wyld_op_n1": "",
        "wyld_op_n2": "",
        "wyld_op_n3": "",
        "resistance_skill_n0": "",
        "resistance_skill_n1": "",
        "resistance_skill_n2": "",
        "resistance_edge_n0": "",
        "sense_skill_n0": "",
        "sense_skill_n1": "",
        "sense_skill_n2": "",
        "sense_edge_n0": "",
        "echo1_name_n0": "",
        "echo1_skill_n0": "",
        "echo1_skill_n1": "",
        "echo1_skill_n2": "",
        "echo1_skill_n3": "",
        "echo1_skill_n4": "",
        "echo1_skill_n5": "",
        "echo1_skill_n6": "",
        "echo1_trait_n0": "",
        "attack1_skill_n0": "",
        "attack1_skill_n1": "",
        "attack1_skill_n2": "",
        "attack1_edge_n0": "",
        "manipulation1_skill_n0": "",
        "manipulation1_skill_n1": "",
        "manipulation1_skill_n2": "",
        "manipulation1_edge_n0": "",
        "nature1_skill_n0": "",
        "nature1_skill_n1": "",
        "nature1_skill_n2": "",
        "nature1_edge_n0": "",
        "echo2_name_n0": "",
        "echo2_skill_n0": "",
        "echo2_skill_n1": "",
        "echo2_skill_n2": "",
        "echo2_skill_n3": "",
        "echo2_skill_n4": "",
        "echo2_skill_n5": "",
        "echo2_skill_n6": "",
        "echo2_trait_n0": "",
        "attack2_skill_n0": "",
        "attack2_skill_n1": "",
        "attack2_skill_n2": "",
        "attack2_edge_n0": "",
        "manipulation2_skill_n0": "",
        "manipulation2_skill_n1": "",
        "manipulation2_skill_n2": "",
        "manipulation2_edge_n0": "",
        "nature2_skill_n0": "",
        "nature2_skill_n1": "",
        "nature2_skill_n2": "",
        "nature2_edge_n0": "",
        "divinity_skill_n0": "",
        "divinity_skill_n1": "",
        "divinity_skill_n2": "",
        "divinity_skill_n3": "",
        "divinity_skill_n4": "",
        "divinity_skill_n5": "",
        "divinity_skill_n6": "",
        "divinity_op_n0": "",
        "divinity_op_n1": "",
        "divinity_op_n2": "",
        "divinity_op_n3": "",
        "faith_skill_n0": "",
        "faith_skill_n1": "",
        "faith_skill_n2": "",
        "faith_edge_n0": "",
        "invocation_skill_n0": "",
        "invocation_skill_n1": "",
        "invocation_skill_n2": "",
        "invocation_edge_n0": "",
        "spec_mastery1_name_n0": "",
        "spec_mastery1_skill_n0": "",
        "spec_mastery1_skill_n1": "",
        "spec_mastery1_skill_n2": "",
        "spec_mastery1_skill_n3": "",
        "spec_mastery1_skill_n4": "",
        "spec_mastery1_skill_n5": "",
        "spec_mastery1_edge_n0": "",
        "spec_mastery1_edge_n1": "",
        "spec_mastery1_edge_n2": "",
        "spec_mastery2_name_n0": "",
        "spec_mastery2_skill_n0": "",
        "spec_mastery2_skill_n1": "",
        "spec_mastery2_skill_n2": "",
        "spec_mastery2_skill_n3": "",
        "spec_mastery2_skill_n4": "",
        "spec_mastery2_skill_n5": "",
        "spec_mastery2_edge_n0": "",
        "spec_mastery2_edge_n1": "",
        "spec_mastery2_edge_n2": "",
        "spec_mastery3_name_n0": "",
        "spec_mastery3_skill_n0": "",
        "spec_mastery3_skill_n1": "",
        "spec_mastery3_skill_n2": "",
        "spec_mastery3_skill_n3": "",
        "spec_mastery3_skill_n4": "",
        "spec_mastery3_skill_n5": "",
        "spec_mastery3_edge_n0": "",
        "spec_mastery3_edge_n1": "",
        "spec_mastery3_edge_n2": "",
        "earned_edge_n0": "",
        "earned_edge_n1": "",
        "earned_edge_n2": "",
        "earned_edge_n3": "",
        "earned_edge_n4": "",
        "earned_trait_n0": "",
        "earned_trait_n1": "",
        "earned_trait_n2": "",
        "earned_trait_n3": "",
        "earned_trait_n4": "",
        "team_edge_n0": "",
        "team_edge_n1": "",
        "team_edge_n2": "",
        "team_edge_n3": "",
        "team_edge_n4": "",
        "team_trait_n0": "",
        "team_trait_n1": "",
        "team_trait_n2": "",
        "team_trait_n3": "",
        "team_trait_n4": "",
        "temporary_edge_n0": "",
        "temporary_edge_n1": "",
        "temporary_edge_n2": "",
        "temporary_edge_n3": "",
        "temporary_edge_n4": "",
        "temporary_trait_n0": "",
        "temporary_trait_n1": "",
        "temporary_trait_n2": "",
        "temporary_trait_n3": "",
        "temporary_trait_n4": "",
        "environmental_trait_n0": "",
        "environmental_trait_n1": "",
        "environmental_trait_n2": "",
        "environmental_trait_n3": "",
        "environmental_trait_n4": "",
        "s_bodyweb_comp_n0": "",
        "s_headlink_comp_n0": "",
        "s_optics_comp_n0": "",
        "s_neural_rewiring_comp_n0": "",
        "s_biosculpting_comp_n0": "",
        "s_nanocore_comp_n0": "",
        "s_biocore_comp_n0": "",
        "bodyweb_n0": "",
        "chemjet_n0": "",
        "cnsbooster_n0": "",
        "dermalplate_n0": "",
        "monoclaws_n0": "",
        "steelmuscles_n0": "",
        "bodystash_n0": "",
        "headlink_n0": "",
        "combatlink_n0": "",
        "dronelink_n0": "",
        "nervelink_n0": "",
        "neuralcomm_n0": "",
        "socialanalyser_n0": "",
        "vcs_n0": "",
        "optics_n0": "",
        "brainbooster_n0": "",
        "eagleeye_n0": "",
        "forensicscanner_n0": "",
        "taclink_n0": "",
        "thermalimaging_n0": "",
        "threatanalyser_n0": "",
        "neuralrewiring_n0": "",
        "audiowire_n0": "",
        "decrypter_n0": "",
        "godlink_n0": "",
        "weaveview_n0": "",
        "weavelink_n0": "",
        "ultrasonics_n0": "",
        "biosculpting_n0": "",
        "decentralisedheart_n0": "",
        "dns_n0": "",
        "magnaview_n0": "",
        "pharm_n0": "",
        "musclefibers_n0": "",
        "oxycycler_n0": "",
        "nanocore_n0": "",
        "chameleonfield_n0": "",
        "ecmcloak_n0": "",
        "escapegas_n0": "",
        "nanoarmour_n0": "",
        "nbsu_n0": "",
        "nanoregen_n0": "",
        "biocore_n0": "",
        "aquashift_n0": "",
        "beautifier_n0": "",
        "cloneorgan_n0": "",
        "pheromones_n0": "",
        "stressshift_n0": "",
        "voicecontrol_n0": "",
        "soulweaving_n0": "",
        "soulweaving_n1": "",
        "soulweaving_n2": "",
        "soulweaving_n3": "",
        "soulweaving_n4": "",
        "rune_enchantment_n0": "",
        "rune_enchantment_n1": "",
        "rune_enchantment_n2": "",
        "rune_enchantment_n3": "",
        "rune_enchantment_n4": "",
        "drug_toxin_n0": "",
        "drug_toxin_n1": "",
        "drug_toxin_n2": "",
        "drug_toxin_n3": "",
        "drug_toxin_n4": "",
        "drug_toxin_n5": "",
        "physical_wound_n0": "",
        "physical_wound_n1": "",
        "physical_wound_n2": "",
        "smarts_wound_n0": "",
        "smarts_wound_n1": "",
        "smarts_wound_n2": "",
        "resources_wound_n0": "",
        "resources_wound_n1": "",
        "resources_wound_n2": "",
        "wyld_wound_n0": "",
        "wyld_wound_n1": "",
        "wyld_wound_n2": "",
        "divinity_wound_n0": "",
        "divinity_wound_n1": "",
        "divinity_wound_n2": "",
        "vehicle_wound_n0": "",
        "vehicle_wound_n1": "",
        "vehicle_wound_n2": "",
        "physical_injury_n0": "",
        "physical_injury_n1": "",
        "physical_injury_n2": "",
        "physical_injury_n3": "",
        "physical_injury_n4": "",
        "physical_injury_n5": "",
        "physical_injury_n6": "",
        "physical_injury_n7": "",
        "physical_injury_n8": "",
        "physical_injury_n9": "",
        "physical_injury_n10": "",
        "physical_injury_n11": "",
        "smarts_injury_n0": "",
        "smarts_injury_n1": "",
        "smarts_injury_n2": "",
        "smarts_injury_n3": "",
        "smarts_injury_n4": "",
        "smarts_injury_n5": "",
        "smarts_injury_n6": "",
        "smarts_injury_n7": "",
        "smarts_injury_n8": "",
        "smarts_injury_n9": "",
        "smarts_injury_n10": "",
        "smarts_injury_n11": "",
        "resources_injury_n0": "",
        "resources_injury_n1": "",
        "resources_injury_n2": "",
        "resources_injury_n3": "",
        "resources_injury_n4": "",
        "resources_injury_n5": "",
        "resources_injury_n6": "",
        "resources_injury_n7": "",
        "resources_injury_n8": "",
        "resources_injury_n9": "",
        "resources_injury_n10": "",
        "resources_injury_n11": "",
        "wyld_injury_n0": "",
        "wyld_injury_n1": "",
        "wyld_injury_n2": "",
        "wyld_injury_n3": "",
        "wyld_injury_n4": "",
        "wyld_injury_n5": "",
        "wyld_injury_n6": "",
        "wyld_injury_n7": "",
        "wyld_injury_n8": "",
        "wyld_injury_n9": "",
        "wyld_injury_n10": "",
        "wyld_injury_n11": "",
        "divinity_injury_n0": "",
        "divinity_injury_n1": "",
        "divinity_injury_n2": "",
        "divinity_injury_n3": "",
        "divinity_injury_n4": "",
        "divinity_injury_n5": "",
        "divinity_injury_n6": "",
        "divinity_injury_n7": "",
        "divinity_injury_n8": "",
        "divinity_injury_n9": "",
        "divinity_injury_n10": "",
        "divinity_injury_n11": "",
        "corruption_injury_n0": "",
        "corruption_injury_n1": "",
        "corruption_injury_n2": "",
        "corruption_injury_n3": "",
        "corruption_injury_n4": "",
        "corruption_injury_n5": "",
        "corruption_injury_n6": "",
        "corruption_injury_n7": "",
        "corruption_injury_n8": "",
        "corruption_injury_n9": "",
        "corruption_injury_n10": "",
        "corruption_injury_n11": "",
        "geas_injury_n0": "",
        "geas_injury_n1": "",
        "geas_injury_n2": "",
        "geas_injury_n3": "",
        "geas_injury_n4": "",
        "geas_injury_n5": "",
        "geas_injury_n6": "",
        "geas_injury_n7": "",
        "geas_injury_n8": "",
        "geas_injury_n9": "",
        "geas_injury_n10": "",
        "geas_injury_n11": "",
        "vehicle_injury_n0": "",
        "vehicle_injury_n1": "",
        "vehicle_injury_n2": "",
        "vehicle_injury_n3": "",
        "vehicle_injury_n4": "",
        "vehicle_injury_n5": "",
        "vehicle_injury_n6": "",
        "vehicle_injury_n7": "",
        "vehicle_injury_n8": "",
        "vehicle_injury_n9": "",
        "vehicle_injury_n10": "",
        "vehicle_injury_n11": "",
    }


class LiveCharacterModel(BaseModel):
    """This is the compiled and live character as calculated from the mod_ids and other info in the CharacterModel.
    Leave nothing as Optional[str/list etc.] unless you are happy for it to have a default value of null!!!"""

    def __init__(self, **kwargs):
        super(LiveCharacterModel, self).__init__(**kwargs)

    # CHARACTER INFO
    live_char_id: int
    char_id: int
    deleted: bool = False
    char_name: Optional[str]
    player_name: Optional[str]
    player_id: int
    char_archetype: Optional[str]
    char_type: str = "Character"
    char_age: int = 18
    char_gender: str = ""
    char_description: str = ""
    char_picture: str = ""
    gamedata_name: str = ""
    breed_name: str = "Human"
    culture: str = "Truean"

    # TALENT POINTS
    tp_total: int = 0
    tp_spent: int = 0
    tp_unspent: int = 0
    tp_create: int = 30
    tp_missions: int = 0
    tp_bonus: int = 0
    breed_tp_spent: int = 0
    breed_tp_bonus: int = 0

    # TIMESTAMPS
    char_created: Optional[datetime]
    char_modified: Optional[datetime]

    # DISCIPLE
    pledged_disciple: str = ""
    syncretic_disciple: Optional[str]
    avatar: Optional[str]
    gift_curses: str = ""
    allow_soulweaving: bool = False
    allow_runes: bool = False
    total_corruption: int = 0
    corruption: int = 0
    soulweaving: Optional[str]
    heresies: list = []
    geas: list = []
    rune_enchantments: list = []
    blessings: list = []
    bound_rezhadi: list = []
    corruption_extra: int = 0
    corruption_mult: int = 1  # Multiplier for Wyld Cancer received from SID etc
    corruption_perm_threshold: int = 20  # Corruption Cancer per Perm. Divinity Injury?
    corruption_perm_injuries_count: int = 0
    healed_corruption_perm_injuries: int = 0
    corruption_perm_injuries: list = []  # List of Corruption Injuries

    # LANGUAGES
    total_languages: int = 0  # Total number of languages known by char
    bonus_languages: int = 0  # How many languages beyond 1 should they get
    language_count: int = 0
    language: str = ""
    lang_standard: bool = True
    lang_zani: bool = False
    lang_arish: bool = False
    lang_jenis: bool = False
    lang_gethan: bool = False
    lang_chigo: bool = False
    lang_extasian: bool = False
    lang_kapaethjan: bool = False
    lang_sarov: bool = False
    lang_kanchurian: bool = False
    lang_divine: bool = False
    lang_atropoan: bool = False
    lang_guttertalk: bool = False
    lang_high_extasian: bool = False
    lang_ballaen: bool = False
    lang_rezhadi: bool = False
    lang_other: bool = False
    lang_other_name: Optional[str]

    # WYLD CANCER
    wyld_cancer_total: int = 0  # Total Wyld Cancer
    wyld_cancer: int = 0  # Wyld Cancer from Sliverware etc
    wyld_cancer_extra: int = (
        0  # Wyld Cancer received from Wylding, Echo Power Use and environmental effects
    )
    wyld_cancer_mult: int = 1  # Multiplier for Wyld Cancer received from SID etc
    wyld_cancer_perm_threshold: int = 20  # Wyld Cancer per Perm. Wyld Injury?
    wyld_perm_injuries_count: int = 0
    healed_wyld_perm_injuries: int = (
        0  # How many Permanent Wyld Injuries have been healed by Isoke?
    )
    wyld_perm_injuries: list = []  # List of Wyld Injuries

    # GEAR AND MISSIONS
    weapons: dict = {}
    gear: dict = {}
    char_missions: dict = {}
    char_contacts: dict = {}
    weapons_note: str = ""  # String of all weapons
    gear_note: str = ""  # String of all gear
    char_missions_note: str = ""  # String of all missions
    char_contacts_note: str = ""  # String of all contacts

    # SOCIAL AND CAREER
    citizen: str = ""
    social_class: str = ""
    lifestyle: str = ""
    lifestyle_change: int = 0
    organisation: str = ""
    rank: str = ""
    rank_list: str = ""
    rank_bonus: int = 0
    commendations: int = 0
    reprimands: int = 0
    reputation: int = 0

    # EDGES AND TRAITS
    edges_note: str = ""  # String of all character's Edges
    traits_note: str = ""  # String of all character's Traits
    team_edges_note: str = ""  # String of all character's Team Edges
    team_traits_note: str = ""  # String of all character's Team Traits
    temporary_edges_note: str = ""  # String of all character's Temporary Edges
    temporary_traits_note: str = ""  # String of all character's Temporary Traits
    environmental_traits_note: str = ""
    remove_limit: list = []
    remove_trait: list = []
    valid_edge: list = []
    valid_trait: list = []
    creature_edges: bool = False

    # SLIVERWARE
    allow_bioware: bool = False
    sliverware_note: str = ""  # String of all character's Sliverware
    sliverware_failure: int = 0
    s_bodyweb_comp: int = 0
    s_headlink_comp: int = 0
    s_optics_comp: int = 0
    s_neural_rewiring_comp: int = 0
    s_biosculpting_comp: int = 0
    s_nanocore_comp: int = 0
    s_biocore_comp: int = 0
    sliver_bodyweb: bool = False
    sliver_chemjet: bool = False
    sliver_cnsbooster: bool = False
    sliver_dermalplate: bool = False
    sliver_monoclaws: bool = False
    sliver_steelmuscles: bool = False
    sliver_bodystash: bool = False
    sliver_headlink: bool = False
    sliver_combatlink: bool = False
    sliver_dronelink: bool = False
    sliver_nervelink: bool = False
    sliver_neuralcomm: bool = False
    sliver_socialanalyser: bool = False
    sliver_vcs: bool = False
    sliver_optics: bool = False
    sliver_brainbooster: bool = False
    sliver_eagleeye: bool = False
    sliver_forensicscanner: bool = False
    sliver_taclink: bool = False
    sliver_thermalimaging: bool = False
    sliver_threatanalyser: bool = False
    sliver_neuralrewiring: bool = False
    sliver_audiowire: bool = False
    sliver_decrypter: bool = False
    sliver_godlink: bool = False
    sliver_weaveview: bool = False
    sliver_weavelink: bool = False
    sliver_ultrasonics: bool = False
    sliver_biosculpting: bool = False
    sliver_decentralisedheart: bool = False
    sliver_dns: bool = False
    sliver_magnaview: bool = False
    sliver_pharm: bool = False
    sliver_musclefibers: bool = False
    sliver_oxycycler: bool = False
    sliver_nanocore: bool = False
    sliver_chameleonfield: bool = False
    sliver_ecmcloak: bool = False
    sliver_escapegas: bool = False
    sliver_nanoarmour: bool = False
    sliver_nbsu: bool = False
    sliver_nanoregen: bool = False
    sliver_biocore: bool = False
    sliver_aquashift: bool = False
    sliver_beautifier: bool = False
    sliver_cloneorgan: bool = False
    sliver_pheromones: bool = False
    sliver_stressshift: bool = False
    sliver_voicecontrol: bool = False

    # PHYSICAL
    physical: int = 0
    physical_actual: int = 0
    physical_limit: int = 0
    physical_dl: int = 0
    athletics: int = 0
    athletics_limit: int = 0
    athletics_dl: int = 0
    endurance: int = 0
    endurance_limit: int = 0
    endurance_dl: int = 0

    # KILLER
    killer: int = 0
    killer_actual: int = 0
    killer_limit: int = 0
    killer_dl: int = 0
    energy: int = 0
    energy_limit: int = 0
    energy_dl: int = 0
    guns: int = 0
    guns_limit: int = 0
    guns_dl: int = 0
    melee: int = 0
    melee_limit: int = 0
    melee_dl: int = 0

    # CLOAK
    cloak: int = 0
    cloak_actual: int = 0
    cloak_limit: int = 0
    cloak_dl: int = 0
    con: int = 0
    con_limit: int = 0
    con_dl: int = 0
    disguise: int = 0
    disguise_limit: int = 0
    disguise_dl: int = 0
    sneak: int = 0
    sneak_limit: int = 0
    sneak_dl: int = 0

    # SMARTS
    smarts: int = 0
    smarts_actual: int = 0
    smarts_limit: int = 0
    smarts_dl: int = 0
    control: int = 0
    control_limit: int = 0
    control_dl: int = 0
    knowledge: int = 0
    knowledge_limit: int = 0
    knowledge_dl: int = 0

    # SANDMAN
    sandman: int = 0
    sandman_actual: int = 0
    sandman_limit: int = 0
    sandman_dl: int = 0
    perception: int = 0
    perception_limit: int = 0
    perception_dl: int = 0
    psychology: int = 0
    psychology_limit: int = 0
    psychology_dl: int = 0
    streetwise: int = 0
    streetwise_limit: int = 0
    streetwise_dl: int = 0

    # WEAVER
    weaver: int = 0
    weaver_actual: int = 0
    weaver_limit: int = 0
    weaver_dl: int = 0
    hardtech: int = 0
    hardtech_limit: int = 0
    hardtech_dl: int = 0
    medic: int = 0
    medic_limit: int = 0
    medic_dl: int = 0
    hacking: int = 0
    hacking_limit: int = 0
    hacking_dl: int = 0

    # RESOURCES
    resources: int = 0
    resources_actual: int = 0
    resources_limit: int = 0
    resources_dl: int = 0
    network: int = 0
    network_limit: int = 0
    network_dl: int = 0
    influence: int = 0
    influence_limit: int = 0
    influence_dl: int = 0

    # MOUTH
    mouth: int = 0
    mouth_actual: int = 0
    mouth_limit: int = 0
    mouth_dl: int = 0
    intimidate: int = 0
    intimidate_limit: int = 0
    intimidate_dl: int = 0
    leadership: int = 0
    leadership_limit: int = 0
    leadership_dl: int = 0
    persuade: int = 0
    persuade_limit: int = 0
    persuade_dl: int = 0

    # VAPOUR
    vapour: int = 0
    vapour_actual: int = 0
    vapour_limit: int = 0
    vapour_dl: int = 0
    aircraft: int = 0
    aircraft_limit: int = 0
    aircraft_dl: int = 0
    groundcraft: int = 0
    groundcraft_limit: int = 0
    groundcraft_dl: int = 0
    spacecraft: int = 0
    spacecraft_limit: int = 0
    spacecraft_dl: int = 0

    # WYLD
    wyld: int = 0
    wyld_actual: int = 0
    wyld_limit: int = 0
    wyld_dl: int = 0
    wylding: int = 0
    resistance: int = 0
    resistance_limit: int = 0
    resistance_dl: int = 0
    sense: int = 0
    sense_limit: int = 0
    sense_dl: int = 0

    # GENERAL ECHO
    allow_echo: int = 0
    allow_echo1: bool = False
    allow_echo2: bool = False
    echo_names: Optional[list]
    echo1_name: Optional[str]
    echo2_name: Optional[str]
    magnitude: int = 0
    echo_max_dl: int = 0
    echo_wyld_cancer: int = 0
    echo_wyld_damage: int = 0

    # ECHO1
    echo1: Optional[int]
    echo1_actual: int = 0
    echo1_limit: int = 0
    echo1_dl: int = 0
    attack1: Optional[int]
    attack1_limit: int = 0
    attack1_dl: int = 0
    manipulation1: Optional[int]
    manipulation1_limit: int = 0
    manipulation1_dl: int = 0
    nature1: Optional[int]
    nature1_limit: int = 0
    nature1_dl: int = 0

    # ECHO2
    echo2: Optional[int]
    echo2_actual: int = 0
    echo2_limit: int = 0
    echo2_dl: int = 0
    attack2: Optional[int]
    attack2_limit: int = 0
    attack2_dl: int = 0
    manipulation2: Optional[int]
    manipulation2_limit: int = 0
    manipulation2_dl: int = 0
    nature2: Optional[int]
    nature2_limit: int = 0
    nature2_dl: int = 0

    # DIVINITY
    divinity: int = 0
    divinity_actual: int = 0
    divinity_limit: int = 0
    divinity_dl: int = 0
    faith: int = 0
    faith_limit: int = 0
    faith_dl: int = 0
    invocation: int = 0
    invocation_limit: int = 0
    invocation_dl: int = 0
    allow_syncretic_disciple: bool = False
    allow_gifts: bool = True

    # VEHICLE
    ai_online: bool = True
    comms_online: bool = True
    stealth_online: bool = True
    stealth: int = 0
    stealth_dl: int = 0
    sensors_online: bool = True
    sensors: int = 0
    sensors_dl: int = 0
    piloting_dl: int = 0
    heat_cap: int = 0
    scom: int = 0
    action_cap: int = 0
    grav_drive: int = 0
    wyld_shield: bool = False
    wyld_sensors: bool = False
    wyld_sensors_online: bool = True
    heat: int = 0
    heat_modifier: int = 0
    heat_reset: bool = False
    spacecraft_zone: str = ""

    # VEHICLE DEBUG
    injury_size: str = ""
    repair_skill: str = ""

    # OPPORTUNITIES
    allow_op_use: bool = True
    allow_op_healing: bool = True
    allow_op_rerolls: bool = True
    allow_op_plus2: bool = True
    allow_op_plus1: bool = True
    allow_physical_op_healing: bool = True
    allow_smarts_op_healing: bool = True
    allow_resources_op_healing: bool = True
    allow_wyld_op_healing: bool = True
    allow_divinity_op_healing: bool = True
    physical_op: int = 0
    smarts_op: int = 0
    resources_op: int = 0
    wyld_op: int = 0
    divinity_op: int = 0
    temporary_op: int = 0
    combat_op: int = 0
    overlord_op: int = 0
    mook_op: int = 0
    team_op: int = 0

    # ARMOUR & HEALTH VALUES
    physical_wt: int = 0
    physical_wt_bonus: int = 0
    physical_dam_mult: int = 0
    physical_av: int = 0
    physical_av_actual: int = 0
    physical_av_max: int = 12
    physical_av_min: int = 2
    smarts_wt: int = 0
    smarts_wt_bonus: int = 0
    smarts_dam_mult: int = 0
    smarts_av: int = 0
    smarts_av_actual: int = 0
    smarts_av_max: int = 6
    smarts_av_min: int = 2
    resources_wt: int = 0
    resources_wt_bonus: int = 0
    resources_dam_mult: int = 0
    resources_av: int = 0
    resources_av_actual: int = 0
    resources_av_max: int = 6
    resources_av_min: int = 2
    wyld_wt: int = 0
    wyld_wt_bonus: int = 0
    wyld_dam_mult: int = 0
    wyld_av: int = 0
    wyld_av_actual: int = 0
    wyld_av_max: int = 6
    wyld_av_min: int = 2
    divinity_wt: int = 0
    divinity_wt_bonus: int = 0
    divinity_dam_mult: int = 0
    divinity_av: int = 0
    divinity_av_actual: int = 0
    divinity_av_max: int = 6
    divinity_av_min: int = 2
    vehicle_wt: int = 0
    vehicle_wt_bonus: int = 0
    vehicle_dam_mult: int = 0
    vehicle_av: int = 0
    vehicle_av_actual: int = 0
    vehicle_av_max: int = 12
    vehicle_av_min: int = 2
    mook_wt: int = 0
    mook_wt_bonus: int = 0
    mook_dam_mult: int = 0
    stabilise: int = 0
    survival: int = 0

    # DAMAGE VALUES
    physical_dt: int = 0
    physical_wounds: int = 0
    physical_injuries: list = []
    physical_dam_max: bool = False
    smarts_dt: int = 0
    smarts_wounds: int = 0
    smarts_injuries: list = []
    smarts_dam_max: bool = False
    resources_dt: int = 0
    resources_wounds: int = 0
    resources_injuries: list = []
    resources_dam_max: bool = False
    wyld_dt: int = 0
    wyld_wounds: int = 0
    wyld_injuries: list = []
    wyld_dam_max: bool = False
    divinity_dt: int = 0
    divinity_wounds: int = 0
    divinity_injuries: list = []
    divinity_dam_max: bool = False
    mook_wounds: int = 0
    vehicle_dt: int = 0
    vehicle_wounds: int = 0
    vehicle_injuries: list = []
    vehicle_dam_max: bool = False

    # SPECIAL DAMAGE
    stun_duration: int = 0
    emp_duration: int = 0
    mortal_wound: bool = False
    stabilised: bool = True

    # IMMUNITIES
    physical_immunity: bool = False
    smarts_immunity: bool = False
    resources_immunity: bool = False
    wyld_immunity: bool = False
    divinity_immunity: bool = False
    stun_immunity: bool = False
    emp_immunity: bool = False
    toxin_immunity: bool = False
    intimidate_immunity: bool = False
    heat_immunity: bool = False
    fire_immunity: bool = False
    echo_immunity: bool = False
    corruption_immunity: bool = False
    soulweaving_immunity: bool = False

    # HEALiING AND RESISTANCES
    healing_dl: int = 0
    resist_toxin: int = 0
    resist_toxin_limit: int = 0
    resist_toxin_dl: int = 0
    resist_emp: int = 0
    resist_emp_limit: int = 0
    resist_emp_dl: int = 0
    resist_stun: int = 0
    resist_stun_limit: int = 0
    resist_stun_dl: int = 0
    resist_intimidate: int = 0
    resist_intimidate_limit: int = 0
    resist_intimidate_dl: int = 0
    resist_echo: int = 0
    resist_echo_limit: int = 0
    resist_echo_dl: int = 0
    resist_wyld: int = 0
    resist_wyld_limit: int = 0
    resist_wyld_dl: int = 0
    resist_corruption: int = 0
    resist_soulweaving: int = 0
    resist_soulweaving_dl: int = 0

    # GENERAL DEFENCE
    defence: int = 0

    # AVAILABILITY
    availability: int = 0
    availability_limit: int = 0
    availability_dl: int = 0

    # OTHER SKILLS
    scale: int = 1
    scale_actual: int = 1
    scale_dl: int = 0
    scale_limit: int = 0
    speed: int = 1
    speed_actual: int = 1
    speed_dl: int = 0
    speed_limit: int = 0
    initiative: int = 0
    initiative_bonus: int = 0
    initiative_dl: int = 0
    initiative_limit: int = 0  # Max Initiative
    initiative_note: str = ""

    # SPECIALISATION MASTERIES
    smx_name1: str = ""
    smx_name2: str = ""
    smx_name3: str = ""
    smx1: int = 0
    smx2: int = 0
    smx3: int = 0

    # BOOSTS AND COMPLICATIONS
    complications: list = []
    boosts: list = []

    # NOTES
    physical_note: str = ""
    killer_note: str = ""
    cloak_note: str = ""
    smarts_note: str = ""
    sandman_note: str = ""
    weaver_note: str = ""
    resources_note: str = ""
    mouth_note: str = ""
    vapour_note: str = ""
    wyld_note: str = ""
    echo_note: str = ""
    divinity_note: str = ""
    gift_curses_note: str = ""
    general_note: str = ""
    vehicle_note: str = ""
    mook_note: str = ""
    injury_note: str = ""
    sc_injury_note: str = ""
    wound_note: str = ""
    perm_wyld_injury_note: str = ""
    warning_note: str = ""
    character_note: str = ""
    gm_note: str = ""

    # PLAYER NOTES
    player_note: str = ""
    pledged_disciple_note: str = ""
    mission_note: str = ""
    contacts_allies_enemies_note: str = ""
    soulweaving_note: str = ""
    heresies_note: str = ""
    geas_note: str = ""
    blessings_note: str = ""
    corruption_note: str = ""
    perm_corruption_injury_note: str = ""

    # SYSTEM
    # This keeps track of what mod_ids have been applied to the character to prevent repetition
    applied_mods: list = []

    # %TEXT% REPLACEMENT
    # This is for replacing %TEXT% in mod_ids at specific mod_location with replacement_text
    # In form text_replace_mods:{"mod_location": {"mod_id": "replacement_text"}
    text_replace_mods: dict = {}

    sliver_complete: dict = {
        "s_bodyweb_comp_n0": "",
        "s_headlink_comp_n0": "",
        "s_optics_comp_n0": "",
        "s_neural_rewiring_comp_n0": "",
        "s_biosculpting_comp_n0": "",
        "s_nanocore_comp_n0": "",
        "s_biocore_comp_n0": "",
    }

    # DEBUG
    replace_text: str = ""
    custom: str = ""
    injury_try: str = ""
    twin: str = ""
    parent: str = ""
    children: str = ""

    # TOUCHED BY -> There should be one of these for each mutable value. Should this be a dynamic dict instead?
    text_replace_mods_touched_by: str = ""
    sliver_complete_touched_by: str = ""
    gamedata_name_touched_by: str = ""
    breed_name_touched_by: str = ""
    culture_touched_by: str = ""
    pledged_disciple_touched_by: str = ""
    syncretic_disciple_touched_by: str = ""
    avatar_touched_by: str = ""
    gift_curses_touched_by: str = ""
    allow_soulweaving_touched_by: str = ""
    allow_runes_touched_by: str = ""
    total_corruption_touched_by: str = ""
    corruption_touched_by: str = ""
    soulweaving_touched_by: str = ""
    heresies_touched_by: str = ""
    geas_touched_by: str = ""
    rune_enchantments_touched_by: str = ""
    blessings_touched_by: str = ""
    bound_rezhadi_touched_by: str = ""
    corruption_extra_touched_by: str = ""
    corruption_mult_touched_by: str = ""
    corruption_perm_threshold_touched_by: str = ""
    corruption_perm_injuries_count_touched_by: str = ""
    healed_corruption_perm_injuries_touched_by: str = ""
    corruption_perm_injuries_touched_by: str = ""

    # Languages touched...
    language_touched_by: str = ""
    total_languages_touched_by: str = "Base = 2"
    bonus_languages_touched_by: str = ""
    language_count_touched_by: str = ""
    lang_standard_touched_by: str = ""
    lang_zani_touched_by: str = ""
    lang_arish_touched_by: str = ""
    lang_jenis_touched_by: str = ""
    lang_gethan_touched_by: str = ""
    lang_chigo_touched_by: str = ""
    lang_extasian_touched_by: str = ""
    lang_kapaethjan_touched_by: str = ""
    lang_sarov_touched_by: str = ""
    lang_kanchurian_touched_by: str = ""
    lang_divine_touched_by: str = ""
    lang_atropoan_touched_by: str = ""
    lang_guttertalk_touched_by: str = ""
    lang_high_extasian_touched_by: str = ""
    lang_ballaen_touched_by: str = ""
    lang_rezhadi_touched_by: str = ""
    lang_other_touched_by: str = ""

    # Talent Points touched...
    tp_spent_touched_by: str = ""
    tp_bonus_touched_by: str = ""
    tp_create_touched_by: str = ""
    tp_missions_touched_by: str = ""
    tp_unspent_touched_by: str = ""
    tp_total_touched_by: str = "Base = 30"
    breed_tp_spent_touched_by: str = ""
    breed_tp_bonus_touched_by: str = ""

    # Wyld Cancer touched...
    wyld_cancer_total_touched_by: str = ""
    wyld_cancer_touched_by: str = ""
    wyld_cancer_extra_touched_by: str = ""
    wyld_cancer_mult_touched_by: str = ""
    wyld_cancer_perm_threshold_touched_by: str = ""
    wyld_perm_injuries_count_touched_by: str = ""
    healed_wyld_perm_injuries_touched_by: str = ""
    wyld_perm_injuries_touched_by: str = ""

    # Weapons and Gear touched...
    weapons_note_touched_by: str = ""
    gear_note_touched_by: str = ""
    char_missions_note_touched_by: str = ""
    char_contacts_note_touched_by: str = ""
    weapons_touched_by: str = ""
    gear_touched_by: str = ""
    char_missions_touched_by: str = ""
    char_contacts_touched_by: str = ""

    # Social and Career touched...
    citizen_touched_by: str = ""
    social_class_touched_by: str = ""
    lifestyle_touched_by: str = ""
    lifestyle_change_touched_by: str = ""
    organisation_touched_by: str = ""
    rank_touched_by: str = ""
    rank_bonus_touched_by: str = ""
    commendations_touched_by: str = ""
    reprimands_touched_by: str = ""
    reputation_touched_by: str = ""

    # Edges Traits touched...
    edges_note_touched_by: str = ""
    traits_note_touched_by: str = ""
    team_edges_note_touched_by: str = ""
    team_traits_note_touched_by: str = ""
    temporary_edges_note_touched_by: str = ""
    temporary_traits_note_touched_by: str = ""
    environmental_traits_note_touched_by: str = ""
    remove_limit_touched_by: str = ""
    remove_trait_touched_by: str = ""
    valid_edge_touched_by: str = ""
    valid_trait_touched_by: str = ""
    creature_edges_touched_by: str = ""

    # Sliverware touched...
    allow_bioware_touched_by: str = ""
    sliverware_note_touched_by: str = ""
    sliverware_failure_touched_by: str = ""
    s_bodyweb_comp_touched_by: str = ""
    s_headlink_comp_touched_by: str = ""
    s_optics_comp_touched_by: str = ""
    s_neural_rewiring_comp_touched_by: str = ""
    s_biosculpting_comp_touched_by: str = ""
    s_nanocore_comp_touched_by: str = ""
    s_biocore_comp_touched_by: str = ""
    sliver_bodyweb_touched_by: str = ""
    sliver_chemjet_touched_by: str = ""
    sliver_cnsbooster_touched_by: str = ""
    sliver_dermalplate_touched_by: str = ""
    sliver_monoclaws_touched_by: str = ""
    sliver_steelmuscles_touched_by: str = ""
    sliver_bodystash_touched_by: str = ""
    sliver_headlink_touched_by: str = ""
    sliver_combatlink_touched_by: str = ""
    sliver_dronelink_touched_by: str = ""
    sliver_nervelink_touched_by: str = ""
    sliver_neuralcomm_touched_by: str = ""
    sliver_socialanalyser_touched_by: str = ""
    sliver_vcs_touched_by: str = ""
    sliver_optics_touched_by: str = ""
    sliver_brainbooster_touched_by: str = ""
    sliver_eagleeye_touched_by: str = ""
    sliver_forensicscanner_touched_by: str = ""
    sliver_taclink_touched_by: str = ""
    sliver_thermalimaging_touched_by: str = ""
    sliver_threatanalyser_touched_by: str = ""
    sliver_neuralrewiring_touched_by: str = ""
    sliver_audiowire_touched_by: str = ""
    sliver_decrypter_touched_by: str = ""
    sliver_godlink_touched_by: str = ""
    sliver_weaveview_touched_by: str = ""
    sliver_weavelink_touched_by: str = ""
    sliver_ultrasonics_touched_by: str = ""
    sliver_biosculpting_touched_by: str = ""
    sliver_decentralisedheart_touched_by: str = ""
    sliver_dns_touched_by: str = ""
    sliver_magnaview_touched_by: str = ""
    sliver_pharm_touched_by: str = ""
    sliver_musclefibers_touched_by: str = ""
    sliver_oxycycler_touched_by: str = ""
    sliver_nanocore_touched_by: str = ""
    sliver_chameleonfield_touched_by: str = ""
    sliver_ecmcloak_touched_by: str = ""
    sliver_escapegas_touched_by: str = ""
    sliver_nanoarmour_touched_by: str = ""
    sliver_nbsu_touched_by: str = ""
    sliver_nanoregen_touched_by: str = ""
    sliver_biocore_touched_by: str = ""
    sliver_aquashift_touched_by: str = ""
    sliver_beautifier_touched_by: str = ""
    sliver_cloneorgan_touched_by: str = ""
    sliver_pheromones_touched_by: str = ""
    sliver_stressshift_touched_by: str = ""
    sliver_voicecontrol_touched_by: str = ""

    # Skills touched...
    physical_touched_by: str = ""
    physical_dl_touched_by: str = ""
    physical_limit_touched_by: str = ""
    athletics_touched_by: str = ""
    athletics_limit_touched_by: str = ""
    athletics_dl_touched_by: str = ""
    endurance_touched_by: str = ""
    endurance_dl_touched_by: str = ""
    endurance_limit_touched_by: str = ""
    killer_touched_by: str = ""
    killer_limit_touched_by: str = ""
    killer_dl_touched_by: str = ""
    energy_touched_by: str = ""
    energy_limit_touched_by: str = ""
    energy_dl_touched_by: str = ""
    guns_touched_by: str = ""
    guns_dl_touched_by: str = ""
    guns_limit_touched_by: str = ""
    melee_touched_by: str = ""
    melee_dl_touched_by: str = ""
    melee_limit_touched_by: str = ""
    cloak_touched_by: str = ""
    cloak_dl_touched_by: str = ""
    cloak_limit_touched_by: str = ""
    con_touched_by: str = ""
    con_dl_touched_by: str = ""
    con_limit_touched_by: str = ""
    disguise_touched_by: str = ""
    disguise_dl_touched_by: str = ""
    disguise_limit_touched_by: str = ""
    sneak_touched_by: str = ""
    sneak_dl_touched_by: str = ""
    sneak_limit_touched_by: str = ""
    smarts_touched_by: str = ""
    smarts_dl_touched_by: str = ""
    smarts_limit_touched_by: str = ""
    control_touched_by: str = ""
    control_dl_touched_by: str = ""
    control_limit_touched_by: str = ""
    knowledge_touched_by: str = ""
    knowledge_dl_touched_by: str = ""
    knowledge_limit_touched_by: str = ""
    sandman_touched_by: str = ""
    perception_touched_by: str = ""
    perception_dl_touched_by: str = ""
    perception_limit_touched_by: str = ""
    psychology_touched_by: str = ""
    psychology_dl_touched_by: str = ""
    psychology_limit_touched_by: str = ""
    streetwise_touched_by: str = ""
    streetwise_dl_touched_by: str = ""
    streetwise_limit_touched_by: str = ""
    weaver_touched_by: str = ""
    weaver_dl_touched_by: str = ""
    weaver_limit_touched_by: str = ""
    hardtech_touched_by: str = ""
    hardtech_dl_touched_by: str = ""
    hardtech_limit_touched_by: str = ""
    medic_touched_by: str = ""
    medic_dl_touched_by: str = ""
    medic_limit_touched_by: str = ""
    hacking_touched_by: str = ""
    hacking_dl_touched_by: str = ""
    hacking_limit_touched_by: str = ""
    resources_touched_by: str = ""
    resources_dl_touched_by: str = ""
    resources_limit_touched_by: str = ""
    network_touched_by: str = ""
    network_dl_touched_by: str = ""
    network_limit_touched_by: str = ""
    influence_touched_by: str = ""
    influence_dl_touched_by: str = ""
    influence_limit_touched_by: str = ""
    mouth_touched_by: str = ""
    mouth_dl_touched_by: str = ""
    mouth_limit_touched_by: str = ""
    intimidate_touched_by: str = ""
    intimidate_dl_touched_by: str = ""
    intimidate_limit_touched_by: str = ""
    leadership_touched_by: str = ""
    leadership_dl_touched_by: str = ""
    leadership_limit_touched_by: str = ""
    persuade_touched_by: str = ""
    persuade_dl_touched_by: str = ""
    persuade_limit_touched_by: str = ""
    vapour_touched_by: str = ""
    vapour_dl_touched_by: str = ""
    vapour_limit_touched_by: str = ""
    aircraft_touched_by: str = ""
    aircraft_dl_touched_by: str = ""
    aircraft_limit_touched_by: str = ""
    groundcraft_touched_by: str = ""
    groundcraft_dl_touched_by: str = ""
    groundcraft_limit_touched_by: str = ""
    spacecraft_touched_by: str = ""
    spacecraft_dl_touched_by: str = ""
    spacecraft_limit_touched_by: str = ""
    wyld_touched_by: str = ""
    wyld_dl_touched_by: str = ""
    wyld_limit_touched_by: str = ""
    resistance_touched_by: str = ""
    resistance_dl_touched_by: str = ""
    resistance_limit_touched_by: str = ""
    sense_touched_by: str = ""
    sense_dl_touched_by: str = ""
    sense_limit_touched_by: str = ""
    allow_echo_touched_by: str = ""
    allow_echo1_touched_by: str = ""
    allow_echo2_touched_by: str = ""
    echo_names_touched_by: str = ""
    echo1_name_touched_by: str = ""
    echo2_name_touched_by: str = ""
    magnitude_touched_by: str = ""
    echo_max_dl_touched_by: str = ""
    echo_wyld_cancer_touched_by: str = ""
    echo_wyld_damage_touched_by: str = ""
    echo1_touched_by: str = ""
    echo1_dl_touched_by: str = ""
    echo1_limit_touched_by: str = ""
    attack1_touched_by: str = ""
    attack1_dl_touched_by: str = ""
    attack1_limit_touched_by: str = ""
    manipulation1_touched_by: str = ""
    manipulation1_dl_touched_by: str = ""
    manipulation1_limit_touched_by: str = ""
    nature1_touched_by: str = ""
    nature1_dl_touched_by: str = ""
    nature1_limit_touched_by: str = ""
    echo2_touched_by: str = ""
    echo2_dl_touched_by: str = ""
    echo2_limit_touched_by: str = ""
    attack2_touched_by: str = ""
    attack2_dl_touched_by: str = ""
    attack2_limit_touched_by: str = ""
    manipulation2_touched_by: str = ""
    manipulation2_dl_touched_by: str = ""
    manipulation2_limit_touched_by: str = ""
    nature2_touched_by: str = ""
    nature2_dl_touched_by: str = ""
    nature2_limit_touched_by: str = ""
    divinity_touched_by: str = ""
    divinity_dl_touched_by: str = ""
    divinity_limit_touched_by: str = ""
    faith_touched_by: str = ""
    faith_dl_touched_by: str = ""
    faith_limit_touched_by: str = ""
    invocation_touched_by: str = ""
    invocation_dl_touched_by: str = ""
    invocation_limit_touched_by: str = ""
    allow_syncretic_disciple_touched_by: str = ""
    allow_gifts_touched_by: str = ""
    ai_online_touched_by: str = ""
    comms_online_touched_by: str = ""
    stealth_online_touched_by: str = ""
    stealth_touched_by: str = ""
    stealth_dl_touched_by: str = ""
    sensors_online_touched_by: str = ""
    sensors_touched_by: str = ""
    sensors_dl_touched_by: str = ""
    piloting_dl_touched_by: str = ""
    heat_cap_touched_by: str = ""
    scom_touched_by: str = ""
    action_cap_touched_by: str = ""
    grav_drive_touched_by: str = ""
    wyld_shield_touched_by: str = ""
    wyld_sensors_touched_by: str = ""
    wyld_sensors_online_touched_by: str = ""
    heat_touched_by: str = ""
    heat_modifier_touched_by: str = ""
    heat_reset_touched_by: str = ""
    injury_size_touched_by: str = ""
    repair_skill_touched_by: str = ""

    # Opportunity Points touched...
    allow_op_use_touched_by: str = ""
    allow_op_healing_touched_by: str = ""
    allow_op_rerolls_touched_by: str = ""
    allow_op_plus2_touched_by: str = ""
    allow_op_plus1_touched_by: str = ""
    allow_physical_op_healing_touched_by: str = ""
    allow_smarts_op_healing_touched_by: str = ""
    allow_resources_op_healing_touched_by: str = ""
    allow_wyld_op_healing_touched_by: str = ""
    allow_divinity_op_healing_touched_by: str = ""
    physical_op_touched_by: str = ""
    smarts_op_touched_by: str = ""
    resources_op_touched_by: str = ""
    wyld_op_touched_by: str = ""
    divinity_op_touched_by: str = ""
    temporary_op_touched_by: str = ""
    combat_op_touched_by: str = ""
    overlord_op_touched_by: str = ""
    mook_op_touched_by: str = ""
    team_op_touched_by: str = ""

    # Wound Thresholds and AVs touched...
    physical_wt_touched_by: str = "Base = Physical (Endurance)/3 + 1"
    physical_wt_bonus_touched_by: str = ""
    physical_dam_mult_touched_by: str = ""
    physical_av_touched_by: str = ""
    physical_av_actual_touched_by: str = ""
    physical_av_max_touched_by: str = ""
    physical_av_min_touched_by: str = ""
    smarts_wt_touched_by: str = "Base = Smarts (Control)/3 + 1"
    smarts_wt_bonus_touched_by: str = ""
    smarts_dam_mult_touched_by: str = ""
    smarts_av_touched_by: str = ""
    smarts_av_actual_touched_by: str = ""
    smarts_av_max_touched_by: str = ""
    smarts_av_min_touched_by: str = ""
    resources_wt_touched_by: str = "Base = Resources (Influence/3 + 1"
    resources_wt_bonus_touched_by: str = ""
    resources_dam_mult_touched_by: str = ""
    resources_av_touched_by: str = ""
    resources_av_actual_touched_by: str = ""
    resources_av_max_touched_by: str = ""
    resources_av_min_touched_by: str = ""
    wyld_wt_touched_by: str = "Base = Wyld (Resistance)/3 + 1"
    wyld_wt_bonus_touched_by: str = ""
    wyld_dam_mult_touched_by: str = ""
    wyld_av_touched_by: str = ""
    wyld_av_actual_touched_by: str = ""
    wyld_av_max_touched_by: str = ""
    wyld_av_min_touched_by: str = ""
    divinity_wt_touched_by: str = "Base = Divinity (Faith)/3 + 1"
    divinity_wt_bonus_touched_by: str = ""
    divinity_dam_mult_touched_by: str = ""
    divinity_av_touched_by: str = ""
    divinity_av_actual_touched_by: str = ""
    divinity_av_max_touched_by: str = ""
    divinity_av_min_touched_by: str = ""
    vehicle_wt_touched_by: str = ""
    vehicle_wt_bonus_touched_by: str = ""
    vehicle_dam_mult_touched_by: str = ""
    vehicle_av_touched_by: str = ""
    vehicle_av_actual_touched_by: str = ""
    vehicle_av_max_touched_by: str = ""
    vehicle_av_min_touched_by: str = ""
    mook_wt_touched_by: str = (
        "Base = (Physical (Endurance) + Smarts (Control) + Resources (Influence) + "
        "Wyld (Resistance) + Divinity (Faith))/7 + 1"
    )
    mook_wt_bonus_touched_by: str = ""
    mook_dam_mult_touched_by: str = ""
    stabilise_touched_by: str = ""
    survival_touched_by: str = ""
    mortal_wound_touched_by: str = ""
    stabilised_touched_by: str = ""

    # Damage Taken/Wounds/Injuries touched...
    physical_dt_touched_by: str = ""
    physical_wounds_touched_by: str = ""
    physical_injuries_touched_by: str = ""
    physical_dam_max_touched_by: str = ""
    smarts_dt_touched_by: str = ""
    smarts_wounds_touched_by: str = ""
    smarts_injuries_touched_by: str = ""
    smarts_dam_max_touched_by: str = ""
    resources_dt_touched_by: str = ""
    resources_wounds_touched_by: str = ""
    resources_injuries_touched_by: str = ""
    resources_dam_max_touched_by: str = ""
    wyld_dt_touched_by: str = ""
    wyld_wounds_touched_by: str = ""
    wyld_injuries_touched_by: str = ""
    wyld_dam_max_touched_by: str = ""
    divinity_dt_touched_by: str = ""
    divinity_wounds_touched_by: str = ""
    divinity_injuries_touched_by: str = ""
    divinity_dam_max_touched_by: str = ""
    mook_wounds_touched_by: str = ""
    vehicle_dt_touched_by: str = ""
    vehicle_wounds_touched_by: str = ""
    vehicle_injuries_touched_by: str = ""
    vehicle_dam_max_touched_by: str = ""
    stun_duration_touched_by: str = ""
    emp_duration_touched_by: str = ""

    # Immunities touched...
    physical_immunity_touched_by: str = ""
    smarts_immunity_touched_by: str = ""
    resources_immunity_touched_by: str = ""
    wyld_immunity_touched_by: str = ""
    divinity_immunity_touched_by: str = ""
    stun_immunity_touched_by: str = ""
    emp_immunity_touched_by: str = ""
    toxin_immunity_touched_by: str = ""
    intimidate_immunity_touched_by: str = ""
    heat_immunity_touched_by: str = ""
    fire_immunity_touched_by: str = ""
    echo_immunity_touched_by: str = ""
    corruption_immunity_touched_by: str = ""
    soulweaving_immunity_touched_by: str = ""

    # Healing and resist touched...
    healing_dl_touched_by: str = ""
    resist_toxin_touched_by: str = ""
    resist_toxin_limit_touched_by: str = ""
    resist_toxin_dl_touched_by: str = ""
    resist_emp_touched_by: str = ""
    resist_emp_limit_touched_by: str = ""
    resist_emp_dl_touched_by: str = ""
    resist_stun_touched_by: str = ""
    resist_stun_limit_touched_by: str = ""
    resist_stun_dl_touched_by: str = ""
    resist_intimidate_touched_by: str = ""
    resist_intimidate_limit_touched_by: str = ""
    resist_intimidate_dl_touched_by: str = ""
    resist_echo_touched_by: str = ""
    resist_echo_limit_touched_by: str = ""
    resist_echo_dl_touched_by: str = ""
    resist_wyld_touched_by: str = ""
    resist_wyld_limit_touched_by: str = ""
    resist_wyld_dl_touched_by: str = ""
    resist_corruption_touched_by: str = ""
    resist_soulweaving_touched_by: str = ""
    resist_soulweaving_dl_touched_by: str = ""
    defence_touched_by: str = ""

    # Availability touched...
    availability_limit_touched_by: str = ""
    availability_dl_touched_by: str = ""
    availability_touched_by: str = ""

    # Other stats touched...
    scale_touched_by: str = "Base = 1"
    scale_dl_touched_by: str = ""
    scale_limit_touched_by: str = ""
    speed_touched_by: str = "Base = 1"
    speed_dl_touched_by: str = ""
    speed_limit_touched_by: str = ""
    initiative_touched_by: str = "Base = (Physical + Smarts + Resources)/3"
    initiative_bonus_touched_by: str = ""
    initiative_dl_touched_by: str = ""
    initiative_limit_touched_by: str = ""
    initiative_note_touched_by: str = ""

    # Specialisation Masteries touched...
    smx_name1_touched_by: str = ""
    smx_name2_touched_by: str = ""
    smx_name3_touched_by: str = ""
    smx1_touched_by: str = ""
    smx2_touched_by: str = ""
    smx3_touched_by: str = ""

    # Complication and Boosts touched...
    complications_touched_by: str = ""
    boosts_touched_by: str = ""

    # Notes touched...
    physical_note_touched_by: str = ""
    killer_note_touched_by: str = ""
    cloak_note_touched_by: str = ""
    smarts_note_touched_by: str = ""
    sandman_note_touched_by: str = ""
    weaver_note_touched_by: str = ""
    resources_note_touched_by: str = ""
    mouth_note_touched_by: str = ""
    vapour_note_touched_by: str = ""
    wyld_note_touched_by: str = ""
    echo_note_touched_by: str = ""
    divinity_note_touched_by: str = ""
    gift_curses_note_touched_by: str = ""
    soulweaving_note_touched_by: str = ""
    heresies_note_touched_by: str = ""
    geas_note_touched_by: str = ""
    blessings_note_touched_by: str = ""
    corruption_note_touched_by: str = ""
    perm_corruption_injury_note_touched_by: str = ""
    general_note_touched_by: str = ""
    vehicle_note_touched_by: str = ""
    mook_note_touched_by: str = ""
    injury_note_touched_by: str = ""
    sc_injury_note_touched_by: str = ""
    wound_note_touched_by: str = ""
    perm_wyld_injury_note_touched_by: str = ""
    warning_note_touched_by: str = ""
    character_note_touched_by: str = ""
    gm_note_touched_by: str = ""
    player_note_touched_by: str = ""
    pledged_disciple_note_touched_by: str = ""
    mission_note_touched_by: str = ""
    contacts_allies_enemies_note_touched_by: str = ""

    # DEBUG
    replace_text_touched_by: str = ""
    custom_touched_by: str = ""
    injury_try_touched_by: str = ""
    twin_touched_by: str = ""
    parent_touched_by: str = ""
    children_touched_by: str = ""


def create_character_db(
    db="broken_shield_characters.sqlite",
    db_path="./characters/",
):
    # IF broken_shield_gamedata DOESN'T EXIST CREATE IT.
    conn = sqlite3.connect(db_path + db)
    cursor = conn.cursor()
    logging.info(f"SQLite: connecting to db = {db_path}{db}")

    drop_table_sql1 = f"DROP TABLE IF EXISTS players"
    drop_table_sql2 = f"DROP TABLE IF EXISTS characters"
    drop_table_sql3 = f"DROP TABLE IF EXISTS live_characters"

    # PlayerModel DB Table
    create_table_sql1 = (
        f"CREATE TABLE IF NOT EXISTS players (player_id INT PRIMARY_KEY NOT NULL, player_name TEXT, "
        f"player_real_name TEXT, player_email TEXT, player_json TEXT, deleted BOOL)"
    )

    # CharacterModel DB Table
    create_table_sql2 = (
        f"CREATE TABLE IF NOT EXISTS characters (char_id INT PRIMARY_KEY NOT NULL, char_name TEXT, "
        f"char_archetype TEXT, player_id INT, char_type TEXT, char_json TEXT, deleted BOOL)"
    )

    # Live character DB table
    create_table_sql3 = (
        f"CREATE TABLE IF NOT EXISTS live_characters (live_char_id INT PRIMARY_KEY NOT NULL, "
        f"char_id INT, player_id INT, char_name TEXT, live_char_json TEXT, deleted BOOL)"
    )

    logging.info(f"SQLite: drop tables = {drop_table_sql1}")
    logging.info(f"SQLite: drop tables = {drop_table_sql2}")
    logging.info(f"SQLite: drop tables = {drop_table_sql3}")
    logging.info(f"SQLite: create table = {create_table_sql1}")
    logging.info(f"SQLite: create table  = {create_table_sql2}")
    logging.info(f"SQLite: create table  = {create_table_sql3}")

    cursor.execute(drop_table_sql1)
    cursor.execute(drop_table_sql2)
    cursor.execute(drop_table_sql3)
    cursor.execute(create_table_sql1)
    cursor.execute(create_table_sql2)
    cursor.execute(create_table_sql3)

    conn.commit()
    conn.close()


def main() -> None:
    """Main function"""

    # Default Character
    # dc = DefaultCharacter()
    # dc_dict = dc.dict()
    # print(dc.nodes)

    # tp = PlayerModel(player_id=1, player_name="Gobion")
    # tc = CharacterModel(char_id=1, name="Test", player_id=1)
    # lc = LiveCharacterModel(live_char_id=1, char_id=1, name="Test")

    # Converts tc into a dict()
    # tp_dict = tp.dict()
    # tc_dict = tc.dict()
    # lc_dict = lc.dict()

    # Checking type of tc_dict t prove it is a dict
    # cd_type = type(tc_dict)
    # print(cd_type)

    # Dumps tc_dict into a usable dict
    # pretty_player = dumps(tp_dict, indent=4)
    # pretty = dumps(tc_dict, indent=4)
    # pretty_live = dumps(lc_dict, indent=4)
    # print(pretty_player)
    # print(pretty)
    # print(pretty_live)

    # create_character_db()


if __name__ == "__main__":
    main()
