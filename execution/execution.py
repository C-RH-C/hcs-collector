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
    with open(dest_csv_file, "w+") as file_csv:
        mywriter = csv.writer(file_csv,delimiter=',') # ,quotechar='"'
        print("created a mywriter")
        mywriter.writerows(csv_file)

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
            generate_report(path_to_csv_dir, csv_files_list, path_to_json_dir, json_files_list)


def generate_report(path_to_csv_dir, csv_files_list, path_to_json_dir, json_files_list):
    """
    TODO
    """
    # print("generating the report by ondemand")
    print("")
    print("## RHEL On-Demand")
    print("")
    ondemand_rhel(path_to_csv_dir, csv_files_list)
    print("## RHEL Add-ons")
    print("")
    ondemand_rhel_related_products_from_json(path_to_json_dir, json_files_list)
    print("## Virtualization")
    print("")
    ondemand_virtualization(path_to_csv_dir, csv_files_list)
    print("## Middleware")
    print("")
    ondemand_mw_from_json(path_to_json_dir, json_files_list)

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


def ondemand_virtualization(path_to_csv_dir, csv_files_list):
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

        virtualization_sockets = 0
        stage_virtualization_sockets = 0

        
        

        with open(path_to_csv_dir + "/" + sheet, "r") as file_obj:
            csv_file = csv.reader(file_obj)
            for row in csv_file:
                # print(row)

                infrastructure_type = row[21]
                installed_product = row[35]

                number_of_sockets = 1
                if (row[11].isnumeric()):
                    number_of_sockets = int(row[11])

                # RHV is covered by products 150, 328, and 415 
                if ('150' in installed_product) or ('328' in installed_product) or ('415' in installed_product):
                    stage_virtualization_sockets = stage_virtualization_sockets + number_of_sockets


    if stage_virtualization_sockets > virtualization_sockets:
        virtualization_sockets = stage_virtualization_sockets
        stage_virtualization_sockets = 0

    

    print("On-Demand, Virtualization Sockets ............: {}".format(virtualization_sockets))
    print("")
def ondemand_rhel_related_products_from_json(path_to_json_dir, json_files_list):
    """
    TODO
    """

    # for debug purposes
    # print(path_to_csv_dir)
    # print(csv_files_list)

    CURRENT_TIMEFRAME_YEAR = path_to_json_dir.split("/")[4]
    CURRENT_TIMEFRAME_MONTH = path_to_json_dir.split("/")[5]
    CURRENT_TIMEFRAME = CURRENT_TIMEFRAME_YEAR + "-" + CURRENT_TIMEFRAME_MONTH

    rhel_ha = 0
    rhel_directoryserver = 0

    for jsonFile in json_files_list:
        
        stage_rhel_ha = 0
        stage_rhel_directoryserver = 0
        

        with open(path_to_json_dir + "/" + jsonFile, "r") as file_obj:
            data = json.load(file_obj)
            if ('results' in data):
                for inventoryItem in data['results']:
                    # print(row)
                    # get the number of cores.
                    system_profile = inventoryItem['system_profile']
                    installed_products = []
                    installed_packages = []
                    installed_services = []
                    if ('installed_products' in system_profile): installed_products = system_profile['installed_products']
                    if ('installed_packages' in system_profile): installed_packages = system_profile['installed_packages']
                    if ('installed_services' in system_profile): installed_services =  system_profile['installed_services']
               

                    installed_product_list = []
                    for product in installed_products:
                        installed_product_list.append(product['id'])
                    
                    ha_packages_installed = False
                    directory_server_packages_installed = False
                    for package_name in installed_packages:
                        if (package_name.startswith("rgmanager") or package_name.startswith("pcs-") or package_name.startswith("pacemaker")): ha_packages_installed = True
                        if (package_name.startswith("389-ds")): directory_server_packages_installed = True

                    directory_server_services_running = False
                    ha_services_running = False
                    for service_name in installed_services:
                        if ("pcsd" in service_name): ha_services_running = True
                        

                    # HA is covered by products 159, 83, and 84
                    if (('83' in installed_product_list) or ('84' in installed_product_list) or ('159' in installed_product_list) or ha_packages_installed or ha_services_running):
                        stage_rhel_ha = stage_rhel_ha + 1
                    
                    # Directory Server is covered by products 159, 83, and 84
                    if (('200' in installed_product_list) or directory_server_packages_installed):
                        stage_rhel_directoryserver = stage_rhel_directoryserver + 1
        
        if stage_rhel_ha > rhel_ha:
            rhel_ha = stage_rhel_ha
            stage_rhel_ha = 0

        if stage_rhel_directoryserver > rhel_directoryserver:
            rhel_directoryserver = stage_rhel_directoryserver
            stage_rhel_directoryserver = 0


    print("On-Demand, HA Node ...........................: {}".format(rhel_ha))
    print("On-Demand, Directory Server Node .............: {}".format(rhel_directoryserver))
    print("")


