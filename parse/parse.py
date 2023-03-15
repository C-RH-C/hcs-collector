
import json
import click
from execution import execution
from setup_env import setup_env

setup_env.standard_conf_file()


@click.group()
@click.option("--tag", default='none', help="The tag registered with insights, by which you would like the analysis broen down")
def main():
    """
    Command line tool for HCS - Hybrid Commited Spend
    """
    pass


@main.group()
def setup():
    """
    Setup the basic configuration
    """
    pass


@setup.command()
def crhc_cli():
    """
    Set the path of crhc-cli
    """
    setup_env.setup_crhc_path()


@setup.command()
def base_dir():
    """
    Set the basedir that will be used to store the data
    """
    setup_env.setup_basedir()


@setup.command()
def view():
    """
    View the current configuration
    """
    response = setup_env.view_current_conf()
    print(json.dumps(response, indent=4))


@main.command()
def collect():
    """
    Collect the information using crhc-cli
    """
    execution.collect_data()


@main.command()
def process(tag):
    """
    Only process the local information with no necessity of download
    """
    execution.process_data(tag)



