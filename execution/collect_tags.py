import os
import csv 
import json

def append_tags_to_inventory_csv(dest_csv_file, crhc_cli):
    print("appending inventory tags to csv")
    results = []
    with open(dest_csv_file, "r") as file_obj:
        csv_file = csv.reader(file_obj)
        batch_size=50
        batch_count=0
        row_batch=[]
        first_row = True
        for row in csv_file:
            # ignore the header row of the csv file
            if (first_row):
                first_row = False
                results.append(row)
                continue
            if (batch_count< batch_size-1):
                row_batch.append(row)
                batch_count = batch_count+1
            else:
                # we've now got to the batch size - so going to go and get the tags and augment the values
                row_batch.append(row)
                append_tags_to_swatch_rows(row_batch, crhc_cli, results)
                batch_count=0
                row_batch = []
        # sweep up any left overs
        append_tags_to_swatch_rows(row_batch, crhc_cli, results)
            

    with open(dest_csv_file, "w+") as f:
        mywriter = csv.writer(f,delimiter=',') # ,quotechar='"'
        mywriter.writerows(results)

def append_tags_to_swatch_rows(swatch_row_array, crhc_cli, results):
    is_first = True
    crhc_api = " get /api/inventory/v1/hosts/"
    for swatch_row in swatch_row_array:
      if (is_first):
          crhc_api = crhc_api + swatch_row[0]
          is_first = False
      else:
          crhc_api = crhc_api + ","+  swatch_row[0]
    
    if (not is_first):
        # This means there is at least one entry in the array
        print("api call is : " + crhc_cli + crhc_api + "/tags > /tmp/tags.json")
        os.system(crhc_cli + crhc_api + "/tags > /tmp/tags.json")
        with open("/tmp/tags.json", "r") as file_tag:
            tag_result=json.load(file_tag)
            if ('results' in tag_result):
                for swatch_row in swatch_row_array:
                    id = swatch_row[0]
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
                        swatch_row.append(tag_string)
                    # append each modified row back into the results to be written back to the file
                    results.append(swatch_row)

def append_tags_to_inventory_json(dest_json_file, crhc_cli):
    print("appending inventory tags to json")
    batch_size=50
    with open(dest_json_file, "r") as file_obj:
        data = json.load(file_obj)
        if ('results' in data):
            batch_count=0
            inventory_batch = []
            for inventory_item in data['results']:
                # print(row)
                # get the number of cores.
                if (batch_count< batch_size-1):
                    inventory_batch.append(inventory_item)
                    batch_count = batch_count+1
                else:
                    # we've now got to the batch size - so going to go and get the tags and augment the values
                    inventory_batch.append(inventory_item)
                    append_tags_to_inventory_array(inventory_batch, crhc_cli)
                    batch_count=0
                    inventory_batch = []
            # just sweep up any left overs
            append_tags_to_inventory_array(inventory_batch, crhc_cli)

    with open(dest_json_file, "w") as file_obj:
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