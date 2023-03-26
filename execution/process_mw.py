import json

def ondemand_mw_from_json(path_to_json_dir, json_files_list, tag):
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