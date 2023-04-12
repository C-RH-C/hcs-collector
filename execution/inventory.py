import os
import json

def download(invfile, crhc_cli):
    batch_size=50
    os.system(crhc_cli + " inventory list_all > " + invfile)
    
    with open(invfile, "r") as file_obj:
        data = json.load(file_obj)
        if ('results' in data):
            batch_count=0
            inventory_batch = []
            for inventory_item in data['results']:

                if (batch_count< batch_size-1):
                    inventory_batch.append(inventory_item)
                    batch_count = batch_count+1
                else:
                    # we've now got to the batch size - so going to go and get the tags and augment the values
                    inventory_batch.append(inventory_item)
                    append_tags_to_inventory_array(inventory_batch, crhc_cli)
                    batch_count=0
                    inventory_batch = []
            # just process the last few ids
            if (len(inventory_batch) >0):
                append_tags_to_inventory_array(inventory_batch, crhc_cli)
    # we've iterated over all items and got the tags - now write the appended values back to the file
    with open(invfile, "w") as file_obj:
        json.dump(data,file_obj, indent=2)

def append_tags_to_inventory_array(inventory_item_array, crhc_cli):
    # this is going to get tags in batches, and add to original downloaded inventory data in order to reduce time
    is_first = True
    crhc_api = " get /api/inventory/v1/hosts/"
    for inventory_item in inventory_item_array:
      if (is_first):
          crhc_api = crhc_api + inventory_item.get('server').get('id')
          is_first = False
      else:
          crhc_api = crhc_api + ","+  inventory_item.get('server').get('id')
    
    if (not is_first):
        # This means there is at least one entry in the array
        # print("api call is : " + crhc_cli + crhc_api + "/tags > /tmp/tags.json")
        os.system(crhc_cli + crhc_api + "/tags > /tmp/tags.json")
        with open("/tmp/tags.json", "r") as file_tag:
            tag_result=json.load(file_tag)
            if ('results' in tag_result):
                # now loop over the inventory_item_array, finding the tags in the results, and adding them to the json
                for inventory_item in inventory_item_array:
                    id = inventory_item.get('server').get('id')
                    if (tag_result['results'].get(id)):
                        tagid = tag_result['results'].get(id)
                        inventory_item.get('server')['tags'] = tagid
