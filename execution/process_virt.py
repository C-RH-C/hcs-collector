import csv
from execution import util

def ondemand_virtualization(path_to_csv_dir, csv_files_list, tag):
    """
    TODO
    """

    # for debug purposes
    # print(path_to_csv_dir)
    # print(csv_files_list)

    CURRENT_TIMEFRAME_YEAR = util.get_year_from_path(path_to_csv_dir)
    CURRENT_TIMEFRAME_MONTH = util.get_month_from_path(path_to_csv_dir)
    CURRENT_TIMEFRAME = CURRENT_TIMEFRAME_YEAR + "-" + CURRENT_TIMEFRAME_MONTH

    max_by_tag = {}
    virtualization_sockets = 0
    for sheet in csv_files_list:

        stage_virtualization_sockets = 0
        stage_by_tag = {}
        
        

        with open(path_to_csv_dir + "/" + sheet, "r") as file_obj:
            csv_file = csv.reader(file_obj)
            for row in csv_file:
                # print(row)

                infrastructure_type = row[21]
                installed_product = row[35]
                vmtags = row[len(row)-1]
                tagvalue=""
                if (tag != "none"):
                    #check if tag exists in vmtags
                    tagvalue = util.get_tag_value(vmtags, tag)

                number_of_sockets = 1
                if (row[11].isnumeric()):
                    number_of_sockets = int(row[11])

                # RHV is covered by products 150, 328, and 415 
                if ('150' in installed_product) or ('328' in installed_product) or ('415' in installed_product):
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
    
    if (sockets.isdigit()):
        if (tagvalue in stage_by_tag):
            tag_summary = stage_by_tag.get(tagvalue)
        else:
            tag_summary = stage_by_tag.setdefault(tagvalue, { 'sockets':0})

        tag_summary['sockets'] = tag_summary['sockets'] + int(sockets)