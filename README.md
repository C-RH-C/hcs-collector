# **Archived Project**

For more information, please visit the issue [https://issues.redhat.com/browse/RHIN-2342](https://issues.redhat.com/browse/RHIN-2342)

---

# hcs-collector - Command Line Tool

Welcome to hcs-collector, this app will help our customers to collect daily the information from `console.redhat.com` and generate a report that will reflect some kind of consumption during the month for On-Demand subscriptions.

---

**Disclaimer**: This project or the binary files available in the Releases area are NOT delivered and/or released by Red Hat. This is an independent project to help customers and Red Hat Support team to export and/or collect the data from console.redhat.com for counting purposes of `HCS` or `Hybrid Committed Spend Program`. 

---

<h1>How it works?</h1>

Combined with [crhc-cli](https://github.com/C-RH-C/crhc-cli), this tool will collect the information daily, will keep the data in a place defined by the user and whenever the customer need, they will be able to generate the consumption report. The analysis process will be checking all the local files and will be presenting the `max concurrent value` of each month. At this moment, this is just a pilot and we are counting:

* RHEL Physical, Virtual and VDC
* RHEL versions (virtual and physical RHEL 5, 6, 7, 8 and 9)
* RHEL addons (HA and Directory Server)
* RHV
* JBoss Middleware (JBoss EAP and JWS)
* Ansible Managed Hosts

---

<h1>Main Menu</h1>

- Here you can see the main menu and some options that we have already

```
$ ./hcs-collector.py 
Usage: hcs-collector.py [OPTIONS] COMMAND [ARGS]...

  Command line tool for HCS - Hybrid Commited Spend

Options:
  --help  Show this message and exit.

Commands:
  collect  Collect the information using crhc-cli
  process  Only process the local information with no necessity of download
  setup    Setup the basic configuration
```

Basically, you need to configure [crhc-cli](https://github.com/C-RH-C/crhc-cli) to be working properly in your environment, after that, you can just download the `hcs-collector` binary from the release area, and execute the commands below

  - `./hcs-collector setup base-dir` to setup where you would like to store the data
  - `./hcs-collector setup crhc-cli` to setup where the crhc-cli binary is located

After that, you can execute 

  - `./hcs-collector collect` to download daily the files, feel free to add in your cronjob and
  - `./hcs-collector process [--tag='tagname']` anytime to proceed with the analysis.  Specifying a tag will break the analysis down by the values of that tag.  Tagging vms can be done with the insights client, by specifying a tag file in /etc/insights-client/tags.yaml 


---

<h1>Some Examples</h1>

- Here we can see the current configuration. All the information was adde via CLI tool.

```
$ ./hcs-collector.py setup view
{
    "base_dir": "/home/user/hcs_data",
    "crhc_cli": "/home/user/demo/crhc"
}
```

- Here we can see the content of the `hcs_data` directory

```
$ pwd
/home/user/hcs_data
$ tree .
.
└── 2022
    ├── 03
    │   ├── CSV
    │   │   ├── match_inv_sw_03-12-2022.csv
    │   │   ├── match_inv_sw_03-13-2022.csv
    │   │   ├── match_inv_sw_03-14-2022.csv
    │   │   ├── match_inv_sw_03-15-2022.csv
    │   │   ├── match_inv_sw_03-16-2022.csv
    │   │   ├── match_inv_sw_03-17-2022.csv
    │   │   ├── match_inv_sw_03-18-2022.csv
    │   │   ├── match_inv_sw_03-19-2022.csv
    │   │   ├── match_inv_sw_03-20-2022.csv
    │   │   ├── match_inv_sw_03-21-2022.csv
    │   │   ├── match_inv_sw_03-22-2022.csv
    │   │   ├── match_inv_sw_03-23-2022.csv
    │   │   ├── match_inv_sw_03-24-2022.csv
    │   │   ├── match_inv_sw_03-25-2022.csv
    │   │   ├── match_inv_sw_03-26-2022.csv
    │   │   ├── match_inv_sw_03-27-2022.csv
    │   │   ├── match_inv_sw_03-28-2022.csv
    │   │   ├── match_inv_sw_03-29-2022.csv
    │   │   ├── match_inv_sw_03-30-2022.csv
    │   │   └── match_inv_sw_03-31-2022.csv
    │   └── JSON
    │       ├── inventory_03-12-2022.json
    │       ├── inventory_03-13-2022.json
    │       ├── inventory_03-14-2022.json
    │       ├── inventory_03-15-2022.json
    │       ├── inventory_03-16-2022.json
    │       ├── inventory_03-17-2022.json
    │       ├── inventory_03-18-2022.json
    │       ├── inventory_03-19-2022.json
    │       ├── inventory_03-20-2022.json
    │       ├── inventory_03-21-2022.json
    │       ├── inventory_03-22-2022.json
    │       ├── inventory_03-23-2022.json
    │       ├── inventory_03-24-2022.json
    │       ├── inventory_03-25-2022.json
    │       ├── inventory_03-26-2022.json
    │       ├── inventory_03-27-2022.json
    │       ├── inventory_03-28-2022.json
    │       ├── inventory_03-29-2022.json
    │       ├── inventory_03-30-2022.json
    │       ├── inventory_03-31-2022.json
    │       ├── swatch_03-12-2022.json
    │       ├── swatch_03-13-2022.json
    │       ├── swatch_03-14-2022.json
    │       ├── swatch_03-15-2022.json
    │       ├── swatch_03-16-2022.json
    │       ├── swatch_03-17-2022.json
    │       ├── swatch_03-18-2022.json
    │       ├── swatch_03-19-2022.json
    │       ├── swatch_03-20-2022.json
    │       ├── swatch_03-21-2022.json
    │       ├── swatch_03-22-2022.json
    │       ├── swatch_03-23-2022.json
    │       ├── swatch_03-24-2022.json
    │       ├── swatch_03-25-2022.json
    │       ├── swatch_03-26-2022.json
    │       ├── swatch_03-27-2022.json
    │       ├── swatch_03-28-2022.json
    │       ├── swatch_03-29-2022.json
    │       ├── swatch_03-30-2022.json
    │       └── swatch_03-31-2022.json
    └── 04
        ├── CSV
        │   └── match_inv_sw_04-01-2022.csv
        └── JSON
            ├── inventory_04-01-2022.json
            └── swatch_04-01-2022.json

7 directories, 63 files
```

Note. The structure above will be created automatically. No manual intervention is required.


- And here we can see the output of `process` option

```
$ ./hcs-collector.py process

## RHEL On-Demand

Max Concurrent RHEL On-Demand, referrent to ..: 2022-03
On-Demand, Physical Node .....................: 973
On-Demand, Virtual Node ......................: 5092
Virtual Data Center, Virtual Node ............: 3742
Unknown ......................................: 0

## RHEL Versions

Max Concurrent RHEL On-Demand, by version ....: 2022-03
On-Demand, Physical RHEL 6....................: 250
On-Demand, Virtual RHEL 6.....................: 1000
On-Demand, Physical RHEL 7....................: 723
On-Demand, Virtual RHEL 7.....................: 2000
On-Demand, Physical RHEL 8....................: 0
On-Demand, Virtual RHEL 8.....................: 2092
On-Demand, Physical RHEL 9....................: 0
On-Demand, Virtual RHEL 9.....................: 0

## RHEL Add-ons

On-Demand, High Availability, Physical Node...: 0
On-Demand, High Availability, Virtual Node....: 12
On-Demand, Directory Server Node .............: 20

## Virtualization

On-Demand, Virtualization Sockets ............: 192

## Middleware

On-Demand, JBoss EAP Cores ...................: 312
On-Demand, JWS Cores .........................: 474

## RHEL Virtual Data Center

Virtual Data Center, Hypervisor ..............: 198
Virtual Data Center, Hypervisor Sockets ......: 766

## Ansible Managed Hosts

On-Demand, Ansible Managed Hosts .............: 487

## RHEL On-Demand

Max Concurrent RHEL On-Demand, referrent to ..: 2022-04
On-Demand, Physical Node .....................: 978
On-Demand, Virtual Node ......................: 5500
Virtual Data Center, Virtual Node ............: 3787
Unknown ......................................: 0

## RHEL Add-ons

On-Demand, High Availability, Physical Node...: 0
On-Demand, High Availability, Virtual Node....: 12
On-Demand, Directory Server Node .............: 20

## Virtualization

On-Demand, Virtualization Sockets ............: 192

## Middleware

On-Demand, JBoss EAP Cores ...................: 324
On-Demand, JWS Cores .........................: 496

## RHEL Virtual Data Center

Virtual Data Center, Hypervisor ..............: 198
Virtual Data Center, Hypervisor Sockets ......: 766

## Ansible Managed Hosts

On-Demand, Ansible Managed Hosts .............: 533
```

Another option is to use the --tag to break down the overall usage by tag.  This is so that you can break down your usage by environment, or business unit or any other criteria, and can help with internal cross charging.
 
Tags can be defined by creating the file /etc/insights-client/tags.yaml.  The contents of the file are a set of named value pairs - e.g. environment=Dev, or environment=Prod.  After creating the file, when the insights-client next runs, the tags will be uploaded to insights and then you can break down the usages based on those tags.  Systems which are not tagged will be counted in the overall number, but not in the breakdown.  You can find out more about how to set custom tags on your systems [here](https://access.redhat.com/documentation/en-us/red_hat_insights/2023/html/client_configuration_guide_for_red_hat_insights/con-insights-client-tagging-overview_insights-cg-adding-tags#con-insights-client-custom-system-tagging_insights-cg-adding-tags).
 
Here's an example of using --tag=environment to break down the usage by environment.

```
$ ./hcs-collector.py process --tag=environment
## RHEL On-Demand

Max Concurrent RHEL On-Demand, referrent to ..: 2022-04
On-Demand, Physical Node .....................: 978
  Dev ........................................: 278
  Prod .......................................: 700
On-Demand, Virtual Node ......................: 5500
  Dev ........................................: 1500
  Prod .......................................: 4000
Unknown ......................................: 0

Max Concurrent RHEL On-Demand, by version ....: 2022-03
On-Demand, Physical RHEL 6....................: 250
  Dev ........................................: 100
  Prod .......................................: 150 
On-Demand, Virtual RHEL 6.....................: 1000
  Dev ........................................: 400
  Prod .......................................: 600
On-Demand, Physical RHEL 7....................: 723
  Dev ........................................: 223
  Prod .......................................: 500
On-Demand, Virtual RHEL 7.....................: 2000
  Dev ........................................: 700
  Prod .......................................: 1300
On-Demand, Physical RHEL 8....................: 0
On-Demand, Virtual RHEL 8.....................: 2092
  Dev ........................................: 692
  Prod .......................................: 1400
On-Demand, Physical RHEL 9....................: 0
On-Demand, Virtual RHEL 9.....................: 0

## RHEL Add-ons

On-Demand, HA Node ...........................: 12
  Dev ........................................: 2
  Prod .......................................: 10
On-Demand, Directory Server Node .............: 20
  Dev ........................................: 0
  Prod .......................................: 20

## Virtualization

On-Demand, Virtualization Sockets ............: 192
  Dev ........................................: 0
  Prod .......................................: 192

## Middleware

On-Demand, JBoss EAP Cores ...................: 324
  Dev ........................................: 120
  Prod .......................................: 204
On-Demand, JWS Cores .........................: 196
  Dev ........................................: 68
  Prod .......................................: 128

## Ansible Managed Hosts

On-Demand, Ansible Managed Hosts .............: 487
```


Ps.: This pilot is still very recent, Please, if you get any issue or improvements that you would like to share, feel free to submit a new [Issue](https://github.com/C-RH-C/hcs-collector/issues/new/choose)

Thank you!

Waldirio (waldirio@gmail.com)
