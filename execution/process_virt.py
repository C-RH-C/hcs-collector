import json
from execution import util

def ondemand_virtualization(path_to_json_dir, json_files_list, tag):
    """
    TODO
    """

    # for debug purposes
    # print(path_to_csv_dir)
    # print(csv_files_list)

    CURRENT_TIMEFRAME_YEAR = path_to_json_dir.split("/")[4]
    CURRENT_TIMEFRAME_MONTH = path_to_json_dir.split("/")[5]
    CURRENT_TIMEFRAME = CURRENT_TIMEFRAME_YEAR + "-" + CURRENT_TIMEFRAME_MONTH

    max_by_tag = {}
    virtualization_sockets = 0
    for jsonFile in json_files_list:

        stage_virtualization_sockets = 0
        stage_by_tag = {}
        
        with open(path_to_json_dir + "/" + jsonFile, "r") as file_obj:
            data = json.load(file_obj)
            if ('results' in data):
                for inventoryItem in data['results']:

                    system_profile = inventoryItem['system_profile']
                    number_of_sockets = 1
                    installed_products = []
                    if ('installed_products' in system_profile): installed_products = system_profile['installed_products']
                    if ('number_of_sockets' in system_profile): number_of_sockets = system_profile['number_of_sockets']

                    
                    tagvalue=""
                    if (tag != "none"):
                        #check if tag exists in vmtags
                        tagvalue = util.get_json_tag_value(inventoryItem.get('server').get('tags'), tag)

                    installed_product_list = []
                    for product in installed_products:
                        installed_product_list.append(product['id'])

                    # RHV is covered by products 150, 328, and 415 
                    if ('150' in installed_product_list) or ('328' in installed_product_list) or ('415' in installed_product_list):
                        if (tag != "none" and tagvalue!=""):
                            count_rhev_value_by_tag(infrastructure_type, stage_by_tag, tagvalue)
                        stage_virtualization_sockets = stage_virtualization_sockets + number_of_sockets


        if stage_virtualization_sockets > virtualization_sockets:
            virtualization_sockets = stage_virtualization_sockets
            update_rhv_value_by_tag(stage_by_tag, max_by_tag)

    

    print("On-Demand, Virtualization Sockets ............: {}".format(virtualization_sockets))
    if (tag != "none"):
        for tagvalue in max_by_tag:
            util.pretty_print(2,tagvalue, max_by_tag[tagvalue]['sockets'])
    print("")

def update_rhv_value_by_tag(stage_by_tag, max_by_tag):
    for tagvalue in stage_by_tag:

        if (tagvalue in max_by_tag):
            if (stage_by_tag[tagvalue]['sockets'] > max_by_tag[tagvalue]['sockets']):
                max_by_tag[tagvalue]['sockets'] = stage_by_tag[tagvalue]['sockets']
            
        else:
            max_by_tag.setdefault(tagvalue, { 'sockets': stage_by_tag[tagvalue]['sockets']})

def count_rhev_value_by_tag(sockets, stage_by_tag, tagvalue):
    if (tagvalue in stage_by_tag):
        tag_summary = stage_by_tag.get(tagvalue)
    else:
        tag_summary = stage_by_tag.setdefault(tagvalue, { 'sockets':0})

    tag_summary['sockets'] = tag_summary['sockets'] +sockets