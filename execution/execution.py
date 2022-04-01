"""
TODO
"""

import csv
import shutil
import os
from datetime import datetime
from setup_env import setup_env


def initial_directory_setup():
    """
    TODO
    """
    print("initial directory setup")
    CURRENT_YEAR = str(datetime.now().strftime('%Y'))
    CURRENT_MONTH = str(datetime.now().strftime('%m'))
    CURRENT_DAY = str(datetime.now().strftime('%d'))

    base_dir = setup_env.view_current_conf()['base_dir']

    CURRENT_YEAR_DIR = base_dir + "/" + CURRENT_YEAR
    CURRENT_MONTH_DIR = CURRENT_YEAR_DIR + "/" + CURRENT_MONTH
    CURRENT_JSON_DIR = CURRENT_MONTH_DIR + "/" + "JSON"
    CURRENT_CSV_DIR = CURRENT_MONTH_DIR + "/" + "CSV"

    if not os.path.exists(CURRENT_YEAR_DIR):
        print("dir {} it's not there yet, creating ...".format(CURRENT_YEAR_DIR))
        os.makedirs(CURRENT_YEAR_DIR)

    if not os.path.exists(CURRENT_MONTH_DIR):
        print("dir {} it's not there yet, creating ...".format(CURRENT_MONTH_DIR))
        os.makedirs(CURRENT_MONTH_DIR)

    if not os.path.exists(CURRENT_JSON_DIR):
        print("dir {} it's not there yet, creating ...".format(CURRENT_JSON_DIR))
        os.makedirs(CURRENT_JSON_DIR)

    if not os.path.exists(CURRENT_CSV_DIR):
        print("dir {} it's not there yet, creating ...".format(CURRENT_CSV_DIR))
        os.makedirs(CURRENT_CSV_DIR)

    # At this moment keeping the hard code path
    CSV_FILE = "/tmp/match_inv_sw.csv"
    JSON_FILE_INV = "/tmp/inventory.json"
    JSON_FILE_SWATCH = "/tmp/swatch.json"

    DEST_CSV_FILE = CURRENT_CSV_DIR + "/" + "match_inv_sw_" + CURRENT_MONTH + "-" + CURRENT_DAY + "-" + CURRENT_YEAR + ".csv"
    DEST_JSON_FILE_INV = CURRENT_JSON_DIR + "/" + "inventory_" + CURRENT_MONTH + "-" + CURRENT_DAY + "-" + CURRENT_YEAR + ".json"
    DEST_JSON_FILE_SWATCH = CURRENT_JSON_DIR + "/" + "swatch_" + CURRENT_MONTH + "-" + CURRENT_DAY + "-" + CURRENT_YEAR + ".json"

    crhc_cli = setup_env.view_current_conf()['crhc_cli']
    print(crhc_cli)

    print("Cleaning the current cache files")
    os.system(crhc_cli + " ts clean")

    print("Downloading and creating the new match info")
    os.system(crhc_cli + " ts match")
    shutil.copy(CSV_FILE, DEST_CSV_FILE)
    shutil.copy(JSON_FILE_INV, DEST_JSON_FILE_INV)
    shutil.copy(JSON_FILE_SWATCH, DEST_JSON_FILE_SWATCH)
    # print(base_dir)


def collect_data():
    """
    TODO
    """
    print("collect data")
    initial_directory_setup()


def process_data():
    """
    TODO
    """
    # print("process data")

    base_dir = setup_env.view_current_conf()['base_dir']

    years = os.listdir(base_dir)
    # print(YEARS)
    for year in years:
        # print(year)
        months = os.listdir(base_dir + "/" + year)
        for month in months:
            # print(month)
            path_to_csv_dir = base_dir + "/" + year + "/" + month + "/" + "CSV"
            csv_files_list = os.listdir(path_to_csv_dir)
            # print(csv_files_list)
            generate_report(path_to_csv_dir, csv_files_list)


def generate_report(path_to_csv_dir, csv_files_list):
    """
    TODO
    """
    # print("generating the report by ondemand")
    print("")
    print("## RHEL On-Demand")
    print("")
    ondemand_rhel(path_to_csv_dir, csv_files_list)


def ondemand_rhel(path_to_csv_dir, csv_files_list):
    """
    TODO
    """

    # for debug purposes
    # print(path_to_csv_dir)
    # print(csv_files_list)

    CURRENT_TIMEFRAME_YEAR = path_to_csv_dir.split("/")[4]
    CURRENT_TIMEFRAME_MONTH = path_to_csv_dir.split("/")[5]
    CURRENT_TIMEFRAME = CURRENT_TIMEFRAME_YEAR + "-" + CURRENT_TIMEFRAME_MONTH

    for sheet in csv_files_list:

        rhel_physical = 0
        stage_rhel_physical = 0
        rhel_virtual = 0
        stage_rhel_virtual = 0
        unknown = 0
        stage_unknown = 0

        with open(path_to_csv_dir + "/" + sheet, "r") as file_obj:
            csv_file = csv.reader(file_obj)
            for row in csv_file:
                # print(row)

                infrastructure_type = row[21]
                installed_product = row[35]

                if ('69' in installed_product) or ('479' in installed_product):
                    if infrastructure_type == "physical":
                        stage_rhel_physical = stage_rhel_physical + 1
                    elif infrastructure_type == "virtual":
                        stage_rhel_virtual = stage_rhel_virtual + 1
                    else:
                        stage_unknown = stage_unknown + 1

    if stage_rhel_physical > rhel_physical:
        rhel_physical = stage_rhel_physical
        stage_rhel_physical = 0

    if stage_rhel_virtual > rhel_virtual:
        rhel_virtual = stage_rhel_virtual
        stage_rhel_virtual = 0

    print("Max Concurrent RHEL On-Demand, referrent to ..: {}".format(CURRENT_TIMEFRAME))
    print("On-Demand, Physical Node .....................: {}".format(rhel_physical))
    print("On-Demand, Virtual Node ......................: {}".format(rhel_virtual))
    print("Unknown ......................................: {}".format(unknown))
    print("")
