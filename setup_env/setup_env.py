import os
import json

home_dir = os.path.expanduser("~")
CONF_FILE = home_dir + "/.hcs_collect.conf"


def standard_conf_file():
    """
    TODO
    """
    # print("standard conf file")
    dic_conf = {"base_dir": "", "crhc_cli": ""}

    if not os.path.exists(CONF_FILE):
        # print("conf file doesnt exist")
        with open(CONF_FILE, "w") as file_obj:
            file_obj.write(json.dumps(dic_conf, indent=4))
    else:
        # print("conf file is there")
        pass


def setup_basedir():
    """
    TODO
    """
    print("setup basedir path")
    home_dir = os.path.expanduser("~")

    base_dir = input("Please, type the path to the dir that will be used to store the data [~/hcs_data]: ")
    if (base_dir == ""):
        base_dir = home_dir + "/hcs_data"

    print(base_dir)

    if os.path.exists(base_dir) and os.path.isdir(base_dir):
        print("the dir is present")
        update_conf_file("base_dir", base_dir)
    else:
        print("please, fix the base_dir path")
    pass


def setup_crhc_path():
    """
    TODO
    """
    print("setup crhc path")

    crhc_cli_path = input("Please, type the path to the crhc-cli binary: ")
    if (crhc_cli_path == ""):
        print("Please, you need to type a valid path!")

    print(crhc_cli_path)

    if os.path.exists(crhc_cli_path) and os.path.isfile(crhc_cli_path):
        print("the file is present")
        update_conf_file("crhc", crhc_cli_path)
    else:
        print("please, fix the crhc-cli path")


def update_conf_file(field, path):
    """
    TODO
    """
    print("updating conf file")
    with open(CONF_FILE, "r") as file_obj:
        current_value_dic = json.load(file_obj)
        # print(current_value_dic)

    if field == "crhc":
        current_value_dic['crhc_cli'] = path

        with open(CONF_FILE, "w") as file_obj:
            file_obj.write(json.dumps(current_value_dic, indent=4))

    if field == "base_dir":
        current_value_dic['base_dir'] = path

        with open(CONF_FILE, "w") as file_obj:
            file_obj.write(json.dumps(current_value_dic, indent=4))


def view_current_conf():
    """
    TODO
    """
    # print("view the current configuration")

    try:

        with open(CONF_FILE, "r") as file_obj:
            aux = json.load(file_obj)
            # print(json.dumps(aux, indent=4))
            return aux
    except FileNotFoundError:
        print("Conf file {} not found. You need to inform the base-dir and crhc-cli path".format(CONF_FILE))
