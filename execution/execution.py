"""
TODO
"""

import csv
import shutil
import os
import subprocess
import json
from datetime import datetime
from setup_env import setup_env
from execution import process_mw
from execution import process_rhel
from execution import process_virt
from execution import process_rhel_addons


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
    append_tags_to_inventory_json(DEST_JSON_FILE_INV, crhc_cli)
    append_tags_to_inventory_csv(DEST_CSV_FILE, crhc_cli)
    # print(base_dir)

def append_tags_to_inventory_csv(dest_csv_file, crhc_cli):
    print("appending inventory tags to csv")
    results = []
    with open(dest_csv_file, "r") as file_obj:
        csv_file = csv.reader(file_obj)
        first_row = True
        for row in csv_file:
            if (first_row):
                first_row = False
                continue
            id = row[0]
            os.system(crhc_cli + " get /api/inventory/v1/hosts/" + id + "/tags > /tmp/tags.json")
            with open("/tmp/tags.json", "r") as file_tag:
                tag_result=json.load(file_tag)
                if ('results' in tag_result):
                    if (tag_result['results'].get(id)):
                        tag_string=""
                        first_tag = True
                        tags = tag_result['results'].get(id)
                        for tag in tags:
                            if (first_tag):
                                first_tag = False
                            else:
                                tag_string = tag_string + ";"
                            tag_string = tag_string + tag.get("key") + "=" + tag.get("value")
                        row.append(tag_string)
            results.append(row)

    with open(dest_csv_file, "w+") as f:
        mywriter = csv.writer(f,delimiter=',') # ,quotechar='"'
        mywriter.writerows(results)

def append_tags_to_inventory_json(dest_json_file, crhc_cli):
    print("appending inventory tags to json")
    with open(dest_json_file, "r") as file_obj:
        data = json.load(file_obj)
        if ('results' in data):
            for inventoryItem in data['results']:
                # print(row)
                # get the number of cores.
                id = inventoryItem.get('server').get('id')
                system_profile = inventoryItem['system_profile']
                # get the tags for the system
                os.system(crhc_cli + " get /api/inventory/v1/hosts/" + id + "/tags > /tmp/tags.json")
                with open("/tmp/tags.json", "r") as file_tag:
                    tag_result=json.load(file_tag)
                    if ('results' in tag_result):
                        if (tag_result['results'].get(id)):
                            tagid = tag_result['results'].get(id)
                            inventoryItem.get('server')['tags'] = tagid
    with open(dest_json_file, "w") as file_obj:
        json.dump(data,file_obj, indent=2)



def collect_data():
    """
    TODO
    """
    print("collect data")
    initial_directory_setup()


def process_data(tag):
    """
    TODO
    """
    print("process data with a tag of " + tag)

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
            path_to_json_dir = base_dir + "/" + year + "/" + month + "/" + "JSON"
            json_files_list = os.listdir(path_to_json_dir)
            # print(csv_files_list)
            generate_report(path_to_csv_dir, csv_files_list, path_to_json_dir, json_files_list, tag)


def generate_report(path_to_csv_dir, csv_files_list, path_to_json_dir, json_files_list, tag):
    """
    TODO
    """
    # print("generating the report by ondemand")
    print("")
    print("## RHEL On-Demand")
    print("")
    process_rhel.ondemand_rhel(path_to_csv_dir, csv_files_list, tag)
    print("## RHEL Add-ons")
    print("")
    process_rhel_addons.ondemand_rhel_related_products_from_json(path_to_json_dir, json_files_list, tag)
    print("## Virtualization")
    print("")
    process_virt.ondemand_virtualization(path_to_csv_dir, csv_files_list, tag)
    print("## Middleware")
    print("")
    process_mw.ondemand_mw_from_json(path_to_json_dir, json_files_list, tag)







