import os
import json
import subprocess
import time
from execution import util



def download(invfile, crhc_cli):
    batch_size=50
    get_host_info(invfile, crhc_cli, batch_size)
    print('got host info : ' + time.ctime())
    with open(invfile, "r") as file_obj:
        data = json.load(file_obj)
        if ('results' in data):
            
            batch_count=0
            inventory_batch = []
            number_batches=0
            for inventory_item in data['results']:

                if (batch_count< batch_size-1):
                    inventory_batch.append(inventory_item)
                    batch_count = batch_count+1
                else:
                    # we've now got to the batch size - so going to go and get the tags and augment the values
                    number_batches = number_batches+1
                    if number_batches%20 == 0:
                        print('Batch : '  +str(number_batches) + time.ctime())
                    inventory_batch.append(inventory_item)
                    append_tags_to_inventory_array(inventory_batch, crhc_cli)
                    append_system_profile_to_inventory_array(inventory_batch, crhc_cli)
                    batch_count=0
                    inventory_batch = []
            # just process the last few ids
            if (len(inventory_batch) >0):
                print('Batch : Final Batch ' + time.ctime())
                append_tags_to_inventory_array(inventory_batch, crhc_cli)
                append_system_profile_to_inventory_array(inventory_batch, crhc_cli)
    print('appended system_details : '  + time.ctime())
    # we've iterated over all items and got the tags - now write the appended values back to the file
    with open(invfile, "w") as file_obj:
        json.dump(data,file_obj, indent=2)
    print('writing json file : '  + time.ctime())

def get_host_info(invfile, crhc_cli, batch_size):

    # first thing, lets get the overall page size.

    size_json = util.make_crhc_api_call([crhc_cli,"get","/api/inventory/v1/hosts?per_page=50"])

    check_response = divmod(size_json["total"], batch_size)

    if check_response[1] == 0:
        num_of_pages = check_response[0] + 1
    else:
        num_of_pages = check_response[0] + 2

    
    
    list_of_servers = []
    inventory_full_detail = {"results": "", "total": size_json["total"]}
    inventory_full_detail["results"] = list_of_servers
    stage_list = []
    stage_dic = {"server": stage_list}

    for page in range(1, num_of_pages):
        api = crhc_cli
        response = util.make_crhc_api_call([crhc_cli,"get","/api/inventory/v1/hosts?per_page=" + str(batch_size)+ "&page=" + str(page)])
        for server in response["results"]:

            try:
                stage_dic["server"] = server
            except json.decoder.JSONDecodeError:
                stage_dic["server"] = {}

            list_of_servers.append(stage_dic)
            stage_dic = {}
    
    print("Number of servers in inventory = " + str(len(inventory_full_detail["results"])))
    with open(invfile, "w") as file_obj:
        json.dump(inventory_full_detail,file_obj, indent=2)





def append_tags_to_inventory_array(inventory_item_array, crhc_cli):
    # this is going to get tags in batches, and add to original downloaded inventory data in order to reduce time
    is_first = True
    crhc_api = "/api/inventory/v1/hosts/"
    for inventory_item in inventory_item_array:
      if (is_first):
          crhc_api = crhc_api + inventory_item.get('server').get('id')
          is_first = False
      else:
          crhc_api = crhc_api + ","+  inventory_item.get('server').get('id')
    
    if (not is_first):
        # This means there is at least one entry in the array
        # print("api call is : " + crhc_cli + crhc_api + "/tags > /tmp/tags.json")
        tag_result = util.make_crhc_api_call([crhc_cli,"get",crhc_api + "/tags"])
        if ('results' in tag_result):
            # now loop over the inventory_item_array, finding the tags in the results, and adding them to the json
            for inventory_item in inventory_item_array:
                id = inventory_item.get('server').get('id')
                if (tag_result['results'].get(id)):
                    tagid = tag_result['results'].get(id)
                    inventory_item.get('server')['tags'] = tagid

def append_system_profile_to_inventory_array(inventory_item_array, crhc_cli):
    # this is going to get tags in batches, and add to original downloaded inventory data in order to reduce time
    is_first = True
    crhc_api = "/api/inventory/v1/hosts/"
    for inventory_item in inventory_item_array:
      if (is_first):
          crhc_api = crhc_api + inventory_item.get('server').get('id')
          is_first = False
      else:
          crhc_api = crhc_api + ","+  inventory_item.get('server').get('id')
    

    if (not is_first):
        # This means there is at least one entry in the array
        # print("api call is : " + crhc_cli + crhc_api + "/tags > /tmp/tags.json")
        profile_result = util.make_crhc_api_call([crhc_cli,"get",crhc_api + '/system_profile'])
        
        if ('results' in profile_result):
            for system_profile in profile_result['results']:
   
                # now loop over the inventory_item_array, finding the tags in the results, and adding them to the json
                for inventory_item in inventory_item_array:
                    id = inventory_item.get('server').get('id')
                    if (system_profile['id'] == id):
                        profile = system_profile['system_profile']
                        inventory_item['system_profile'] = profile

