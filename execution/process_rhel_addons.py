import csv
from execution import util

def ondemand_rhel_related_products(path_to_csv_dir, csv_files_list, tag):
    """
    TODO
    """

    # for debug purposes
    # print(path_to_csv_dir)
    # print(csv_files_list)

    CURRENT_TIMEFRAME_YEAR = util.get_year_from_path(path_to_csv_dir)
    CURRENT_TIMEFRAME_MONTH = util.get_month_from_path(path_to_csv_dir)
    CURRENT_TIMEFRAME = CURRENT_TIMEFRAME_YEAR + "-" + CURRENT_TIMEFRAME_MONTH

    rhel_ha_physical = 0
    rhel_ha_virtual =0
    rhel_directoryserver = 0
    for sheet in csv_files_list:

        # adding rhel_ha physical and virtual

        stage_rhel_ha_physical = 0
        stage_rhel_ha_virtual = 0
        stage_rhel_directoryserver = 0

        with open(path_to_csv_dir + "/" + sheet, "r") as file_obj:
            csv_file = csv.reader(file_obj)
            for row in csv_file:
                # print(row)

                infrastructure_type = row[21]
                installed_product = row[35]

                # HA is covered by products 83, 84 and 159
                if ('83' in installed_product) or ('84' in installed_product) or ('159' in installed_product):
                    if infrastructure_type == "physical":
                        stage_rhel_ha_physical = stage_rhel_ha_physical + 1
                    elif infrastructure_type == "virtual":
                        stage_rhel_ha_virtual = stage_rhel_ha_virtual + 1

                # Directory Server is covered by product 200
                if ('200' in installed_product):
                        stage_rhel_directoryserver = stage_rhel_directoryserver + 1

        if stage_rhel_ha_physical > rhel_ha_physical:
            rhel_ha_physical = stage_rhel_ha_physical
            stage_rhel_ha_physical = 0

        if stage_rhel_ha_virtual > rhel_ha_virtual:
            rhel_ha_virtual = stage_rhel_ha_virtual
            stage_rhel_ha_virtual = 0

        if stage_rhel_directoryserver > rhel_directoryserver:
            rhel_directoryserver = stage_rhel_directoryserver
            stage_rhel_directoryserver = 0


    print("On-Demand, High Availability, Physical Node...: {}".format(rhel_ha_physical))
    print("On-Demand, High Availability, Virtual Node....: {}".format(rhel_ha_virtual))
    print("On-Demand, Directory Server Node .............: {}".format(rhel_directoryserver))
    print("")
