import json

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
