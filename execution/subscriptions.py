
import os
import json

def download(swatchfile, crhc_cli):
    batch_size=10
    os.system(crhc_cli + " swatch list_all > " + swatchfile)
    with open(swatchfile, "r") as file_obj:
        result = json.load(file_obj)
        if ('data' in result):
          swatch_data = result['data']
          batch_count=0
          swatch_batch = []
          crhc_api = "get /api/inventory/v1/hosts/"
          for swatch_item in swatch_data:
              if (batch_count< batch_size-1):
                  swatch_batch.append(swatch_item)
                  batch_count = batch_count+1
              else:
                  # we've now got to the batch size - so going to go and get the tags and augment the values
                  swatch_batch.append(swatch_item)
                  append_tags_to_swatch_array(swatch_batch, crhc_api)
                  batch_count=0
                  swatch_batch = []
          # just process the last few ids
          if (swatch_batch.count >0):
              append_tags_to_swatch_array(swatch_batch, crhc_api)
    # we've iterated over all items and got the tags - now write the appended values back to the file
    with open(swatchfile, "w") as file_obj:
        json.dump(result,file_obj, indent=2)
        

def append_tags_to_swatch_array(swatch_item_array, crhc_cli):
    # this is going to get tags in batches, and add to original downloaded swatch data in order to reduce time
    is_first = True
    crhc_api = " get /api/inventory/v1/hosts/"
    for swatch_item in swatch_item_array:
      if (is_first):
          crhc_api = crhc_api + swatch_item.get('inventory_id')
          is_first = False
      else:
          crhc_api = crhc_api + ","+  swatch_item['inventory_id']
    
    if (not is_first):
        # This means there is at least one entry in the array
        print("api call is : " + crhc_cli + crhc_api + "/tags > /tmp/tags.json")
        os.system(crhc_cli + crhc_api + "/tags > /tmp/tags.json")
        with open("/tmp/tags.json", "r") as file_tag:
            tag_result=json.load(file_tag)
            if ('results' in tag_result):
                # now loop over the swatch_item_array, finding the tags in the results, and adding them to the json
                for swatch_item in swatch_item_array:
                    id = swatch_item['inventory_id']
                    if (tag_result['results'].get(id)):
                        tagid = tag_result['results'].get(id)
                        swatch_item['tags'] = tagid

