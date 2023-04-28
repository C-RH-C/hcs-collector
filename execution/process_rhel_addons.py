import json
from execution import util

def ondemand_rhel_related_products_from_json(path_to_json_dir, json_files_list, tag):
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
    max_by_tag = {}

    for jsonFile in json_files_list:
        
        stage_rhel_ha = 0
        stage_rhel_directoryserver = 0
        stage_by_tag = {}
        

        with open(path_to_json_dir + "/" + jsonFile, "r") as file_obj:
            data = json.load(file_obj)
            if ('results' in data):
                for inventoryItem in data['results']:
                    # print(row)
                    # get the number of cores.
                    if (util.is_fresh(inventoryItem['server']['stale_timestamp'],CURRENT_TIMEFRAME_YEAR, CURRENT_TIMEFRAME_MONTH, jsonFile[13:15])):
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
                        
                        if (tag != "none"):
                            #check if tag exists in vmtags
                            tagvalue = util.get_tag_value_from_json(inventoryItem.get('server').get('tags'), tag)


                        # HA is covered by products 159, 83, and 84
                        if (('83' in installed_product_list) or ('84' in installed_product_list) or ('159' in installed_product_list) or ha_packages_installed or ha_services_running):
                            stage_rhel_ha = stage_rhel_ha + 1
                            if (tag != "none" and tagvalue!=""):
                                count_addons_value_by_tag("ha", stage_by_tag, tagvalue)
                      
                        
                        # Directory Server is covered by products 159, 83, and 84
                        if (('200' in installed_product_list) or directory_server_packages_installed):
                            stage_rhel_directoryserver = stage_rhel_directoryserver + 1
                            if (tag != "none" and tagvalue!=""):
                                count_addons_value_by_tag("ds", stage_by_tag, tagvalue)
        
        if stage_rhel_ha > rhel_ha:
            rhel_ha = stage_rhel_ha
            stage_rhel_ha = 0

        if stage_rhel_directoryserver > rhel_directoryserver:
            rhel_directoryserver = stage_rhel_directoryserver
            stage_rhel_directoryserver = 0
        
        if (tag != "none"):
            update_max_value_by_tag(stage_by_tag, max_by_tag)


    print("On-Demand, HA Node ...........................: {}".format(rhel_ha))
    if (tag != "none"):
        for tagvalue in max_by_tag:
            util.pretty_print(2,tagvalue, max_by_tag[tagvalue]['ha'])
    print("On-Demand, Directory Server Node .............: {}".format(rhel_directoryserver))
    if (tag != "none"):
        for tagvalue in max_by_tag:
            util.pretty_print(2,tagvalue, max_by_tag[tagvalue]['ds'])
    print("")


def count_addons_value_by_tag(addon_type, stage_by_tag, tagvalue):
    if (tagvalue in stage_by_tag):
        tag_summary = stage_by_tag.get(tagvalue)
    else:
        tag_summary = stage_by_tag.setdefault(tagvalue, { 'ha':0, 'ds': 0})
    if addon_type == "ha":
        tag_summary['ha'] = tag_summary['ha'] + 1
    elif addon_type == "ds":
        tag_summary['ds'] = tag_summary['ds'] + 1

def update_max_value_by_tag(stage_by_tag, max_by_tag):
    for tagvalue in stage_by_tag:

        if (tagvalue in max_by_tag):
            if (stage_by_tag[tagvalue]['ha'] > max_by_tag[tagvalue]['ha']):
                max_by_tag[tagvalue]['ha'] = stage_by_tag[tagvalue]['ha']
            if (stage_by_tag[tagvalue]['ds'] > max_by_tag[tagvalue]['ds']):
                max_by_tag[tagvalue]['ds'] = stage_by_tag[tagvalue]['ds']
            
        else:
            max_by_tag.setdefault(tagvalue, { 'ha': stage_by_tag[tagvalue]['ha'], 'ds': stage_by_tag[tagvalue]['ds']})
            