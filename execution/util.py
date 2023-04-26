import datetime
import json
import subprocess
from execution import token

def pretty_print(indent, msg, value):
    pretty_msg = ""
    for x in range(indent):
        pretty_msg = pretty_msg +" "
    pretty_msg = pretty_msg + msg + " "
    msg_len = len(pretty_msg)
    for x in range(msg_len,46):
        pretty_msg = pretty_msg + "."
    pretty_msg = pretty_msg + ": " + str(value)
    print (pretty_msg)

def get_tag_value (taglist, tag):
    #print(taglist)
    tag_value=""
    if (tag in taglist):
        #print(" found " + tag + " in " + taglist)
        starting_with_tag = taglist[taglist.index(tag):]
        if (";" in starting_with_tag):
            starting_with_tag = starting_with_tag[:starting_with_tag.index(";")]
        if("=" in starting_with_tag):
            tag_value = starting_with_tag[starting_with_tag.index("=")+1:]
    return tag_value

def get_tag_value_from_json (json_tag_array, tag):
    #print(taglist)
    tag_value=""
    if (json_tag_array):
        for vmtag in json_tag_array:
            if (vmtag.get('key') == tag):
                tag_value = vmtag.get('value')
    return tag_value

def is_fresh(stale_timestamp, year, month, day):
    stale_date_string = stale_timestamp
    is_fresh=True
    if (len(stale_date_string) > 19):
        stale_date_string = stale_timestamp[:19]
    try: 
        stale_date = datetime.datetime.strptime(stale_date_string,"%Y-%m-%dT%H:%M:%S")
        current_time = datetime.datetime.today().time()
        current_date = datetime.datetime(int(year),int(month),int(day), current_time.hour, current_time.minute, current_time.second)
        if (stale_date < current_date):
            is_fresh = False
    except Exception as e:
        is_fresh=True
        print("Exception in is_fresh : " + str(e))
    
    return is_fresh

def make_crhc_api_call(command):
    tries=0
    done = False
    result = ""
    while tries <3 and not done:
        try:
            text_result = subprocess.check_output(command,text=True)
            result = json.loads(text_result)
            done = True
        except subprocess.CalledProcessError as e:
            tries = tries +1
            print ("Exception in append_system_profile: " + str(e))
            #print ("APi call was : " + end_url)
            print ("trying again - " + str(tries) + " of 3")
        except Exception as e2:
            print ("Exception in append_system_profile: " + str(e2))
            tries = tries +1
    return result

