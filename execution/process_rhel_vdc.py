import csv
from execution import util

def virtualdatacenter_rhel(path_to_csv_dir, csv_files_list, tag):
    """
    TODO
    """

    CURRENT_TIMEFRAME_YEAR = util.get_year_from_path(path_to_csv_dir)
    CURRENT_TIMEFRAME_MONTH = util.get_month_from_path(path_to_csv_dir)
    CURRENT_TIMEFRAME = CURRENT_TIMEFRAME_YEAR + "-" + CURRENT_TIMEFRAME_MONTH

    for sheet in csv_files_list:

        virt_who = 0
        stage_virt_who = 0
        vdc_sockets = 0
        stage_vdc_sockets = 0

        with open(path_to_csv_dir + "/" + sheet, "r") as file_obj:
            csv_file = csv.reader(file_obj)
            for row in csv_file:
                # print(row)

                infrastructure_type = row[21]
                number_of_guests = row[40]

                if (infrastructure_type == "physical") and (number_of_guests.isnumeric()):
                    stage_virt_who = stage_virt_who + 1

                    hypervisor_number_of_sockets = 0
                    if (row[11].isnumeric()):
                        hypervisor_number_of_sockets = int(row[11])
                    stage_vdc_sockets = stage_vdc_sockets + hypervisor_number_of_sockets

    if stage_virt_who > virt_who:
        virt_who = stage_virt_who
        stage_virt_who = 0

    if stage_vdc_sockets > vdc_sockets:
        vdc_sockets = stage_vdc_sockets
        stage_vdc_sockets = 0

    print("Virtual Data Center, Hypervisor ..............: {}".format(virt_who))
    print("Virtual Data Center, Hypervisor Sockets ......: {}".format(vdc_sockets))
    print("")