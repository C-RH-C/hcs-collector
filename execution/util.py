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

def get_year_from_path(file_path):
    path_array = file_path.split("/")
    year = path_array[len(path_array) -3]
    return year

def get_month_from_path(file_path):
    path_array = file_path.split("/")
    month = path_array[len(path_array) -2]
    return month
    