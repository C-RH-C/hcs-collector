
import os
import json
import subprocess
import time
from execution import util

def download(swatchfile, crhc_cli):
    batch_size=50
    os.system(crhc_cli + " swatch list_all > " + swatchfile)
    

def append_tags_to_swatch_array(swatch_item_array, crhc_cli):
    # this is going to get tags in batches, and add to original downloaded swatch data in order to reduce time
    is_first = True
    crhc_api = "/api/inventory/v1/hosts/"
    for swatch_item in swatch_item_array:
      if (is_first):
          crhc_api = crhc_api + swatch_item.get('inventory_id')
          is_first = False
      else:
          crhc_api = crhc_api + ","+  swatch_item['inventory_id']
    
    if (not is_first):
        # This means there is at least one entry in the array
        #print("api call is : " + crhc_cli + crhc_api + "/tags > /tmp/tags.json")
        tag_result=util.make_crhc_api_call([crhc_cli,"get",crhc_api + "/tags"])
 
        if ('results' in tag_result):
            # now loop over the swatch_item_array, finding the tags in the results, and adding them to the json
            for swatch_item in swatch_item_array:
                id = swatch_item['inventory_id']
                if (tag_result['results'].get(id)):
                    tagid = tag_result['results'].get(id)
                    swatch_item['tags'] = tagid