def ondemand_mw_from_json(path_to_json_dir, json_files_list):
    """
    TODO
    """

    # for debug purposes
    # print(path_to_csv_dir)
    # print(csv_files_list)

    CURRENT_TIMEFRAME_YEAR = path_to_json_dir.split("/")[4]
    CURRENT_TIMEFRAME_MONTH = path_to_json_dir.split("/")[5]
    CURRENT_TIMEFRAME = CURRENT_TIMEFRAME_YEAR + "-" + CURRENT_TIMEFRAME_MONTH

    jboss_eap_cores = 0
    jws_cores = 0
    for jsonFile in json_files_list:

        stage_jboss_eap_cores = 0
        stage_jws_cores = 0


        with open(path_to_json_dir + "/" + jsonFile, "r") as file_obj:
            data = json.load(file_obj)
            if ('results' in data):
                for inventoryItem in data['results']:
                    # print(row)
                    # get the number of cores.
                    system_profile = inventoryItem['system_profile']
                    cores_per_socket = 1
                    number_of_cores = 1
                    number_of_sockets = 1
                    installed_products = []
                    installed_packages = []
                    installed_services = []
                    if ('installed_products' in system_profile): installed_products = system_profile['installed_products']
                    if ('installed_packages' in system_profile): installed_packages = system_profile['installed_packages']
                    if ('installed_services' in system_profile): installed_services =  system_profile['installed_services']
                    if ('number_of_sockets' in system_profile): number_of_sockets = system_profile['number_of_sockets']
                    if ('cores_per_socket' in system_profile): cores_per_socket = system_profile['cores_per_socket']
                    number_of_cores = cores_per_socket * number_of_sockets

                    installed_product_list = []
                    for product in installed_products:
                        installed_product_list.append(product['id'])
                    
                    eap_packages_installed = False
                    for package_name in installed_packages:
                        if (package_name.startswith("eap")): eap_packages_installed = True

                    jws_services_running = False
                    eap_services_running = False
                    for service_name in installed_services:
                        if ("eap" in service_name): eap_services_running = True
                        if ("jws" in service_name): jws_services_running = True

                    if not (('150' in installed_product_list) or ('328' in installed_product_list) or ('415' in installed_product_list)):
                        #RHV is not installed - beacuase that entitles EAP or JWS to be installed
                        if ('151' in installed_product_list) or ('183' in installed_product_list):
                            stage_jboss_eap_cores = stage_jboss_eap_cores + number_of_cores
                        elif (eap_packages_installed or eap_services_running):
                            stage_jboss_eap_cores = stage_jboss_eap_cores + number_of_cores
                        elif ('152' in installed_product_list) or ('184' in installed_product_list) or ('185' in installed_product_list) or jws_services_running:
                            stage_jws_cores = stage_jws_cores + number_of_cores


        if stage_jboss_eap_cores > jboss_eap_cores:
            jboss_eap_cores = stage_jboss_eap_cores
            stage_jboss_eap_cores = 0

        if stage_jws_cores > jws_cores:
            jws_cores = stage_jws_cores
            stage_jws_cores = 0

    print("On-Demand, JBoss EAP Cores ...................: {}".format(jboss_eap_cores))
    print("On-Demand, JWS Cores .........................: {}".format(jws_cores))
    print("")
