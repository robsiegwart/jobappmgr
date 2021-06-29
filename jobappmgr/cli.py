'''
Command-line interface for the app-mgr program.
'''

import shutil
import yaml
import os
import click
from jobappmgr import (
    get_or_create_output_directory,
    render_cover_letter
)


@click.group()
def cli():
    pass


@cli.command(help='Organize a resume and cover letter based on a YAML configuration file.')
@click.argument('config_file')
def run(config_file):
    '''Run the generation routine'''
    # Load config file
    with open(config_file) as f:
        config = yaml.safe_load(f.read())

    # Establish output directories
    outdir = get_or_create_output_directory(config)

    # Copy the resume file
    shutil.copy2(config['resume'], outdir)
    click.echo(f'Copied resume file "{os.path.basename(config["resume"])}"')
    
    # Render the cover letter template
    cl = render_cover_letter(config, outdir)

    click.echo('Finished')


@cli.command(help='Insert a YAML file in the current directory')
def init(*args,**kwargs):
    '''Insert a sample YAML file as a template'''
    pass