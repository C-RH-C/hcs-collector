import json
from execution import util

def ondemand_ansible_from_json(path_to_json_dir, json_files_list, tag):
    """
    TODO
    """

    # for debug purposes
    # print(path_to_csv_dir)
    # print(csv_files_list)

    CURRENT_TIMEFRAME_YEAR = path_to_json_dir.split("/")[4]
    CURRENT_TIMEFRAME_MONTH = path_to_json_dir.split("/")[5]
    CURRENT_TIMEFRAME = CURRENT_TIMEFRAME_YEAR + "-" + CURRENT_TIMEFRAME_MONTH

    ansible_unique_hosts = 0

    for jsonFile in json_files_list:

        stage_ansible_unique_hosts = 0

        if ('ansible' in jsonFile ) :
            with open(path_to_json_dir + "/" + jsonFile, "r") as file_obj:
                data = json.load(file_obj)
                if ('total_unique_host_count' in data):
                    stage_ansible_unique_hosts = data['total_unique_host_count']
                    if (stage_ansible_unique_hosts > ansible_unique_hosts):
                        ansible_unique_hosts = stage_ansible_unique_hosts
                    

    print("On-Demand, Ansible Managed Hosts .............: {}".format(ansible_unique_hosts))
    
    print("")

