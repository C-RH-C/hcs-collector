import csv
from execution import util

def process_rhel_versions(path_to_csv_dir, csv_files_list, tag):
    """
    TODO
    """

    # for debug purposes
    # print(path_to_csv_dir)
    # print(csv_files_list)

    CURRENT_TIMEFRAME_YEAR = path_to_csv_dir.split("/")[4]
    CURRENT_TIMEFRAME_MONTH = path_to_csv_dir.split("/")[5]
    CURRENT_TIMEFRAME = CURRENT_TIMEFRAME_YEAR + "-" + CURRENT_TIMEFRAME_MONTH
    OS_VERSIONS = ['5','6','7','8','9']

    # max values for the month
    max_versions={}
    max_versions_by_tag = {}

    for sheet in csv_files_list:

        #counted values for this sheet/day
        stage_versions={}
        stage_versions_by_tag = {}

        with open(path_to_csv_dir + "/" + sheet, "r") as file_obj:
            csv_file = csv.reader(file_obj)
            
            for row in csv_file:
                # print(row)
                installed_product = row[35]
                os_version = row[17]
                major_os = os_version[0]
                infrastructure_type = row[21]
                # only want infra type to be physical or virtual - so if not physical, assume virtual
                if (infrastructure_type != 'physical'):
                    infrastructure_type='virtual'
                vmtags = row[len(row)-1]
                tagvalue=""
                if (tag != "none"):
                    #check if tag exists in vmtags
                    tagvalue = util.get_tag_value(vmtags, tag)
                

                if (tag != "none" and tagvalue!=""):
                    count_rhel_version_by_tag(major_os, infrastructure_type, stage_versions_by_tag, tagvalue)

                if (major_os not in stage_versions):
                    stage_versions.setdefault(major_os, {'physical':0, 'virtual':0})
                stage_count = stage_versions.get(major_os).get(infrastructure_type)
                stage_versions[major_os][infrastructure_type] = stage_count+1

                    

        # check whether this day's numbers are bigger than the largest this month so far
        for major_os in OS_VERSIONS:
            if (major_os in max_versions) and (major_os in stage_versions):
                # Have both a previous high mark, and mark for today - so need to compare
                if (stage_versions[major_os]['physical'] > max_versions[major_os]['physical']):
                    max_versions[major_os]['physical'] = stage_versions[major_os]['physical']
                if (stage_versions[major_os]['virtual'] > max_versions[major_os]['virtual']):
                    max_versions[major_os]['virtual'] = stage_versions[major_os]['virtual']
            elif (major_os in stage_versions):
                # First time this os has been found for this month
                max_versions.setdefault(major_os, {'physical':0, 'virtual':0})
                max_versions[major_os]['physical'] = stage_versions[major_os]['physical']
                max_versions[major_os]['virtual'] = stage_versions[major_os]['virtual']
            else:
                # If there isnt a value for this OS - put in a zero
                if (major_os not in max_versions):
                    max_versions.setdefault(major_os, {'physical':0, 'virtual':0})

            if (tag != "none"):
                update_max_version_by_tag(stage_versions_by_tag, max_versions_by_tag, major_os, infrastructure_type)


    print("Max Concurrent RHEL On-Demand, by version ....: {}".format(CURRENT_TIMEFRAME))
    for major_os in OS_VERSIONS:
        if (major_os in max_versions):
            print("On-Demand, Physical RHEL " + major_os + "....................: {}".format(max_versions[major_os]['physical']))
            if (tag != "none"):
                for tagvalue in max_versions_by_tag:
                    if (max_versions_by_tag[tagvalue][major_os]['physical'] >0):
                        util.pretty_print(2,tagvalue, max_versions_by_tag[tagvalue][major_os]['physical'])
            print("On-Demand, Virtual RHEL " + major_os + ".....................: {}".format(max_versions[major_os]['virtual']))
            if (tag != "none"):
                for tagvalue in max_versions_by_tag:
                    if (max_versions_by_tag[tagvalue][major_os]['virtual'] >0):
                        util.pretty_print(2,tagvalue, max_versions_by_tag[tagvalue][major_os]['virtual'])
        else:
            print("On-Demand, Physical RHEL " + major_os + "....................: 0")
            print("On-Demand, Virtual RHEL " + major_os + ".....................: 0")
    
    print("")



def update_max_version_by_tag(stage_by_tag, max_by_tag, major_os, infra_type):
    
    if (major_os.isdigit()):
        for tagvalue in stage_by_tag:
    
            if (tagvalue in max_by_tag):
                if (stage_by_tag[tagvalue][major_os][infra_type] > max_by_tag[tagvalue][major_os][infra_type]):
                    max_by_tag[tagvalue][major_os][infra_type] = stage_by_tag[tagvalue][major_os][infra_type]
            else:
                max_by_tag.setdefault(tagvalue, { '5':{'physical':0,'virtual':0}, '6': {'physical':0,'virtual':0}, '7':{'physical':0,'virtual':0}, '8':{'physical':0,'virtual':0}, '9':{'physical':0,'virtual':0}})
                max_by_tag[tagvalue][major_os][infra_type] = stage_by_tag[tagvalue][major_os][infra_type]
            

def count_rhel_version_by_tag(major_os, infrastructure_type, versions_by_tag, tagvalue):
    
    if (major_os.isdigit()):
        if (tagvalue in versions_by_tag):
            tag_summary = versions_by_tag.get(tagvalue)
        else:
            tag_summary = versions_by_tag.setdefault(tagvalue, { '5':{'physical':0,'virtual':0}, '6': {'physical':0,'virtual':0}, '7':{'physical':0,'virtual':0}, '8':{'physical':0,'virtual':0}, '9':{'physical':0,'virtual':0}})

        tag_summary[major_os][infrastructure_type] = tag_summary.get(major_os).get(infrastructure_type) +1
   

