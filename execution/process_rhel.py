import json
from execution import util

def ondemand_rhel(path_to_json_dir, json_files_list, tag):
    """
    TODO
    """

    # for debug purposes
    # print(path_to_csv_dir)
    # print(csv_files_list)

    CURRENT_TIMEFRAME_YEAR = path_to_json_dir.split("/")[4]
    CURRENT_TIMEFRAME_MONTH = path_to_json_dir.split("/")[5]
    CURRENT_TIMEFRAME = CURRENT_TIMEFRAME_YEAR + "-" + CURRENT_TIMEFRAME_MONTH

    # max values for the month
    rhel_physical = 0
    rhel_virtual = 0
    unknown = 0
    max_by_tag = {}

    for jsonFile in json_files_list:


        #counted values for this sheet/day
        stage_rhel_physical = 0
        stage_rhel_virtual = 0
        stage_unknown = 0
        stage_by_tag = {}

        with open(path_to_json_dir + "/" + jsonFile, "r") as file_obj:
            data = json.load(file_obj)
            
            if ('data' in data):
                for swatch_item in data['data']:
                # print(row)
                    infrastructure_type = swatch_item.get('hardware_type')
                    vmtags = swatch_item.get('tags')
                    tagvalue=""
                    if (tag != "none"):
                        #check if tag exists in vmtags
                        tagvalue = util.get_tag_value_from_json(vmtags, tag)
                    
                    if (tag != "none" and tagvalue!=""):
                        count_rhel_value_by_tag(infrastructure_type, stage_by_tag, tagvalue)

                    if infrastructure_type == "PHYSICAL":
                        stage_rhel_physical = stage_rhel_physical + 1
                    elif infrastructure_type == "VIRTUALIZED":
                        stage_rhel_virtual = stage_rhel_virtual + 1
                    else:
                        stage_unknown = stage_unknown + 1

        # check whether this day's numbers are bigger than the largest this month so far
        if stage_rhel_physical > rhel_physical:
            rhel_physical = stage_rhel_physical 

        if stage_rhel_virtual > rhel_virtual:
            rhel_virtual = stage_rhel_virtual
        
        if stage_unknown > unknown:
            unknown = stage_unknown
        
        if (tag != "none"):
            update_max_value_by_tag(stage_by_tag, max_by_tag)


    print("Max Concurrent RHEL On-Demand, referrent to ..: {}".format(CURRENT_TIMEFRAME))
    print("On-Demand, Physical Node .....................: {}".format(rhel_physical))
    if (tag != "none"):
        for tagvalue in max_by_tag:
            util.pretty_print(2,tagvalue, max_by_tag[tagvalue]['physical'])
    print("On-Demand, Virtual Node ......................: {}".format(rhel_virtual))
    if (tag != "none"):
        for tagvalue in max_by_tag:
            util.pretty_print(2,tagvalue, max_by_tag[tagvalue]['virtual'])
    print("Unknown ......................................: {}".format(unknown))
    print("")



def update_max_value_by_tag(stage_by_tag, max_by_tag):
    for tagvalue in stage_by_tag:

        if (tagvalue in max_by_tag):
            if (stage_by_tag[tagvalue]['physical'] > max_by_tag[tagvalue]['physical']):
                max_by_tag[tagvalue]['physical'] = stage_by_tag[tagvalue]['physical']
            if (stage_by_tag[tagvalue]['virtual'] > max_by_tag[tagvalue]['virtual']):
                max_by_tag[tagvalue]['virtual'] = stage_by_tag[tagvalue]['virtual']
            if (stage_by_tag[tagvalue]['unknown'] > max_by_tag[tagvalue]['unknown']):
                max_by_tag[tagvalue]['unknown'] = stage_by_tag[tagvalue]['unknown']
        else:
            max_by_tag.setdefault(tagvalue, { 'physical': stage_by_tag[tagvalue]['physical'], 'virtual': stage_by_tag[tagvalue]['virtual'], 'unknown': stage_by_tag[tagvalue]['unknown']})
            

def count_rhel_value_by_tag(infrastructure_type, stage_by_tag, tagvalue):
    if (tagvalue in stage_by_tag):
        tag_summary = stage_by_tag.get(tagvalue)
    else:
        tag_summary = stage_by_tag.setdefault(tagvalue, { 'physical':0, 'virtual': 0, 'unknown': 0})
    if infrastructure_type == "PHYSICAL":
        tag_summary['physical'] = tag_summary['physical'] +1
    elif infrastructure_type == "VIRTUALIZED":
        tag_summary['virtual'] = tag_summary['virtual'] +1
    else:
        tag_summary['unknown'] = tag_summary['unknown'] +1

